import sys
    
import loginOps as login
import productOps as products
import orderOps as order
import operations as ops

    
CUSTOMER = "CUSTOMER"
ADMIN = "ADMIN"


def main_menu():
    while True:
        ops.clear_console()

        print("\n\n\t1. Customer Login")
        print("\n\t2. Customer Register")
        print("\n\t3. Admin Login")
        
        res = input("\n\n\tEnter your choice from menu (q = quit): ")
        
        global cust_details, admin_details
        
        if res == 1 or res == '1':            
            cust_details = login.user_login(CUSTOMER)
            if cust_details:
                customer_menu(cust_details)
                
        elif res == 2 or res == '2':            
            cust_details = login.customer_register()
            if cust_details:
                customer_menu(cust_details)
                
        elif res == 3 or res == '3':            
            admin_details = login.user_login(ADMIN)
            if admin_details:
                admin_menu(admin_details)
                
        elif res == 'q' or res == 'Q':
            sys.exit(0)
            
        else:
            continue

def customer_menu(customer_details):
    global cust_details

    while True:
        ops.clear_console()

        print("\n")
        print("CUSTOMER MENU".center(ops.size.columns))
        
        print(ops.right_align("Logged in as: {}".format(customer_details[1])))
        
        print("\n\t1. List of Available Products")
        print("\n\t2. New Order")
        print("\n\t3. My Account")
        print("\n\t4. View Past Orders")
        print("\n\t5. Logout")
        
        res = input("\n\n\tEnter your choice from menu (q = quit): ")
        
        if res == 1 or res == "1":
            products.show_product_data()
            
        elif res == 2 or res == "2":
            order.new_order(customer_details)
            
        elif res == 3 or res == "3":            
            ops.print_details(customer_details)
            
        elif res == 4 or res == "4":            
            order.view_past_orders(customer_details)
            
        elif res == 5 or res == '5':
            login.customer_logout()
            cust_details = None
            main_menu()
            
        elif res == 'q' or res == 'Q':
            sys.exit(0)
            
        else:
            continue

def admin_menu(admn_details):
    global admin_details

    while True:
        ops.clear_console()

        print("\n")
        print("ADMIN LOGIN".center(ops.size.columns))
        
        print(ops.right_align("Logged in as admin: {}".format(admn_details[1])))

        
        print("\n\t1. INVENTORY MENU")
        print("\n\t2. ORDER MENU")
        print("\n\t4. LOGOUT")

        res = input("\n\n\tEnter your choice from menu (q = quit): ")
        
        if res == 1 or res == '1':
            inventory_menu(admn_details)
            
        elif res == 2 or res == '2':
            order_menu(admn_details)
            
        elif res == 4 or res == '4':
            login.admin_logout()
            admin_details = None
            main_menu()
            
        elif res == 'q' or res == 'Q':
            sys.exit(0)
            
        else:
            continue

def inventory_menu(admn_details):
    global admin_details

    while True:
        ops.clear_console()

        print("\n")
        print("INVENTORY MENU".center(ops.size.columns))
        
        print(ops.right_align("Logged in as admin: {}".format(admn_details[1])))

        print("\n\t1. Add New Product")
        print("\n\t2. Edit Existing Product")
        print("\n\t3. Delete Existing Product")
        print("\n\t4. List of Available Products")
        print("\n\t5. Back to Admin Menu")
        print("\n\t6. Logout")
    
        res = input("\n\n\tEnter your choice from menu (q = quit): ")
    
        if res == 1 or res == '1':
            products.new_product()
            
        elif res == 2 or res == '2':
            products.edit_product()
        
        elif res == 3 or res == '3':
            products.delete_product()
            
        elif res == 4 or res == '4':
            products.show_product_data()
            
        elif res == 5 or res == '5':
            admin_menu(admn_details)
            
        elif res == 6 or res == '6':
            login.admin_logout()
            admin_details = None
            main_menu()
            
        elif res == 'q' or res == 'Q':
            sys.exit(0)
            
        else:
            continue
        
def order_menu(admn_details):
    global admin_details
    
    while True:
        ops.clear_console()

        print("\n")
        print("ORDER MENU".center(ops.size.columns))

        print(ops.right_align("Logged in as admin: {}".format(admn_details[1])))
        
        print("\n\t1. View Past Orders")
        print("\n\t2. Back to Admin Menu")
        print("\n\t3. Logout")
       
        res = input("\n\n\tEnter your choice from menu (q = quit): ")
        
        if res == 1 or res == '1':
            order.view_admin_orders(admn_details)
            
        elif res == 2 or res == '2':
            admin_menu(admn_details)
            
        elif res == 3 or res == '3':      
            login.admin_logout()
            admin_details = None
            main_menu()
            
        elif res == 'q' or res == 'Q':
            sys.exit(0)
        
        else:
            continue
    
    
if __name__ == "__main__":
    
    cust_details, admin_details = None, None

    main_menu()
    