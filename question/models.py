from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from linuxturkey import settings


class QuestionCategoryModel(models.Model):
    categoryID = models.AutoField(verbose_name='Kategori ID', primary_key=True)
    categoryName = models.CharField(verbose_name='Kategori Adi', max_length=150)

    def __str__(self):
        return self.categoryName


class QuestionModel(models.Model):
    id = models.AutoField(verbose_name='Soru ID', primary_key=True)
    questionTitle = models.CharField(verbose_name='Soru Başlığı', max_length=150)
    questionContent = RichTextUploadingField(verbose_name='Sorunuz')
    questionCreateDate = models.DateTimeField(verbose_name='Soru Olusturma Tarihi', auto_now_add=True)
    questionEditDate = models.DateTimeField(verbose_name='Soru Guncellenme Tarihi', null=True)
    questionViewCounter = models.IntegerField(verbose_name='Okunma Sayisi', default=0)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    categoryID = models.ForeignKey(QuestionCategoryModel, models.CASCADE, verbose_name='Kategori')
    slug = models.SlugField(unique=True, editable=False, max_length=135)
    emailNotifications = models.BooleanField(verbose_name='Soruya cevap gelirse mail gönderilsin mi?', default=True)

    def __str__(self):
        return self.questionTitle

    def get_unique_slug(self):
        slug = slugify(self.questionTitle)
        unique_slug = slug
        counter = 1
        while QuestionModel.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(QuestionModel, self).save(*args, **kwargs)


class AnswerModel(models.Model):
    id = models.AutoField(verbose_name='Cevap ID', primary_key=True)
    answer = RichTextUploadingField(verbose_name='Cevabınız')
    answerDate = models.DateTimeField(verbose_name='Cevap Tarih', auto_now_add=True)
    bestAnswer = models.BooleanField(verbose_name='En Iyi Cevap', default=0)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    questionID = models.ForeignKey(QuestionModel, related_name='answer', on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name='score', default=0)

    class Meta:
        ordering = ['-answerDate']

    def __str__(self):
        return self.answer

    def children(self):
        return AnswerModel.objects.filter(parent=self)

    def get_score_count(self):
        score = self.score
        return score

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        else:
            return True

    def __unicode__(self):
        return '{} : {}'.format(self.id, self.answer)

    # TODO : devam et gruplandırıp puanı topla ılk ucu dondur context


class QuestionReportModel(models.Model):
    reportID = models.AutoField(verbose_name='Rapor ID', primary_key=True)
    questionID = models.ForeignKey(QuestionModel, models.CASCADE)
    reporterID = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True)
    reportReason = models.CharField(verbose_name='Raporlama Sebebi', max_length=255)


class FavoriteQuestionModel(models.Model):
    favoriteQuestionID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    questionID = models.ForeignKey(QuestionModel, models.CASCADE)
    addDate = models.DateTimeField(auto_now_add=True)


class ScoreModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='score_user', on_delete=True)
    answer = models.ForeignKey(AnswerModel, on_delete=True, related_name='score_answer')
    score_status = models.SmallIntegerField(verbose_name='Score durumu', null=True, default=0)

    def __str__(self):
        return "{} {} {}".format(self.user, self.answer, self.score_status)
