# Generated by Django 3.2 on 2021-04-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_book_currentuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='currentuser',
            field=models.CharField(default='none', max_length=1000),
        ),
    ]
