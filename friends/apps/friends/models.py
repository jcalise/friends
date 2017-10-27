# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['pword']) < 8 or len(postData['cword']) < 8:
            errors["password"] = "Your password must be at least 8 characters long."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Your email is invalid."
        if len(postData['name']) < 5 or len(postData['alias']) < 3:
            errors["name"] = "Your name is too short, should be 5 or more characters."
        if len(postData['alias']) < 3:
            errors['alias'] = "Your alias is too short, should be 3 or more characters"
        if not postData['pword'] == postData['cword']:
            errors['mismatch'] = "Your passwords do not match."
        return errors;

    def login(self, postData):
        errors = {}
        if len(postData['pword']) < 8:
            errors["password"] = "Your password must be at least 8 characters long."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Your email is invalid."
        return errors;

    

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    bday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    relationships = models.ManyToManyField('self', through='Friendships',
                                           symmetrical=False,
                                           related_name='related_to+')
                                           
    def __unicode__(self):
        return self.name
    
class Friendships(models.Model):
    from_person = models.ForeignKey(User, related_name='from_people')
    to_person = models.ForeignKey(User, related_name='to_people')