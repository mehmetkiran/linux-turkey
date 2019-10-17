# Generated by Django 2.1.5 on 2019-03-02 18:04

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Makale ID')),
                ('articleTitle', models.CharField(max_length=250, verbose_name='Makale Basligi')),
                ('articleContent', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Makale')),
                ('articleViewCounter', models.IntegerField(default=0, verbose_name='Okunma sayisi')),
                ('articleCreateDate', models.DateTimeField(auto_now_add=True, verbose_name='Olusturulma Tarihi')),
                ('articleCoverImage', models.ImageField(blank=True, default='article/Dma7XY2XgAIWNOZ.jpg', null=True, upload_to='article/', verbose_name='Kapak Fotoğrafı')),
                ('slug', models.SlugField(editable=False, max_length=135, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('commentID', models.AutoField(primary_key=True, serialize=False, verbose_name='Yorum ID')),
                ('comment', models.TextField(verbose_name='Yorum')),
                ('commentDate', models.DateTimeField(auto_now_add=True, verbose_name='Yorum Tarihi')),
                ('articleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='article.ArticleModel')),
            ],
        ),
    ]