# Generated by Django 3.2.9 on 2021-11-16 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('task', models.TextField()),
                ('branch', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('timeneed', models.IntegerField()),
                ('timedone', models.DecimalField(decimal_places=2, max_digits=3)),
                ('weight', models.CharField(max_length=10)),
                ('level', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
    ]
