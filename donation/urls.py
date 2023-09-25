from django.urls import path
from . import views

urlpatterns = [
    path('', views.donate, name="donate"),
    path('add_area/', views.addArea, name="add_area"),
    path('money_donation/', views.moneyDonation, name="money_donation"),
    path('item_donation/', views.itemDonation, name="item_donation"),

    path('process_Money_donations/', views.processMoneyDonations, name="process_Money_donations"),
    path('accept_Money_Donations/<str:pk>/', views.verifyMoneyDonation, name="accept_Money_Donations"),
    path('decline_Money_Donations/<str:pk>/', views.declineMoneyDonations, name="decline_Money_Donations"),
    path('view_Money_Donations/', views.viewDonationRecords, name="view_Money_Donations"),
    path('total/', views.viewTotal, name="total"),
  
    path('process_Item_donations/', views.processItemDonations, name="process_Item_donations"),
    path('accept_Item_Donations/<str:pk>/', views.verifyItemDonation, name="accept_Item_Donations"),
    path('decline_Item_Donations/<str:pk>/', views.declineItemDonations, name="decline_Item_Donations"),
    path('view_Item_Donations/', views.viewItemRecords, name="view_Item_Donations"),

    path('my_Money_Donations/', views.myMoneyDonations, name="my_Money_Donations"),
    path('my_Item_Donations/', views.myItemDonations, name="my_Item_Donations"),

    path('download_money_donations/', views.downloadMoneyDonations, name="download_money_donations"),
    path('download_item_donations/', views.downloadItemDonations, name="download_item_donations"),

    path('download_my_money_donations/', views.downloadMyMoneyDonations, name="download_my_money_donations"),
    path('download_my_item_donations/', views.downloadMyItemDonations, name="download_my_item_donations"),
]