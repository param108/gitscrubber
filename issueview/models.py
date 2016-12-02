from __future__ import unicode_literals
from django.contrib.auth.models import User 
from django.db import models

# Create your models here.
class Issue(models.Model):
  repository = models.CharField(max_length=100)
  issueid = models.CharField(max_length=10)
  title = models.TextField()
  url = models.TextField()
  created = models.CharField(max_length=50)
  updated = models.CharField(max_length=50)
  assigned = models.CharField(max_length=50) #assignee.login
  release = models.CharField(max_length=50)
  status = models.CharField(max_length=50)
  comments = models.TextField()
  changed = models.BooleanField(default=False)
  user = models.ForeignKey(User)

class Repository(models.Model):
  repository = models.CharField(max_length=100)
  user = models.ForeignKey(User)
