from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
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
    this_user = User.objects.get(username=username)
    posts = Post.objects.order_by('create_time').reverse()
    context = {'username':username, 
                'first_name':thisuser.first_name, 
                'last_name':thisuser.last_name, 
                'posts':posts,
                'bio':thisuser.profile.bio,
                'age':thisuser.profile.age}
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def edit_profile(request):
    context={}
    user = request.user

    if request.method == 'GET':
        context['userform'] = UserForm(instance=user)
        context['profileform'] = ProfileForm(instance=user.profile)
        context['username'] = user.username
        
    else:
        userform = UserForm(request.POST,instance=user)
        profileform = ProfileForm(request.POST,request.FILES,instance=user.profile)
        if userform.is_valid() and profileform.is_valid():
            user.profile.content_type = profileform.cleaned_data['picture'].content_type
            userform.save()
            profileform.save()
            context['message'] = 'User #{0} saved.'.format(user.username)
            # context['userform'] = userform
            # context['profileform'] = profileform
            context = {'username':user.username,
                        'first_name':user.first_name,
                        'last_name':user.last_name,
                        'bio':user.profile.bio,
                        'age':user.profile.age}
            return render(request,'socialnetwork/profile.html',context)
        else:
            context['userform'] = userform
            context['profileform'] = profileform
            context['username'] = user.username
    return render(request, 'socialnetwork/editprofile.html', context)

def get_photo(request, username):
    this_user = User.objects.get(username=username)
    profile = get_object_or_404(Profile, user=this_user)

    # Probably don't need this check as form validation requires a picture be uploaded.
    if not profile.picture:
        raise Http404

    return HttpResponse(profile.picture)

def follow(request, username):
    this_user = request.user
    this_profile = get_object_or_404(Profile, user=this_user)
    that_user = get_object_or_404(User, username=username)
    that_profile = get_object_or_404(Profile, user=that_user)
    this_profile.following.add(that_profile)
    return redirect(reverse('profile',args=[username]))

    
