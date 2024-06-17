from django.db import models
from django.contrib.auth import get_user_model
from article.models import Article


class CommentManager(models.Manager):
    def published_comments(self):
        return self.filter(status="published")

class Comment(models.Model):


    STATUS_CHOICES = [
        ("draft", "پیش نویس"),
        ("published", "منتشرشده"),
    ]
    
    user = models.ForeignKey(get_user_model(), verbose_name='user', related_name = 'comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='article', related_name = 'comments', on_delete=models.CASCADE)
    content = models.TextField('content')
    datetime_create = models.DateTimeField('datetime_create', auto_now_add=True)
    reply = models.ForeignKey(("self"), verbose_name='reply', related_name = 'comment_replies', on_delete=models.CASCADE, blank=True, null=True)
    is_reply = models.BooleanField('is_reply', default=False)
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[1][0])
    objects = CommentManager()

    def __str__(self):
        return f" comment_id :{self.id}"
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
