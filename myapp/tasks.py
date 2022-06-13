import requests
import datetime
import threading
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
                article_img_url=article['urlToImage']
                article_url=article['url']
                article_title = article['title']
                print(len(article_title))
                if article_url:
                    if len(article_url)>250:
                        shortener=pyshorteners.Shortener()
                        x = shortener.tinyurl.short(article_url)
                        article_url = x

                if article_img_url:
                    if len(article_img_url)>200:
                        shortener=pyshorteners.Shortener()
                        x = shortener.tinyurl.short(article_img_url)
                        article_img_url = x    

                article_instance=Articles(
                    article_img_url=article_img_url,
                    article_author=article['author'],
                    article_title=article['title'],
                    article_description=article['description'][:249],
                    article_url=article_url,
                    article_publish=article['publishedAt'],
                    article_category=article_category[index]
                )
                article_instance.save()
                user=UserProfile.objects.filter(
                    news_preference_1=article_category[index].lower()).values('user_id__email') 
                email = []
                for profile in user:
                    email.append(profile['user_id__email'])
                send_mail_func.delay(email, 
                                    health_article['author'],
                                    health_article['title'],
                                    health_article['url'],
                                    article_category[index]
                                    )
    return 'Done'                                
    #     try:
    #         try:
    #             art=Articles.objects.get(article_title=health_article['title'])
    #         except:
    #             art=None  
    #         if art==None:
    #             a=Articles(
    #                 article_img_url=health_article['urlToImage'],
    #                 article_author=health_article['author'],
    #                 article_title=health_article['title'],
    #                 article_description=health_article['description'],
    #                 article_url=health_article['url'],
    #                 article_publish=health_article['publishedAt'],
    #                 article_category='Health'
    #             )
    #             a.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='health').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email'])
    #             send_mail_func.delay(email, 
    #                                 health_article['author'],
    #                                 health_article['title'],
    #                                 health_article['url'],
    #                                 'Health'
    #                                 )
    #     except:
    #         pass
    #     try:
    #         try:
    #             art=Articles.objects.get(article_title=entertainment_article['title'])
    #         except:
    #             art=None  
    #         if art==None:
    #             a=Articles(
    #                 article_img_url=entertainment_article['urlToImage'],
    #                 article_author=entertainment_article['author'],
    #                 article_title=entertainment_article['title'],
    #                 article_description=entertainment_article['description'], 
    #                 article_url=entertainment_article['url'],
    #                 article_publish=entertainment_article['publishedAt'],
    #                 article_category='Entertainment'
    #                 )
    #             a.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='entertainment').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email'])
    #             send_mail_func.delay(
    #                                 email,
    #                                 entertainment_article['author'],
    #                                 entertainment_article['title'],
    #                                 entertainment_article['url'],
    #                                 'Entertainment'
    #                                 )
    #     except:
    #         pass

    #     try:
    #         try:
    #             art = Articles.objects.get(article_title=general_article['title'])
    #         except:
    #             art = None  
    #         if art==None:
    #             article=Articles(
    #                 article_img_url=general_article['urlToImage'],
    #                 article_author=general_article['author'],
    #                 article_title=general_article['title'],
    #                 article_description=general_article['description'],
    #                 article_url=general_article['url'],
    #                 article_publish=general_article['publishedAt'], 
    #                 article_category='General'
    #                 )
    #             article.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='general').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email']) 
    #             send_mail_func.delay(email,general_article['author'],
    #                                 general_article['title'],
    #                                 general_article['url'],
    #                                 'General'
    #                                 )
    #     except:
    #         pass

    #     try:
    #         try:
    #             art=Articles.objects.get(article_title=business_article['title'])
    #         except:
    #             art=None  
    #         if art==None:
    #             a=Articles(article_img_url=business_article['urlToImage'],
    #                         article_author=business_article['author'],
    #                         article_title=business_article['title'], 
    #                         article_description=business_article['description'],
    #                         article_url=business_article['url'],
    #                         article_publish=business_article['publishedAt'],
    #                         article_category='Business'
    #                         )
    #             a.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='business').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email'])
    #             send_mail_func.delay(email,
    #                     business_article['author'],
    #                     business_article['title'],
    #                     business_article['url'],
    #                     'Business'
    #                     )

    #     except:
    #         pass

    #     try:
    #         try:
    #             art=Articles.objects.get(article_title=sports_article['title'])
    #         except:
    #             art=None  
    #         if art==None:
    #             a=Articles(article_img_url=sports_articles['urlToImage'],
    #             article_author=sports_articles['author'], 
    #             article_title=sports_articles['title'],
    #             article_description=sports_articles['description'],
    #             article_url=sports_articles['url'], 
    #             article_publish=sports_articles['publishedAt'],
    #             article_category='Sports')
    #             a.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='sports').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email'])  
    #             send_mail_func.delay(email,sports_article['author'],
    #                     sports_article['title'],sports_article['url'],
    #                     'Sports'
    #                     )
    #     except:
    #         pass

    #     try:
    #         try:
    #             art=Articles.objects.get(article_title=science_article['title'])
    #         except:
    #             art=None  
    #         if art==None:   
    #             a=Articles(article_img_url=science_articles['urlToImage'],
    #                         article_author=science_articles['author'], 
    #                         article_title=science_articles['title'], 
    #                         article_description=science_articles['description'], 
    #                         article_url=science_articles['url'], 
    #                         article_publish=science_articles['publishedAt'], 
    #                         article_category='Science'
    #                         )
    #             a.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='science').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email'])
    #             print(email) 
    #             send_mail_func.delay(email,science_article['author'],
    #                 science_article['title'],
    #                 science_article['url'],
    #                 'Science'
    #             )
    #     except:
    #         pass 

    #     try:
    #         try:
    #             art=Articles.objects.get(article_title=technology_article['title'])
    #         except:
    #             art=None    
    #         if art==None:
    #             a=Articles(
    #                 article_img_url=technology_articles['urlToImage'],
    #                 article_author=technology_articles['author'], 
    #                 article_title=technology_articles['title'], 
    #                 article_description=technology_articles['description'], 
    #                 article_url=technology_articles['url'], 
    #                 article_publish=technology_articles['publishedAt'], 
    #                 article_category='Technology'
    #             )
    #             a.save()
    #             user=UserProfile.objects.filter(
    #                 news_preference_1='technology').values('user_id__email') 
    #             email = []
    #             for profile in user:
    #                 email.append(profile['user_id__email'])  
    #             send_mail_func.delay(email,technology_article['author'],
    #                                 technology_article['title'],
    #                                 technology_article['url'],
    #                                 'Technology'
    #                                 )
    #     except:
    #         pass           
    # return ('Done Finally')