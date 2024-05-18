import json
from django.core.management.base import BaseCommand
from recom.models import Article
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
class Command(BaseCommand):
    help = 'Import data from train.jsonl to Article model'
        
    def handle(self, *args, **options):
        nltk.download('stopwords')
        nltk.download('punkt')
        def preprocess_text(text):
            text = ' '.join(text)
            # Küçük harfe çevirme
            text = text.lower()
            # Noktalama işaretlerini kaldırma
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Tokenize etme
            tokens = word_tokenize(text)
            # Stopwords'leri kaldırma
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [word for word in tokens if word not in stop_words]
            # Kelimelerin köklerini bulma (stemming)
            stemmer = PorterStemmer()
            stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
            return stemmed_tokens

        with open('train.jsonl', 'r') as file:
            for line in file:
                data = json.loads(line)
                article=Article.objects.create(
                    paper_id=data['paper_id'],
                    document=data['document'],
                    cleaned_document=preprocess_text(data['document']),
                    doc_bio_tags=data['doc_bio_tags'],
                    extractive_keyphrases=data['extractive_keyphrases'],
                    abstractive_keyphrases=data['abstractive_keyphrases'],
                    other_metadata=data['other_metadata']
                )
                print(article.cleaned_document)
                self.stdout.write(self.style.SUCCESS('Data imported successfully!'))

        self.stdout.write(self.style.SUCCESS('tamamlandı.'))
    
