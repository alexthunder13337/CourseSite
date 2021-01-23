from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Course
from registrar.models import SendHomework
from registrar.models import Policy
from registrar.models import Lesson


# Public Functions
# --------------------

@login_required(login_url='/landpage')
def overview_page(request, course_id):
    course = Course.objects.get(id=course_id)
    students = course.students.all()
    slist= []
    for student in students:
        slist.append(student.student_id)
    student_homeworks = SendHomework.objects.filter(student__in=slist)
    try:
        policy = Policy.objects.get(course=course)
    except Policy.DoesNotExist:
        policy = None

    try:
        lessons = Lesson.objects.filter(course=course_id)
    except Lesson.DoesNotExist:
        lessons = None
    for student in students:
        print(student.user.first_name)
        for lesson in lessons:
            print(lesson.title)
            for shw in student_homeworks:
                if shw.lesson.lesson_id == lesson.lesson_id and shw.student.student_id == student.student_id:
                    print(shw, shw.lesson.lesson_id, shw.student.student_id)


    return render(request, 'teacher/overview/view.html', {
        'homeworks': student_homeworks,
        'lessons': lessons,
        'course': course,
        'policy': policy,
        'students': students,
        'user': request.user,
        'tab': 'overview',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


