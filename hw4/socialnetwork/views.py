from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports the model class
from socialnetwork.models import *
from socialnetwork.forms import *

from datetime import datetime

# Action for the default /todolist2/ route.
@login_required
def home(request):
    # Gets a list of all the posts in the todo-list database.
    all_posts = Post.objects.order_by('create_time').reverse()
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    return render(request, 'socialnetwork/index.html', {'posts': all_posts})


# Action for the /socialnetwork/add-post route.
@login_required
def add_post(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new post to the database if the request parameter is present
    if 'post' not in request.POST or not request.POST['post']:
        errors.append('You must enter a post message to add.')
    else:
        new_post = Post(text=request.POST['post'],
                        user=request.user,
                        create_time=datetime.now())
        new_post.save()

    # Sets up data needed to generate the view, and generates the view
    posts = Post.objects.order_by('create_time').reverse()
    context = {'posts': posts, 'errors': errors}
    return render(request, 'socialnetwork/index.html', context)


# Action for the /socialnetwork/delete-post route.
@login_required
def delete_post(request, post_id):
    errors = []

    if request.method != 'POST':
        errors.append('Deletes must be done using the POST method')
    else:
        # Deletes the post if present in the todo-list database.
        try:
            post_to_delete = Post.objects.get(id=post_id)
            post_to_delete.delete()
        except ObjectDoesNotExist:
            errors.append('The post did not exist in the To Do List.')

    posts = Post.objects.order_by('create_time').reverse()
    context = {'posts': posts, 'errors': errors}
    return render(request, 'socialnetwork/index.html', context)

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)
    
    form = RegistrationForm(request.POST)
    context['form']=form

    # Check the validity of the form data
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html',context)

    #At this point, the form is valid 
    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    # Logs in the new user and redirects to global stream
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    
    login(request, new_user)
    return redirect('/socialnetwork/')

@login_required
def profile(request,username):
    context={}
    thisuser = User.objects.get(username=username)
    posts = Post.objects.order_by('create_time').reverse()
    context = {'username':username, 'first_name':thisuser.first_name, 'last_name':thisuser.last_name, 'posts':posts}
    return render(request, 'socialnetwork/profile.html', context)