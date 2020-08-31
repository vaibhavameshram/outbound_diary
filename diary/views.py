from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic
from .models import Article, Student

class IndexView(generic.ListView):
    template_name = 'diary/index.html'
    context_object_name = 'latest_student_list'

    def get_queryset(self):
     """Return the last five published students (not including those set to be published in the future)."""

     return Student.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
    
