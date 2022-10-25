import random

from main.models import User  # noqa

# Create your referral link here.


# Create Referral Link
def create_referral_link():
    referral_link_users = User.objects.all().exclude(referral_link=None)

    referral_link = ''
    flag = False

    while True:
        for x in range(6):
            referral_link = referral_link + random.choice(list('ABCDEFGHIGKLMNOPQRSTUVYXWZ1234567890'))

        if not referral_link_users:
            flag = True
        else:
            for referral_link_user in referral_link_users.values_list():
                if referral_link_user[5] == referral_link:
                    continue
                else:
                    flag = True
        if flag:
            break

    return referral_link
