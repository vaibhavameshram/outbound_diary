from django.contrib import admin

from .models import Article, Student

class ArticleInline(admin.TabularInline):
    model = Article
    extra=1

class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['full_name']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ArticleInline]
    list_display = ('full_name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['full_name']

admin.site.register(Student, StudentAdmin)