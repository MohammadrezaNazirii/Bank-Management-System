import tkinter as tk

class User(tk.Toplevel):
    def __init__(self, parent, db_handler):
        super().__init__()
        self.title("User Page")
        self.geometry("1000x900")
        self.db_handler = db_handler

        # UI elements for requesting a loan
        self.label_loan = tk.Label(self, text="Loan:")
        self.entry_loan = tk.Entry(self)
        self.label_account_loan = tk.Label(self, text="Account No:")
        self.entry_account_loan = tk.Entry(self)
        self.button_request_loan = tk.Button(self, text="Request Loan", command=self.request_loan)
        self.label_loan.pack(pady=5)
        self.entry_loan.pack(pady=5)
        self.label_account_loan.pack(pady=5)
        self.entry_account_loan.pack(pady=5)
        self.button_request_loan.pack(pady=5)

        # UI elements for withdrawing money
        self.label_withdraw = tk.Label(self, text="Withdraw:")
        self.entry_withdraw = tk.Entry(self)
        self.label_account_withdraw = tk.Label(self, text="Account No:")
        self.entry_account_withdraw = tk.Entry(self)
        self.button_withdraw = tk.Button(self, text="Withdraw", command=self.withdraw)
        self.label_withdraw.pack(pady=5)
        self.entry_withdraw.pack(pady=5)
        self.label_account_withdraw.pack(pady=5)
        self.entry_account_withdraw.pack(pady=5)
        self.button_withdraw.pack(pady=5)

        # UI elements for depositing money
        self.label_deposit = tk.Label(self, text="Deposit:")
        self.entry_deposit = tk.Entry(self)
        self.label_account_deposit = tk.Label(self, text="Account No:")
        self.entry_account_deposit = tk.Entry(self)
        self.button_deposit = tk.Button(self, text="Deposit", command=self.deposit)
        self.label_deposit.pack(pady=5)
        self.entry_deposit.pack(pady=5)
        self.label_account_deposit.pack(pady=5)
        self.entry_account_deposit.pack(pady=5)
        self.button_deposit.pack(pady=5)

        # UI elements for making a payment
        self.label_payment = tk.Label(self, text="Payment(Month):")
        self.entry_payment = tk.Entry(self)
        self.button_payment = tk.Button(self, text="Payment", command=self.make_payment)
        self.label_payment.pack(pady=5)
        self.entry_payment.pack(pady=5)
        self.button_payment.pack(pady=5)

        # UI element for viewing installments
        self.label_account_deposit = tk.Label(self, text="Account No:")
        self.entry_account_deposit = tk.Entry(self)
        self.button_view_installments = tk.Button(self, text="View Installments", command=self.view_installments)
        self.label_account_deposit.pack(pady=5)
        self.entry_account_deposit.pack(pady=5)
        self.button_view_installments.pack(pady=5)
    
        
        # UI element for going back to login/signup page
        self.button_go_back = tk.Button(self, text="Go Back", command=self.go_back)
        self.button_go_back.pack(pady=10)

    def request_loan(self):
        loan_amount = self.entry_loan.get()
        account_number = self.entry_account_loan.get()
        # Add your logic for requesting a loan
        # ...

    def withdraw(self):
        withdraw_amount = self.entry_withdraw.get()
        account_number = self.entry_account_withdraw.get()
        # Add your logic for withdrawing money
        # ...

    def deposit(self):
        deposit_amount = self.entry_deposit.get()
        account_number = self.entry_account_deposit.get()
        # Add your logic for depositing money
        # ...

    def make_payment(self):
        payment_amount = self.entry_payment.get()
        # Add your logic for making a payment
        # ...

    def view_installments(self):
        account_number = self.entry_account_withdraw.get()
        # Add your logic for viewing installments
        # ...
    
    def go_back(self):
        # Destroy the current window to go back to the login/signup page
        self.destroy()


class DatabaseHandler:
    def __init__(self):
        # Your database handler initialization logic goes here
        pass

# Create a root window
root = tk.Tk()

# Create a database handler instance
db_handler = DatabaseHandler()

# Create an instance of the User class
user_page = User(root, db_handler)

# Run the GUI
user_page.mainloop()