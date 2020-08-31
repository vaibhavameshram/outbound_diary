import datetime
from django.db import models
from django.utils import timezone

class Student(models.Model):
    full_name = models.CharField(max_length=70)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.full_name
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Article(models.Model):
    pub_date = models.DateTimeField('date published')
    image = models.CharField(max_length=200)
    program = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    research_area =models.CharField(max_length=200)
    dura = models.CharField(max_length=200)
    content = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.university