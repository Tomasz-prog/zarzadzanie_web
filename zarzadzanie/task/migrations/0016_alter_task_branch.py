# Generated by Django 3.2.9 on 2021-12-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0015_auto_20211224_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='branch',
            field=models.PositiveSmallIntegerField(choices=[(0, 'todo'), (1, 'potencjalne błedy użytkownika'), (2, 'znalezione błędy'), (3, 'usprawnienia'), (4, 'CSS')], default=0),
        ),
    ]