from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Course
import json
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/landpage')
def access_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    students = course.students.all()
    tier1_students = course.tier1_students.all()
    tier2_students = course.tier2_students.all()
    return render(request, 'teacher/access/view.html', {
        'students': students,
        'tier1_students': tier1_students,
        'tier2_students': tier2_students,
        'teacher': teacher,
        'course': course,
        'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
        'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
        'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
        'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
        'user': request.user,
        'tab': 'lectures',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def access_set(request, course_id):
    response_data = {'status': 'error', 'student_tier': 'failed'}
    course = Course.objects.get(id=course_id)
    data = request.GET
    student_id = data['student_id']
    student = Student.objects.get(student_id=student_id)
    tier = data['tier']
    event = data['event_status']
    if event == '0':
        print('EVENT = 0')
        if tier == '1':
            print('TIER 1...')
            course.tier1_students.remove(student)
            print('STUDENT REMOVED')
        elif tier == '2':
            print('TIER 2....')
            course.tier2_students.remove(student)
            print('STUDENT REMOVED')
    elif event == '1':
        if tier == '1':
            course.tier1_students.add(student)
        elif tier == '2':
            course.tier2_students.add(student)
    response_data = {'status': 'success', 'student_tier': 'updated'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
