import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Student


class StudentModelTests(TestCase):

    def test_was_published_recently_with_future_student(self):
        """
        was_published_recently() returns False for students whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_student = Student(pub_date=time)
        self.assertIs(future_student.was_published_recently(), False)

    def test_was_published_recently_with_old_student(self):
     """
     was_published_recently() returns False for students whose pub_date
     is older than 1 day.

     """
     time = timezone.now() - datetime.timedelta(days=1, seconds=1)
     old_student = Student(pub_date=time)
     self.assertIs(old_student.was_published_recently(), False)

    def test_was_published_recently_with_recent_student(self):
     """
     was_published_recently() returns True for students whose pub_date
     is within the last day.
     """
     time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
     recent_student = Student(pub_date=time)
     self.assertIs(recent_student.was_published_recently(), True)
    

def create_student(full_name, days):
     """
     Create a question with the given `full_name` and published the
     given number of `days` offset to now (negative for students published
     in the past, positive for students that have yet to be published).
     """
     time = timezone.now() + datetime.timedelta(days=days)
     return Student.objects.create(full_name=full_name, pub_date=time)
 
class StudentIndexViewTests(TestCase):
    def test_no_student(self):
        """
        If no students exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('diary:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No students are available.")
        self.assertQuerysetEqual(response.context['latest_student_list'], [])

    def test_past_student(self):
        """
        Students with a pub_date in the past are displayed on the
        index page.
        """
        create_student(full_name="Past student.", days=-30)
        response = self.client.get(reverse('diary:index'))
        self.assertQuerysetEqual(
            response.context['latest_student_list'],
            ['<Student: Past question.>']
        )

    def test_future_student(self):
         """
         Students with a pub_date in the future aren't displayed on
         the index page.
         """
         create_student(full_name="Future student.", days=30)
         response = self.client.get(reverse('diary:index'))
         self.assertContains(response, "No student are available.")
         self.assertQuerysetEqual(response.context['latest_student_list'], [])

    def test_future_student_and_past_student(self):
         """
         Even if both past and future students exist, only past students
         are displayed.
         """
         create_student(full_name="Past student.", days=-30)
         create_student(full_name="Future student.", days=30)
         response = self.client.get(reverse('diary:index'))
         self.assertQuerysetEqual(
             response.context['latest_student_list'],
             ['<Student: Past student.>']
        )

    def test_two_past_students(self):
         """
         The students index page may display multiple students.
         """
         create_student(full_name="Past student 1.", days=-30)
         create_student(full_name="Past student 2.", days=-5)
         response = self.client.get(reverse('diary:index'))
         self.assertQuerysetEqual(
             response.context['latest_student_list'],
             ['<Student: Past student 2.>', '<Student: Past student 1.>']
        )

class StudentDetailViewTests(TestCase):
    def test_future_student(self):
        """
        The detail view of a student with a pub_date in the future
        returns a 404 not found.
        """
        future_student = create_student(full_name='Future student.', days=5)
        url = reverse('diary:detail', args=(future_student.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_student(self):
        """
        The detail view of a student with a pub_date in the past
        displays the student's text.
        """
        past_student = create_student(full_name='Past Student.', days=-5)
        url = reverse('diary:detail', args=(past_student.id,))
        response = self.client.get(url)
        self.assertContains(response, past_student.full_name)