# Generated by Django 3.2.9 on 2021-11-16 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20211116_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='level',
            field=models.CharField(choices=[(1, 'medium'), (0, 'easy'), (2, 'hard')], max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(0, 'not started'), (1, 'in progress'), (2, 'done')], max_length=10),
        ),
    ]
