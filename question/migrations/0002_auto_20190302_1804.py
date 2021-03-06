# Generated by Django 2.1.5 on 2019-03-02 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='questionreportmodel',
            name='reporterID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='categoryID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.QuestionCategoryModel', verbose_name='Kategori'),
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoritequestionmodel',
            name='questionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.QuestionModel'),
        ),
        migrations.AddField(
            model_name='favoritequestionmodel',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answermodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.AnswerModel'),
        ),
        migrations.AddField(
            model_name='answermodel',
            name='questionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='question.QuestionModel'),
        ),
        migrations.AddField(
            model_name='answermodel',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
