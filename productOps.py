from tabulate import tabulate
import operations as ops
import databaseConnection as dbo


def show_product_data():
    
    ops.clear_console()

    print("\n")
    print("LIST OF PRODUCTS".center(ops.size.columns))
    print("\n")
    
    res = dbo.get_products()
    
    data = []
    for row in res:
        data.append([row[0], row[1], row[2], row[3], row[4]])

    print("\n", tabulate(data, headers=["ID", "Name", "Description", "Price", "Qty"]))
    
    input("\n\n\n\tPress Enter to return back...")


def new_product():
    ops.clear_console()
    
    print("\n")
    print("Add New Product".center(ops.size.columns))
    
    pname = input("\n\n\tProduct Name: ")
    pdesc = input("\n\tProduct Description: ")
    pprice = input("\n\tProduct Price: ")
    pqty = input("\n\tProduct Quantity: ")
    
    dbo.add_product(pname, pdesc, pprice, pqty)
    
    print("\n\n\tProduct Added Successfully")
    input("\n\tPress enter to continue...")
    
def edit_product():
    while True:
        ops.clear_console()
        
        print("\n")
        print("Edit Product".center(ops.size.columns))
        
        print(ops.right_align("0 = All Products"))
        print(ops.right_align("Q = Quit"))
    
        
        pid = input("\n\n\tProduct ID: ")
        
        if pid == '0' or pid == 0:
            show_product_data()
            continue
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
                
            print("\n\tLeave field blank if not to be updated.")
        
            pname = input("\n\tNew Product Name: ")
            pdesc = input("\n\tNew Product Description: ")
            pprice = input("\n\tNew Product Price: ")
            pqty = input("\n\tNew Product Quantity: ")
    
            print("\n")
    
            if len(pname) > 0:
                dbo.update_product("PRODUCT_NAME", pname, pid)
                print("\n\tProduct Name updated.")
            
            if len(pdesc) > 0:
                dbo.update_product("PRODUCT_DESC", pdesc, pid)
                print("\n\tProduct Description updated.")
    
            if len(pprice) > 0:
                dbo.update_product("PRODUCT_PRICE", pprice, pid)
                print("\n\tProduct Price updated.")
    
            if len(pqty) > 0:
                dbo.update_product("PRODUCT_QTY", pqty, pid)
                print("\n\tProduct Quantity updated.")
            
            input("\n\n\tPress enter to continue...")
            break
        
        
def delete_product():
    while True:
        ops.clear_console()
        
        print("\n")
        print("Delete Product".center(ops.size.columns))
        
        print(ops.right_align("0 = All Products"))
        print(ops.right_align("Q = Quit"))
    
        
        pid = input("\n\n\tProduct ID: ")
        
        if pid == '0' or pid == 0:
            show_product_data()
            continue
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
                
                res = input("\n\n\tAre you sure you want to delete this product? (y/n): ")
                
                if res == 'y' or res == 'Y':
                    dbo.remove_product(pid)
                    print("\n\n\tProduct deleted successfully")
                    input("\n\tPress enter to continue...")
                    break
                elif res == 'n' or res == 'N':
                    breaks