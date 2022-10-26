from django.contrib import messages
from django.views.generic import TemplateView, RedirectView, CreateView, UpdateView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordChangeView,
    PasswordChangeDoneView
)
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.conf import settings

from main.services.emails import send_registration_email
from main.services.qr_code import create_qr_code
from main.services.referral_link import create_referral_link
from main.services.token_generator import TokenGenerator
from main import forms
from main.models import User, Referral, Product, UserProduct, UserReferralTotal, Transaction
from main.services import telegram
from main.services.transaction_number import create_transaction_number

# Create your views here.


# Main Page
class Index(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'


# Registration Page
class RegistrationUser(CreateView):
    template_name = 'main/authorization/registration.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, ref_link=None, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)

        self.user = None
        self.ref_link = None

        if ref_link:
            self.user = User.objects.filter(referral_link=ref_link)

            if not self.user:
                return HttpResponseRedirect(reverse_lazy('registration'))
            else:
                self.user = User.objects.get(referral_link=ref_link)

        if request.method == "POST":

            if self.user:
                self.form = forms.RegistrationUserForm(request.POST)

            else:
                self.form = forms.RegistrationUserReferralLinkForm(request.POST)
                self.ref_link = request.POST.get('referral_link_main_user')

                if self.ref_link:
                    self.user = User.objects.filter(referral_link=self.ref_link)

                    if not self.user:
                        return HttpResponseRedirect(reverse_lazy('registration'))
                    else:
                        self.user = User.objects.get(referral_link=self.ref_link)

            if self.form.is_valid():
                self.obj = self.form.save(commit=False)
                self.obj.referral_link = create_referral_link()
                self.obj.is_active = False
                self.obj.save()

                self.ref_user = User.objects.get(id=self.obj.id)
                create_qr_code(self.ref_user.referral_link)
                self.ref_user.referral_link_qr_code = f"referral_qr_code/{self.ref_user.referral_link}.png"
                self.ref_user.save()

                if self.user:

                    if not self.ref_link:
                        self.ref_user.referral_link_main_user = ref_link
                        self.ref_user.save()

                    Referral.objects.create(main_user=self.user, referral_user=self.ref_user)

                # send_registration_email(
                #     request=request,
                #     user_instance=self.obj,
                # )

                return HttpResponseRedirect(reverse_lazy('pre_activate'))

        elif request.method == "GET":
            if self.user:
                self.form = forms.RegistrationUserForm()

            else:
                self.form = forms.RegistrationUserReferralLinkForm()
                self.ref_link = request.POST.get('referral_link_main_user')

        return render(
            request,
            self.template_name,
            context={
                'form': self.form,
            }
        )


# Activate User
class PreActivateUser(TemplateView):
    template_name = 'main/authorization/activate.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('index'))

        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)


# Activate User
class ActivateUser(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            user_pk = force_bytes(urlsafe_base64_decode(uidb64))
            current_user = User.objects.get(pk=user_pk)

        except (User.DoesNotExist, ValueError, TypeError):
            return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user)
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('page_not_found_404'))


# LogIn Page
class LoginUser(LoginView):
    template_name = 'main/authorization/login.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.email = request.POST.get('username')
        self.password = request.POST.get('password')
        self.user = User.objects.filter(email=self.email)

        if not self.user:
            form.error_messages = {
                'invalid_login': 'Электронная почта или пароль введены не правильно!'
            }

        else:
            self.user = User.objects.get(email=self.email)

            if not self.user.is_active:
                send_registration_email(
                    request=self.request,
                    user_instance=self.user
                )
                form.error_messages = {
                    'invalid_login': 'Активируйте вашу учетную запись! '
                                     'На ваш адрес электронной почты отправлено письмо с активацией.'
                }

            else:
                self.authenticate = authenticate(request, username=self.email, password=self.password)
                if self.authenticate is not None:
                    login(request, self.user)
                    return HttpResponseRedirect(reverse_lazy('index'))

                else:
                    form.error_messages = {
                        'invalid_login': 'Электронная почта или пароль введены не правильно!'
                    }
        return self.form_invalid(form)


# LogOut Page
class LogoutUser(LogoutView):
    pass


# Reset Password Page
class PasswordResetUser(PasswordResetView):
    email_template_name = 'main/authorization/password_reset/password_reset_email.html'
    template_name = 'main/authorization/password_reset/password_reset.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('index'))
        return self.render_to_response(self.get_context_data())


# Reset Password Done Page
class PasswordResetDoneUser(PasswordResetDoneView):
    template_name = 'main/authorization/password_reset/password_reset_done.html'


# Reset Password Confirm Page
class PasswordResetConfirmUser(PasswordResetConfirmView):
    template_name = 'main/authorization/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('index')


# Product Page
class ProductUser(LoginRequiredMixin, TemplateView):
    template_name = 'main/product.html'

    def dispatch(self, request, product=None, *args, **kwargs):

        if product:
            self.product = Product.objects.filter(id=product)

            if not self.product:
                return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

            self.product = Product.objects.get(id=product)
            self.user_products = UserProduct.objects.filter(product=self.product, user=request.user)

            if not self.product.active:
                return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

            if self.user_products:
                return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

            if request.user.money >= self.product.money:
                self.user_ref_link = request.user.referral_link_main_user

                self.user = User.objects.get(id=request.user.pk)
                self.user.money -= self.product.money
                self.user.save()

                if self.user_ref_link:
                    self.user_ref_main = User.objects.get(referral_link=self.user_ref_link)
                    self.user_ref_products = UserReferralTotal.objects.filter(product=self.product, user=self.user_ref_main)

                    if self.user_ref_products:
                        self.user_ref_products = UserReferralTotal.objects.get(product=self.product, user=self.user_ref_main)
                        self.user_ref_products.total_ref_user += 1
                        self.user_ref_products.save()

                    else:
                        UserReferralTotal.objects.create(product=self.product, user=self.user_ref_main, total_ref_user=1)

                UserProduct.objects.create(product=self.product, user=request.user)
                return HttpResponseRedirect(reverse_lazy('product'))

            else:
                return HttpResponseRedirect(reverse_lazy('send'))

        self.products = Product.objects.all()

        context = {
            'products': self.products,
        }

        for pk in range(1, 9):
            context[f'user_product_{pk}'] = UserProduct.objects.filter(product=pk, user=request.user.pk)

        return render(
            request,
            self.template_name,
            context=context,
        )


# USDT Page
class USDTPageUser(LoginRequiredMixin, TemplateView):
    template_name = 'main/usdt.html'


# Referral Page
class ReferralUser(LoginRequiredMixin, TemplateView):
    template_name = 'main/referral.html'

    def get(self, request, *args, **kwargs):
        self.products = Product.objects.all()

        context = {
            'products': self.products,
        }

        for pk in range(1, 9):
            context[f'user_ref_product_{pk}'] = UserReferralTotal.objects.filter(product=pk, user=request.user.pk)

        return self.render_to_response(context)


# User Account Page
class AccountUser(LoginRequiredMixin, TemplateView):
    template_name = 'main/account.html'

    def get(self, request, *args, **kwargs):
        self.referral_user = UserReferralTotal.objects.filter(user=request.user.pk)
        self.referral = Referral.objects.filter(main_user=request.user.pk).count()

        context = {
            'total_ref_money': 0,
        }

        for referral_user in self.referral_user.values_list():
            context['total_ref_money'] += referral_user[4]

        context['total_ref_user'] = self.referral
        context['url'] = settings.ALLOWED_HOSTS[0]

        return self.render_to_response(context)


# User Change Password Page
class ChangePasswordUser(LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/change_password/change_password.html'
    success_url = reverse_lazy('account')


# User Change Password Done Page
class ChangePasswordDoneUser(LoginRequiredMixin, PasswordChangeDoneView):
    pass


# Transaction Send
class TransactionSendUser(LoginRequiredMixin, CreateView):
    template_name = 'main/transaction_send.html'
    class_form = forms.TransactionUserForm

    def dispatch(self, request, *args, **kwargs):

        if request.method == "POST":
            self.form = forms.TransactionUserForm(request.POST)

            if self.form.is_valid():
                self.obj = self.form.save(commit=False)
                self.obj.user_email = request.user.email
                self.obj.transaction_name = 'send'
                self.obj.transaction_num = create_transaction_number()
                self.obj.save()

                self.transaction_id = self.obj.id
                self.transaction = Transaction.objects.get(id=self.transaction_id)

                self.message = f'{request.user.email}, номер кошелька: "{self.obj.wallet}", пополнил счёт на сумму {self.obj.money} USDT!'

                telegram.send_message_telegram(self.message)

                return HttpResponseRedirect(reverse_lazy('account'))

        elif request.method == "GET":
            self.form = forms.TransactionUserForm()

        return render(
            request,
            self.template_name,
            context={
                'form': self.form,
            }
        )


# Transaction Post
class TransactionPostUser(LoginRequiredMixin, CreateView):
    template_name = 'main/transaction_post.html'
    class_form = forms.TransactionUserForm

    def dispatch(self, request, *args, **kwargs):
        self.min_suma = 0

        if request.user.money > 0:
            self.user_maney = request.user.money
            self.min_suma = self.user_maney - request.user.money * 15 / 100

        if request.method == "POST":
            self.form = forms.TransactionUserForm(request.POST)

            if self.form.is_valid():
                if float(request.POST.get('money')) > self.min_suma:
                    messages.error(request, 'У вас не достаточно USDT!')
                else:
                    self.obj = self.form.save(commit=False)
                    self.obj.user_email = request.user.email
                    self.obj.transaction_name = 'post'
                    self.obj.transaction_num = create_transaction_number()
                    self.obj.save()

                    self.transaction_id = self.obj.id
                    self.transaction = Transaction.objects.get(id=self.transaction_id)

                    self.message = f'{request.user.email}, номер кошелька: "{self.obj.wallet}", хочет вывести: {self.obj.money} USDT!'

                    telegram.send_message_telegram(self.message)

                    return HttpResponseRedirect(reverse_lazy('account'))

        elif request.method == "GET":
            self.form = forms.TransactionUserForm()

        return render(
            request,
            self.template_name,
            context={
                'form': self.form,
                'min_suma': self.min_suma,
            }
        )


# Transaction Story
class TransactionStoryUser(LoginRequiredMixin, TemplateView):
    template_name = 'main/transaction_story.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_transactions = Transaction.objects.filter(user_email=request.user.email).order_by('-id')

        return render(
            request,
            self.template_name,
            context={
                'user_transactions': self.user_transactions,
            }
        )


# Instruction Send Page
class InstructionUser(LoginRequiredMixin, TemplateView):
    template_name = 'main/instruction.html'


# Transaction Processing Page (only Super User)
class TransactionProcessing(LoginRequiredMixin, TemplateView):
    template_name = 'main/superuser/transaction_processing.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

        self.user_transactions = Transaction.objects.all().order_by('-id')

        return render(
            request,
            self.template_name,
            context={
                'user_transactions': self.user_transactions,
            }
        )


# Transaction Processing PK Page (only Super User)
class TransactionProcessingPk(LoginRequiredMixin, UpdateView):
    template_name = 'main/superuser/transaction_processing_pk.html'
    form_class = forms.UpdateTransactionUserForm

    def dispatch(self, request, pk=None, *args, **kwargs):

        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

        self.pk = None
        self.user = None
        self.transaction = get_object_or_404(Transaction, id=pk)

        if pk:
            self.pk = Transaction.objects.filter(id=pk)

            if self.pk:
                self.pk = Transaction.objects.get(id=pk)
                self.user = User.objects.get(email=self.pk.user_email)

        if request.method == "POST":
            self.form = forms.UpdateTransactionUserForm(request.POST, instance=self.transaction)

            if self.form.is_valid():
                self.obj = self.form.save(commit=False)
                self.obj.status = 'success'
                self.obj.update_transaction = timezone.now()
                self.obj.save()

                if self.obj.transaction_name == 'send':
                    self.user.money += self.obj.money
                    self.user.save()
                else:
                    self.commission = round((self.obj.money * 15 / 85), 2)
                    self.superuser = User.objects.filter(email='yourmoneygun@gmail.com')

                    if self.superuser:
                        self.superuser = User.objects.get(email='yourmoneygun@gmail.com')
                        self.superuser.money += self.commission
                        self.superuser.save()

                    self.commission += self.obj.money
                    self.user.money -= self.commission
                    self.user.save()

                return HttpResponseRedirect(reverse_lazy('transaction_processing'))

        elif request.method == "GET":
            self.form = forms.UpdateTransactionUserForm(instance=self.transaction)

        return render(
            request,
            self.template_name,
            context={
                'form': self.form,
                'user': self.user,
                'pk': self.pk,
            }
        )


# Transaction Processing Unsuccess Page (only Super User)
class TransactionProcessingUnsuccess(LoginRequiredMixin, TemplateView):
    template_name = 'main/superuser/transaction_processing_unsuccess.html'

    def dispatch(self, request, pk=None, *args, **kwargs):

        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse_lazy('page_not_found_404'))

        if pk:
            self.pk = Transaction.objects.get(id=pk)
            self.pk.status = 'unsuccess'
            self.pk.update_transaction = timezone.now()
            self.pk.save()

            return HttpResponseRedirect(reverse_lazy('transaction_processing'))

        return HttpResponseRedirect(reverse_lazy('transaction_processing'))


# Class Page Not Found (404)
class PageNotFound(LoginRequiredMixin, TemplateView):
    template_name = 'main/page_404.html'


# Page Not Found (404)
def page_not_found_view(request, exception):
    return render(request, 'main/page_404.html', status=404)
