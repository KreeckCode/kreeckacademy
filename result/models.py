from django.db import models
from django.urls import reverse

from accounts.models import Student
from app.models import Session, Semester
from course.models import Course

YEARS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (4, '5'),
        (4, '6'),
    )

# LEVEL_COURSE = "Level course"
BACHLOAR_DEGREE = "Bachloar"
MASTER_DEGREE = "Master"

LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BACHLOAR_DEGREE, "Bachloar Degree"),
    (MASTER_DEGREE, "Master Degree"),
)

FIRST = "First"
SECOND = "Second"
THIRD = "Third"
FINAL = "Final"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
    (FINAL, "Final"),
)

A_plus = "A+"
A = "A"
A_minus = "A-"
B_plus = "B+"
B = "B"
B_minus = "B-"
C_plus = "C+"
C = "C"
C_minus = "C-"
D = "D"
F = "F"
NG = "NG"

GRADE = (
        (A_plus, "A+"),
        (A, "A"),
        (A_minus, "A-"),
        (B_plus, "B+"),
        (B, "B"),
        (B_minus, "B-"),
        (C_plus, "C+"),
        (C, "C"),
        (C_minus, "C-"),
        (D, "D"),
        (F, "F"),
        (NG, "NG"),
)

PASS = "PASS"
FAIL = "FAIL"

COMMENT = (
    (PASS, "PASS"),
    (FAIL, "FAIL"),
)


class TakenCourseManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='taken_courses')
    assignment = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    mid_exam = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    quiz = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    attendance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    final_exam = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    grade = models.CharField(choices=GRADE, max_length=2, blank=True)
    point = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.course.slug})

    def __str__(self):
        return "{0} ({1})".format(self.course.title, self.course.code)

    def get_total(self, assignment, mid_exam, quiz, attendance, final_exam):
        # Define weightage for each component
        weight_assignment = 0.20
        weight_mid_exam = 0.30
        weight_quiz = 0.20
        weight_final_exam = 0.30

        # Calculate weighted scores
        weighted_assignment = float(assignment) * weight_assignment
        weighted_mid_exam = float(mid_exam) * weight_mid_exam
        weighted_quiz = float(quiz) * weight_quiz
        weighted_final_exam = float(final_exam) * weight_final_exam

        # Extra points for attendance (if 100%)
        extra_points = 5 if float(attendance) == 100 else 0

        # Calculate total score
        total_score = weighted_assignment + weighted_mid_exam + weighted_quiz + weighted_final_exam + extra_points

        return total_score

    def get_grade(self, total):
        if total >= 90:
            grade = 'A+'
        elif total >= 85:
            grade = 'A'
        elif total >= 80:
            grade = 'A-'
        elif total >= 75:
            grade = 'B+'
        elif total >= 70:
            grade = 'B'
        elif total >= 65:
            grade = 'B-'
        elif total >= 60:
            grade = 'C+'
        elif total >= 55:
            grade = 'C'
        elif total >= 50:
            grade = 'C-'
        elif total >= 45:
            grade = 'D'
        else:
            grade = 'F'
        return grade

    def get_comment(self, grade):
        if grade == 'F':
            comment = 'FAIL'
        else:
            comment = 'PASS'
        return comment

    def get_point(self, grade):
        credit = self.course.credit
        if grade == 'A+':
            point = 4
        elif grade == 'A':
            point = 4
        elif grade == 'A-':
            point = 3.75
        elif grade == 'B+':
            point = 3.5
        elif grade == 'B':
            point = 3
        elif grade == 'B-':
            point = 2.75
        elif grade == 'C+':
            point = 2.5
        elif grade == 'C':
            point = 2
        elif grade == 'C-':
            point = 1.75
        elif grade == 'D':
            point = 1
        else:
            point = 0
        return int(credit) * point

    def calculate_gpa(self, total_credit_in_semester):
        current_semester = Semester.objects.get(is_current_semester=True)
        student = TakenCourse.objects.filter(student=self.student, course__level=self.student.level, course__semester=current_semester)
        p = 0
        point = 0
        for i in student:
            credit = i.course.credit
            point = self.get_point(i.grade)
            p += int(credit) * point
        try:
            gpa = (p / total_credit_in_semester)
            return round(gpa, 2)
        except ZeroDivisionError:
            return 0
    
    def calculate_cgpa(self):
        current_semester = Semester.objects.get(is_current_semester=True)
        previousResult = Result.objects.filter(student__id=self.student.id, level__lt=self.student.level)
        previousCGPA = 0
        for i in previousResult:
            if i.cgpa is not None:
                previousCGPA += i.cgpa
        cgpa = 0
        if str(current_semester) == "SECOND":
            first_sem_gpa = 0.0
            sec_sem_gpa = 0.0
            try:
                first_sem_result = Result.objects.get(student=self.student.id, semester="FIRST", level=self.student.level)
                first_sem_gpa += first_sem_result.gpa
            except:
                first_sem_gpa = 0

            try:
                sec_sem_result = Result.objects.get(student=self.student.id, semester="SECOND", level=self.student.level)
                sec_sem_gpa += sec_sem_result.gpa
            except:
                sec_sem_gpa = 0

            taken_courses = TakenCourse.objects.filter(student=self.student, student__level=self.student.level)
            TCC = 0
            TCP = 0
            for i in taken_courses:
                TCP += float(i.point)
            for i in taken_courses:
                TCC += int(i.course.credit)

            try:
                cgpa = TCP / TCC
                return round(cgpa, 2)
            except ZeroDivisionError:
                return 0


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField(null=True)
    cgpa = models.FloatField(null=True)
    semester = models.CharField(max_length=100, choices=SEMESTER)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
