# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect,reverse,HttpResponse
from django.contrib import messages
from .models import User,Friendships
import bcrypt



def index(request):
    return render(request, 'friends/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('index'))
    else:
        hash_pw = bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], bday=request.POST['bday'], password=hash_pw)
        user.save()
        request.session['id'] = user.id
        request.session['loggedin'] = True
        return redirect(reverse('main'))
    return redirect(reverse('index'))

def login(request):
    errors = User.objects.login(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
        return redirect(reverse('index'))
    else:
        errors = {}
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            login_success =  bcrypt.checkpw(request.POST['pword'].encode(), user.password.encode())
            print login_success
        except:
            login_success = False
            errors["invalid"] = "Your password is invalid or email does not exist."
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        
        if login_success:
            request.session['id'] = user.id
            request.session['loggedin'] = True
            return redirect(reverse('main'))

    return redirect(reverse('index'))

def main(request):
    if 'loggedin' not in request.session:
        return redirect(reverse('index'))
    else:
        user = User.objects.get(id=request.session['id'])
        context = {
            'user': user,
            'all_users': User.objects.all().exclude(to_people__from_person=user),
            'friends': user.relationships.filter(to_people__from_person=user)
        }
        
        return render(request, 'friends/main.html', context)

def logout(request):
    request.session.clear()
    return redirect(reverse('index'))

def view(request, id):
    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, 'friends/user.html', context)

def add(request, id):
    user = User.objects.get(id=request.session['id'])
    friend = User.objects.get(id=id)
    
    Friendships.objects.create(from_person=user, to_person=friend)
    Friendships.objects.create(from_person=friend, to_person=user)
    
    return redirect(reverse('main'))

def remove(request, id):
    user = User.objects.get(id=request.session['id'])
    friend = User.objects.get(id=id)
    
    Friendships.objects.filter(from_person=user, to_person=friend).delete()
    Friendships.objects.filter(from_person=friend, to_person=user).delete()
    
    return redirect(reverse('main'))



   
