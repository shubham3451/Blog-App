from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import SignUpForm, LogInForm, ProfileForm, EditUserForm, CreatePostForm
from app.models import MyUser,Post, Profile as Profiles
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  PasswordChangeForm
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.

def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logIn')
        else:
            messages.error(request,"Please enter the details correctly")
    else:
        form = SignUpForm()

    return render(request, 'SignUp.html', {'form': form})

def LogIn(request):
    if request.method == 'POST':
        form = LogInForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
               login(request, user)
               return redirect('dashboard')
            else:
                messages.error(request, "email or password do not match")
        else:
            messages.error(request, "please enter valid details")
    else:
        form = LogInForm()
    return render(request, 'LogIn.html',{'form':form})

@login_required
def LogOut(request):
    logout(request=request)
    return redirect('logIn')


def Profile(request, username=None):
    if username:
        # Get the user profile of the user whose username is passed in the URL
        user = get_object_or_404(MyUser, username=username)
    else:
        # Default to the current logged-in user
        user = request.user
    
    # Fetch the posts of the user
    posts = Post.objects.filter(author=user)
    
    # Get the user profile (if exists)
    profile = None
    try:
        profile = user.profile
    except Profiles.DoesNotExist:
        profile = None
    
    return render(request, 'profile.html', {'user': user, 'profile': profile, 'posts': posts})

@login_required
def Dashboard(request):
    search_query = request.GET.get('q', '')  # Get the search query from the URL parameters
    posts = Post.objects.all().order_by('-date_posted')  # Get all posts, ordered by the most recent

    if search_query:
        # Filter posts based on the search query in the username or content
        posts = posts.filter(Q(author__username__icontains=search_query) | Q(content__icontains=search_query))

    return render(request, 'dashboard.html', {
        'posts': posts,
        'search_query': search_query,
        'user':request.user
    })

@login_required
def search_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        # Assuming you are searching for usernames
        users = MyUser.objects.filter(username__icontains=query).values_list('username', flat=True)
        return JsonResponse({'results': list(users)})
    return JsonResponse({'results': []})


@login_required
def passwordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'changepassword.html', {'form':form})

@login_required
def SetUpProfile(request):
    profile = Profiles.objects.get_or_create(user=request.user)[0] 
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        form = ProfileForm(request.POST, request.FILES,instance=profile)
        if user_form and form.is_valid():
            form.save()
            user_form.save()
            return redirect('profile')
        else:
            messages.error(request,"please enter details correctly")
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'updateprofile.html', {'user_form':user_form, 'profile_form':profile_form, })

@login_required
def DeleteUser(request):
    user = request.user
    user.delete()
    messages.success(request, "your account has successfully deleted")
    return redirect('logIn')


@login_required
def CreatePost(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post Added")
            return redirect('profile')
        else:
            messages.error(request, "please enter details correctly")
    else:
        form = CreatePostForm()
    return render(request, 'create_post.html', {'form':form})

@login_required
def EditPost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponse('Permission denied')
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            messages.success(request, "post updated")
            return redirect('profile')
        else:
            messages.error(request,"please enter the details correctly")
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'editpost.html', {'form':form})

@login_required
def deletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, "This post has been deleted")
    else:
        return HttpResponse("permission denied")
    return redirect('profile')
    

    




