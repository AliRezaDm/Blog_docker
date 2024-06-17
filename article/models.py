from django.db import models

# Create your models here.
from django.db import models

from django.db import models
from django.utils import timezone, html 
from extensions.utils import jalali_converter

#Managers 
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='P')
     
class CategoryManager(models.Manager):
    def active(self):
         return self.filter(status=True)
    

class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیردسته')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True, verbose_name='وضعیت نمایش')
    position = models.IntegerField()
    
    class Meta:
            verbose_name = 'دسته بندی '
            verbose_name_plural = 'دسته بندی ها '
            ordering = ['parent__id', 'position']

    def __str__(self) -> str:
         return self.title
    
    # initiatting Manager
    objects = CategoryManager()


class Article(models.Model):

    STATUS_CHOICE = (
        ('P', 'منتشر شده '),  
        ('D', 'پیش نویس')
    )   

    title = models.CharField(max_length=200, verbose_name='موضوع')
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='بدنه اصلی')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر مقاله')
    publish =  models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, verbose_name='وضعیت')
    
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها '
        ordering = ['-publish']
    def __str__ (self):
        return self.title

    

    def jpublish(self):
        return jalali_converter(self.publish )
        
    jpublish.short_description = short_decsription = 'زمان انتشار'
    
    def thumbnail_tag(self):
         return html.format_html("<img width=100; height=75; style='border-radius:10px;'src='{}'>".format(self.thumbnail.url))
    thumbnail_tag.short_description = short_decsription = 'تصویر مقاله'

    def category_to_str(self):
         return " - ".join([category.title for category in self.category.active()])
    category_to_str.short_description = 'دسته بندی'

# initiatting Manager    
    objects = ArticleManager()

    