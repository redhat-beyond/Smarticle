from .models.article import Article
from django.shortcuts import render, redirect
from .models.user import User
from .models.subject import Subject
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateArticleForm, NewUserForm, EditArticleForm
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages


def error_404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=404)


def search(request):
    search_input = ''
    articles = []
    message = ''
    search_method = 'title'

    if request.method == 'POST':
        search_input = request.POST['searchInput']
        search_method = request.POST['searchOptions']
        # just to identify in test case if search_input is empty
        if search_input == '':
            message = "please enter a title!"

        if search_method == 'title':
            articles = Article.search_by_title(search_input)
            if len(articles) == 0:
                message = 'Article didn\'t found'
        elif search_method == 'subject':
            subject = Subject.get_subject_by_name(search_input)
            if subject is None:
                message = 'Subject Not Valid'
            else:
                articles = Article.search_by_subject(subject.id)
        elif search_method == 'user':
            try:
                user = User.get_user_by_nickname(search_input)
                articles = Article.search_by_user(user.id)
            except ObjectDoesNotExist:
                message = 'User Name Not Valid'

    num_articles = len(articles)
    return render(request, 'searchArticle/search_article.html', {'articles': articles,
                                                                 'num_articles': num_articles,
                                                                 'search_input': search_input,
                                                                 'search_method': search_method,
                                                                 'message': message})


def create_article(request):
    # TODO when we end to create authentication and authorization, change "User1"
    user = User.get_user_by_nickname("User1")

    if request.method == "POST":
        form = CreateArticleForm(request.POST, initial={'user_id': user})
        if form.is_valid():
            form.save()
            return redirect(f'/my_articles/{user.nickname}')
    elif request.method == "DELETE":
        raise Http404()
    else:
        form = CreateArticleForm(initial={'user_id': user})

    return render(request, 'article/article.html', {
        "user": user,
        'form': form,
    })


def my_articles(request, nickname=''):
    try:
        user = User.get_user_by_nickname(nickname)
        my_articles = Article.search_by_user(user)
        num_articles = len(my_articles)

        return render(request, 'myArticles/my_articles.html', {
            'user': user,
            'my_articles': my_articles,
            'num_articles': num_articles
        })
    except User.DoesNotExist:
        raise Http404()


def home_page(request):
    articles = []
    articles = Article.objects.all()
    return render(request, 'landing/homepage.html', {'articles': articles})


def about_page(request):
    return render(request, 'about/about.html', {})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    form = NewUserForm()
    registration_attempt = False
    if request.method == 'POST':
        registration_attempt = True
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            nickname = form.cleaned_data.get('nickname')
            messages.success(request, 'Account '+nickname+' created successfully')
            # CHANGE THIS TO login
            return redirect('homepage')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'signup/signup.html', {'register_form': form, 'registration_attempt': registration_attempt})


def delete_article(request, article_pk):
    try:
        article = Article.objects.get(id=article_pk)
        article.delete()
        return redirect(home_page)

    except User.DoesNotExist:
        raise Http404()


def edit_article(request, article_pk):
    try:
        article = Article.objects.get(article_pk)

        initial = {'article_id': article, 'title': article.title,
                   'subject': article.subject_id, 'content': article.content}
        if request.method == "POST":
            form = EditArticleForm(request.POST, initial=initial)
            if form.is_valid():
                form.save()
                return render(request, 'editArticle/edit_article.html', initial)
        # elif request.method == "DELETE":
        #     raise Http404()
        else:
            form = EditArticleForm(initial=initial)

        return render(request, 'editArticle/edit_article.html', {
            'article_pk': article_pk,
            'form': form,
        })
    except User.DoesNotExist:
        # raise Http404()
        return redirect(home_page)
