# Generated by Django 4.1.3 on 2022-11-23 11:48

from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('projboard', '0003_alter_article_subject_id'),
    ]

    def generate_user_data(apps, schema_editor):
        from projboard.models import User

        test_data = [
            ['Smarticle@walla.co.il', '123456', 'John Doe', 'User1'],
            ['testEmail@gmail.com', '123456', 'Full Name', 'User2'],
        ]
        with transaction.atomic():
            for u in test_data:
                User(email=u[0], password=u[1], name=u[2], nickname=u[3]).save()

    operations = [
        migrations.RunPython(generate_user_data),
    ]