from .models.article import Article, View_Article, Like
from django.shortcuts import render, redirect
from .models.user import User
from .models.subject import Subject
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateArticleForm, UserForm, CustomUserForm, NewUserForm, EditArticleForm
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def error_404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=404)


def search(request, user_nickname):

    try:
        user_nickname = request.user.username
        user = User.get_user_by_nickname(user_nickname)
    except ObjectDoesNotExist:
        raise Http404()

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
                                                                 'user': user,
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
        nickname = request.user.username
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


def home_page(request, user_nickname=None):
    articles = []
    articles = Article.objects.all()
    if user_nickname is not None:
        try:
            user = User.get_user_by_nickname(user_nickname)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, 'landing/homepage.html', {'articles': articles,
                                                         'user': user})

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
            return redirect('login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'signup/signup.html', {'register_form': form, 'registration_attempt': registration_attempt})


def show_article(request, user_nickname, article_pk):

    try:
        user = User.get_user_by_nickname(user_nickname)
        article = Article.objects.get(pk=article_pk)
        liked = True
        try:
            Like.objects.get(user_id=user.id, article_id=article_pk)
        except ObjectDoesNotExist:
            liked = False

        if request.method == 'POST':
            like_method = request.POST['like_method']
            if like_method == 'Add':
                Like.create_like(user_id=user, article_id=article)
                liked = True
            else:
                Like.delete_like(user_id=user.id, article_id=article_pk)
                liked = False

        else:
            try:
                View_Article.objects.get(user_id=user.id, article_id=article_pk)
            except ObjectDoesNotExist:
                new_view = View_Article(user_id=user, article_id=article)
                new_view.save()

        return render(request, 'show/read_article.html', {'article': article, 'user': user, 'liked': liked})

    except ObjectDoesNotExist:
        raise Http404()


def show_article_for_guest(request, article_pk):
    try:
        article = Article.objects.get(pk=article_pk)
    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'show/read_article.html', {'article': article})


def delete_article(request, article_pk):
    try:
        article = Article.objects.get(id=article_pk)
        user = article.user_id
        article.delete()
        nickname = user.nickname
        return redirect(f"/my_articles/{nickname}/")

    except Article.DoesNotExist:
        raise Http404()


def edit_article(request, article_pk=None):
    try:
        article = Article.objects.get(id=article_pk)
        user_id = article.user_id

        title = article.title
        subject_id = article.subject_id
        content = article.content

        initial = {'title': title, 'subject_id': subject_id, 'content': content}

        if request.method == "POST":
            form = EditArticleForm(request.POST)
            if form.is_valid():
                article.edit(form.data['title'], form.data['content'], form.cleaned_data['subject_id'])
                return redirect(f"/my_articles/{user_id.nickname}/")
        elif request.method == "DELETE":
            raise Http404()
        else:
            form = EditArticleForm(initial=initial)

        return render(request, 'editArticle/edit_article.html', {
            'form': form
        })
    except Article.DoesNotExist:
        raise Http404()


@login_required
def custom_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        custom_user_form = CustomUserForm(
            request.POST, instance=request.user.user
        )
        if user_form.is_valid() and custom_user_form.is_valid():
            user_form.save()
            custom_user_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect(home_page)
    else:
        user_form = UserForm(instance=request.user)
        custom_user_form = CustomUserForm(instance=request.user.user)

    return render(
        request,
        'login/login.html',
        {'user_form': user_form, 'custom_user_form': custom_user_form},
    )


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Username OR password is incorrect")
    return render(
        request,
        "login/login.html",
    )


def logout_user(request):
    logout(request)
    return redirect("login")
