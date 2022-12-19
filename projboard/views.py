from .models.article import Article
from django.shortcuts import render
from .models.user import User
from .forms import CreateArticleForm


def board(request):
    return render(request, 'projboard/board.html', {})


def search(request):
    search_title = ''
    articles = []
    message = ''
    if request.method == 'POST':
        search_title = request.POST['title']
        if search_title != '':
            articles = Article.search_by_title(search_title)
        else:
            message = "please enter a title!"

    num_articles = len(articles)
    return render(request, 'projboard/searchArticle/search_article.html', {'articles': articles,
                                                                           'num_articles': num_articles,
                                                                           'search_title': search_title,
                                                                           'message': message})


def create_article(request):
    # TODO when we end to create authentication and authorization, change "User1"
    user = User.get_user_by_nickname("User1")

    if request.method == "POST":
        form = CreateArticleForm(request.POST, initial={'user_id': user})
        if form.is_valid():
            form.save()
            # TODO when we end to create the "my articles" page, change the redirect
            return render(request, 'projboard/board.html', {'articles': Article.search_by_user(user)})
    else:
        form = CreateArticleForm(initial={'user_id': user})

    return render(request, 'article/article.html', {
        "user": user,
        'form': form,
    })
