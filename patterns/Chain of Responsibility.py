class Account:
    __successor = None
    __balance = None

    def __init__(self, balance: float):
        self.__balance = balance

    def set_next(self, account: 'Account'):
        self.__successor = account

    def get_balance(self):
        print(self.__balance)

    def pay(self, amount_to_pay: float) -> bool:
        if self.can_pay(amount_to_pay=amount_to_pay):
            print(f'Оплата {amount_to_pay} используя {self.__str__()}')
            self.__balance -= amount_to_pay
            return True
        elif self.__successor:
            print(f'Нельзя оплатить используя {self.__str__()}')
            self.__successor.pay(amount_to_pay=amount_to_pay)
        else:
            print(f'Нельзя оплатить. На счетах отсутствуют средства')

    def can_pay(self, amount_to_pay: float) -> bool:
        return self.__balance >= amount_to_pay


class Bank(Account):
    def __str__(self):
        return 'Bank account'


class PayPal(Account):
    def __str__(self):
        return 'PayPal account'


class BitCoin(Account):
    def __str__(self):
        return 'BitCoin account'


bank = Bank(100)
paypal = PayPal(200)
bitcoin = BitCoin(400)

bank.set_next(paypal)
paypal.set_next(bitcoin)

bank.pay(320)

lst_account = [Bank(100), PayPal(200), BitCoin(400)]

current_account = None
counter = 0
while True:
    if counter + 1 < len(lst_account):
        lst_account[counter].set_next(lst_account[counter+1])
        result = lst_account[counter].pay(320)
        counter += 1
        if result:
            break





