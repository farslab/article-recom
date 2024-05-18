from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(default="000", max_length=15, blank=True)
    school = models.CharField(default="Boş", max_length=100, blank=True)
    interest = models.CharField( blank=True, null=True,max_length=100)
    interests_fasttext_vector= models.JSONField(blank=True, null=True)
    interests_scibert_vector= models.JSONField(blank=True, null=True)



class Article(models.Model):
    paper_id = models.CharField(max_length=255)
    document = models.JSONField()
    cleaned_document= models.JSONField()
    doc_bio_tags = models.JSONField()
    extractive_keyphrases = models.JSONField()
    abstractive_keyphrases = models.JSONField()
    other_metadata = models.JSONField()
    fasttext_vector = models.JSONField(blank=True, null=True)
    scibert_vector = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.paper_id
