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
    before=datetime.datetime.now()
    def task1():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=health&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        health_response = requests.get(url)
        health_data = health_response.json()
        global health_articles 
        health_articles=  health_data['articles']
    def task2():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=entertainment&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        entertainment_response = requests.get(url)
        entertainment_data = entertainment_response.json()
        global entertainment_articles
        entertainment_articles =  entertainment_data['articles']
    def task3():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=general&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        general_response = requests.get(url)
        general_data = general_response.json()
        global general_articles
        general_articles =  general_data['articles']
    def task4():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=business&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        business_response = requests.get(url)
        business_data = business_response.json()
        global business_articles
        business_articles =  business_data['articles']
    def task5():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=sports&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        sports_response = requests.get(url)
        sports_data = sports_response.json()
        global sports_articles
        sports_articles =  sports_data['articles']
    def task6():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=science&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        science_response = requests.get(url)
        science_data = science_response.json()
        global science_articles
        science_articles =  science_data['articles']
    def task7():
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=technology&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        technology_response = requests.get(url)
        technology_data = technology_response.json()
        global technology_articles
        technology_articles =  technology_data['articles']

    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2')  
    t3 = threading.Thread(target=task3, name='t3')
    t4 = threading.Thread(target=task4, name='t4')
    t5 = threading.Thread(target=task5, name='t5')
    t6 = threading.Thread(target=task6, name='t6') 
    t7 = threading.Thread(target=task7, name='t7')  
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()

    for health_article, entertainment_article, general_article,\
        business_article, sports_article, science_article, technology_article in (zip(health_articles,
        entertainment_articles,
        general_articles,business_articles,
        sports_articles, 
        science_articles, technology_articles)):
        article_list=[health_article, entertainment_article, general_article,
        business_article, sports_article, science_article, technology_article]
        article_category=['Health', 'Entertainment', 'General',
        'Business', 'Sports', 'Science', 'Technology']
        for index, article in enumerate(article_list):
            try:
                art=Articles.objects.get(article_title=article['title'])
            except:
                art=None  
            if art==None:
                article_instance=Articles(
                    article_img_url=article['urlToImage'],
                    article_author=article['author'],
                    article_title=article['title'][:250],
                    article_description=article['description'][:249],
                    article_url=article['url'],
                    article_publish=article['publishedAt'],
                    article_category=article_category[index]
                )
                article_instance.save()
                email=UserProfile.objects.filter(
                    news_preference_1=article_category[index].lower()
                    ).values_list('user_id__email',flat=True) 
                email=list(email)    
                send_mail_func.delay(email, 
                                    health_article['author'],
                                    health_article['title'],
                                    health_article['url'],
                                    article_category[index]
                                    )     
    return 'Done'                        
    
