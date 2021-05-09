
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:id>", views.profile, name="profile"),
    path("class", views.classr, name="classr"),
    path("newclassroom", views.newclassroom, name="newclassroom"),
    path("classroom/<str:class_id>", views.classroom_page, name="classroom_page"),
    path("deleteclassroom/<str:deleteclass_id>", views.deleteclassroom, name="deleteclassroom"),
    path("changecoverphoto/<str:profile_id>", views.changecoverphoto, name="changecoverphoto"),
    path("updateprofile/<str:profile_id2>", views.updateprofile, name="updateprofile"),
    path("editpost/<str:profile_id3>", views.editpost, name="editpost"),
    path("editcomment/<str:profile_id4>", views.editcomment, name="editcomment"),
    path("confirmuser", views.confirmuser, name="confirmuser"),
    path("home", views.home, name="home"),
    path("tasks", views.tasks, name="tasks"),
    path("viewtask/<str:task_id>", views.viewtask, name="viewtask"),
    path("unenroll/<str:classroom_id_leave>", views.unenroll, name="unenroll"),
    path("checkclass/<str:class_code_id>", views.checkclass, name="checkclass"),
    path("newtask", views.newtask, name="newtask")


]
