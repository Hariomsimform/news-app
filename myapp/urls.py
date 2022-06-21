from django.urls import path
from .views import add_news, approve_news, delete, improve_news, logout_reqest, news_editor, news_publisher,news_reporter, pending_from_editor, pending_from_publisher, publish_news, register, login, home, reject_news, reporter_publish_news, send_comment, task_mail, user_profile
urlpatterns = [
    path('task-mail/', task_mail, name='task_mail' ),
    path('', register, name='register' ),
    path('login/',login, name='login'),
    path('home/',home, name='home'),
    path('user-profile/', user_profile, name='user-profile'),
    path('logout/', logout_reqest, name='logout-request'),
    path('admin-backend/', news_reporter, name='news-reporter'),
    path('news-editor/', news_editor, name='news-editor'),
    path('news-publisher/', news_publisher, name='news-publisher'),
    path('add-news/', add_news, name='add-news'),  
    path('improve-news/<int:id>', improve_news, name='improve-news'),
    path('approved/<int:id>', approve_news, name='approve-news'), 
    path('rejected/<int:id>', reject_news, name='reject-news'),
    path('published/<int:id>/', publish_news, name='add-news'),
    path('pending-news-editor/', pending_from_editor, name='pending-news'),
    path('pending-news-publisher/', pending_from_publisher, name='pending-news'),
    path('sent-comment/<int:id>', send_comment, name='send-comments'),
    path('commented-news/', pending_from_editor, name='pending-news'),
    path('published-news/', reporter_publish_news, name='reporter-publish-news'),
    path('delete/', delete, name='delete'),
    path('published-news-publisher/', reporter_publish_news, name='delete')

]