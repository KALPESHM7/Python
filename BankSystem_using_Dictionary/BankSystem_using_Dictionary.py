from datetime import datetime
def log_transactions(transaction_type):
    def decorator(func):
        def wrapper(self,amount):
            result = func(self,amount)
            self._transactions.append(Transaction(transaction_type,amount))
            return result
        return wrapper
    return decorator
class  BankAccount:
    initial_counter = 100

    def __init__(self,name,initial_amount):
        self.account_number = BankAccount.initial_counter
        BankAccount.initial_counter += 1
        self.account_holder = name
        self._balance = initial_amount
        self._transactions = [] # creating a private list for log 
        self._transactions.append(Transaction("Account Created",initial_amount,"Initial_deposit"))
    @log_transactions("Deposit")
    def deposit(self,amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be Positive.")
        self._balance += amount
        print(f"{amount} is Deposited. New balance is:{self._balance}")
    @log_transactions("Withdrawal")    
    def withdraw(self,amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal Amount should be Positive.")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient Balance!")
        else:
            self._balance -= amount
            print(f"{amount} is withdrawn. The new Balance is {self._balance}")
        
    def see_balance(self):
        return self._balance
    def display_details(self):
        print(f"Account Number: {self.account_number}")
        print(f"Account Holder:{self.account_holder}")
        print(f"Balance is:{self._balance}")
    def show_transactions(self):
        print (f"\n Tranactions History for account{self.account_number}:")
        if not self._transactions:
            print("No Transactions")
        else:
            for txn in self.iterate_transactions():
                print(txn)
    def iterate_transactions(self):
        ''' A Generator that yields one transactions at a time '''
        for txn in self._transactions:
            yield txn
class SavingsAccount(BankAccount):
    def __init__(self,name,initial_amount):
        super().__init__(name,initial_amount) # super keyword is used to get the method and the attributes of the base class(BankAccount)
        self.interest_rate = 0.04
    def display_details(self):
        super().display_details()
        print(f"Account Type: Savings and the interest rate is {self.interest_rate}")
class CheckingAccount(BankAccount):
    def __init__(self,name,initial_amount):
        super().__init__(name,initial_amount)
        self.overdraft_limit = 500
    def withdraw(self,amount):
        if amount > self._balance + self.overdraft_limit:
            print("Withdraw exceed the Overdraft limit")
        else:
            self._balance -= amount
            print(f"{amount} is being Withdrawen.The New Balance is {self._balance}")
    def display_details(self):
        super().display_details()
        print("Account Type: Checking")
class Transaction:
    def __init__(self,typeot,amount,note=""):
        self.typeot = typeot
        self.amount = amount
        self.timestamp = datetime.now() # to note down the current time
        self.note = note
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {self.typeot} | {self.amount} | {self.note}" # to return the log in the given format 
class BankError(Exception): # We create this class for doing custome error
    '''so this will be the base class.'''
    pass
class InvalidAmountError(BankError):
    '''Raised When the amount is zero or negative '''
    pass
class InsufficientFundsError(BankError):
    ''' Raised when the account doesnt have balance'''
    pass
class AccountNotFoundError(BankError):
    '''Raised when when there is no account number'''
    pass
    

account = {}
def main():
    
    while True:
        print("====== Bank Account ======")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Display Account Details")
        print("5. View Transactions History")
        print("6. Exit")
        
        choice = int(input("Enter Your Choice:"))
        if choice == 1:
            name = input("Enter the Account Holder name:")
            acc_type = input("Enter the account type (savings/checking):").lower()
            initial_amount = int(input("Enter the initial amount:"))
            
            if acc_type == "savings":
                acc = SavingsAccount(name,initial_amount)
            elif acc_type == "checking":
                acc = CheckingAccount(name,initial_amount)
            else:
                print("Invalid account type")
                continue
            account[acc.account_number] = acc # in dictionary we give it as keyvalue pair so the key is acc.account_number and the  value is the object refereing to it (i.e name and initial_amount)
            ''' Here we are assigning key as account number and the acc object which has name and initial amount '''
            print(f"Created Account Successfully {name},The account number is {acc.account_number}")
        elif choice == 2: # for Deposit
            acc_num = int(input("Enter the Account Number:"))
            if acc_num in account:
                try:
                    amount=int(input("Enter the amount to be Deposited:"))
                    account[acc_num].deposit(amount)
                except InvalidAmountError as e:
                    print("Error:", e)
            else:
                print("Account Not found!")
        elif choice == 3: # For withdraw
            acc_num = int(input("Enter the account number:"))
            if acc_num in account:
                try:
                    amount = float(input("Enter the amount to be withdrawn:"))
                    account[acc_num].withdraw(amount)
                except (InvalidAmountError,InsufficientFundsError) as e:
                    print("Error:", e)
            else:
                print("Account Not found")
        elif choice == 4:
            acc_num = int(input("Enter the Account Number:"))
            if acc_num in account:
                account[acc_num].display_details()
            else:
                print("Account not found")
        elif choice == 5:
            acc_num = int(input("Enter the account number:"))
            if acc_num in account:
                account[acc_num].show_transactions()
            else:
                print("Account  Not Found! ")
                          
        elif choice == 6:
            print("Thank You for using the Banking System.")
            break
        else:
            print("Invalid choice .Try again ")

if __name__ == "__main__":
    main()
            
                

# code for testing using Pytest:

# Testing Cretation of account 
test_account = SavingsAccount("Kalpesh",1000)
assert test_account.account_holder == "Kalpesh"
assert test_account._balance == 1000
assert test_account.account_number >=100
print("Account test is passed")


#Testing Deposit
test_account.deposit(500)
assert test_account._balance == 1500

#try:
 #   test_account.deposit(-100)
#except InvalidAmountError as e:
 #   assert str(e) =="Deposit amount must be Positive"
print("Deposit Tested Successfully")


# Testing Withdrawal
test_account.withdraw(200)
assert test_account._balance == 1300
try:
    test_account.withdraw(5000)
except InsufficientFundsError as e:
    assert str(e) == "Insufficient Balance!"
print("Withdrawal Tested Successfully")


check_acc = CheckingAccount("K", 100)
check_acc.withdraw(500)  
assert check_acc._balance == -400

check_acc.withdraw(200)  # Should exceed overdraft
# Should print "Withdraw exceed the Overdraft limit" but not raise error
assert check_acc._balance == -400  # Balance shouldn't change
