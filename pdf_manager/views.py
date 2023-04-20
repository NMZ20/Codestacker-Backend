import os

import fitz
import PyPDF2
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .gs_service import get_blob
from .models import File, Sentence
from .serializers import FileSerializer, SentenceSerializer


class UploadFile(APIView):
    def post(self, request):
        file = request.FILES["file"]

        # Check the file type
        if not file.name.endswith(".pdf"):
            return Response({"error": "File is not a PDF."}, status=400)

        existing_file = File.objects.filter(name=file.name).first()

        if existing_file:
            return Response(
                {"error": f"A file with the name ({file.name}) already exists."},
                status=400,
            )

        # Create a new blob object and upload the file data to it
        blob = get_blob(file.name)
        blob.upload_from_file(file)

        pdf_reader = PyPDF2.PdfReader(file)

        # Add new record to the File table in the DB
        pdf_file = File()
        pdf_file.name = file.name
        pdf_file.size = file.size / 1024
        pdf_file.number_of_pages = len(pdf_reader.pages)
        pdf_file.save()

        # Extract text from each page and concatenate into a single string
        text = ""
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

        # Split the text into sentences
        sentences = text.split(".")

        # Save each sentence as a new instance of the Sentence model
        for sentence in sentences:
            if len(sentence) > 0:
                s = Sentence(pdf_file=pdf_file)
                s.sentence = sentence.strip()
                s.save()

        pdf_reader.stream.close()

        return Response({"success": "File uploaded successfully."}, status=200)


class ListFiles(APIView):
    def get(self, request):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class Search(APIView):
    def get(self, request, keyword):
        sentences = Sentence.objects.filter(sentence__contains=keyword)
        serializer = SentenceSerializer(sentences, many=True)
        return Response(serializer.data)


class FileRetrieve(APIView):
    def get(self, request, id):
        file = get_object_or_404(File, id=id)

        blob = get_blob(file.name)
        file_content = blob.download_as_bytes()

        if blob is not None:
            response = HttpResponse(file_content, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{file.name}"'
            return response
        else:
            return Response(status=404)


class DeleteFile(APIView):
    def get(self, request, id):
        file = get_object_or_404(File, id=id)

        blob = get_blob(file.name)

        # deletes the file from the cloud storage
        blob.delete()
        # delete the file record in the DB
        file.delete()

        return Response({"success": "File deleted successfully."}, status=200)


class RetrieveSentences(APIView):
    def get(self, request, id):
        sentences = Sentence.objects.filter(pdf_file__id=id)
        if sentences:
            serializer = SentenceSerializer(sentences, many=True)
            return Response(serializer.data)
        return Response(
            {f"not found": "PDF file with id {id} is not found."}, status=404
        )


class CheckOccurence(APIView):
    def get(self, request, id, word):
        get_object_or_404(File, id=id)

        total_count = 0
        sentences = []
        for sentence in Sentence.objects.filter(pdf_file__id=id):
            count = sentence.sentence.count(word)
            if count > 0:
                total_count += count
                sentences.append(sentence)

        data = {
            "number_of_occurences": total_count,
            "sentences": [
                {
                    "text": obj.sentence,
                }
                for obj in sentences
            ],
        }
        return Response(data)


class TopWords(APIView):
    def get(self, request, id):
        get_object_or_404(File, id=id)

        sentences = Sentence.objects.filter(pdf_file__id=id)

        exclude_words = [
            "the",
            "but",
            "it",
            "and",
            "is",
            "or",
            "#",
            "a",
            "an",
            "at",
            "on",
            "in",
        ]

        # Count the occurrences of all words in the documents
        word_counts = {}

        for sentence in sentences:
            # Split the sentence into individual words
            words = [
                word
                for word in sentence.sentence.lower().split()
                if word not in exclude_words
            ]
            for word in words:
                # Count the occurrences of each word
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

        # Sort the word counts by their values in descending order
        sorted_word_counts = sorted(
            word_counts.items(), key=lambda x: x[1], reverse=True
        )

        # Return the top 5 words as a DRF response
        top_words = sorted_word_counts[:5]
        return Response(top_words)


class GetPage(APIView):
    def get(self, request, id, page_number):
        if page_number == 0:
            return Response({"error": "0 is not a valid page number"}, status=400)

        file = get_object_or_404(File, id=id)

        blob = get_blob(file.name)
        file_content = blob.download_as_bytes()

        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        doc = fitz.open(stream=file_content, filetype="pdf")  # open document

        try:
            page = doc[page_number - 1]
        except:
            return Response({"not found": "Page not found."}, status=404)

        pix = page.get_pixmap(matrix=mat)  # render page to an image

        image_path = f"{file.name}_page{page_number}.png"

        pix.save(image_path)

        with open(image_path, "rb") as f:
            image_data = f.read()

        os.remove(image_path)

        response = HttpResponse(image_data, content_type="image/png")
        response["Content-Disposition"] = f'inline; filename="{os.path.splitext(file.name)[0]}_page{page_number}.png"'
        return response
