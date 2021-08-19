import operations as ops
import productOps as products
import databaseConnection as dbo
import billingOps as billing
from tabulate import tabulate

cart = []

def new_order(cust_details):
    
    while True:
        ops.clear_console()
        
        print("\n")
        print("New Order".center(ops.size.columns))
        
        print(ops.right_align("Logged in as: {}".format(cust_details[1])))
        print("\n")
        print(ops.right_align("There are {} products in your cart".format(len(cart))))
        print("\n")
        print(ops.right_align("0 = All Products"))
        print(ops.right_align("C = View Cart"))
        print(ops.right_align("Q = Quit"))
        print(ops.right_align("O = Checkout"))



        pid = input("\n\n\tProduct ID: ")
        
        if pid == '0' or pid == 0:
            products.show_product_data()
            continue
        
        elif pid == 'c' or pid == 'C':
            show_cart()
            continue
        
        elif pid == 'o' or pid == 'O':
            billing.checkout(cust_details, cart)
            break
        
        elif pid == 'q' or pid == 'Q':
            break
        
        else:
            try:
                pdetails = dbo.check_pid(pid)
                
            except:
                continue
            
            if not pdetails:
                print("\n\n\tWrong Product ID, check product list by pressing 0.")
                input("\n\tPress enter to continue...")
                continue
            else:
                print(ops.right_align("Product Details: {}".format(pdetails)))
        
        qty = input("\n\tQuantity: ")
        
        if qty == '0' or qty == 0:
            products.show_product_data()
            continue
        
        if qty == 'c' or qty == 'C':
            show_cart()
            continue
        
        elif qty == 'o' or qty == 'O':
            billing.checkout(cust_details, cart)
            break
        
        if qty == 'q' or qty == 'Q':
            break
        
        
        else:
            
            for item in cart:
                if int(item[0]) == int(pid):
                    qty = int(qty) + item[-1]
                    
            if dbo.chck_qty(pid, qty):
                add_to_cart(pdetails, qty)
                
                rs = input("\n\n\tAdd more products? (y/n): ")
                if rs == 'y' or rs == 'Y':
                    continue
                elif rs == 'n' or rs == 'N':
                    billing.checkout(cust_details, cart)
                    break
                else:
                    break
            
            else:
                print("\n\tInvalid Quantity entered. Quantity should be less than available.")
                print("\tCheck product list by pressing 0.")
                input("\n\tPress enter to continue...")
                continue
        
def add_to_cart(pdetails, qty):
    if len(cart) > 0:
        for item in cart:   
            updated = False
            
            if int(pdetails[0]) == int(item[0]):
                item[-1] = int(qty)
                item[-2] = pdetails[-2] * int(qty)
                updated = True
                break
        if not updated:
            cart.append([pdetails[0], pdetails[1], pdetails[2], pdetails[3]*int(qty), int(qty)])        
    else:
        cart.append([pdetails[0], pdetails[1], pdetails[2], pdetails[3]*int(qty), int(qty)])        

    
def show_cart():
    ops.clear_console()
    
    print("\n")
    print("Your Cart".center(ops.size.columns))
    
    print("\n", tabulate(cart, headers=["ID", "Name", "Description", "Price", "Qty"]))
    
    input("\n\n\n\tPress Enter to return back...")

    
def view_past_orders(cust_details):    
    ops.clear_console()
    
    print("\n")
    print("Past Orders".center(ops.size.columns))
    
    result = dbo.sql_get_orders(cust_details[0])

    print(ops.right_align("Logged in as: {}".format(cust_details[1])))

    print("\n", tabulate(result, headers=["OID", "DATE", "PID", "NAME", "DESCRIPTION", "QTY", "PRICE", "TOTAL"]))

    input("\n\n\tPress enter to continue...")
    
def view_admin_orders(admin_details):
    ops.clear_console()
    
    print("\n")
    print("Past Orders".center(ops.size.columns))
    
    result = dbo.sql_get_orders()

    print(ops.right_align("Logged in as: {}".format(admin_details[1])))

    print("\n", tabulate(result, headers=["OID", "DATE", "CID", "CUSERNAME", "PID", "NAME", "DESCRIPTION", "QTY", "PRICE", "TOTAL"]))

    input("\n\n\tPress enter to continue...")
