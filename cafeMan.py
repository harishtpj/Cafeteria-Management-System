# The School Cafeteria Management System
# Written by M.V.Harish Kumar - Grade 12 'A' 
# on 05-09-2024
import mysql.connector as ms
from cliElem import *

conn = ms.connect(host="localhost", user="cafeAdmin", passwd="cafe@p$wd", db="cafeteria")

def validateInput(prompt, vals=None, itype=str):
    while True:
        try:
            data = input(prompt)
            if itype == bool:
                if data not in "TF":
                    log('E', "Invalid input for boolean data. Please try again")
                else:
                    return {'T': 'True', 'F': 'False'}.get(data, "")
            elif vals is not None and data not in vals:
                log('E', "Invalid input for given options. Please try again")
            else:
                if itype in [int, float]:
                    return itype("0"+data)
                return itype(data)
        except ValueError:
            log('E', "Invalid input typed. Please try again")


def staffMan(dbCur, userData):
    options = ["Add new user", "Edit user details", "View users", "Delete user"]
    header = [('id', 'name', 'username', 'password', 'status')] 
    opt = inputLOV("How would you like to manage staffs?", options)

    if opt == "Add new user":
        print(cols+"-"*10)
        print(cols + colors.bold + "Adding new user", colors.reset)
        name = input(cols+"Enter Staff name: ")
        uname = input(cols+"Enter userid for user: ")
        passwd = input(cols+"Enter password for user: ")
        dbCur.execute("SELECT MAX(id)+1 FROM staff")
        query = "INSERT INTO staff VALUES ({}, '{}', '{}', '{}', 'A')" \
                .format(dbCur.fetchone()[0], name, uname, passwd)
        dbCur.execute(query)
        conn.commit()
        log('S', "Added new user sucessfully!")
    
    elif opt == "Edit user details":
        print("-"*10)
        print(cols, colors.bold + "Updating User", colors.reset)
        log('I', "Leaving a field empty will retain the previous value")
        query = "SELECT * FROM staff"
        dbCur.execute(query)
        print(genTable(header + dbCur.fetchall()))
        while True:
            uid = validateInput(cols+"Enter the user id to edit: ", None, int)
            dbCur.execute("SELECT * FROM staff WHERE id = {}".format(uid))
            data = dbCur.fetchone()
            if data is not None:
                break
            log('E', 'No user for given id:', uid)
        name = input(cols+"Enter Staff name[Default: {}]: ".format(data[1]))
        if not name:
            name = data[1]
        uname = input(cols+"Enter userid[Default: {}]: ".format(data[2]))
        if not uname:
            uname = data[2]
        passwd = input(cols+"Enter password[Default: {}]: ".format(data[3]))
        if not passwd:
            passwd = data[3]
        sts = validateInput(cols+"Enter Status[Default: {}]: ".format(data[4]), "AI")
        if not sts:
            sts = data[4]
        query = "UPDATE staff SET name='{}',userid='{}',passwd='{}',status='{}' WHERE id = {}" \
                .format(name, uname, passwd, sts, uid)
        dbCur.execute(query)
        conn.commit()
        log('S', "Updated user sucessfully!")

    elif opt == "View users":
        opt = inputLOV("How would you like to view users?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM staff"
        elif opt == "Search":
            uid = validateInput(cols+"Enter the user id: ", None, int)
            query = "SELECT * FROM staff WHERE id = {}".format(uid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            log('I', f"No such user with id {uid} found")
        else:
            print(genTable(header + data))

    elif opt == "Delete user":
        print("-"*10)
        print(cols+colors.bold + "Deleting user", colors.reset)
        query = "SELECT * FROM staff"
        dbCur.execute(query)
        print(genTable(header + dbCur.fetchall()))
        uid = validateInput(cols+"Enter the user id to delete: ", None, int)
        dbCur.execute("DELETE FROM staff WHERE id = {}".format(uid))
        conn.commit()
        log('S', "Deleted user sucessfully!")

def custMan(dbCur, userData):
    options = ["Add new customer", "Edit customer details", "View customers", "Delete customer"]
    header = [('custId', 'name', 'type', 'status')] 
    kindSwitch = {'S': 'Student', 'T': 'Staff'}
    opt = inputLOV("How would you like to manage customers?", options)

    if opt == "Add new customer":
        print(cols+"-"*10)
        print(cols+colors.bold + "Adding new customer", colors.reset)
        name = input(cols+"Enter name of the customer: ")
        ckind = validateInput(cols+"Enter customer kind[(S)tudent/s(T)aff]: ", "ST")
        dbCur.execute("SELECT MAX(custId)+1 FROM customer")
        query = "INSERT INTO customer VALUES ({}, '{}', '{}', 'A')" \
                .format(dbCur.fetchone()[0], name, kindSwitch[ckind])
        dbCur.execute(query)
        conn.commit()
        log('S', "Added new customer sucessfully!")
    
    elif opt == "Edit customer details":
        print("-"*10)
        print(cols, colors.bold + "Updating customer", colors.reset)
        log('I', "Leaving a field empty will retain the previous value")
        query = "SELECT * FROM customer"
        dbCur.execute(query)
        print(genTable(header + dbCur.fetchall()))
        while True:
            cid = validateInput(cols+"Enter the custId to edit: ", None, int)
            dbCur.execute("SELECT * FROM customer WHERE custId = {}".format(cid))
            data = dbCur.fetchone()
            if data is not None:
                break
            log('E', 'No customer for given id:', cid)
        custId = validateInput(cols+"Enter custId[Default: {}]: ".format(data[0]), None, int)
        if not custId:
            custId = data[0]
        name = input("Enter name[Default: {}]: ".format(data[1]))
        if not name:
            name = data[1]
        ckind = validateInput(cols+"Enter customer kind[(S)tudent/s(T)aff][Default: {}]: ".format(data[2]), "TS")
        ckind = kindSwitch.get(ckind, data[2])
        sts = validateInput(cols+"Enter Status[(A)ctive/(I)nactive][Default: {}]: ".format(data[3]), "AI")
        if not sts:
            sts = data[3]
        query = "UPDATE customer SET custId={},name='{}',custType='{}',status='{}' WHERE custId = {}" \
                .format(custId, name, ckind, sts, cid)
        dbCur.execute(query)
        conn.commit()
        log('S', "Updated customer sucessfully!")

    elif opt == "View customers":
        opt = inputLOV("How would you like to view customers?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM customer"
        elif opt == "Search":
            cid = validateInput(cols+"Enter the custId: ", None, int)
            query = "SELECT * FROM customer WHERE custId = {}".format(cid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            log('I', f"No such customer with code {cid} found")
        else:
            print(genTable(header + data))

    elif opt == "Delete customer":
        print("-"*10)
        print(cols+colors.bold + "Deleting customer", colors.reset)
        query = "SELECT * FROM customer"
        dbCur.execute(query)
        print(genTable(header + dbCur.fetchall()))
        cid = validateInput("Enter the custId to delete: ", None, int)
        dbCur.execute("DELETE FROM customer WHERE custId = {}".format(cid))
        conn.commit()
        log('S', "Deleted user sucessfully!")

def menuMan(dbCur, userData):
    options = ["Add item", "View items", "Update rate", "Delete item"]
    header = [("itemCode", "itemName", "rate")]
    opt = inputLOV("Choose an operation", options)

    if opt == "Add item":
        print(cols+"-"*10)
        print(cols+colors.bold + "Adding new menu Item", colors.reset)
        name = input(cols+"Enter name of menu item: ")
        rate = validateInput(cols+"Enter rate: ", None, float)
        dbCur.execute("SELECT MAX(itemCode)+1 FROM items")
        dbCur.execute("INSERT INTO items VALUES ({}, '{}', {})".format(dbCur.fetchone()[0], name, rate))
        conn.commit()
        log('S', "Added new menu item successfully!")

    elif opt == "View items":
        dbCur.execute("SELECT * FROM items")
        print(genTable(header + dbCur.fetchall()))

    elif opt == "Update rate":
        print(cols+"-"*10)
        print(cols+colors.bold + "Updating rate", colors.reset)
        dbCur.execute("SELECT * FROM items")
        print(genTable(header + dbCur.fetchall()))
        while True:
            icd = validateInput(cols+"Enter the itemCode to edit: ", None, int)
            dbCur.execute("SELECT * FROM items WHERE itemCode = {}".format(icd))
            data = dbCur.fetchone()
            if data is not None:
                break
            log('E', 'No item for given itemCode:', icd)
        rt = validateInput(cols+"Enter new rate: ", None, float)
        dbCur.execute("UPDATE items SET rate = {} where itemCode = {}".format(rt,icd))
        conn.commit()
        log('S', "Updated rate sucessfully!")

    elif opt == "Delete item":
        print(cols+"-"*10)
        print(cols+colors.bold + "Deleting menu item", colors.reset)
        dbCur.execute("SELECT * FROM items")
        print(genTable(header + dbCur.fetchall()))
        icd = validateInput(cols+"Enter the itemCode to delete: ", None, int)
        dbCur.execute("DELETE FROM items WHERE itemCode = {}".format(icd))
        conn.commit()
        log('S', "Deleted item sucessfully!")

def getReceiptData(dataTable):
    data = []
    opt = "y"
    while opt.lower() == 'y':
        print(dataTable)
        icd = validateInput(cols+"Enter itemCode: ", None, int)
        qty = validateInput(cols+"Enter quantity: ", None, int)
        data.append((icd, qty))
        opt = validateInput("Do you want to continue[y/n]: ", "yn")
    return data

def stockMan(dbCur, userData):
    options = ["Add receipt", "View receipt", "Update quantity", "Delete item"]
    header = [("itemCode", "itemName", "quantity")]
    opt = inputLOV("Choose an operation", options)

    if opt == "Add receipt":
        print(cols+"-"*10)
        print(cols+colors.bold + "Adding new receipt", colors.reset)
        
        dbCur.execute("SELECT * FROM items")
        dbCur.executemany("INSERT INTO dailyStock VALUES (%s, current_date(), %s)",
                          getReceiptData(genTable(header + dbCur.fetchall())))
        conn.commit()
        log('S', "Added receipt successfully!")

    elif opt == "View receipt":
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        print(genTable(header + dbCur.fetchall()))

    elif opt == "Update quantity":
        print(cols+"-"*10)
        print(cols+colors.bold + "Updating quantity", colors.reset)
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        print(genTable(header + dbCur.fetchall()))
        while True:
            icd = validateInput(cols+"Enter the itemCode to update: ", None, int)
            dbCur.execute("SELECT * FROM items WHERE itemCode = {}".format(icd))
            data = dbCur.fetchone()
            if data is not None:
                break
            log('E', 'No item for given itemCode:', icd)
        qty = validateInput(cols+"Enter new quantity: ", None, int)
        dbCur.execute("UPDATE dailyStock SET quantity = {} WHERE itemCode = {} \
                AND receiptDate = current_date()".format(qty,icd))
        conn.commit()
        log('S', "Updated quantity sucessfully!")

    elif opt == "Delete item":
        print(cols+"-"*10)
        print(cols+colors.bold + "Deleting receipt item", colors.reset)
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        print(genTable(header + dbCur.fetchall()))
        icd = validateInput(cols+"Enter the itemCode to delete: ", None, int)
        dbCur.execute("DELETE FROM dailyStock WHERE receiptDate = current_date() AND itemCode = {}".format(icd))
        conn.commit()
        log('S', "Deleted item sucessfully!")

def addBill(dbCur, custCode, query):
    opt = "y"
    while opt.lower() == 'y':
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        header = [("itemCode", "itemName", "quantity")]
        print(genTable(header + dbCur.fetchall()))

        icd = validateInput(cols+"Enter itemCode: ", None, int)
        
        while True:
            qty = validateInput(cols+"Enter quantity: ", None, int)

            dbCur.execute("SELECT quantity FROM dailyStock \
                    WHERE itemCode = {} AND receiptDate = current_date()".format(icd))
            threshold = dbCur.fetchone()[0]
            if qty <= threshold:
                dbCur.execute("UPDATE dailyStock SET quantity = quantity - {} \
                        WHERE itemCode = {} AND receiptDate = current_date()".format(qty, icd))
                dbCur.execute(query % (icd, qty))
                break
            log('E', "Only", threshold, "unit(s) is available, enter another value")

        opt = validateInput("Do you want to continue[y/n]: ", "yn")
    return data

def printBill(cid, dt, custData, billData):
    kind = validateInput("Do you want to print bill on screen[y/n]: ", "yn")
    if kind == "y":
        printBanner("The Velammal Cafeteria - Bill Report")
        for k, v in custData.items():
            print(cols,"{}: {}".format(k, v))
        print(genTable(billData, footer=True))
    else:
        log('I', "Printing to file")
        bname = "bill_{}_{}.txt".format(cid, dt)
        with open(bname, 'w') as billF:
            billF.write(printBanner("The Velammal Cafeteria - Bill Report", asStr=True)+'\n')
            for k, v in custData.items():
                billF.write(cols+"{}: {}\n".format(k, v))
            billF.write(genTable(billData, footer=True))
        log('S', "Succesfully printed bill to", bname)


def salesMan(dbCur, userData):
    options = ["Add bill", "Update bill", "Delete bill"]
    itemHdr = [("itemCode", "itemName", "quantity")]
    opt = inputLOV("Choose an operation", options)

    if opt == "Add bill":
        print(cols+"-"*10)
        print(cols+colors.bold + "Adding new bill", colors.reset)
        custData = {}

        dbCur.execute("SELECT * FROM customer")
        print(genTable(itemHdr + dbCur.fetchall()))
        while True:
            custData['custCode'] = validateInput(cols+"Enter the custId: ", None, int)
            dbCur.execute("SELECT name FROM customer WHERE custId = {}".format(custData['custCode']))
            data = dbCur.fetchone()
            if data is not None:
                custData['Name'] = data[0]
                break
            log('E', 'No customer for given id:', custData['custCode'])
        
        dbCur.execute("SELECT IFNULL(MAX(tokenId),0)+1 FROM sales WHERE tDate = current_date()")
        custData['Token ID'] = dbCur.fetchone()[0]
        query = "INSERT INTO sales VALUES({}, current_date(), {}, %s, %s)" \
                .format(custData['Token ID'], custData['custCode'])
        log('I', "Current Token id is", custData['Token ID']) 
        addBill(dbCur, custData['custCode'], query)

        conn.commit()
        log('S', "Added bill successfully!")
        pBill = validateInput("Do you want to print bill[y/n]: ", "yn")
        if pBill == 'y':
            dbCur.execute("SELECT current_date()+0")
            dt = dbCur.fetchone()[0]
            dbCur.execute("SELECT i.itemName, s.qty, s.qty*i.rate \
                    FROM items i, sales s WHERE i.itemCode = s.itemCode AND \
                    s.custCode = {} AND s.tokenId = {} AND s.tDate = current_date()" \
                    .format(custData['custCode'], custData['Token ID']))
            billData = dbCur.fetchall()
            total = 0
            for sno in range(len(billData)):
                total += billData[sno][2]
                billData[sno] = (sno+1,) + billData[sno]
            billData = [('SNO', 'Item', 'Quantity', 'Price')] + billData + [('', '', 'Total', total)]
            printBill(custData['custCode'], dt, custData, billData)

    elif opt == "View receipt":
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        print(genTable(header + dbCur.fetchall()))

    elif opt == "Update quantity":
        print(cols+"-"*10)
        print(cols+colors.bold + "Updating quantity", colors.reset)
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        print(genTable(header + dbCur.fetchall()))
        while True:
            icd = validateInput(cols+"Enter the itemCode to update: ", None, int)
            dbCur.execute("SELECT * FROM items WHERE itemCode = {}".format(icd))
            data = dbCur.fetchone()
            if data is not None:
                break
            log('E', 'No item for given itemCode:', icd)
        qty = validateInput(cols+"Enter new quantity: ", None, int)
        dbCur.execute("UPDATE dailyStock SET quantity = {} WHERE itemCode = {} \
                AND receiptDate = current_date()".format(qty,icd))
        conn.commit()
        log('S', "Updated quantity sucessfully!")

    elif opt == "Delete item":
        print(cols+"-"*10)
        print(cols+colors.bold + "Deleting receipt item", colors.reset)
        dbCur.execute("SELECT i.itemCode, i.itemName, s.quantity FROM dailyStock s, items i \
                WHERE i.itemCode = s.itemCode AND s.receiptDate = current_date();")
        print(genTable(header + dbCur.fetchall()))
        icd = validateInput(cols+"Enter the itemCode to delete: ", None, int)
        dbCur.execute("DELETE FROM dailyStock WHERE receiptDate = current_date() AND itemCode = {}".format(icd))
        conn.commit()
        log('S', "Deleted item sucessfully!")

def mainMenu(dbCur, userData):
    while True:
        options = ["User control", "Manage Customers", "Customize menu", "Daily Stock receipt",
                   "Daily Sales entry", "Exit"]
        opt = inputLOV("What would you like to do?", options)
        if opt == "User control":
            if userData['name'] != 'Administrator':
                log('E', "User", userData['name'], "doesn't have rights to manage users!")
            else:
                staffMan(dbCur, userData)
        elif opt == "Manage Customers":
            if userData['name'] != 'Administrator':
                log('E', "User", userData['name'], "doesn't have rights to manage customers!")
            else:
                custMan(dbCur, userData)
        elif opt == "Customize menu":
            menuMan(dbCur, userData)
        elif opt == "Daily Stock receipt":
            stockMan(dbCur, userData)
        elif opt == "Daily Sales entry":
            salesMan(dbCur, userData)
        elif opt == "Exit":
            print(cols, f"Logging out user: {userData['name']}...")
            break
    
    log('S', "Successfully logged out!")
    print(cols, "Thank you")

if conn.is_connected():
    cur = conn.cursor()

    print(colors.clear, end="")
    printBanner("Welcome to Cafeteria Management System")
    uname = input(cols + "Enter Username: ")
    pswd = input(cols + "Enter password: ")
    cur.execute(f"SELECT name, passwd FROM staff WHERE userId = '{uname}' AND status = 'A'")
    data = cur.fetchall()
    if data != []:
        if data[0][1] == pswd:
            userData = {"name": data[0][0], "username": uname}
            log('I', 'Logon Success')
            print(cols, colors.bold, f"\bWelcome, {userData['name']}", colors.reset)
            mainMenu(cur, userData)
        else:
            log('E', "Invalid password for user:", uname)
    else:
        log('E', "No such user in database:", uname)

input("Press enter to continue...")
conn.commit()
conn.close()

