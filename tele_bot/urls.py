from django.conf.urls import url
from django.contrib import admin
from funbot.views import TelegramBotView,ChatLogView

urlpatterns = [
    url(r'^chat_api/?$', TelegramBotView.as_view()),
    url(r'^$', ChatLogView.as_view(),name='chat_log'),
    url(r'^admin/', admin.site.urls)
]
