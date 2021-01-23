from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from registrar.models import Lecture
from registrar.models import Lesson
from registrar.models import Homework
from registrar.models import SendHomework
from student.forms import HWUploadForm
from account.models import Student
from django import forms
import json
import datetime


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


@login_required(login_url='/landpage')
def lessons_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user.id)
    hw_lessons = []
    hw_students = {}
    if student in course.tier1_students.all():
        tier1 = True
    else:
        tier1 = False
    if student in course.tier2_students.all():
        tier2 = True
    else:
        tier2 = False
    try:
        lessons = Lesson.objects.filter(course=course_id).order_by('lesson_num')
        homeworks = Homework.objects.filter(Lesson__in=lessons)
        student_hws = SendHomework.objects.filter(lesson__in=lessons)
        for hw in homeworks:
            hw_lessons.append(hw.Lesson.lesson_id)
        for lesson in lessons:
            for st in student_hws:
                if st.lesson.lesson_id == lesson.lesson_id and request.user.id == st.student.user.id:
                    hw_students[lesson.lesson_id] = request.user.id
                    break
                else:
                    hw_students[lesson.lesson_id] = 0
    except Lecture.DoesNotExist:
        lessons = None
        homeworks = None
    return render(request, 'course/lesson/view.html', {
        'tier1': tier1,
        'tier2': tier2,
        'course': course,
        'student': student,
        'homeworks': homeworks,
        'student_hws': student_hws,
        'hw_lessons': hw_lessons,
        'hw_students': hw_students,
        'lessons': lessons,
        'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
        'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
        'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
        'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
        'user': request.user,
        'tab': 'lessons',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def lesson(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user.id)
    if student in course.tier1_students.all():
        tier1 = True
    else:
        tier1 = False
    if student in course.tier2_students.all():
        tier2 = True
    else:
        tier2 = False
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            # Check to see if any fields where missing from the form.
            if request.POST['lesson_id'] != '':
                try:
                    lesson_id = int(request.POST['lesson_id'])
                    lesson = Lesson.objects.get(lesson_id=lesson_id)
                except Lesson.DoesNotExist:
                    lesson = None
                return render(request, 'course/lesson/details.html', {
                    'tier1': tier1,
                    'tier2': tier2,
                    'lesson': lesson,
                    'student': student,
                    'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
                    'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
                    'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
                    'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
                    'user': request.user,
                    'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
                    'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                    'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
                })


@login_required(login_url='/landpage')
def view_lesson_hw(request, course_id, lesson_id):
    response_data = {}
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user.id)
    hw_lessons = []
    hw_students = {}
    if student in course.tier1_students.all():
        tier1 = True
    else:
        tier1 = False
    if student in course.tier2_students.all():
        tier2 = True
    else:
        tier2 = False
    hw_lessons = []
    hw_students = {}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                homework = Homework.objects.get(Lesson=lesson_id)
            except Homework.DoesNotExist:
                homework = None
            return render(request, 'course/lesson/details.html', {
                'tier1': tier1,
                'tier2': tier2,
                'course': course,
                'student': student,
                'lesson': lesson,
                'homework': homework,
                'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
                'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
                'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
                'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
                'user': request.user,
                'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
                'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
            })

@login_required(login_url='/landpage')
def studenthw_modal(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user.id)
    hw_lessons = []
    hw_students = {}
    if student in course.tier1_students.all():
        tier1 = True
    else:
        tier1 = False
    if student in course.tier2_students.all():
        tier2 = True
    else:
        tier2 = False
    if request.method == u'POST':
        # Get the lesson_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular lesson.
        lesson_id = int(request.POST['lesson_id'])
        student_hw_id = int(request.POST['student_hw_id'])
        form = None
        if student_hw_id > 0:
            hw = SendHomework.objects.get(student_hw_id=student_hw_id)
            form = HWUploadForm(instance=hw)
        else:
            form = HWUploadForm()
        return render(request, 'course/lesson/sendhwmodal.html', {
            'form': form,
            'lesson': lesson_id,
            'student': student,
            'student_hw_id': student_hw_id,
        })

@login_required(login_url='/landpage')
def lesson_table(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user.id)
    hw_lessons = []
    hw_students = {}
    if student in course.tier1_students.all():
        tier1 = True
    else:
        tier1 = False
    if student in course.tier2_students.all():
        tier2 = True
    else:
        tier2 = False
    hw_lessons = []
    hw_students = {}
    try:
        lessons = Lesson.objects.filter(course=course_id).order_by('lesson_num')
        homeworks = Homework.objects.filter(Lesson__in=lessons)
        student_hws = SendHomework.objects.filter(lesson__in=lessons)
        for hw in homeworks:
            hw_lessons.append(hw.Lesson.lesson_id)
        for lesson in lessons:
            for st in student_hws:
                if st.lesson.lesson_id == lesson.lesson_id and request.user.id == st.student.user.id:
                    hw_students[lesson.lesson_id] = request.user.id
                    break
                else:
                    hw_students[lesson.lesson_id] = 0
    except Lecture.DoesNotExist:
        lessons = None
        homeworks = None
    return render(request, 'course/lesson/table.html', {
        'tier1': tier1,
        'tier2': tier2,
        'course': course,
        'homeworks': homeworks,
        'student_hws': student_hws,
        'hw_lessons': hw_lessons,
        'hw_students': hw_students,
        'lessons': lessons,
        'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
        'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
        'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
        'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
        'user': request.user,
        'student': student,
        'tab': 'lessons',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def save_hw(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user.id)
    hw_lessons = []
    hw_students = {}
    if student in course.tier1_students.all():
        tier1 = True
    else:
        tier1 = False
    if student in course.tier2_students.all():
        tier2 = True
    else:
        tier2 = False
    response_data = {'status': 'failed', 'message': 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            lesson_id = lesson_id
            student_hw_id = int(request.POST['student_hw_id'])
            form = None
            # If lesson already exists, then lets update only, else insert.
            if student_hw_id > 0:
                hw = SendHomework.objects.filter(student_hw_id=student_hw_id)[0]
                form = HWUploadForm(instance=hw, data=request.POST, files=request.FILES)
            else:
                form = HWUploadForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                response_data = {'status': 'success', 'message': 'saved'}
            else:
                response_data = {'status': 'failed', 'message': json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")