from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Create your models here.
# class that defines the user account role


class SohaeUserRole(Enum):

    ADMIN = "Administrator"
    MOD = "Moderator"
    USER = "User"
    OWNER = "Dormitory Owner"

# Custom user fields


class SohaeUser(AbstractUser):

    name = models.CharField(blank=True, max_length=255)
    role = models.CharField(
        max_length=30,
        default=SohaeUserRole.USER,
        choices=[(tag, tag.value) for tag in SohaeUserRole]
    )

    def __str__(self):
        return self.email

# choices defining dormitory type


DORMTYPE_CHOICES = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("COED", "Co-ed"),
]


# Dormitory class


class SohaeDorm(models.Model):
    dorm_name = models.CharField(max_length=255)
    dorm_type = models.CharField(max_length=10, choices=DORMTYPE_CHOICES)
    dorm_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    dorm_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.dorm_name