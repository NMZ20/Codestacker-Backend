import uuid
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=3)
    number_of_pages = models.IntegerField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Sentence(models.Model):
    sentence = models.TextField()
    pdf_file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return self.sentence
