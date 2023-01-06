from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__latest__'),
        ('accounts', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from django.conf import settings

        if not settings.DEBUG:
            return

        from django.contrib.auth.models import User
        from django.templatetags.static import static

        from accounts.models import Account

        dev_accounts = ['man1', 'man2', 'man3', 'woman1', 'woman2']
        with transaction.atomic():
            for dev_account in dev_accounts:
                user = User.objects.create_user(dev_account)
                Account(
                    user=user,
                    avatar_url=static(f"builtin_avatars/{dev_account}.png")
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
