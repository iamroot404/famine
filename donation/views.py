from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import DonationForm, ItemsForm, AreaForm
from . models import  Donation, Amount, Items, Area

from datetime import date
import string    
import random
from django.db.models import Sum

from django.http import HttpResponse

from . utils import render_to_pdf

# Create your views here.

@login_required(login_url= 'login')
def donate(request):
    if request.method == 'POST':
        type = request.POST['type']

        if type == 'Items Donation':
            return redirect('item_donation')
        else:
            return redirect('money_donation')

    return render(request, 'donation/donation.html')

@login_required(login_url= 'login')
def moneyDonation(request):
    current_user = request.user
    form = DonationForm()

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid:
            donation = form.save(commit=False)
            donation.user = current_user

            
            #trans id
            S = 10
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")

            transaction_id = current_date + str(ran)
            donation.transaction_id = transaction_id
            donation.save()
            messages.success(request, 'Your Donation has been sent please wait for Admin Verification!')
            return redirect('money_donation')

    context = {
        'form': form,
    }

    return render(request, 'donation/money_donation.html', context)

@login_required(login_url= 'login')
def itemDonation(request):
    current_user = request.user
    form = ItemsForm()

    if request.method == 'POST':
        form = ItemsForm(request.POST)
        if form.is_valid:
            donation = form.save(commit=False)
            donation.user = current_user
            donation.save()
            messages.success(request, 'Your Donation has been sent please wait for Admin Verification!')
            return redirect('item_donation')

    context = {
        'form': form,
    }

    return render(request, 'donation/item_donation.html', context)

@login_required(login_url= 'login')
def processMoneyDonations(request):
    user = request.user
    if  user.is_staff == True:

        donations = Donation.objects.filter(is_verified=False)
        
    
        context = {
            'donations': donations,
        }
        return render(request, 'donation/viewMoneyDonations.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def verifyMoneyDonation(request, pk):
    user = request.user
    if  user.is_staff == True:


        try:     

            donations = Donation.objects.get(id=pk)
            tot = Amount.objects.get(type='TOTAL')
           
            

            amount = donations.amount
            # bal = balance.balance
            tott = tot.money

            # total = amount + bal
            # balance.balance = total
            # balance.save()

            # balance.paid = savings
            # balance.save()

            totav = amount + tott
            tot.money = totav
            tot.save()

            donations.is_verified = True
            donations.save()


    
            return redirect('process_Money_donations')
        except(Amount.DoesNotExist, Donation.DoesNotExist):
            return redirect('account')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')


@login_required(login_url= 'login')
def declineMoneyDonations(request, pk):
    user = request.user
    if  user.is_staff == True:

        donations = Donation.objects.get(id=pk)
        donations.delete()
        return redirect('process_Money_donations')

    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def viewDonationRecords(request):
    user = request.user
    if  user.is_staff == True:

        donations = Donation.objects.filter(is_verified=True)
        
    
        context = {
            'donations': donations,
        }
        return render(request, 'donation/view_donations_records.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')


@login_required(login_url= 'login')
def processItemDonations(request):
    user = request.user
    if  user.is_staff == True:

        donations = Items.objects.filter(is_verified=False)
        
    
        context = {
            'donations': donations,
        }
        return render(request, 'donation/viewItemDonations.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def verifyItemDonation(request, pk):
    user = request.user
    if  user.is_staff == True:


        try:     

            donations = Items.objects.get(id=pk)
            donations.is_verified = True
            donations.save()

            return redirect('process_Item_donations')
        except(Amount.DoesNotExist, Donation.DoesNotExist):
            return redirect('account')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')


@login_required(login_url= 'login')
def declineItemDonations(request, pk):
    user = request.user
    if  user.is_staff == True:

        donations = Items.objects.get(id=pk)
        donations.delete()
        return redirect('process_Item_donations')

    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def viewItemRecords(request):
    user = request.user
    if  user.is_staff == True:

        donations = Items.objects.filter(is_verified=True)
        
    
        context = {
            'donations': donations,
        }
        return render(request, 'donation/view_items_records.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def viewTotal(request):
     user = request.user
     if  user.is_staff == True:
        tott = Amount.objects.get(type='TOTAL')
        
        context = {
            'tott': tott,
        }
        return render(request, 'donation/total.html', context)
     else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')


@login_required(login_url='login')
def addArea(request):
    user = request.user
    profile = request.user
    form = AreaForm()
    
    if  user.is_staff == True:

        if request.method =='POST':
           
            form = AreaForm(request.POST)
            if form.is_valid():
                area =  form.save(commit=False)
                area.user = profile
                area.save()

               
                messages.success(request, 'Area was added successfully!')    
                return redirect('add_area')
        context = {'form': form}
        return render(request, "donation/add_area.html", context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def myMoneyDonations(request):
    current_user = request.user 
    try:
        
        donations = Donation.objects.filter(user=current_user, is_verified=True)
        
        context = {
        'donations': donations,
        
        }
        return render(request, 'donation/mymoneydonation.html', context)
    except(Donation.DoesNotExist):
        messages.error(request, 'You have not donated!')
        return redirect('account')

@login_required(login_url= 'login')
def myItemDonations(request):
    current_user = request.user 
    try:
        
        donations = Items.objects.filter(user=current_user, is_verified=True)
        
        context = {
        'donations': donations,
        
        }
        return render(request, 'donation/myItemdonation.html', context)
    except(Donation.DoesNotExist):
        messages.error(request, 'You have not donated!')
        return redirect('account')

@login_required(login_url= 'login')
def downloadMoneyDonations(request):
    user = request.user
    if  user.is_staff == True:
       donations = Donation.objects.filter(is_verified=True)
        
       context = {
            'donations': donations,
        }
       
       pdf = render_to_pdf('donation/moneydownload.html', context)
       return HttpResponse(pdf, content_type='application/pdf')
       

        
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def downloadItemDonations(request):
    user = request.user
    if  user.is_staff == True:
       donations = Items.objects.filter(is_verified=True)
        
       context = {
            'donations': donations,
        }
       
       pdf = render_to_pdf('donation/itemdownload.html', context)
       return HttpResponse(pdf, content_type='application/pdf')
       

        
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def downloadMyMoneyDonations(request):
    current_user = request.user 
    
    donations = Donation.objects.filter(is_verified=True, user=current_user)
    
    context = {
        'donations': donations,
    }
    
    pdf = render_to_pdf('donation/moneydownload.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
       

        
    
   
@login_required(login_url= 'login')
def downloadMyItemDonations(request):
    current_user = request.user 
    
    donations = Items.objects.filter(is_verified=True, user=current_user)
    
    context = {
        'donations': donations,
    }
    
    pdf = render_to_pdf('donation/itemdownload.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
       

        
    
    

