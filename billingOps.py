# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 19:14:09 2021

@author: singh
"""

import operations as ops
from tabulate import tabulate
import main
import orderOps as order
import databaseConnection as dbo


def checkout(customer_details, cart):
    total_amt = 0.0
        
    for item in cart:
        total_amt = total_amt + item[-2]
            
    total_amt = round(total_amt, 2)
    
    
    while True:
        ops.clear_console()
        
        print("\n")
        print("CHECKOUT".center(ops.size.columns))
        
        print("\n", tabulate(cart, headers=["ID", "Name", "Description", "Price", "Qty"]))
        
        print(ops.right_align("Total Amount: {}".format(total_amt)))
        
        res = input("\n\tConfirm the order? (y/n): ")
        
        
        if res == 'y' or res == 'Y':
            print("\n\n\tPlease pay the amount at cash counter.")
            order.cart = []
            dbo.fulfill_products(cart)
            oid = dbo.add_order(customer_details, cart)
            
            input("\n\tPress enter to continue...")
            order_successful(oid)
            
            break
            
        elif res == 'n' or res == 'N':
            main.customer_menu(customer_details)
            
        else:
            continue
    
def order_successful(oid):
    ops.clear_console()
    
    print("\n\n")
    print("~~~~~ O R D E R   S U C C E S S F U L ~~~~~".center(ops.size.columns))
    print("\n\n")
    
    print("Your Order ID is: {}".format(oid).center(ops.size.columns))
    
    print("\n\n\tThanks for ordering with us.")
    input("\n\tPress Enter to continue...")
    
    

    