import pytest
from projboard.forms import CreateArticleForm


@pytest.mark.django_db
def test_form_valid():
    form_data = {
        'user_id': 1,
        'title': 'Test Title',
        'subject_id': 1,
        'content': 'Test content',
        'date': '2022-12-22',
    }
    form = CreateArticleForm(data=form_data)
    if form.is_valid():
        assert True
    else:
        assert False


@pytest.mark.django_db
def test_form_invalid_missing_title():
    form_data = {
        # Missing title to fill the form, assertion true means the form is not valid
        'user_id': 1,
        'subject_id': 1,
        'content': 'Test content',
        'date': '2022-12-22',
    }
    form = CreateArticleForm(data=form_data)
    if form.is_valid():
        assert False
    else:
        assert True
