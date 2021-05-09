from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=7)
    profilepicture = models.FileField(blank="True", default="defaultprofile.jpg")
    coverphoto = models.FileField(blank="True", default="defaultcoverphoto.jpg")
    students_child = models.ManyToManyField("User", related_name="student_child", blank="True")

    def serialize(self):
        return {
            "role": self.role,
            "username": self.username.username,
            "profilepicture": self.profilepicture,
        }



class postobject(models.Model):
    date = models.CharField(max_length=40)
    parent_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent_user")
    content = models.CharField(max_length=256)
    uploadedfile = models.FileField(blank=True, null=True)

    def serialize(self):
        return {
            "date": self.date,
            "parent_user": self.username.username,
            "content": self.content
        }

class classroom(models.Model):
    hex_color = models.CharField(max_length=7)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
    classname = models.CharField(max_length=40)
    password = models.CharField(max_length=156, blank="True")
    classcoverphoto = models.FileField(blank=True, null=True)
    description = models.CharField(max_length=256, blank="True")

    students = models.ManyToManyField("User", related_name="sudents", blank="True")

class activity(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    attachedlink = models.CharField(max_length=256, blank="True")
    attachedfile = models.FileField(blank=True, null=True)
    percent = models.CharField(blank=True, max_length=16)
    for_class = models.ForeignKey(classroom, on_delete=models.CASCADE, related_name="for_classroom")

    closed = models.BooleanField(default=False)

    completed_students = models.ManyToManyField("User", related_name="completed_students", blank="True")

class announcement(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    date = models.CharField(max_length=40)
    for_class = models.ManyToManyField("classroom", related_name="for_class", blank="True")
    heading = models.CharField(max_length=128)
    urgency = models.CharField(max_length=8)

class comment(models.Model):
    date = models.CharField(max_length=40)
    parent_ann = models.ForeignKey(postobject, on_delete=models.CASCADE, related_name="parent_ann")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    content = models.CharField(max_length=256)
