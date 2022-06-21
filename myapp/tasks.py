import requests
import datetime
import threading
import pyshorteners
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import UserProfile, Articles

@shared_task(bind=True)
def send_mail_func(duration, email,article_author, article_title, article_url,
                        article_category
                        ):
    mail_subject = f'Hey, new article for you'
    message = f"Hey| this is mail to inform you new article is published on your topic: {article_category}| Article Author: {article_author}| Article Title: {article_title}| Read Full Article Here- {article_url}"
    to_email = email
    print(to_email)
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=to_email,
        fail_silently=True,
    )
    return "Done" 

@shared_task(bind=True)
def task_mail(self):
    # print(time.time.now())
    categories = ['Health', 'Entertainment','General', 'Business', 'Sports', 'Science','Technology']
    news_dict = {}
    for category in categories:
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category={category}&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        print(url)
        news_response = requests.get(url)
        news_data = news_response.json()    
        news_dict[category+'_articles']=news_data['articles']
    for index, news in enumerate(news_dict):
        for article in news_dict[news]:
            try:
                art=Articles.objects.get(article_title=article['title'])
            except:
                art=None  
            if art==None:
                if article['description']==None:
                    article['description']='None'
                article_instance=Articles(
                    article_img_url=article['urlToImage'],
                    article_author=article['author'],
                    article_title=article['title'][:250],
                    article_description=article['description'][:249],
                    article_url=article['url'],
                    article_publish=article['publishedAt'],
                    article_category=categories[index]
                )
                article_instance.save()
                email=UserProfile.objects.filter(
                    news_preference_1=categories[index].lower()
                    ).values_list('user_id__email',flat=True) 
                email=list(email)    
                send_mail_func.delay(email, 
                                    article['author'],
                                    article['title'],
                                    article['url'],
                                    categories[index]
                                    )                    
    return ('Done')
