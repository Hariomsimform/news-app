from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    news_preference_1 = models.CharField(max_length=50)
    news_preference_2 = models.CharField(max_length=50)
    news_preference_3 = models.CharField(max_length=50)
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return '{} {} {}'.format(self.news_preference_1,
                                 self.news_preference_2,
                                 self.news_preference_3
                                )

class Articles(models.Model):
    article_img_url = models.URLField(max_length=500,null=True)
    article_author = models.CharField(max_length=250,null=True)
    article_title = models.TextField()
    article_description = models.TextField()
    article_url = models.URLField(max_length=500)
    article_publish = models.DateTimeField()
    article_category = models.CharField(max_length=50)
    
    def __str__(self):
        return '{} {} {}'.format(self.article_title,
                                 self.article_author,
                                 self.article_img_url
                                 )

class News(models.Model):
    article_img = models.ImageField(upload_to="images/")
    article_author = models.CharField(max_length=250,null=True)
    article_title = models.TextField()
    article_description = models.TextField()
    article_publish = models.DateTimeField(null=True)
    # article_reporter = models.OneToOneField(User, on_delete=models.CASCADE)
    # article_editor = models.OneToOneField(User, on_delete=models.CASCADE)
    # article_publisher = models.OneToOneField(User, on_delete=models.CASCADE)
    reporter_condition = models.CharField(max_length=10, default=None, null=True)
    editor_condition = models.CharField(max_length=20, default=None, null=True)
    publisher_condition = models.CharField(max_length=20, default=None, null=True)

class Comments(models.Model):
    comment=models.CharField(max_length=100)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)