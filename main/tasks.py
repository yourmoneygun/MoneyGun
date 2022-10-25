from celery import shared_task

from main.services import telegram  # noqa
from main import models  # noqa

# Create your tasks here.


# Tasks Send Money
@shared_task
def send_money():
    products = models.Product.objects.all()
    user_products = models.UserProduct.objects.all()
    referrals = models.Referral.objects.all()
    user_referrals = models.UserReferralTotal.objects.all()

    if user_products:
        for user_product in user_products.values_list():
            product = models.Product.objects.get(id=user_product[1])
            user = models.User.objects.get(id=user_product[2])
            user_prod = models.UserProduct.objects.get(product=user_product[1], user=user_product[2])
            user_prod.total_price += round(float(product.money / 25), 2)
            user_prod.save()
            user.money += round(float(product.money / 25), 2)
            user.save()

    if user_products and referrals:
        for referral in referrals.values_list():
            main_user = models.User.objects.get(id=referral[1])
            ref_user = models.User.objects.get(id=referral[2])

            for user_product in user_products.values_list():
                if user_product[2] == ref_user.id:
                    product = models.Product.objects.get(id=user_product[1])
                    main_user.money += round((product.money / 25 / 10), 2)
                    main_user.save()

    if products and user_referrals:
        for user_referral in user_referrals.values_list():
            for product in products.values_list():
                if product[0] == user_referral[1]:
                    user_referral_get = models.UserReferralTotal.objects.get(id=user_referral[0])
                    user_referral_get.total_ref_money += round((user_referral[3] * (product[3] / 25 / 10)), 2)
                    user_referral_get.save()

    # telegram.send_message_telegram("! SUCCESS !")
