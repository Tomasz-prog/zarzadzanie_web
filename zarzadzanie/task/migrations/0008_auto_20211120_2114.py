# Generated by Django 3.2.9 on 2021-11-20 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_auto_20211120_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='branch',
            field=models.CharField(choices=[(1, 'potencjalne bledy uzytkownika'), (0, 'todo'), (2, 'znalezione bledy')], max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(1, 'in progress'), (0, 'not started'), (2, 'done')], max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='timedone',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
