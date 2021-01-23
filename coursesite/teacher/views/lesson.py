from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Course
from registrar.models import Homework
from registrar.models import Lesson
from teacher.forms import LessonForm
from teacher.forms import HomeworkForm
from django import forms
from django.contrib import messages


@login_required(login_url='/landpage')
def lesson_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'teacher/lesson/view.html', {
        'teacher': teacher,
        'course': course,
        'user': request.user,
        'tab': 'lessons',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def lesson_table(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    try:
        lessons = Lesson.objects.filter(course=course).order_by('-lesson_num')
        homeworks = Homework.objects.filter(Lesson=lessons)
        hw_dict = {}
        for lesson in lessons:
            for hw in homeworks:
                if lesson.lesson_id == hw.Lesson.lesson_id:
                    hw_dict[lesson.lesson_id] = hw.hw_id
                    break
                else:
                    hw_dict[lesson.lesson_id] = 0
    except Lesson.DoesNotExist:
        lessons = None
        homeworks = None
    return render(request, 'teacher/lesson/table.html', {
        'homeworks': homeworks,
        'hw_dict': hw_dict,
        'teacher': teacher,
        'course': course,
        'lessons': lessons,
        'user': request.user,
    })


@login_required(login_url='/landpage')
def lesson_modal(request, course_id):
    if request.method == u'POST':
        # Get the lesson_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular lesson.
        lesson_id = int(request.POST['lesson_id'])
        form = None
        if lesson_id > 0:
            lesson = Lesson.objects.get(lesson_id=lesson_id)
            form = LessonForm(instance=lesson)
        else:
            form = LessonForm()
        return render(request, 'teacher/lesson/modal.html', {
            'form': form,
        })


@login_required(login_url='/landpage')
def hwlesson_modal(request, course_id):
    lesson_id = int(request.GET['lesson_id'])
    hw_id = int(request.GET['hw_id'])
    form = None
    if hw_id > 0:
        hw = Homework.objects.get(hw_id=hw_id)
        form = HomeworkForm(instance=hw)
        form.fields['Lesson'].widget = forms.HiddenInput()
    else:
        form = HomeworkForm()
        form.fields['Lesson'].widget = forms.HiddenInput()
    print(request.POST)

    return render(request, 'teacher/lesson/hwmodal.html', {'form': form, 'lesson': lesson_id})


@login_required(login_url='/landpage')
def save_lesson(request, course_id):
    response_data = {'status': 'failed', 'message': 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            lesson_id = int(request.POST['lesson_id'])
            form = None

            # If lesson already exists, then lets update only, else insert.
            if lesson_id > 0:
                lesson = Lesson.objects.get(lesson_id=lesson_id)
                form = LessonForm(instance=lesson, data=request.POST, files=request.FILES)
            else:
                form = LessonForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.course = course
                instance.save()
                response_data = {'status': 'success', 'message': 'saved'}
            else:
                response_data = {'status': 'failed', 'message': json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def save_hw(request, course_id):
    response_data = {'status': 'failed', 'message': 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            lesson_id = int(request.POST['Lesson'])
            hw_id = int(request.POST['hw_id'])
            form = None
            # If lesson already exists, then lets update only, else insert.
            if hw_id > 0:
                hw = Homework.objects.get(hw_id=hw_id)
                form = HomeworkForm(instance=hw, data=request.POST, files=request.FILES)
            else:
                form = HomeworkForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                response_data = {'status': 'success', 'message': 'saved'}
            else:
                response_data = {'status': 'failed', 'message': json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_lesson(request, course_id):
    response_data = {'status': 'failed', 'message': 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            lesson_id = int(request.POST['lesson_id'])
            teacher = Teacher.objects.get(user=request.user)
            try:
                lesson = Lesson.objects.get(lesson_id=lesson_id)
                if lesson.course.teacher == teacher:
                    lesson.delete()
                    response_data = {'status': 'success', 'message': 'deleted'}
                else:
                    response_data = {'status': 'failed', 'message': 'unauthorized deletion'}
            except Lesson.DoesNotExist:
                response_data = {'status': 'failed', 'message': 'record not found'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
