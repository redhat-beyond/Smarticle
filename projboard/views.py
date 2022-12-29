from django.shortcuts import render
from .models.article import Article


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
