from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db import models

from main.managers import UserManager  # noqa

# Create your models here.


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    referral_link = models.CharField(
        max_length=6,
        unique=True,
        null=True,
        blank=True,
    )
    referral_link_qr_code = models.ImageField(
        upload_to='referral_qr_code/',
        null=True,
        blank=True,
    )
    referral_link_main_user = models.CharField(
        max_length=6,
        null=True,
        blank=True,
    )
    money = models.FloatField(
        default=0,
        null=False,
        blank=False,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_joined = models.DateTimeField(
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.email} | money: {self.money}"


# Referral Model
class Referral(models.Model):
    main_user = models.ForeignKey(
        User,
        null=False,
        related_name="main_users",
        on_delete=models.CASCADE,
    )
    referral_user = models.ForeignKey(
        User,
        null=False,
        related_name="referral_users",
        on_delete=models.CASCADE,
    )


# Product Model (VIP)
class Product(models.Model):
    img_product = models.ImageField(
        upload_to='image_product/',
        blank=True,
        null=True,
    )
    level = models.IntegerField(
        unique=True,
        null=False,
        blank=False,
    )
    money = models.FloatField(
        default=0,
        null=False,
        blank=False,
    )
    active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"Level:{self.level} <--> money:{self.money}"


# User Buy Product Model
class UserProduct(models.Model):
    product = models.ForeignKey(
        Product,
        null=False,
        related_name="products",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        null=False,
        related_name="users",
        on_delete=models.CASCADE,
    )
    total_price = models.FloatField(
        default=0,
        null=False,
        blank=False,
    )


# User Referral Total Model
class UserReferralTotal(models.Model):
    product = models.ForeignKey(
        Product,
        null=False,
        related_name="product_referrals",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        null=False,
        related_name="user_referrals",
        on_delete=models.CASCADE,
    )
    total_ref_user = models.IntegerField(
        default=0,
        null=False,
        blank=False,
    )
    total_ref_money = models.FloatField(
        default=0,
        null=False,
        blank=False,
    )


# Transaction Model
class Transaction(models.Model):
    user_email = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )
    # default (send OR post)
    transaction_name = models.CharField(
        max_length=512,
        null=True,
        blank=True,
    )
    transaction_num = models.CharField(
        max_length=512,
        unique=True,
        null=True,
        blank=True,
    )
    money = models.FloatField(
        null=False,
        blank=False,
    )
    wallet = models.CharField(
        max_length=512,
        null=False,
        blank=False,
    )
    # in processing (success OR unsuccess)
    status = models.CharField(
        max_length=512,
        default='in_process',
        null=False,
        blank=False,
    )
    update_transaction = models.DateTimeField(
        null=True,
        blank=True,
    )
    create_transaction = models.DateTimeField(
        default=timezone.now,
    )
