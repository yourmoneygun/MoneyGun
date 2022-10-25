from django.contrib import admin

from main import models  # noqa


# Register your admins here.


# User Admin
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


# Referral Admin
@admin.register(models.Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass


# Product Admin
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


# UserProduct Admin
@admin.register(models.UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    pass


# UserReferralTotal Admin
@admin.register(models.UserReferralTotal)
class UserReferralTotalAdmin(admin.ModelAdmin):
    pass


# Transaction Admin
@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
