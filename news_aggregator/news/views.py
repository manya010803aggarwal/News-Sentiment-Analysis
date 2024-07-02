# # news/views.py
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib import messages
# from .models import User, SharedArticle
# from textblob import TextBlob
# from .model import get_sentiment_and_entities
# import requests
# import json

# API_KEY = '3f323a2c4dfb4a6691f34be7a74ae68e'
# logged_in = False
# user_email = ''
# user_name = ''
# searched = False

# def index(request):
#     global logged_in, user_email, user_name, searched
#     if request.method == "POST":
#         if 'logout-button' in request.POST:
#             logged_in = True
#             user_email = ''
#             user_name = ''
#             searched = False
#             url = f'https://newsapi.org/v2/top-headlines?category=general&language=en&apiKey={API_KEY}'
#             response = requests.get(url)
#             articles = response.json().get('articles', [])
#             return render(request, 'index.html', {'data': articles, 'x': logged_in, 'y': user_name, 'z': searched})

#         elif 'submit-button-1' in request.POST:
#             searched = True
#             keywords = request.POST.get('article-keywords-phrase', '')
#             language = request.POST.get('language', 'en')
#             search_from = request.POST.get('search-from', '')
#             search_to = request.POST.get('search-to', '')
#             sorting = request.POST.get('dropdown-menu', 'relevancy')

#             url = f'https://newsapi.org/v2/everything?q={keywords}&language={language}&from={search_from}&to={search_to}&sortBy={sorting}&apiKey={API_KEY}'
#             response = requests.get(url)
#             articles = response.json().get('articles', [])
#             return render(request, 'index.html', {'data': articles, 'x': logged_in, 'y': user_name, 'z': searched})

#     url = f'https://newsapi.org/v2/top-headlines?category=general&language=en&apiKey={API_KEY}'
#     response = requests.get(url)
#     articles = response.json().get('articles', [])
#     return render(request, 'index.html', {'data': articles, 'x': logged_in, 'y': user_name, 'z': searched})


# def login(request):
#     global logged_in, user_email, user_name
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         try:
#             user = User.objects.get(email=email, password=password)
#             logged_in = True
#             user_email = user.email
#             user_name = user.name
#             return redirect('index')
#         except User.DoesNotExist:
#             messages.error(request, "Invalid login credentials")
#             return redirect('login')
#     return render(request, 'login.html')

# def register(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "User already exists")
#         else:
#             User.objects.create(name=name, email=email, password=password)
#             messages.success(request, "Registration successful")
#             return redirect('login')
#     return render(request, 'register.html')

# def shared(request):
#     global logged_in, user_email, user_name
#     shared_articles = SharedArticle.objects.filter(email_2=user_email)
#     shared_data = [
#         {"email_1": article.email_1, "name_1": article.name_1, "article_info": json.loads(article.article_info)}
#         for article in shared_articles
#     ]
#     return render(request, 'shared.html', {'x': logged_in, 'y': user_name, 'z': shared_data})

# def article_info(request):
#     global logged_in, user_email, user_name
#     info = json.loads(request.POST.get('article-info', '{}'))

#     b = TextBlob(info.get('description', ''))
#     info['language'] = b.detect_language()
#     if info['language'] == 'en':
#         info['sentiment'], info['entities'], info['explained_entities'] = get_sentiment_and_entities(info['description'])
#     else:
#         info['sentiment'] = 'Cannot analyze in non-English language'
#         info['entities'] = 'Cannot analyze in non-English language'

#     if request.method == 'POST' and 'submit-button' in request.POST:
#         shared_to = request.POST['shared-to']
#         SharedArticle.objects.create(
#             email_1=user_email, name_1=user_name,
#             email_2=shared_to, article_info=json.dumps(info)
#         )
#     return render(request, 'article.html', {'x': logged_in, 'y': user_name, 'info': info})

# news/views.py
# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from django.contrib import messages
# from .models import User, SharedArticle
# from textblob import TextBlob
# from .model import get_sentiment_and_entities  # Correct import
# import requests
# import json

# API_KEY = '3f323a2c4dfb4a6691f34be7a74ae68e'

# def index(request):
#     # Use session variables instead of global variables
#     logged_in = request.session.get('logged_in', False)
#     user_email = request.session.get('user_email', '')
#     user_name = request.session.get('user_name', '')
#     searched = request.session.get('searched', False)

#     if request.method == "POST":
#         if 'logout-button' in request.POST:
#             # Clear session
#             request.session.flush()
#             url = f'https://newsapi.org/v2/top-headlines?category=general&language=en&apiKey={API_KEY}'
#             try:
#                 response = requests.get(url)
#                 response.raise_for_status()  # Raise an exception for HTTP errors
#                 articles = response.json().get('articles', [])
#             except requests.RequestException:
#                 articles = []
#                 messages.error(request, "Error fetching news articles.")
#             return render(request, 'index.html', {'data': articles, 'logged_in': False, 'user_name': '', 'searched': False})

#         elif 'submit-button-1' in request.POST:
#             request.session['searched'] = True
#             keywords = request.POST.get('article-keywords-phrase', '')
#             language = request.POST.get('language', 'en')
#             search_from = request.POST.get('search-from', '')
#             search_to = request.POST.get('search-to', '')
#             sorting = request.POST.get('dropdown-menu', 'relevancy')

#             url = 'https://newsapi.org/v2/everything?'
#             params = {
#                 'apiKey': API_KEY,
#                 'q': keywords,
#                 'language': language,
#                 'from': search_from if search_from else None,
#                 'to': search_to if search_to else None,
#                 'sortBy': sorting
#             }
#             try:
#                 response = requests.get(url, params={k: v for k, v in params.items() if v is not None})
#                 response.raise_for_status()
#                 articles = response.json().get('articles', [])
#             except requests.RequestException:
#                 articles = []
#                 messages.error(request, "Error fetching news articles.")
#             return render(request, 'index.html', {'data': articles, 'logged_in': logged_in, 'user_name': user_name, 'searched': True})

#     # Handle GET request
#     url = f'https://newsapi.org/v2/top-headlines?category=general&language=en&apiKey={API_KEY}'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         articles = response.json().get('articles', [])
#     except requests.RequestException:
#         articles = []
#         messages.error(request, "Error fetching news articles.")
    
#     return render(request, 'index.html', {'data': articles, 'logged_in': logged_in, 'user_name': user_name, 'searched': searched})


# def login(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         try:
#             user = User.objects.get(email=email, password=password)
#             request.session['logged_in'] = True
#             request.session['user_email'] = user.email
#             request.session['user_name'] = user.name
#             return redirect('index')
#         except User.DoesNotExist:
#             messages.error(request, "Invalid login credentials")
#             return redirect('login')
#     return render(request, 'login.html')


# def register(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "User already exists")
#         else:
#             User.objects.create(name=name, email=email, password=password)
#             messages.success(request, "Registration successful")
#             return redirect('login')
#     return render(request, 'register.html')


# def shared(request):
#     user_email = request.session.get('user_email', '')
#     shared_articles = SharedArticle.objects.filter(email_2=user_email)
#     shared_data = [
#         {"email_1": article.email_1, "name_1": article.name_1, "article_info": json.loads(article.article_info)}
#         for article in shared_articles
#     ]
#     return render(request, 'shared.html', {'logged_in': request.session.get('logged_in', False), 'user_name': request.session.get('user_name', ''), 'shared_data': shared_data})


# def article_info(request):
#     user_email = request.session.get('user_email', '')
#     user_name = request.session.get('user_name', '')

#     info = json.loads(request.POST.get('article-info', '{}'))
#     b = TextBlob(info.get('description', ''))
#     info['language'] = b.detect_language()

#     if info['language'] == 'en':
#         info['sentiment'], info['entities'], info['explained_entities'] = get_sentiment_and_entities(info['description'])
#     else:
#         info['sentiment'] = 'Cannot analyze in non-English language'
#         info['entities'] = 'Cannot analyze in non-English language'

#     if request.method == 'POST' and 'submit-button' in request.POST:
#         shared_to = request.POST['shared-to']
#         SharedArticle.objects.create(
#             email_1=user_email, name_1=user_name,
#             email_2=shared_to, article_info=json.dumps(info)
#         )
#     return render(request, 'article.html', {'logged_in': request.session.get('logged_in', False), 'user_name': request.session.get('user_name', ''), 'info': info})



from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User, SharedArticle
from textblob import TextBlob
from .model import get_sentiment_and_entities
import requests
import json
import os

API_KEY = os.getenv('NEWS_API_KEY', '3f323a2c4dfb4a6691f34be7a74ae68e')

def index(request):
    session = request.session
    logged_in = session.get('logged_in', False)
    user_email = session.get('user_email', '')
    user_name = session.get('user_name', '')
    searched = session.get('searched', False)

    if request.method == "POST":
        if 'logout-button' in request.POST:
            session.flush()
            articles, error_msg = fetch_news_articles()
            if error_msg:
                messages.error(request, error_msg)
            return render(request, 'index.html', {'data': articles, 'logged_in': False, 'user_name': '', 'searched': False})

        elif 'submit-button-1' in request.POST:
            session['searched'] = True
            keywords = request.POST.get('article-keywords-phrase', '')
            language = request.POST.get('language', 'en')
            search_from = request.POST.get('search-from', '')
            search_to = request.POST.get('search-to', '')
            sorting = request.POST.get('dropdown-menu', 'relevancy')

            articles, error_msg = fetch_news_articles(keywords, language, search_from, search_to, sorting)
            if error_msg:
                messages.error(request, error_msg)
            return render(request, 'index.html', {'data': articles, 'logged_in': logged_in, 'user_name': user_name, 'searched': True})

    articles, error_msg = fetch_news_articles()
    if error_msg:
        messages.error(request, error_msg)
    return render(request, 'index.html', {'data': articles, 'logged_in': logged_in, 'user_name': user_name, 'searched': searched})

def fetch_news_articles(keywords='', language='en', search_from=None, search_to=None, sorting='relevancy'):
    url = 'https://newsapi.org/v2/top-headlines' if not keywords else 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': API_KEY,
        'q': keywords,
        'language': language,
        'from': search_from,
        'to': search_to,
        'sortBy': sorting
    }
    try:
        response = requests.get(url, params={k: v for k, v in params.items() if v is not None})
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return articles, None
    except requests.RequestException as e:
        return [], str(e)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['logged_in'] = True
                request.session['user_email'] = user.email
                request.session['user_name'] = user.name
                return redirect('index')
            else:
                messages.error(request, "Invalid login credentials")
        except User.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists")
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful")
            return redirect('login')
    return render(request, 'register.html')

def shared(request):
    user_email = request.session.get('user_email', '')
    shared_articles = SharedArticle.objects.filter(email_2=user_email)
    shared_data = shared_articles.values('email_1', 'name_1', 'article_info')
    return render(request, 'shared.html', {'logged_in': request.session.get('logged_in', False), 'user_name': request.session.get('user_name', ''), 'shared_data': shared_data})

def article_info(request):
    user_email = request.session.get('user_email', '')
    user_name = request.session.get('user_name', '')

    if request.method == 'POST':
        info = json.loads(request.POST.get('article_info', '{}'))
        try:
            b = TextBlob(info.get('description', ''))
            info['language'] = b.detect_language()
        except Exception:
            info['language'] = 'unknown'

        if info['language'] == 'en':
            info['sentiment'], info['entities'], info['explained_entities'] = get_sentiment_and_entities(info['description'])
        else:
            info['sentiment'] = 'Cannot analyze in non-English language'
            info['entities'] = 'Cannot analyze in non-English language'

        if 'submit-button' in request.POST:
            shared_to = request.POST['shared-to']
            SharedArticle.objects.create(
                email_1=user_email, name_1=user_name,
                email_2=shared_to, article_info=json.dumps(info)
            )
        return render(request, 'article.html', {'logged_in': request.session.get('logged_in', False), 'user_name': request.session.get('user_name', ''), 'info': info})

    return redirect('index')
