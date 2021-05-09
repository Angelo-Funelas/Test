from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import *

now = datetime.now()

def checkclass(request, class_code_id):
    try:
        checkclassroom = classroom.objects.get(pk=class_code_id)
        if checkclassroom.password:
            return JsonResponse({"password_exists": "true"})
        else:
            return JsonResponse({"password_exists": "false"})
    except:
        return JsonResponse({
            "password_exists": "false",
            "exists": "false"
        })


def unenroll(request, classroom_id_leave):
    if request.user.is_authenticated:
        if request.user.role == 'Student':
            leave_classroom = classroom.objects.get(pk=classroom_id_leave)
            leave_classroom.students.remove(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse('classr'))
        else:
            return render(request, "school/error.html", {
                "error": "Oops, something went wrong."
            })
    else:
        return render(request, "school/error.html", {
            "error": "Not logged in."
        })

@csrf_exempt
def viewtask(request, task_id):
    task = activity.objects.get(pk=task_id)
    if request.method == 'GET':
        if request.user in task.completed_students.all():
            task_finished_status = 'Passed';
        else:
            task_finished_status = 'NotPassed';
        finished_students = []
        for student in task.completed_students.all():
            finished_students.append(f"{student.first_name} {student.last_name}")
        try:
            classcoverphoto = task.for_class.classcoverphoto.url
        except:
            classcoverphoto = ''
        try:
            attachedfile_name = task.attachedfile.name
            attachedfile_url = task.attachedfile.url
            attachedfile_size = task.attachedfile.size
        except:
            attachedfile_name = ''
            attachedfile_url = ''
            attachedfile_size = ''
        return JsonResponse({
            "task_finished_status": task_finished_status,
            "activity_id": task.id,
            "title": task.title,
            "description": task.description,
            "attachedlink": task.attachedlink,
            "attachedfile": {
                "name": attachedfile_name,
                "url": attachedfile_url,
                "size": attachedfile_size
            },
            "forclass": {
                "name": task.for_class.classname,
                "hex_color": task.for_class.hex_color,
                "id": task.for_class.id,
                "classcoverphoto": classcoverphoto
            },
            "finished_students": finished_students,
            "closed": task.closed
        })
    elif request.method == 'POST':
        data4 = json.loads(request.body);
        if data4.get("action") == 'turn_in':
            task.completed_students.add(User.objects.get(pk=data4.get("user_id")))
        if data4.get("action") == 'close':
            if User.objects.get(pk=data4.get("user_id")) == task.for_class.teacher:
                task.closed = True
                task.save()
        if data4.get("action") == 'reopen':
            if User.objects.get(pk=data4.get("user_id")) == task.for_class.teacher:
                task.closed = False
                task.save()


def classr(request):
    classes = classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))
    try:
        if request.method == 'POST':
            #check if class_id is not an empty string
            if request.POST["class_id"] != '':
                class_id = request.POST["class_id"]
            else:
                return render(request, "school/class.html", {
                    "classes": classes,
                    "error": "Invalid classroom ID"
                })
            try:
                classroom_toJoin = classroom.objects.get(pk=class_id)
                if request.user in classroom_toJoin.students.all():
                    return render(request, "school/class.html", {
                        "classes": classes,
                        "error": "You're already in this class."
                    })
                else:
                    if classroom_toJoin.password:
                        try:
                            classroom_PostPassword = request.POST["class_password"]
                        except:
                            return render(request, "school/class.html", {
                                "classes": classes,
                                "error": "Wrong Password."
                            })
                        if classroom_toJoin.password == classroom_PostPassword:
                            classroom_toJoin.students.add(request.user)
                        else:
                            return render(request, "school/class.html", {
                                "classes": classes,
                                "error": "Wrong Password."
                            })
                    else:
                        classroom_toJoin.students.add(request.user)
                        return HttpResponseRedirect(reverse('classr'))

            except classroom.DoesNotExist:
                return render(request, "school/class.html", {
                    "classes": classes,
                    "error": "Invalid classroom ID"
                })

    except:
        return render(request, "school/error.html", {
            "error": "Not logged in."
        })

    if request.user.role == 'Student':
        classes = classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))
        return render(request, "school/class.html", {
            "classes": classes
        })
    elif request.user.role == 'Teacher':
        classes = classroom.objects.filter(teacher=User.objects.get(pk=request.user.id))
        return render(request, "school/class.html", {
            "classes": classes
        })

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "school/index.html", {
            "landing": 'True',
            "previewUser": User.objects.all()[:10]
        })


def home(request):
    if request.user.is_authenticated:
        allposts2 = postobject.objects.exclude(parent_user=User.objects.get(pk=request.user.id)).order_by('-id')
        p2 = Paginator(allposts2, 10)
        page_number2 = request.GET.get('page')
        page_obj2 = p2.get_page(page_number2)

        if request.user.role == 'Student':
            try:
                activities2 = activity.objects.exclude(completed_students__in=User.objects.filter(pk=request.user.id)).filter(closed=False, for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id)))
            except:
                activities2 = []
            classes = classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))
            try:
                tasks_finished_percent2 = int(activity.objects.filter(closed=False, completed_students__in=User.objects.filter(pk=request.user.id), for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))).count())/int(activity.objects.filter(closed=False, for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))).count())
            except:
                tasks_finished_percent2 = 1.;
            return render(request, "school/home.html", {
                "classes": classes,
                "activities": activities2,
                "tasks_finished_percent": str(tasks_finished_percent2*100)[:5],
                "user_posts": page_obj2,
                "comments": comment.objects.all()
            })
        elif request.user.role == 'Teacher':
            classes = classroom.objects.filter(teacher=User.objects.get(pk=request.user.id))
            return render(request, "school/home.html", {
                "classes": classes,
                "user_posts": page_obj2,
                "comments": comment.objects.all()
            })
    else:
        return HttpResponseRedirect(reverse("index"))

def profile(request, id):
    try:
        profile = User.objects.get(pk=id)
    except:
        return render(request, "school/error.html", {
            "error": "Oops, User does not exist."
        })
    if request.user.is_authenticated:
        if request.method == "POST":
            date = now.strftime("%B %d, %Y | %I:%M %p")
            content = request.POST["content"]
            try:
                uploadedfile = request.FILES["uploadedfile"]
            except:
                uploadedfile = ''
            parent_user = User.objects.get(pk=request.user.id)
            postobject.objects.create(parent_user=parent_user, content=content, date=date, uploadedfile=uploadedfile)

#Paginator
    allposts = postobject.objects.filter(parent_user=User.objects.get(pk=id)).order_by('-id')
    p = Paginator(allposts, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    ownedClassrooms = classroom.objects.filter(teacher=User.objects.get(pk=id))
    joinedClassrooms = classroom.objects.filter(students__in=User.objects.filter(pk=id))
    teachers_list = []
    students_list = []
    students = []
    for teacher in classroom.objects.filter(students__in=User.objects.filter(pk=id)):
        teachers_list.append(teacher.teacher)
    for student in classroom.objects.filter(students__in=User.objects.filter(pk=id)):
        for studentss in student.students.all():
            students_list.append(studentss)
    for studenta in classroom.objects.filter(teacher=User.objects.get(pk=id)):
        for studentsas in studenta.students.all():
            students.append(studentsas)
    return render(request, "school/profile.html", {
        "profile": profile,
        "ownedClassrooms": ownedClassrooms,
        "joinedClassrooms": joinedClassrooms,
        "teachers": list(dict.fromkeys(teachers_list)),
        "classmates": list(dict.fromkeys(students_list)),
        "user_posts": page_obj,
        "students": list(dict.fromkeys(students)),
        "page_number": page_number,
        "comments": comment.objects.all()
    })

@csrf_exempt
def confirmuser(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."})
    else:
        data3 = json.loads(request.body)
        try:
            user_object = User.objects.get(username=data3.get("username"))
            pre_first_name = User.objects.get(username=data3.get("username")).first_name
            pre_last_name = User.objects.get(username=data3.get("username")).last_name
            pre_profilepicture = User.objects.get(username=data3.get("username")).profilepicture.url
            pre_email = User.objects.get(username=data3.get("username")).email
            return JsonResponse({
                "user_exists": "true",
                "first_name": pre_first_name,
                "last_name": pre_last_name,
                "profilepicture_url": pre_profilepicture,
                "email": pre_email
            })
        except:
            return JsonResponse({"user_exists": "false"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "school/login.html", {
                "error": "Invalid Password.",
                "landing": 'True'
            })
    else:
        return render(request, "school/login.html", {
            "landing": 'True'
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        try:
            profilepicture = request.FILES["profilepicture"]
        except:
            profilepicture = 'empty'

        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "school/register.html", {
                "error": "Passwords must match.",
                "register": 'True'
            })

        # Attempt to create new user
        try:
            if profilepicture == 'empty':
                user = User.objects.create_user(username, email, password, role=role, first_name=first_name, last_name=last_name)
                user.save()
            else:
                user = User.objects.create_user(username, email, password, profilepicture=profilepicture, role=role, first_name=first_name, last_name=last_name)
                user.save()

        except IntegrityError:
            return render(request, "school/register.html", {
                "error": "Username already taken.",
                "register": 'True'
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "school/register.html", {
            "register": 'True'
        })


@login_required
def newclassroom(request):
    if request.user.role == 'Teacher':
        if request.method != "POST":
            return HttpResponse('request.method is not POST')
        else:
            try:
                password = request.POST["password"]
            except:
                password = ''

            try:
                coverphoto = request.FILES["coverphotoimage"]
            except:
                coverphoto = ''
            hex_color = request.POST["hex_color"]
            classname = request.POST["classroom_name"]
            teacher = User.objects.get(pk=request.user.id)

            classroom.objects.create(hex_color=hex_color, teacher=teacher, classname=classname, classcoverphoto=coverphoto, password=password)
            return HttpResponseRedirect(reverse('classr'))
    else:
        return render(request, "school/error.html", {
            "error": "Oops, something went wrong."
        })
#classroom views
def classroom_page(request, class_id):
#Paginator
    if request.method == 'POST':
        if request.user.role == 'Teacher':
            poster = request.user
            date_announce = now.strftime("%B %d, %Y | %I:%M %p")
            heading = request.POST["heading"]
            urgency = request.POST["urgency"]
            new_ann = announcement.objects.create(poster=poster, date=date_announce, heading=heading, urgency=urgency)
            new_ann.for_class.set(request.POST.getlist('classes'))
        elif request.user.role == 'Student':
            poster = request.user
            date_announce = now.strftime("%B %d, %Y | %I:%M %p")
            heading = request.POST["heading"]
            urgency = 'Casual'
            new_ann = announcement.objects.create(poster=poster, date=date_announce, heading=heading, urgency=urgency)
            new_ann.for_class.add(class_id)

    class_obj = classroom.objects.filter(pk=class_id)
    classposts = announcement.objects.filter(for_class__in=class_obj).order_by('-id')
    p = Paginator(classposts, 10)
    classroom_page = classroom.objects.get(pk=class_id)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    teacher_classrooms = classroom.objects.filter(teacher=User.objects.get(pk=request.user.id))
    try:
        activities = activity.objects.exclude(completed_students__in=User.objects.filter(pk=request.user.id)).filter(for_class=classroom.objects.get(pk=class_id), closed=False)
    except:
        activities = []
    return render(request, "school/classroom.html", {
        "page_obj": page_obj,
        "classroom": classroom_page,
        "teacher_classrooms": teacher_classrooms,
        "activities": activities
    })

def deleteclassroom(request, deleteclass_id):
    if request.user.role == 'Teacher':
        class_to_delete = classroom.objects.get(pk=deleteclass_id)
        class_to_delete.delete()
        return HttpResponseRedirect(reverse('classr'))
    else:
        return render(request, "school/error.html", {
            "error": "Forbidden."
        })

def changecoverphoto(request, profile_id):
    try:
        if int(profile_id) == int(request.user.id):
            if request.method == 'POST':
                try:
                    coverphotourl = request.FILES["coverphoto"]
                    request.user.coverphoto = coverphotourl
                    request.user.save()
                except:
                    pictureurl = request.FILES["profilepicture"]
                    request.user.profilepicture = pictureurl
                    request.user.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'id': profile_id}))
        else:
            return render(request, "school/error.html", {
                "error": "You cannot use this feature on other users."
            })
    except TypeError:
        return render(request, "school/error.html", {
            "error": "Not logged in."
        })
    return render(request, "school/error.html", {
        "error": "Oops, something went wrong."
    })

def updateprofile(request, profile_id2):
    if int(profile_id2) == int(request.user.id):
        if request.method == 'POST':
            try:
                request.user.first_name = request.POST["first_name"]
                request.user.last_name = request.POST["last_name"]
                request.user.username = request.POST["username"]
                request.user.email = request.POST["email"]
                request.user.save()
                return HttpResponseRedirect(reverse('profile', kwargs={'id': request.user.id}))
            except:
                return render(request, "school/error.html", {
                    "error": "Oops, something went wrong."
                })
        else:
            return render(request, "school/error.html", {
                "error": "Oops, something went wrong."
            })
    else:
        return render(request, "school/error.html", {
            "error": "You cannot use this feature on other users."
        })

@login_required
@csrf_exempt
def editpost(request, profile_id3):
    post_toEdit = postobject.objects.get(pk=profile_id3)
    if request.user == post_toEdit.parent_user:
        if request.method == 'PUT':
            data = json.loads(request.body)
            if data.get("delete") == 'True':
                post_toEdit.delete()
                return JsonResponse('success')
            elif data.get("delete") == 'False':
                content_edited = data.get("content")
                post_toEdit.content = content_edited
                post_toEdit.save()
                return JsonResponse('success')
    else:
        return HttpResponse("You cannot use this feature on other users.")

@login_required
@csrf_exempt
def editcomment(request, profile_id4):
    parent_post = postobject.objects.get(pk=profile_id4)
    if request.method == 'PUT':
        data2 = json.loads(request.body)

        if data2.get("edit") == 'True':
            comment_toEdit = comment.objects.get(pk=profile_id4)
            if request.user == comment_toEdit.user:
                return JsonResponse('success')
            else:
                return HttpResponse("You cannot use this feature on other users.")

        elif data2.get("edit") == 'False':
            comment.objects.create(parent_ann=parent_post ,content=data2.get("content"), user=request.user, date=now.strftime("%B %d, %Y | %I:%M %p"))
            return JsonResponse('success')

def tasks(request):
    if request.user.role == 'Student':
        try:
            activities_finished = activity.objects.filter(closed=False, completed_students__in=User.objects.filter(pk=request.user.id), for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id)))
        except:
            activities_finished = []
        try:
            activities = activity.objects.exclude(completed_students__in=User.objects.filter(pk=request.user.id)).filter(closed=False, for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id)))
        except:
            activities = []
        try:
            missed_activities = activity.objects.exclude(completed_students__in=User.objects.filter(pk=request.user.id)).filter(closed=True)
        except:
            missed_activities = []
        try:
            done_activities = activity.objects.filter(completed_students__in=User.objects.filter(pk=request.user.id), closed=True)
        except:
            done_activities = []
        try:
            tasks_finished_percent = int(activity.objects.filter(closed=False, completed_students__in=User.objects.filter(pk=request.user.id), for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))).count())/int(activity.objects.filter(closed=False, for_class__in=classroom.objects.filter(students__in=User.objects.filter(pk=request.user.id))).count())
        except:
            tasks_finished_percent = 1.;
        return render(request, "school/tasks.html", {
            "activities_finished": activities_finished,
            "activities": activities,
            "missed_activities": missed_activities,
            "done_activities": done_activities,
            "tasks_finished_percent": str(tasks_finished_percent*100)[:5]
        })
    elif request.user.role == 'Teacher':
        try:
            classwork = activity.objects.filter(for_class__in=classroom.objects.filter(teacher=request.user));
        except:
            classwork = [];
        for cl in classwork:
            try:
                if int(cl.for_class.students.count()) == 0:
                    cl.percent = int(0)
                else:
                    cl.percent = int(cl.completed_students.count())/int(cl.for_class.students.count())*100
            except:
                cl.percent = int(100)
            cl.save()
        teacher_classrooms = classroom.objects.filter(teacher=User.objects.get(pk=request.user.id))
        return render(request, "school/classwork.html", {
            "classworks": classwork.exclude(closed=True),
            "teacher_classrooms": teacher_classrooms,
            "Closed_classworks": classwork.exclude(closed=False)
        })


def newtask(request):
    if request.method == 'POST':
        if request.user.role == 'Teacher':
            newtask_title = request.POST["title"]
            newtask_description = request.POST["description"]
            try:
                newtask_attachedlink = request.POST["link"]
            except:
                newtask_attachedlink = ''
            try:
                newtask_attachedfile = request.FILES["file"]
            except:
                newtask_attachedfile = ''
            for_class_id = request.POST["for_class"]
            for_class = classroom.objects.get(pk=for_class_id)
            task_date = now.strftime("%B %d, %Y | %I:%M %p")
            ann_newtask_title = f"Classwork '{newtask_title}' has been posted"
            activity.objects.create(title=newtask_title, description=newtask_description, attachedlink=newtask_attachedlink, attachedfile=newtask_attachedfile, for_class=for_class)
            announcementClasswork = announcement.objects.create(poster=request.user, date=task_date, urgency='Classwork', heading=ann_newtask_title)
            announcementClasswork.for_class.add(for_class)
            return HttpResponseRedirect(reverse('tasks'))
        else:
            return HttpResponse('You are not allowed to perform this action.')
    else:
        return HttpResponse('request method not POST.')
