from rest_framework import serializers
from .models import File, Sentence


class FileSerializer(serializers.ModelSerializer):
    size_in_kb = serializers.SerializerMethodField(method_name="get_size")

    class Meta:
        model = File
        fields = ("id", "name", "size_in_kb", "number_of_pages", "upload_time")

    def get_size(self, file: File):
        return str(file.size) + "kb"


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ("id", "sentence", "pdf_file")
