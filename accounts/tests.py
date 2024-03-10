from django.test import TestCase
from django.contrib.auth import get_user_model
from course.models import Program
from .models import User, Student, Parent, DepartmentHead

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            is_student=True,
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(User.objects.count(), 1)

    def test_user_get_full_name(self):
        self.assertEqual(self.user.get_full_name, 'testuser')

    def test_user_get_user_role(self):
        self.assertEqual(self.user.get_user_role, 'Student')


class StudentModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='teststudent',
            password='testpassword',
            email='teststudent@example.com',
            is_student=True,
        )
        self.program = Program.objects.create(title='Test Program')
        self.student = Student.objects.create(student=self.user, level='Bachloar', department=self.program)


class ParentModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testparent',
            password='testpassword',
            email='testparent@example.com',
            is_parent=True,
        )
        self.program = Program.objects.create(title='Test Program') 
        self.student_user = get_user_model().objects.create_user(
            username='teststudent',
            password='testpassword',
            email='teststudent@example.com',
            is_student=True,
        )
        self.student = Student.objects.create(student=self.student_user, level='Bachloar', department=self.program)
        self.parent = Parent.objects.create(user=self.user, student=self.student, first_name='John', last_name='Doe')

class DepartmentHeadModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testhead',
            password='testpassword',
            email='testhead@example.com',
            is_dep_head=True,
        )
        self.program = Program.objects.create(title='Test Program') 
        self.head = DepartmentHead.objects.create(user=self.user, department=self.program)


