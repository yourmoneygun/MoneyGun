import random

from main.models import Transaction  # noqa

# Create your transaction number here.


# Create Transaction Number
def create_transaction_number():
    transaction_numbers = Transaction.objects.all()

    transaction_num = ''
    flag = False

    while True:
        for x in range(6):
            transaction_num = transaction_num + random.choice(list('1234567890'))

        if not transaction_numbers:
            flag = True
        else:
            for transaction_number in transaction_numbers.values_list():
                if transaction_number[3] == transaction_num:
                    continue
                else:
                    flag = True
        if flag:
            break

    return transaction_num
