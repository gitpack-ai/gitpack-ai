from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile',
        primary_key=True, on_delete=models.CASCADE)
    

class Pricing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    third_party_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    avatar_url = models.URLField()
    third_party_id = models.IntegerField(unique=True)
    pricing = models.ForeignKey(Pricing, related_name='organizations', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Repository(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    private = models.BooleanField(default=False)
    third_party_id = models.IntegerField(unique=True)
    organization = models.ForeignKey(Organization, related_name='repositories', on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
