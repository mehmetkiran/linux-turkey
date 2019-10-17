from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from question.models import QuestionCategoryModel
from user.models import UserModel
from linuxturkey import settings
from django.utils.text import slugify


class ArticleModel(models.Model):
    id = models.AutoField(verbose_name='Makale ID', primary_key=True)
    articleTitle = models.CharField(verbose_name='Makale Basligi', max_length=250)
    articleContent = RichTextUploadingField(verbose_name='Makale')
    articleViewCounter = models.IntegerField(verbose_name='Okunma sayisi', default=0)
    articleCreateDate = models.DateTimeField(verbose_name='Olusturulma Tarihi', auto_now_add=True)
    articleAuthor = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    categoryName = models.ForeignKey(QuestionCategoryModel, models.SET(1), verbose_name='Kategori Adı')
    articleCoverImage = models.ImageField(null=True, blank=True, verbose_name='Kapak Fotoğrafı', upload_to='article/',
                                          default='article/Dma7XY2XgAIWNOZ.jpg')
    slug = models.SlugField(unique=True, editable=False, max_length=135)

    def get_unique_slug(self):
        slug = slugify(self.articleTitle)
        unique_slug = slug
        counter = 1
        while ArticleModel.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(ArticleModel, self).save(*args, **kwargs)

    # TODO : Eger ana kategoride herhangi bir eleman varsa kategori silinmesin. Duzelt.


class CommentModel(models.Model):
    commentID = models.AutoField(verbose_name='Yorum ID', primary_key=True)
    comment = models.TextField(verbose_name='Yorum')
    commentDate = models.DateTimeField(verbose_name='Yorum Tarihi', auto_now_add=True)
    articleID = models.ForeignKey(ArticleModel, related_name='answer', on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
