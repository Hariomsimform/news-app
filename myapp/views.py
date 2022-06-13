import time
import pyshorteners
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Articles, UserProfile
from .tasks import send_mail_func
  
def register(request):
    if request.method=='POST':
        user_name = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password'] 
        try:
            check_username = User.objects.get(username=user_name)
            check_email = User.objects.get(email=email)
        except:
            check_username = None
            check_email = None 
        print(check_username, check_email)      
        if check_username and check_email:
            
            return render(request=request, template_name='myapp/register.html',
                            context={'message':'Email and User Name Must Be Unique'}
                            )
        else:
            user = User.objects.create_user(username=user_name,first_name=first_name,
                                            last_name=last_name, email=email, 
                                            password=password)
            user.save()
            print('saved')
            return render(request=request, template_name='myapp/login.html',
                            context={'message':'Account Created Successfully!'})
    else:
        return render(request=request, template_name='myapp/register.html')  


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/home/')
        else:
            return render(request=request,template_name="myapp/login.html",
                            context={'message':'Username and Password Not Same! Try Again'})
    else:
        return render(request, 'myapp/login.html')       

def logout_reqest(request):
	logout(request)
	return render(request=request, template_name='myapp/login.html',
                    context={'message':'Logout Successfully!'})

@login_required(login_url='/login/')
def home(request):
    articles = Articles.objects.order_by('-id')[:200]  
    for article in articles:
        try:
            print('Author:', len(article.article_author),'Title:',len(article.article_title),'Article URL:', len(article.article_url), 'article img url:',len(article.article_img_url),'article descriptin:', len(article.article_description))    
        except:
            pass
    return render(request=request, template_name='myapp/home.html', context={'articles':articles})

@login_required(login_url='/login/')        
def user_profile(request):
    if request.method=='POST':
        first_pref = request.POST['first']
        second_pref = request.POST['second']
        third_pref = request.POST['third']
        user_profile=UserProfile(news_preference_1=first_pref,
                news_preference_2=second_pref, 
                news_preference_3=third_pref,
                user_id=request.user
                )
        user_profile.save()
    return render(request=request,template_name='myapp/user_profile.html')

import requests
import datetime
import threading
def task_mail(self):
    before=datetime.datetime.now()
    def task1():
        global health_articles 
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=health&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        health_response = requests.get(url)
        health_data = health_response.json()
        health_articles=  health_data['articles']
    def task2():
        global entertainment_articles
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=entertainment&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        entertainment_response = requests.get(url)
        entertainment_data = entertainment_response.json()
        entertainment_articles =  entertainment_data['articles']
    def task3():
        global general_articles
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=general&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        general_response = requests.get(url)
        general_data = general_response.json()
        general_articles =  general_data['articles']
    def task4():
        global business_articles
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=business&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        business_response = requests.get(url)
        business_data = business_response.json()
        business_articles =  business_data['articles']
    def task5():
        global sports_articles
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=sports&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        sports_response = requests.get(url)
        sports_data = sports_response.json()
        sports_articles =  sports_data['articles']
    def task6():
        global science_articles
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=science&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        science_response = requests.get(url)
        science_data = science_response.json()
        science_articles =  science_data['articles']
    def task7():
        global technology_articles
        url =  f'https://newsapi.org/v2/top-headlines?language=en&category=technology&apiKey=a67b087124e741b5ab0a7dcdd5b18465'
        technology_response = requests.get(url)
        technology_data = technology_response.json()
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
    print(health_articles,
                entertainment_articles,
                general_articles,
                business_articles,
                sports_articles, 
                science_articles, 
                technology_articles)
    for health_article, entertainment_article, general_article,\
        business_article, sports_article, science_article, technology_article in (zip(
                                    health_articles, entertainment_articles,
                                    general_articles, business_articles,
                                    sports_articles, science_articles, technology_articles)):

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
                # if article_url:
                #     if len(article_url)>199:
                #         shortener=pyshorteners.Shortener()
                #         x = shortener.tinyurl.short(article_url)
                #         article_url = x

                # if article_img_url:
                #     if len(article_img_url)>199:
                #         shortener=pyshorteners.Shortener()
                #         x = shortener.tinyurl.short(article_img_url)
                #         article_img_url = x    

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
            
    return HttpResponse('Done')

dict={'title':"Mithali Raj a catalyst in the growth of Indian women's cricket, but " 'the writing was on the wall for her, - Times of India',}
