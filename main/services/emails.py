from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from main.services.token_generator import TokenGenerator  # noqa

# Create your send email messages here.


# Send Email Message Activate Account
def send_registration_email(request, user_instance):
    mail_subject = "Activate your Money Gun account"
    message = render_to_string(
        'main/authorization/registration_email.html',
        {
            'user': user_instance,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(
                force_bytes(user_instance.id)
            ),
            'token': TokenGenerator().make_token(
                user_instance,
            )
        }
    )

    email = EmailMessage(
        subject=mail_subject,
        body=message,
        to=[user_instance.email],
    )

    email.content_subtype = 'html'

    email.send(fail_silently=False)
