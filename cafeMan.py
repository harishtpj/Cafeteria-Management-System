# The School Cafeteria Management System
# Written by M.V.Harish Kumar - Grade 12 'A' 
# on 05-09-2024
import mysql.connector as ms
import cliElem as cli

conn = ms.connect(host="localhost", user="cafeAdmin", passwd="cafe@p$wd", db="cafeteria")

def validateInput(prompt, vals=None, itype=str):
    while True:
        try:
            data = input(prompt)
            if itype == bool:
                if data not in "TF":
                    cli.log('E', "Invalid input for boolean data. Please try again")
                else:
                    return {'T': 'True', 'F': 'False'}.get(data, "")
            elif vals is not None and data not in vals:
                cli.log('E', "Invalid input for given options. Please try again")
            else:
                if itype in [int, float]:
                    return itype("0"+data)
                return itype(data)
        except ValueError:
            cli.log('E', "Invalid input typed. Please try again")


def staffMan(dbCur, userData):
    options = ["Add new user", "Edit user details", "View users", "Delete user"]
    header = [('id', 'name', 'username', 'password', 'status')] 
    opt = cli.inputLOV("How would you like to manage staffs?", options)

    if opt == "Add new user":
        print(cli.cols+"-"*10)
        print(cli.cols + cli.colors.bold + "Adding new user", cli.colors.reset)
        name = input(cli.cols+"Enter Staff name: ")
        uname = input(cli.cols+"Enter userid for user: ")
        passwd = input(cli.cols+"Enter password for user: ")
        dbCur.execute("SELECT MAX(id)+1 FROM staff")
        query = "INSERT INTO staff VALUES ({}, '{}', '{}', '{}', 'A')" \
                .format(dbCur.fetchone()[0], name, uname, passwd)
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Added new user sucessfully!")
    
    elif opt == "Edit user details":
        print("-"*10)
        print(cli.cols, cli.colors.bold + "Updating User", cli.colors.reset)
        cli.log('I', "Leaving a field empty will retain the previous value")
        query = "SELECT * FROM staff"
        dbCur.execute(query)
        print(cli.genTable(header + dbCur.fetchall()))
        while True:
            uid = validateInput(cli.cols+"Enter the user id to edit: ", None, int)
            dbCur.execute("SELECT * FROM staff WHERE id = {}".format(uid))
            data = dbCur.fetchone()
            if data is not None:
                break
            cli.log('E', 'No user for given id:', uid)
        name = input(cli.cols+"Enter Staff name[Default: {}]: ".format(data[1]))
        if not name:
            name = data[1]
        uname = input(cli.cols+"Enter userid[Default: {}]: ".format(data[2]))
        if not uname:
            uname = data[2]
        passwd = input(cli.cols+"Enter password[Default: {}]: ".format(data[3]))
        if not passwd:
            passwd = data[3]
        sts = validateInput(cli.cols+"Enter Status[Default: {}]: ".format(data[4]), "AI")
        if not sts:
            sts = data[4]
        query = "UPDATE staff SET name='{}',userid='{}',passwd='{}',status='{}' WHERE id = {}" \
                .format(name, uname, passwd, sts, uid)
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Updated user sucessfully!")

    elif opt == "View users":
        opt = cli.inputLOV("How would you like to view users?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM staff"
        elif opt == "Search":
            uid = validateInput(cli.cols+"Enter the user id: ", None, int)
            query = "SELECT * FROM staff WHERE id = {}".format(uid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            cli.log('I', f"No such user with id {uid} found")
        else:
            print(cli.genTable(header + data))

    elif opt == "Delete user":
        print("-"*10)
        print(cli.cols+cli.colors.bold + "Deleting user", cli.colors.reset)
        query = "SELECT * FROM staff"
        dbCur.execute(query)
        print(cli.genTable(header + dbCur.fetchall()))
        uid = validateInput(cli.cols+"Enter the user id to delete: ", None, int)
        dbCur.execute("DELETE FROM staff WHERE id = {}".format(uid))
        conn.commit()
        cli.log('S', "Deleted user sucessfully!")

def custMan(dbCur, userData):
    options = ["Add new customer", "Edit customer details", "View customers", "Delete customer"]
    header = [('custId', 'name', 'type', 'status')] 
    kindSwitch = {'S': 'Student', 'T': 'Staff'}
    opt = cli.inputLOV("How would you like to manage customers?", options)

    if opt == "Add new customer":
        print(cli.cols+"-"*10)
        print(cli.cols+cli.colors.bold + "Adding new customer", cli.colors.reset)
        name = input(cli.cols+"Enter name of the customer: ")
        ckind = validateInput(cli.cols+"Enter customer kind[(S)tudent/s(T)aff]: ", "ST")
        dbCur.execute("SELECT MAX(custId)+1 FROM customer")
        query = "INSERT INTO customer VALUES ({}, '{}', '{}', 'A')" \
                .format(dbCur.fetchone()[0], name, kindSwitch[ckind])
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Added new customer sucessfully!")
    
    elif opt == "Edit customer details":
        print("-"*10)
        print(cli.cols, cli.colors.bold + "Updating customer", cli.colors.reset)
        cli.log('I', "Leaving a field empty will retain the previous value")
        query = "SELECT * FROM customer"
        dbCur.execute(query)
        print(cli.genTable(header + dbCur.fetchall()))
        while True:
            cid = validateInput(cli.cols+"Enter the custId to edit: ", None, int)
            dbCur.execute("SELECT * FROM customer WHERE custId = {}".format(cid))
            data = dbCur.fetchone()
            if data is not None:
                break
            cli.log('E', 'No customer for given id:', cid)
        custId = validateInput(cli.cols+"Enter custId[Default: {}]: ".format(data[0]), None, int)
        if not custId:
            custId = data[0]
        name = input("Enter name[Default: {}]: ".format(data[1]))
        if not name:
            name = data[1]
        ckind = validateInput(cli.cols+"Enter customer kind[(S)tudent/s(T)aff][Default: {}]: ".format(data[2]), "TS")
        ckind = kindSwitch.get(ckind, data[2])
        sts = validateInput(cli.cols+"Enter Status[(A)ctive/(I)nactive][Default: {}]: ".format(data[3]), "AI")
        if not sts:
            sts = data[3]
        query = "UPDATE customer SET custId={},name='{}',custType='{}',status='{}' WHERE custId = {}" \
                .format(custId, name, ckind, sts, cid)
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Updated customer sucessfully!")

    elif opt == "View customers":
        opt = cli.inputLOV("How would you like to view customers?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM customer"
        elif opt == "Search":
            cid = validateInput(cli.cols+"Enter the custId: ", None, int)
            query = "SELECT * FROM customer WHERE custId = {}".format(cid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            cli.log('I', f"No such customer with code {cid} found")
        else:
            print(cli.genTable(header + data))

    elif opt == "Delete customer":
        print("-"*10)
        print(cli.cols+cli.colors.bold + "Deleting customer", cli.colors.reset)
        query = "SELECT * FROM customer"
        dbCur.execute(query)
        print(cli.genTable(header + dbCur.fetchall()))
        cid = validateInput("Enter the custId to delete: ", None, int)
        dbCur.execute("DELETE FROM customer WHERE custId = {}".format(cid))
        conn.commit()
        cli.log('S', "Deleted user sucessfully!")

def menuMan(dbCur, userData):
    options = ["Add item", "View items", "Update rate", "Delete item"]
    header = [("itemCode", "itemName", "rate")]
    opt = cli.inputLOV("Choose an operation", options)

    if opt == "Add item":
        print(cli.cols+"-"*10)
        print(cli.cols+cli.colors.bold + "Adding new menu Item", cli.colors.reset)
        name = input(cli.cols+"Enter name of menu item: ")
        rate = validateInput(cli.cols+"Enter rate: ", None, float)
        dbCur.execute("SELECT MAX(itemCode)+1 FROM items")
        dbCur.execute("INSERT INTO items VALUES ({}, '{}', {})".format(dbCur.fetchone()[0], name, rate))
        conn.commit()
        cli.log('S', "Added new menu item successfully!")

    elif opt == "View items":
        dbCur.execute("SELECT * FROM items")
        print(cli.genTable(header + dbCur.fetchall()))

    elif opt == "Update rate":
        print(cli.cols+"-"*10)
        print(cli.cols+cli.colors.bold + "Updating rate", cli.colors.reset)
        dbCur.execute("SELECT * FROM items")
        print(cli.genTable(header + dbCur.fetchall()))
        while True:
            icd = validateInput(cli.cols+"Enter the itemCode to edit: ", None, int)
            dbCur.execute("SELECT * FROM items WHERE itemCode = {}".format(icd))
            data = dbCur.fetchone()
            if data is not None:
                break
            cli.log('E', 'No item for given itemCode:', icd)
        rt = validateInput(cli.cols+"Enter new rate: ", None, float)
        dbCur.execute("UPDATE items SET rate = {} where itemCode = {}".format(rt,icd))
        conn.commit()
        cli.log('S', "Updated rate sucessfully!")

    elif opt == "Delete item":
        print(cli.cols+"-"*10)
        print(cli.cols+cli.colors.bold + "Deleting menu item", cli.colors.reset)
        dbCur.execute("SELECT * FROM items")
        print(cli.genTable(header + dbCur.fetchall()))
        icd = validateInput(cli.cols+"Enter the itemCode to delete: ", None, int)
        dbCur.execute("DELETE FROM items WHERE itemCode = {}".format(icd))
        conn.commit()
        cli.log('S', "Deleted item sucessfully!")

def mainMenu(dbCur, userData):
    while True:
        options = ["User control", "Manage Customers", "Customize menu", "Daily Stock receipt",
                   "Daily Sales entry", "Exit"]
        opt = cli.inputLOV("What would you like to do?", options)
        if opt == "User control":
            if userData['name'] != 'Administrator':
                cli.log('E', "User", userData['name'], "doesn't have rights to manage users!")
            else:
                staffMan(dbCur, userData)
        elif opt == "Manage Customers":
            if userData['name'] != 'Administrator':
                cli.log('E', "User", userData['name'], "doesn't have rights to manage customers!")
            else:
                custMan(dbCur, userData)
        elif opt == "Add menu Item":
            menuMan(dbCur, userData)
        elif opt == "Daily Stock receipt":
            raise NotImplementedError
        elif opt == "Daily Sales entry":
            raise NotImplementedError
        elif opt == "Exit":
            print(cli.cols, f"Logging out user: {userData['name']}...")
            break
    
    cli.log('S', "Successfully logged out!")
    print(cli.cols, "Thank you")

if conn.is_connected():
    cur = conn.cursor()

    print(cli.colors.clear)
    cli.printBanner("Welcome to Cafeteria Management System")
    uname = input(cli.cols + "Enter Username: ")
    pswd = input(cli.cols + "Enter password: ")
    cur.execute(f"SELECT name, passwd FROM staff WHERE userId = '{uname}' AND status = 'A'")
    data = cur.fetchall()
    if data != []:
        if data[0][1] == pswd:
            userData = {"name": data[0][0], "username": uname}
            cli.log('I', 'Logon Success')
            print(cli.cols, cli.colors.bold, f"\bWelcome, {userData['name']}", cli.colors.reset)
            mainMenu(cur, userData)
        else:
            cli.log('E', "Invalid password for user:", uname)
    else:
        cli.log('E', "No such user in database:", uname)

input("Press any key to continue...")
conn.commit()
conn.close()

