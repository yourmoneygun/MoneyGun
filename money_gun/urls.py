"""money_gun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from main import views

# Create your urls here.


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('registration/', views.RegistrationUser.as_view(), name='registration'),
    path('registration/<str:ref_link>/', views.RegistrationUser.as_view(), name='registration_referral'),
    path('preactivate/', views.PreActivateUser.as_view(), name='pre_activate'),
    path('activate/<str:uidb64>/<str:token>', views.ActivateUser.as_view(), name='activate'),
    path('login/', views.LoginUser.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('password_reset/', views.PasswordResetUser.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetUser.as_view(), name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', views.PasswordResetConfirmUser.as_view(), name='password_reset_confirm'),
    path('products/', views.ProductUser.as_view(), name='product'),
    path('products/<int:product>', views.ProductUser.as_view(), name='product_pk'),
    path('information/', views.USDTPageUser.as_view(), name='information'),
    path('referrals/', views.ReferralUser.as_view(), name='referral'),
    path('account/', views.AccountUser.as_view(), name='account'),
    path('account/send/', views.TransactionSendUser.as_view(), name='send'),
    path('account/post/', views.TransactionPostUser.as_view(), name='post'),
    path('account/story/', views.TransactionStoryUser.as_view(), name='story'),
    path('account/instruction/', views.InstructionUser.as_view(), name='instruction'),
    path('account/change_password/', views.ChangePasswordUser.as_view(), name='password_change'),
    path('account/change_password/done/', views.ChangePasswordDoneUser.as_view(), name='password_change_done'),
    path('page_not_found/', views.PageNotFound.as_view(), name='page_not_found'),

    # For Only SuperUser
    path('money_gun_administration/', admin.site.urls),
    path('transaction_processing/', views.TransactionProcessing.as_view(), name='transaction_processing'),
    path('transaction_processing/<int:pk>/', views.TransactionProcessingPk.as_view(), name='transaction_processing'),
    path('transaction_processing_unsuccess/<int:pk>/', views.TransactionProcessingUnsuccess.as_view(), name='transaction_processing_unsuccess'),
]


handler404 = "main.views.page_not_found_view"


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
