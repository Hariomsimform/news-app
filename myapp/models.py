
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

