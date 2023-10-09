from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    logout(request)
    return redirect('login')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            # Create and save the user in the User model (optional)
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)

            # Save the user profile data in the UserProfile model
            user_profile = UserProfile(username=uname, email=email, password=pass1)
            user_profile.save()

            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('logout')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')




def LogoutPageWithCount(request):
    
    total_users = UserProfile.objects.all().count()

    # Check if the user is authenticated before accessing UserProfile
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(username=request.user.username)
        except UserProfile.DoesNotExist:
            user_profile = None
    else:
        user_profile = None
    
    # Fetch all registered users from UserProfile model
    all_users = UserProfile.objects.all()

    return render(request, 'logout.html', {'total_users': total_users, 'user_profile': user_profile, 'all_users': all_users})
    
