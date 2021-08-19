import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('user.db')
        return con
    except Error:
        print(Error)


def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS Customer(
        CUSTOMER_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        CUSTOMER_USERNAME text NOT NULL, 
        CUSTOMER_FIRST_NAME text, 
        CUSTOMER_LAST_NAME text, 
        CUSTOMER_EMAIL text, 
        CUSTOMER_PASSWORD text NOT NULL, 
        CUSTOMER_ADDRESS text, 
        CUSTOMER_POSTALCODE text, 
        CUSTOMER_CITY text, 
        CUSTOMER_PHONE text)""")
        
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS Admin(
        [ADMIN_ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
        [ADMIN_USERNAME] text NOT NULL, 
        [ADMIN_PASSWORD] text NOT NULL,
        [ADMIN_FIRSTNAME] text,
        [ADMIN_LASTNAME] text, 
        [ADMIN_DATEADDED] TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS Product(
        [PRODUCT_ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
        [PRODUCT_NAME] text, 
        [PRODUCT_DESC] text, 
        [PRODUCT_PRICE] FLOAT, 
        [PRODUCT_QTY] INTEGER)""")
    
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS [Order](
        [ORDER_ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
        [ORDER_DATE] TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        [ORDER_TOTAL] FLOAT, 
        [CustomerID] INTEGER)""")
    
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS OrderDetail(
        [ORDERDETAIL_ID] INTEGER PRIMARY KEY AUTOINCREMENT, 
        [PRODUCT_ID] INTEGER, 
        [PRODUCT_QTY] INTEGER, 
        [PRODUCT_PRICE] FLOAT, 
        [ORDER_ID] INTEGER)""")
    
    con.commit()


con = sql_connection()
sql_table(con)

def add_order(cDetails, cart): 
    total_amt = 0.0
    for item in cart:
        total_amt = total_amt + item[-2]
    total_amt = round(total_amt, 2)
    
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO [Order](ORDER_TOTAL, CustomerID) VALUES(
        {}, {}
        )'''.format(total_amt, cDetails[0]))
    
    con.commit()
    
    cursorObj.execute("SELECT ORDER_ID FROM [Order] WHERE ORDER_DATE = (SELECT MAX(ORDER_DATE) FROM [Order]);")
    res = cursorObj.fetchall()
    
    oid = res[0][0]
    
    for item in cart:
        cursorObj.execute('''INSERT INTO OrderDetail(PRODUCT_ID, PRODUCT_QTY, PRODUCT_PRICE, ORDER_ID) VALUES(
            {}, {}, {}, {}
            )'''.format(item[0], item[-1], item[-2], oid))
    
    con.commit()
    
    return oid

def fulfill_products(cart):
    cursorObj = con.cursor()
    
    for item in cart:
        cursorObj.execute("SELECT PRODUCT_QTY FROM Product WHERE PRODUCT_ID = {}".format(item[0]))
        res = cursorObj.fetchall()
        
        new_qty = res[0][0] - item[-1]
        
        cursorObj.execute("UPDATE Product SET PRODUCT_QTY = {} WHERE PRODUCT_ID = {}".format(new_qty, item[0]))
        con.commit()
        

def get_products():
    cursorObj = con.cursor()

    cursorObj.execute("SELECT * FROM Product;")
    res = cursorObj.fetchall()

    return res        


def add_product(pname, pdesc, pprice, pqty):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO Product(
        PRODUCT_NAME, PRODUCT_DESC, PRODUCT_PRICE, PRODUCT_QTY
        ) VALUES(
            "{}", "{}", {}, {}
        );""".format(pname, pdesc, pprice, pqty))
    
    con.commit()
    
def update_product(attr, value, pid):
    cursorObj = con.cursor()
    cursorObj.execute("""UPDATE Product SET {} = "{}" WHERE PRODUCT_ID = {}""".format(attr, value, pid))
    con.commit()

def remove_product(pid):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM Product WHERE PRODUCT_ID = {}".format(pid))
    
    
def sql_get_orders(customerID=False):
    cursorObj = con.cursor()
    
    if not customerID:
        cursorObj.execute("""SELECT O.ORDER_ID, O.ORDER_DATE, O.CustomerID, C.CUSTOMER_USERNAME,
                      P.PRODUCT_ID, P.PRODUCT_NAME, P.PRODUCT_DESC, 
                      OD.PRODUCT_QTY, OD.PRODUCT_PRICE , O.ORDER_TOTAL
                      FROM [Order] O 
                      JOIN OrderDetail OD ON O.ORDER_ID = OD.ORDER_ID 
                      JOIN Customer C ON O.CustomerID = C.CUSTOMER_ID
                      JOIN Product P ON P.PRODUCT_ID = OD.PRODUCT_ID;""")
    else:
        cursorObj.execute("""SELECT O.ORDER_ID, O.ORDER_DATE,  
                          P.PRODUCT_ID, P.PRODUCT_NAME, P.PRODUCT_DESC, 
                          OD.PRODUCT_QTY, OD.PRODUCT_PRICE , O.ORDER_TOTAL
                          FROM [Order] O 
                          JOIN OrderDetail OD ON O.ORDER_ID = OD.ORDER_ID 
                          JOIN Product P ON P.PRODUCT_ID = OD.PRODUCT_ID
                          WHERE CustomerID = {};""".format(customerID))
                          
    res = cursorObj.fetchall()
    
    return res


def add_customer(username, password, fname, lname, email, address, postalCode, city, phone):
    
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO Customer(
        CUSTOMER_USERNAME, CUSTOMER_PASSWORD, CUSTOMER_FIRST_NAME, 
        CUSTOMER_LAST_NAME, CUSTOMER_EMAIL, CUSTOMER_ADDRESS, CUSTOMER_POSTALCODE,
        CUSTOMER_CITY, CUSTOMER_PHONE)
         VALUES(
            "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}"
            )'''.format(username, password, fname, lname, email, address, postalCode, city, phone))
        
    con.commit()
    return get_details("CUSTOMER", username)

    
def check_username(userType, username):
    cursorObj = con.cursor()
    
    if userType == "CUSTOMER":
        cursorObj.execute('SELECT * FROM Customer WHERE CUSTOMER_USERNAME = "{}"'.format(username))
    
    elif userType == "ADMIN":
        cursorObj.execute('SELECT * FROM Admin WHERE ADMIN_USERNAME = "{}"'.format(username))
        
    res = cursorObj.fetchall()

    if len(res) > 0:
        return True
    else:
        return False


def match_cust_password(username, password):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT CUSTOMER_PASSWORD FROM Customer WHERE CUSTOMER_USERNAME = "{}"'.format(username))
    res = cursorObj.fetchall()
    

    if len(res) > 0:
        if res[0][0] == password:
            return True
        else:
            return False
        

def match_admin_password(username, password):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT ADMIN_PASSWORD FROM Admin WHERE ADMIN_USERNAME = "{}"'.format(username))
    res = cursorObj.fetchall()
    
    
    if len(res) > 0:
        if res[0][0] == password:
            return True
        else:
            return False


def get_details(loginType, username):
    cursorObj = con.cursor()
    
    if loginType == "CUSTOMER":
        cursorObj.execute('SELECT * FROM Customer WHERE CUSTOMER_USERNAME = "{}"'.format(username))
    elif loginType == "ADMIN":
        cursorObj.execute('SELECT * FROM Admin WHERE ADMIN_USERNAME = "{}"'.format(username))
    else:
        print("Internal Error in Login Type")
    
    res = cursorObj.fetchall()
    
    
    if len(res) > 0:
        return res[0]
    
    
def check_pid(pid):
    cursorObj = con.cursor()
    
    cursorObj.execute('SELECT * FROM Product WHERE PRODUCT_ID = {}'.format(int(pid)))
    res = cursorObj.fetchall()
    
    if len(res) > 0:
        return res[0]
    else:
        return False
    
    
def chck_qty(pid, qty):
    cursorObj = con.cursor()
    
    cursorObj.execute('SELECT PRODUCT_QTY FROM Product WHERE PRODUCT_ID = {}'.format(pid))
    res = cursorObj.fetchall()
    
    if len(res) > 0:
        if int(res[0][0]) >= int(qty):
            return True
        else:
            return False
    else:
        print("Internal error. Product doesn't exist.")
        
    
con = sql_connection()
sql_table(con)
