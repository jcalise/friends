# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
import re
import bcrypt
from datetime import date,datetime
from dateutil.parser import parse

NAME_REGEX = re.compile(r'^[A-Za-z]\w+\s+[A-Za-z]\w+$')

class BuddyManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # check password length
        if len(postData['pword']) < 8 or len(postData['cword']) < 8:
            errors["password"] = "Your password must be at least 8 characters long."
        # check name length
        if len(postData['name']) < 5:
            errors["name_len"] = "Your name is too short, should be 5 or more characters."
        # check name and alias validity
        if not NAME_REGEX.match(postData['name']) or NAME_REGEX.match(postData['alias']):
            errors["name"] = "Names and Usernames may only contain letter characters."
        # check alias length
        if len(postData['alias']) < 3:
            errors['alias'] = "Your alias is too short, should be 3 or more characters"
        # check for password matches
        if not postData['pword'] == postData['cword']:
            errors['mismatch'] = "Your passwords do not match."

        if not errors:
            # create new user with hased password
            hash_pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
            buddy = self.create(name=postData['name'], alias=postData['alias'], password=hash_pw)
            buddy.save()
            return buddy
        return errors;

    def login(self, postData):
        errors = {}
        if len(postData['pword']) < 8:
            errors["password"] = "Your password must be at least 8 characters long."
        if len(postData['alias']) < 3:
            errors["alias"] = "Your username is not long enough."

        if len(self.filter(alias=postData['alias'])) > 0:
            # check this user's password
            user = self.filter(alias=postData['alias'])[0]
            if not bcrypt.checkpw(postData['pword'].encode(), user.password.encode()):
                errors["incorrect"] = "Your username or password is incorrect."
        else:
            eerrors["incorrect"] = "Your username or password is incorrect."

        if errors:
            return errors
        return user

class Buddy(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BuddyManager()
                                           
    def __unicode__(self):
        return self.name

class TravelManager(models.Manager):
    def create_trip(self, postData, user):
        errors = {}
        
        if len(postData['dest']) < 1 or len(postData['desc']) < 1 or len(postData['depart']) < 1 or len(postData['ret']) < 1:
             errors["length"] = "All fields are required and can not be left blank."
        
        depart_date = parse(postData['depart'])
        return_date = parse(postData['ret'])
            
        if depart_date <= datetime.today() or return_date <= datetime.today():
            errors["future"] = "Your travel dates must be in the future!"
        if depart_date > return_date:
            errors["return"] = "Your return date must be after your departure date."

        if not errors:
            # create trip and assign creator and traveler
            trip = self.create(destination=postData['dest'], description=postData['desc'], depart_date=postData['depart'], return_date=postData['ret'], created_by=user)
            trip.travelers.add(user)
            trip.save()
            return trip
        return errors

    def join_trip(self, user, trip):
        trip.travelers.add(user)
        trip.save()

    
class Travel(models.Model):
    travelers = models.ManyToManyField(Buddy, related_name='traveler')
    destination = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(Buddy, related_name='creator')
    depart_date = models.DateField()
    return_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TravelManager()

    def __unicode__(self):
        return self.destination
    
