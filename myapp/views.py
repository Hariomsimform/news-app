from hashlib import new
import time
import pyshorteners
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import Articles, UserProfile, News, Comments
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
            if user.groups.filter(name__in=['Reporter', 'Editor',  'Publisher']).exists():
                return redirect('/admin-backend/')
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

@login_required(login_url='/login/')
def news_reporter(request):
    group = request.user.groups.values_list('name',flat=True)
    user_group=group[0]
    print(user_group)
    return render(request, template_name='myapp/reporter.html',context={'user_group':user_group})

@login_required(login_url='/login/')
def news_editor(request):
    return render(request, template_name='myapp/editor.html')

@login_required(login_url='/login/')
def news_publisher(request):
    return render(request, template_name='myapp/publisher.html')

@login_required(login_url='/login/')
@permission_required('myapp.add_news', raise_exception=True)
def add_news(request):
    if request.method=='POST':
        image = request.FILES['image']
        title = request.POST['title']
        desc = request.POST['desc']
        reporter_condition = request.POST.get('draft',False)
        if reporter_condition:
            news=News(article_img=image, article_author="NONE",article_title=title, article_description=desc, reporter_condition=reporter_condition, editor_condition='pending')
        else:
            news=News(article_img=image, article_author="NONE",article_title=title, article_description=desc, reporter_condition=reporter_condition)
        news.save()

        return redirect('/admin-backend/')

    return render(request, template_name='myapp/newsform.html')   
@permission_required('myapp.view_news', raise_exception=True)
def improve_news(request, id):
    if request.method=='POST':
        return HttpResponse('Done')
    news=News.objects.get(id=id)
    return render(request, template_name='myapp/newsform.html', context={'news':news})         

@login_required(login_url='/login/')
@permission_required('myapp.view_news', raise_exception=True)
def pending_from_editor(request):
    articles = News.objects.filter(editor_condition='pending').all()
    article_all_data=[]
    for article in articles:
        article_all_data.append([article, list(article.comments_set.all())])
    group = request.user.groups.values_list('name',flat=True)
    user_group=group[0]
    return render(request, template_name='myapp/editor_article.html', context={'articles_all_data':article_all_data, 'user_group':user_group,'user':request.user})

@login_required(login_url='/login/')
@permission_required('myapp.view_news', raise_exception=True)
def pending_from_publisher(request):
    articles = News.objects.filter(publisher_condition='not published').all()
    return render(request, template_name='myapp/publish_article.html', context={'articles':articles})

@login_required(login_url='/login/')
@permission_required('myapp.change_news','myapp.view_news', raise_exception=True)
def approve_news(request, id):
    news = News.objects.get(id=id)
    news.editor_condition = 'approved'
    news.publisher_condition = 'not published'
    news.save()
    return redirect('/pending-news-editor/')

@permission_required('myapp.change_news', raise_exception=True)
def reject_news(request,id):
    news=News.objects.get(id=id)
    news.editor_condition = 'rejected'
    news.save()
    return redirect('/pending-news-editor/')

@login_required(login_url='/login/')
@permission_required('myapp.change_news','myapp.view_news', raise_exception=True)
def publish_news(request, id):
    news = News.objects.get(id=id)
    news.publisher_condition = 'published'
    news.save()
    return redirect('/pending-news-publisher/')  

@login_required(login_url='/login/')
@permission_required('myapp.add_news', raise_exception=True)
def send_comment(request,id):
    if request.method=='POST':
        news=News.objects.get(id=id)
        comment = request.POST['comment']
        comment = Comments(comment=comment, commentor=request.user, news=news)
        comment.save()
        return redirect('/pending-news-editor/')


@login_required(login_url='/login/')
@permission_required('myapp.view_news', raise_exception=True)
def reporter_publish_news(request):
    article_all_data = News.objects.filter(publisher_condition='published')
    return render(request, template_name='myapp/reporter_publish_news.html', context={'articles_all_data':article_all_data} )


@login_required(login_url='/login/')
@permission_required('myapp.delete_news', raise_exception=True)
def delete(request):
    news=News.objects.filter(id=6).delete()
    return redirect('/admin-backend/')



import requests
import time
def task_mail(self):
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
                print(art.article_title)
                print(categories[index])
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
    return HttpResponse('Done') 

