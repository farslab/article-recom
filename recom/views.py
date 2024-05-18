
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
import fasttext
from transformers import AutoTokenizer, AutoModel
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from sklearn.decomposition import PCA, TruncatedSVD

from .forms import CustomAuthenticationForm
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Article
from django.contrib import auth
@login_required
def recommended_articles(request):
    user = request.user

    if user.interests_fasttext_vector is not None:
        fasttext_user_vector = np.array(user.interests_fasttext_vector).reshape(1, -1)
    else:
        fasttext_user_vector = None

    if user.interests_scibert_vector is not None:
        scibert_user_vector = np.array(user.interests_scibert_vector).reshape(1, -1)
    else:
        scibert_user_vector = None

    articles = Article.objects.all()
    fasttext_similarities = []
    scibert_similarities = []

    for article in articles:
        if article.fasttext_vector and fasttext_user_vector is not None:
            fasttext_vector = np.array(article.fasttext_vector).reshape(1, -1)
            if fasttext_user_vector.shape[1] == fasttext_vector.shape[1]:
                fasttext_sim = cosine_similarity(fasttext_user_vector, fasttext_vector)[0][0]
                fasttext_similarities.append((article, fasttext_sim))
            else:
                # Boyutları eşitlemek için vektörlerin boyutunu değiştir
                fasttext_user_vector = fasttext_user_vector[:, :fasttext_vector.shape[1]]
                fasttext_sim = cosine_similarity(fasttext_user_vector, fasttext_vector)[0][0]
                fasttext_similarities.append((article, fasttext_sim))

        if article.scibert_vector and scibert_user_vector is not None:
            scibert_vector = np.array(article.scibert_vector).reshape(1, -1)
            if scibert_user_vector.shape[1] == scibert_vector.shape[1]:
                scibert_sim = cosine_similarity(scibert_user_vector, scibert_vector)[0][0]
                scibert_similarities.append((article, scibert_sim))
            else:
                # Boyutları eşitlemek için vektörlerin boyutunu değiştir
                scibert_user_vector = scibert_user_vector[:, :scibert_vector.shape[1]]
                scibert_sim = cosine_similarity(scibert_user_vector, scibert_vector)[0][0]
                scibert_similarities.append((article, scibert_sim))

    fasttext_similarities.sort(key=lambda x: x[1], reverse=True)
    scibert_similarities.sort(key=lambda x: x[1], reverse=True)

    top_fasttext_articles = [article for article, _ in fasttext_similarities[:5]]
    top_scibert_articles = [article for article, _ in scibert_similarities[:5]]

    context = {
        'top_fasttext_articles': top_fasttext_articles,
        'top_scibert_articles': top_scibert_articles,
        'user': user
    }

    return render(request, 'recommended_articles.html', context)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        model = fasttext.load_model('cc.en.300.bin')
        scibert_model_name = "allenai/scibert_scivocab_uncased"
        scibert_tokenizer = AutoTokenizer.from_pretrained(scibert_model_name)
        scibert_model = AutoModel.from_pretrained(scibert_model_name)
        if form.is_valid():
            user = form.save(commit=False)
            interests = user.interest.split(',')
            fasttext_vectors = []
            scibert_vectors = []
            # FastText ve SciBERT vektörlerini oluştur
            for interest in interests:
                # SciBERT vektörlerini oluşturma
                scibert_input = scibert_tokenizer(interest, return_tensors="pt", padding=True, truncation=True)
                scibert_outputs = scibert_model(**scibert_input)
                scibert_vector = scibert_outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
              
                # FastText vektörlerini oluşturma
                fasttext_vector = model.get_word_vector(interest)
              
                fasttext_vectors.append(fasttext_vector.tolist())
                scibert_vectors.append(scibert_vector)
            # Oluşturulan vektörleri kullanıcı modeline kaydet
            print(fasttext_vectors)
            print(scibert_vectors)
            user.interests_fasttext_vector = fasttext_vectors
            user.interests_scibert_vector = scibert_vectors
            user.is_staff = True
            user.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def index(request):
    return HttpResponse("Anasayfa")

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        signup = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = CustomAuthenticationForm()
        signup = CustomUserCreationForm() 

    # Eğer kullanıcı zaten oturum açmışsa, ana sayfaya yönlendir
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'login.html', {'form': form, 'signup_form': signup})

def logout_view(request):
    logout(request)
    return redirect('login') 