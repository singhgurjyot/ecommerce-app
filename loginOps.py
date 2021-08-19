

from main import CUSTOMER, ADMIN
import databaseConnection as dbo
import operations as ops


isCustLoggedIn = False
isAdminLoggedIn = False


def user_login(loginType):
    global isCustLoggedIn
    global isAdminLoggedIn
    
    ops.clear_console()
    
    print("\n")
    print("USER LOGIN".center(ops.size.columns))
    
    username = input("\n\tEnter your username: ")
    if dbo.check_username(loginType, username):
        password = input("\n\tEnter your password: ")    
    
        if loginType == CUSTOMER:
    
            if dbo.match_cust_password(username, password):
                isCustLoggedIn = True
                return dbo.get_details(loginType, username)
            
            else:
                isCustLoggedIn = False
                print("\n\n\tWrong username or password")
                print("\n\tPress Enter to continue...")
                input("")   
                return None
                
                
        elif loginType == ADMIN:
            if dbo.match_admin_password(username, password):
                isAdminLoggedIn = True
                return dbo.get_details(loginType, username)
    
            else:
                isAdminLoggedIn = False
                print("\n\n\tWrong username or password")
                print("\n\tPress Enter to continue...")
                input("")
                return None
    else:
        print("\n\n\tUsername doesn't exists. Please register first.")
        print("\n\tPress Enter to continue...")
        input("")
        return None
    
def customer_register():
    global isCustLoggedIn
    
    ops.clear_console()
    
    print("\n")
    print("USER REGISTRATION".center(ops.size.columns))
    
    username = input("\n\tEnter your username: ")
    if not dbo.check_username("CUSTOMER", username):
        password = input("\n\tEnter your password: ")
        
        print("\n\tSkip any field by pressing enter.")
        
        fname = input("\n\tFirst Name: ")
        lname = input("\tLast Name: ")
        email = input("\tEmail: ")
        address = input("\tAddress: ")
        postalCode = input("\tPostal Code: ")
        city = input("\tCity: ")        
        phone = input("\tPhone: ")
        
        return dbo.add_customer(username, password, fname, lname, email, address, postalCode, city, phone)
        
    else:
        print("\n\n\tUsername already exists. Try with another username or login.")
        print("\n\tPress Enter to continue...")
        input("")
        return None
        
def admin_logout():
    global isAdminLoggedIn
    
    isAdminLoggedIn = False
    
def customer_logout():
    global isCustLoggedIn
    
    isCustLoggedIn = False