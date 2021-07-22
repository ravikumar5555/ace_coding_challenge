from django.conf.urls import url
from . import views

transaction_urls = [
    url(r'^transactions', views.TransactionView.as_view(), name='TransactionView')
]