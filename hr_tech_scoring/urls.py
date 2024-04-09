# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='scoring_login'),
    path('index/', views.index, name='scoring_index'),
    path('row/<int:row_id>/', views.detail, name='scoring_detail'),
    # path('create_account/', views.create_account_view, name='scoring_create_account'),
]