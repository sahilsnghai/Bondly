from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpRequest
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
from itertools import chain
# Create your views here.


def index(request):
    logout(request)
    return render(request, 'index.html')


@login_required(login_url="login")
def settings(request):
    user_profile = models.Profile.objects.get(usr=request.user)

    if request.method == "POST":
        if request.FILES.get('image') == None:
            image = user_profile.img_profile
            bio = request.POST.get("bio")
            location = request.POST.get('location')
            Fname = request.POST.get("fname")
            Mname = request.POST.get("lname")
            Lname = request.POST.get("lname")


            user_profile.img_profile = image
            user_profile.location = location
            user_profile.bio = bio
            user_profile.Fname=Fname
            user_profile.Mname=Mname
            user_profile.Lname=Lname
            user_profile.save()

        if request.FILES.get("image") != None:

            image = request.FILES.get("image")
            bio = request.POST.get("bio")
            location = request.POST.get('location')
            Fname = request.POST.get("fname")
            Mname = request.POST.get("lname")
            Lname = request.POST.get("lname")

            user_profile.img_profile = image
            user_profile.location = location
            user_profile.bio = bio
            user_profile.Fname=Fname
            user_profile.Mname=Mname
            user_profile.Lname=Lname

            user_profile.save()
        return redirect('settings')

    context = {'user_profile': user_profile}
    return render(request, 'settings.html', context)


@login_required(login_url='login')
def likes(request,id):
    user = request.user.username
    post = models.Post.objects.get(id=id)
    filterLike = models.LikePost.objects.filter(
        postid=id, username=user).first()

    if filterLike == None:
        newLike = models.LikePost.objects.create(postid=id, username=user)
        post.Likes += 1
        newLike.save()
        post.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        filterLike.delete()
        post.Likes -= 1
        post.save()
        # return redirect('home')
        return redirect(request.META.get('HTTP_REFERER'))


def signup(request):

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('cpassword')

        if password1 == password2 and password1 != None:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Registered.")
                return redirect('login')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Registered.")
                return redirect('login')

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1,first_name=fname, last_name=lname)
                user.save()

                user_login = auth.authenticate(
                    username=username, password=password2)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                
                new_profile = models.Profile.objects.create(
                    usr=user_model, id_usr=user_model.id,Fname=fname,Lname=lname)
            

                new_profile.save()

                messages.info(request, 'User Created.')
                return redirect("settings")
        else:
            messages.info(request, "Password does not matched.")

            return redirect('login')

    else:
        return render(request, 'login.html')


def login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials Invaild')
            return redirect('login')

    else:
        return render(request, 'login.html')


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required(login_url="login")
def home(request):
    user_obj = User.objects.get(username=request.user.username)
    user_profile = models.Profile.objects.get(usr=user_obj)

    followingList = []
    feed = []

    userFollowing = models.Followers.objects.filter(
        follower=request.user.username)
    # print(userFollowing)

    for usrs in userFollowing:
        followingList.append(usrs.user)

    for usrname in userFollowing:
        feed.append(models.Post.objects.filter(user=usrname))

    feedList = list(chain(*feed))

    # feed_post = models.Post.objects.all()
    context = {"user_profile": user_profile,"user_object": user_obj, "posts": feedList}
    return render(request, 'home.html', context)


@login_required(login_url="login")
def upload(request):
    if request.method == "POST":
        print('in upload post')
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        print("usr:", user, "img:", image, "cap:", caption)

        new_post = models.Post.objects.create(
            user=user, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    return redirect('home')


@login_required(login_url='login')
def profile(request, pf):
    user_object = User.objects.get(username=pf)
    user_profile = models.Profile.objects.get(usr=user_object)
    print(request.user.__doc__)
    posts = models.Post.objects.filter(user=pf)
    postsNum = len(posts)
    follor = request.user.username

    if models.Followers.objects.filter(follower=follor, user=pf).first():
        text = "Following"
    else:
        text = "Follow"

    followers = len(models.Followers.objects.filter(user=pf))
    following = len(models.Followers.objects.filter(follower=pf))

    context = {
        'user_object': user_object,
        "user_profile": user_profile,
        "posts": posts,
        'postsNum': postsNum,
        "text": text,
        "followers": followers,
        "following": following
        }
    # print('type:', type(user_profile.img_profile.url),user_profile.img_profile.url, end="")
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def follow(request):

    user = request.POST.get('username')
    follower = request.POST.get('follower')
    if request.method == "POST":
        user = request.POST.get('username')
        follower = request.POST.get('follower')

        if models.Followers.objects.filter(follower=follower, user=user).first():
            del_following = models.Followers.objects.filter(
                follower=follower, user=user)
            del_following.delete()
            return redirect(f'/profile/{user}')
        else:
            newFollow = models.Followers.objects.create(
                follower=follower, user=user)
            newFollow.save()
            return redirect(f'/profile/{user}')
    return redirect(f'/profile/' + user)


@login_required(login_url='login')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = models.Profile.objects.get(usr=user_object)

    if request.method == 'POST':
        username = request.POST.get('username')
        username_object = User.objects.filter(username__icontains=username)

        user_profile = []
        user_profile_list = []

        for users in username_object:
            user_profile.append(users.id)

        for ids in user_profile:
            profile_lists = models.Profile.objects.filter(id_usr=ids)
            user_profile_list.append(profile_lists)
        
        user_profile_list = list(chain(*user_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'user_profile_list': user_profile_list})

def aboutus(request):
    return render(request,'about.html')