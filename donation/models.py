from django.db import models
from accounts.models import Account


# Create your models here.
class Donation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    mpesa_id = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ['-created_date']


class Amount(models.Model):
    money = models.IntegerField()
    type = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class Items(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ['-created_date']

class Area(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    region = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.region

    class Meta:
        ordering = ['-created_date']