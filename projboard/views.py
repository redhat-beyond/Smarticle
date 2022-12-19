from django.shortcuts import render, redirect
from .models.user import User
from .forms import CreateArticleForm


def board(request):
    return render(request, 'projboard/board.html', {})


def create_article(request):
    # TODO when we end to create authentication and authorization, change "User1"
    user = User.get_user_by_nickname("User1")

    if request.method == "POST":
        form = CreateArticleForm(request.POST, initial={'user_id': user})
        if form.is_valid():
            form.save()
            # TODO when we end to create the "my articles" page, change the redirect
            return redirect('board')
    else:
        form = CreateArticleForm(initial={'user_id': user})

    return render(request, 'article/article.html', {
        "user": user,
        'form': form,
    })
