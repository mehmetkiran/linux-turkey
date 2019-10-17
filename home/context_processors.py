from article.models import ArticleModel
from linuxturkey import settings
from linuxturkey.settings import *
from question.models import QuestionModel, AnswerModel, QuestionCategoryModel


def main_logo(request):
    return {'MAIN_LOGO': MAIN_LOGO}


def site_name(request):
    return {'site_name': SITE_NAME}


def statCounter(request):
    questionCount = QuestionModel.objects.count()
    answerCount = AnswerModel.objects.count()
    articleCount = ArticleModel.objects.count()
    return {'questionCount': questionCount, 'answerCount': answerCount, 'articleCount': articleCount}


def categoryList(request):
    categoryList = QuestionCategoryModel.objects.all()
    return {'categoryList': categoryList}


def app_version(request):
    return {'APP_VERSION': settings.APP_VERSION}


def last_question(request):
    lastQuestion = QuestionModel.objects.order_by('-id')[:2]
    return {'lastQuestion': lastQuestion}


def about(request):
    aboutUs = "Linux Türkiye Topluluğunun’nun amacı; Türkiyede’ki GNU linux kullanıcılarına Türkçe destek sağlamak ve" \
              " tecrübe edilmiş deneyimleri paylaşmaktır. Topluluğumuzda GNU linux çekirdeği üzerine yapılandırılmış " \
              "işletim sistemleriyle ve içerikleriyle alakalı tüm sorularınıza cevap bulabilirsiniz. Topluluğumuza " \
              "ait Telegram https://telegram.me/linuxturkey kanalı’nı kullanabilir veya web sitemiz " \
              "https://linuxturkey.org/ içindeki konuları inceleyebilirsiniz. Web sitemize üye olduğunuz takdirde " \
              "yeni konu oluşturabilirsiniz. "

    return {'aboutUs': aboutUs}


def tags(request):
    tags = [
        'gnu/linux',
        'ubuntu',
        'debian',
        'arch',
        'linux',
        'kernel'
    ]

    return {'tags': tags}


def social_media(request):
    social_media_url = ['twitter.com', 'fb.me', 'youtu.be' 'rss']
    social_media_icon = ['twitter', 'facebook', 'youtube', 'rss']
    original_title = ['Twitter', 'Facebook.com', 'Youtube', 'Rss']

    return {'url': social_media_url, 'icon': social_media_icon, 'title': original_title}
