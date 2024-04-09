# myapp/urls.py

from django.urls import path
from . import views, bomb_views, numerosity_views, set_views

urlpatterns = [
    path('login/', views.login_view, name='game_login'),
    path('create_account/', views.create_account_view, name='game_create_account'),
    path('game_select/', views.game_select_view, name='game_select'),

    path('bomb_risk_test/introduction/', bomb_views.introduction, name='game_bomb_introduction'),
    path('bomb_risk_test/test_page/', bomb_views.test_page, name='game_bomb_test_page'),
    path('bomb_risk_test/result_page/', bomb_views.result_page, name='game_bomb_result_page'),

    path('numerosity/introduction/', numerosity_views.introduction, name='game_numerosity_introduction'),
    path('numerosity/test_page/', numerosity_views.test_page, name='game_numerosity_test_page'),
    path('numerosity/result_page/', numerosity_views.result_page, name='game_numerosity_result_page'),

    path('set/introduction/', set_views.introduction_view, name='set_introduction'),
    path('set/testpage1/', set_views.test_page_view1, name='set_testpage1'),
    path('set/testpage2/', set_views.test_page_view2, name='set_testpage2'),
    path('set/mypage/', set_views.my_page_view, name='set_mypage'),
    path('set/results/', set_views.results_view, name='set_results'),
    path('set/end/', set_views.end_view, name='set_end'),
    path('set/leave_page/', set_views.leave_page, name='leave_page'),
]