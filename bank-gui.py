import tkinter as tk
from tkinter import messagebox
import psycopg2
import hashlib

from datetime import datetime

def hash_password_with_sha256(password):
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the password bytes
    sha256_hash.update(password_bytes)

    # Get the hexadecimal representation of the hash
    hashed_password = sha256_hash.hexdigest()

    return hashed_password


class DatabaseHandler:
    def __init__(self, host, port, dbname, user, password):
        self.connection = None
        self.cursor = None
        self.connect_to_database(host, port, dbname, user, password)

    def connect_to_database(self, host, port, dbname, user, password):
        try:
            connection_string = f"host={host} port={port} dbname={dbname} user={user} password={password} sslmode=prefer connect_timeout=10"
            self.connection = psycopg2.connect(connection_string)
            self.cursor = self.connection.cursor()
            print("Connection successful")
        except Exception as e:
            print(f"Error: {str(e)}")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"Error executing query: {str(e)}")

    def execute_select_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing select query: {str(e)}")
            return None


class LoginPage(tk.Tk):
    def __init__(self, db_handler):
        super().__init__()
        self.title("Login Page")
        self.geometry("500x400")
        self.db_handler = db_handler

        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.button_login = tk.Button(self, text="Login", command=self.login_button_clicked)
        self.button_signup = tk.Button(self, text="Sign Up", command=self.open_signup_page)

        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=5)
        self.entry_password.pack(pady=5)
        self.button_login.pack(pady=10)
        self.button_signup.pack(pady=5)

    def login_button_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role_label = self.authenticate_user(username, password)

        if role_label:
            messagebox.showinfo("Login Successful", f"Welcome, {username} !")

            self.open_Admin_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def authenticate_user(self, username, password):
        try:
            # Call the stored procedure to validate user credentials
            self.db_handler.cursor.callproc("validate_user", (username,  hash_password_with_sha256(password)))
            print(hash_password_with_sha256(password))
            
            # Fetch the result
            result = self.db_handler.cursor.fetchone()
            
           

            # Check if the result indicates successful authentication
            if result and result[0] == 1:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            return False

    def open_signup_page(self):
        self.withdraw()
        SignupPage(self, self.db_handler)
    
    def open_Admin_page(self):
        self.withdraw()
        Admin(self, self.db_handler)
        
        


class Admin(tk.Toplevel):
    def __init__(self, parent, db_handler):
        super().__init__()
        self.title("admin Page")
        self.geometry("800x700")
        self.db_handler = db_handler
        self.parent = parent

        self.label_phone = tk.Label(self, text="Phone Number:")
        self.entry_phone = tk.Entry(self)
        self.button_search1 = tk.Button(self, text="Search Users by Phone", command=self.search_users_by_phone)
        self.label_phone.pack(pady=5)
        self.entry_phone.pack(pady=5)
        self.button_search1.pack(pady=5)

        # UI elements for searching users by username
        self.label_username = tk.Label(self, text="Username:")
        self.entry_username = tk.Entry(self)
        self.button_search2 = tk.Button(self, text="Search Users by Username", command=self.search_users_by_username)
        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)
        self.button_search2.pack(pady=5)

        # UI elements for searching accounts by account number
        self.label_accountNumber = tk.Label(self, text="Account Number:")
        self.entry_accountNumber = tk.Entry(self)
        self.button_search3 = tk.Button(self, text="Search Accounts by Account Number", command=self.search_accounts_by_account_number)
        self.label_accountNumber.pack(pady=5)
        self.entry_accountNumber.pack(pady=5)
        self.button_search3.pack(pady=5)

        # UI elements for searching accounts by user ID
        self.label_userID = tk.Label(self, text="User ID:")
        self.entry_userID = tk.Entry(self)
        self.button_search4 = tk.Button(self, text="Search Accounts by User ID", command=self.search_accounts_by_user_id)
        self.label_userID.pack(pady=5)
        self.entry_userID.pack(pady=5)
        self.button_search4.pack(pady=5)
        
        self.button_search5=tk.Button(self, text="sort the loan installments by date", command=self.sort)
        self.button_search5.pack(pady=5)
        
        self.entry_query = tk.Entry(self, width=50)
        self.entry_query.pack(pady=5)

        # Create a Button to execute the query
        self.button_execute_query = tk.Button(self, text="Execute Query", command=self.execute_query)
        self.button_execute_query.pack(pady=5)
        
        self.button_back = tk.Button(self, text="Back to Login", command=self.show_login_page)
        self.button_back.pack(pady=8)
        
    def execute_query(self):
        query = self.entry_query.get()
        print(query)
        try:
            self.db_handler.cursor.execute(query)
            result = self.db_handler.cursor.fetchall()
            print(result)
            # Display the result in the Text widget
            self.show_search_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error executing query: {str(e)}")

        
    def sort(self):
        query = "SELECT * FROM loaninstallments ORDER BY duedate"
        self.db_handler.cursor.execute(query)
        result = self.db_handler.cursor.fetchall()
        # Process the result as needed
        self.show_search_result(result)
                

    def search_users_by_phone(self):
      
        phone_number = self.entry_phone.get()

        query = "SELECT * FROM users WHERE phonenumber LIKE %s"
        # Adding '%' to perform a partial match
        values = ('%' + phone_number + '%',)

        # Execute the query and fetch the result
        self.db_handler.cursor.execute(query, values)
        result = self.db_handler.cursor.fetchall()

        # Show the result in a messagebox
        self.show_search_result(result)
        
    def search_users_by_username(self):
        username = self.entry_username.get()

        query = "SELECT * FROM users WHERE username LIKE %s"
        # Adding '%' to perform a partial match
        values = ('%' + username + '%',)

        # Execute the query and fetch the result
        self.db_handler.cursor.execute(query, values)
        result = self.db_handler.cursor.fetchall()

        # Show the result in a messagebox
        self.show_search_result(result)

    def search_accounts_by_account_number(self):
        account_number = self.entry_accountNumber.get()

        query = "SELECT * FROM account WHERE accountnumber = %s"
        # Adding '%' to perform a partial match
        values = (account_number ,)

        # Execute the query and fetch the result
        self.db_handler.cursor.execute(query, values)
        result = self.db_handler.cursor.fetchall()

        # Show the result in a messagebox
        self.show_search_result(result)

    def search_accounts_by_user_id(self):
        user_id = self.entry_userID.get()

        query = "SELECT * FROM account WHERE userid = %s"
        values = (user_id,)

        # Execute the query and fetch the result
        self.db_handler.cursor.execute(query, values)
        result = self.db_handler.cursor.fetchall()

        # Show the result in a messagebox
        self.show_search_result(result)

    def show_search_result(self, result):
    # Display the result in a messagebox
        if result:
            messagebox.showinfo("Search Result", f"Search returned:\n{result}")
        else:
            messagebox.showinfo("Search Result", "No matching records found.")
    def show_login_page(self):
        # Close the signup window and show the login window
        self.destroy()
        self.parent.deiconify()

            
        # Add your logic for displaying the search result
        # You can use a messagebox or any other UI element to show the result
        # ...
        
        
       
class SignupPage(tk.Toplevel):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.title("Sign Up Page")
        self.geometry("600x500")
        self.parent = parent
        self.db_handler = db_handler
        
        
        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")
        self.label_first_name = tk.Label(self, text="First Name:")
        self.label_last_name = tk.Label(self, text="Last Name:")
        self.label_birth_date = tk.Label(self, text="Birth Date (YYYY-MM-DD):")
        self.label_phone = tk.Label(self, text="PhoneNumber:")
        
       
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_first_name = tk.Entry(self)
        self.entry_last_name = tk.Entry(self)
        self.entry_birth_date = tk.Entry(self)
        self.entry_phone = tk.Entry(self)

        self.button_signup = tk.Button(self, text="Sign Up", command=self.signup_button_clicked)
        self.button_back = tk.Button(self, text="Back to Login", command=self.show_login_page)

        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=5)
        self.entry_password.pack(pady=5)
        self.label_first_name.pack(pady=5)
        self.entry_first_name.pack(pady=5)
        self.label_last_name.pack(pady=5)
        self.entry_last_name.pack(pady=5)
        self.label_birth_date.pack(pady=5)
        self.entry_birth_date.pack(pady=5)
        self.entry_phone.pack(pady=5)

        self.button_signup.pack(pady=5)
        self.button_back.pack(pady=10)

    def signup_button_clicked(self):
        username = self.entry_username.get()
        password = hash_password_with_sha256(self.entry_password.get())
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        birth_date = self.entry_birth_date.get()
        current_time = datetime.now().time()
        phone=self.entry_phone.get()

# Format the time as a string
        formatted_time = current_time.strftime("%H:%M:%S")


        try:
            self.db_handler.cursor.execute(
            "CALL insert_user(%s, %s, %s, %s, %s, %s, %s, %s)",
            (username, password, 'user', formatted_time,
                                                first_name, last_name, birth_date, phone))
    # Commit the transaction if it was successful
            self.db_handler.connection.commit()
            messagebox.showinfo("Sign Up Successful", f"User {username} has been registered!")
        except psycopg2.Error as e:
    # Rollback the transaction in case of an error
            self.db_handler.connection.rollback()
    # Handle the specific exception caused by the RAISE EXCEPTION statement
            if "already exists" in str(e):
                messagebox.showerror("Sign Up Error", f"Username '{username}' already exists.")
            else:
                
                messagebox.showerror("Sign Up Error", f"Error: {str(e)}")
         
        self.show_login_page()
        
    def show_login_page(self):
        # Close the signup window and show the login window
        self.destroy()
        self.parent.deiconify()
     
class User(tk.Toplevel):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.title(" Page")
        self.geometry("600x500")
        self.parent = parent
        self.db_handler = db_handler
        
        
      
    def show_login_page(self):
        # Close the signup window and show the login window
        self.destroy()
        self.parent.deiconify()

if __name__ == "__main__":
    # Database connection details
    db_host = "172.18.0.2"
    db_port = 5432
    db_name = "dbexample"
    db_user = "ali"
    db_password = "123456"

    # Create a DatabaseHandler instance
    db_handler = DatabaseHandler(db_host, db_port, db_name, db_user, db_password)

    # Initialize and run the login page
    login_page = LoginPage(db_handler)
    login_page.mainloop()

    # Close the database connection after the Tkinter loop ends
    db_handler.close_connection()
