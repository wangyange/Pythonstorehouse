#-*-coding:utf-8-*-
from django.conf.urls import patterns, url
from dataCreate import views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
#     url(r'^$',login_required(views.newOrder)),
    url(r'^$',login_required(views.dataHome)),
    url(r'^newProduct$',login_required(views.newProduct)),
    url(r'^newCommodity$',login_required(views.newCommodity)),
    url(r'^newOrder$',login_required(views.newOrder)),
    url(r'^newProcurement$',login_required(views.newProcurement)),
    url(r'^newStock$',login_required(views.newStock)),
    url(r'^newCard$',login_required(views.newCard)),
    url(r'^SelectStock$',login_required(views.SelectStock)),    
)