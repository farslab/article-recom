from django.core.management.base import BaseCommand
from huggingface_hub import hf_hub_download
import fasttext
import fasttext.util
from recom.models import Article 
from transformers import AutoTokenizer, AutoModel

class Command(BaseCommand):
    help = 'Generate FastText vectors for articles and save them in the database'

    def handle(self, *args, **kwargs):
        #modellerin yüklenmesi
        model = fasttext.load_model('cc.en.300.bin')
        scibert_model_name = "allenai/scibert_scivocab_uncased"
        scibert_tokenizer = AutoTokenizer.from_pretrained(scibert_model_name)
        scibert_model = AutoModel.from_pretrained(scibert_model_name)

        articles = Article.objects.all()

        for article in articles:
            cleaned_document = " ".join(article.cleaned_document)            
            #scibert
            scibert_input = scibert_tokenizer(cleaned_document, return_tensors="pt", padding=True, truncation=True)
            scibert_outputs = scibert_model(**scibert_input)
            scibert_embeddings = scibert_outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
            article.scibert_vector = scibert_embeddings
            #fasttext
            vector = model.get_word_vector(cleaned_document)
            article.fasttext_vector = vector.tolist()
            
            article.save()

        self.stdout.write(self.style.SUCCESS('FastText vectors generated and saved successfully for all articles.'))
