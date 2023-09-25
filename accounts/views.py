from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from . forms import RegistrationForm, UserForm, UserProfileForm
from . models import Account, UserProfile
from donation.models import Area
from django.http import HttpResponse
from django.views.generic import View

from . utils import render_to_pdf

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



# Create your views here.
def home(request):
    regions = Area.objects.all()
    
    context = {
        'regions': regions,
    }
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password, is_active=True)

        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect(request.GET['next'] if 'next' in request.GET  else 'home')
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You Are Logged Out!')
    return redirect('login')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Thank you for registering us. We have sent you a verification email to your email address')
            return redirect('/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your Account is Activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation Link!')
        return redirect('register')

@login_required(login_url= 'login')
def account(request):
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'userprofile': userprofile,
    }
    return render(request, 'accounts/account.html', context)

@login_required(login_url = 'login')
def editAccount(request):
    profile = request.user.userprofile
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()

            return redirect('account')
    context = {'form':form}
    return render(request, 'accounts/profile_form.html', context)


@login_required(login_url= 'login')
def viewUsers(request):
    user = request.user
    if  user.is_staff == True:
        profiles = UserProfile.objects.filter(user__is_admin=False, user__is_staff=False)
        profiles_count = UserProfile.objects.filter(user__is_admin=False, user__is_staff=False).count
        context = {
            'profiles': profiles,
            'profiles_count': profiles_count

        }

        return render(request, 'accounts/view_users.html', context)
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def activateUsers(request, pk):
    user = request.user
    if  user.is_staff == True:

        users = Account.objects.get(id=pk)

        users.is_active = True
        users.save()
    
        return redirect('view_users')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')
    

@login_required(login_url= 'login')
def deactivateUsers(request, pk):
    user = request.user
    if  user.is_staff == True:

        users = Account.objects.get(id=pk)

        users.is_active = False
        users.save()
    

        return redirect('view_users')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('acount')
    

@login_required(login_url= 'login')
def downloadUsers(request):
    user = request.user
    if  user.is_staff == True:
        profiles = UserProfile.objects.filter(user__is_admin=False, user__is_staff=False)
        
        context = {
            'profiles': profiles,
        }
        pdf = render_to_pdf('accounts/usersdownload.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
       

        
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')
