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
        print("-"*10)
        print(cli.colors.bold + "Adding new user", cli.colors.reset)
        name = input("Enter name of the user: ")
        uname = input("Enter username for user: ")
        passwd = input("Enter password for user: ")
        dbCur.execute("SELECT MAX(id)+1 FROM staff")
        query = "INSERT INTO staff VALUES ({}, '{}', '{}', '{}', 1)" \
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
            uid = validateInput("Enter the user id to edit: ", None, int)
            dbCur.execute("SELECT * FROM staff WHERE id = {}".format(uid))
            data = dbCur.fetchone()
            if data is not None:
                break
            cli.log('E', 'No user for given id:', uid)
        name = input("Enter name[Default: {}]: ".format(data[1]))
        if not name:
            name = data[1]
        uname = input("Enter username[Default: {}]: ".format(data[2]))
        if not uname:
            uname = data[2]
        passwd = input("Enter password[Default: {}]: ".format(data[3]))
        if not passwd:
            passwd = data[3]
        sts = validateInput("Enter Status[Default: {}]: ".format(bool(data[3])), None, bool)
        if not sts:
            sts = str(bool(data[4]))
        query = "UPDATE staff SET name='{}',username='{}',passwd='{}',status={} WHERE id = {}" \
                .format(name, uname, passwd, int(sts == "True"), uid)
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Updated user sucessfully!")

    elif opt == "View users":
        opt = cli.inputLOV("How would you like to view users?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM staff"
        elif opt == "Search":
            uid = validateInput("Enter the user id: ", None, int)
            query = "SELECT * FROM staff WHERE id = {}".format(uid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            cli.log('I', f"No such user with id {uid} found")
        else:
            print(cli.genTable(header + data))

    elif opt == "Delete user":
        print("-"*10)
        print(cli.colors.bold + "Deleting user", cli.colors.reset)
        query = "SELECT * FROM staff"
        dbCur.execute(query)
        print(cli.genTable(header + dbCur.fetchall()))
        uid = validateInput("Enter the user id to delete: ", None, int)
        dbCur.execute("DELETE FROM staff WHERE id = {}".format(uid))
        conn.commit()
        cli.log('S', "Deleted user sucessfully!")

def custMan(dbCur, userData):
    options = ["Add new customer", "Edit customer details", "View customers", "Delete customer"]
    header = [('custId', 'name', 'type', 'status')] 
    kindSwitch = {'S': 'Student', 'T': 'Staff'}
    opt = cli.inputLOV("How would you like to manage customers?", options)

    if opt == "Add new customer":
        print("-"*10)
        print(cli.colors.bold + "Adding new customer", cli.colors.reset)
        name = input("Enter name of the customer: ")
        ckind = validateInput("Enter customer kind[(S)tudent/s(T)aff]: ", "ST")
        dbCur.execute("SELECT MAX(custId)+1 FROM customer")
        query = "INSERT INTO customer VALUES ({}, '{}', '{}', 1)" \
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
            cid = validateInput("Enter the custId to edit: ", None, int)
            dbCur.execute("SELECT * FROM customer WHERE custId = {}".format(cid))
            data = dbCur.fetchone()
            if data is not None:
                break
            cli.log('E', 'No customer for given id:', cid)
        custId = validateInput("Enter custId[Default: {}]: ".format(data[0]), None, int)
        if not custId:
            custId = data[0]
        name = input("Enter name[Default: {}]: ".format(data[1]))
        if not name:
            name = data[1]
        ckind = validateInput("Enter customer kind[(S)tudent/s(T)aff][Default: {}]: ".format(data[2]), "TS")
        ckind = kindSwitch.get(ckind, data[2])
        sts = validateInput("Enter Status[Default: {}]: ".format(bool(data[3])), None, bool)
        print(repr(sts))
        if not sts:
            sts = str(bool(data[3]))
        print(repr(sts))
        query = "UPDATE customer SET custId={},name='{}',custType='{}',status={} WHERE custId = {}" \
                .format(custId, name, ckind, int(sts == 'True'), cid)
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Updated customer sucessfully!")

    elif opt == "View customers":
        opt = cli.inputLOV("How would you like to view customers?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM customer"
        elif opt == "Search":
            cid = validateInput("Enter the custId: ", None, int)
            query = "SELECT * FROM customer WHERE custId = {}".format(cid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            cli.log('I', f"No such customer with code {cid} found")
        else:
            print(cli.genTable(header + data))

    elif opt == "Delete customer":
        print("-"*10)
        print(cli.colors.bold + "Deleting customer", cli.colors.reset)
        query = "SELECT * FROM customer"
        dbCur.execute(query)
        print(cli.genTable(header + dbCur.fetchall()))
        cid = validateInput("Enter the custId to delete: ", None, int)
        dbCur.execute("DELETE FROM customer WHERE custId = {}".format(cid))
        conn.commit()
        cli.log('S', "Deleted user sucessfully!")
       
def mainMenu(dbCur, userData):
    while True:
        options = ["Manage Staffs", "Manage Customers", "Add new Item", "Manage Daily Stock",
                   "Manage Sales", "Exit"]
        opt = cli.inputLOV("What would you like to do?", options)
        if opt == "Manage Staffs":
            if userData['name'] != 'Administrator':
                cli.log('E', "User", userData['name'], "doesn't have rights to manage users!")
            else:
                staffMan(dbCur, userData)
        elif opt == "Manage Customers":
            if userData['name'] != 'Administrator':
                cli.log('E', "User", userData['name'], "doesn't have rights to manage users!")
            else:
                custMan(dbCur, userData)
        elif opt == "Add new Item":
            raise NotImplementedError
        elif opt == "Manage Daily Stock":
            raise NotImplementedError
        elif opt == "Manage Sales":
            raise NotImplementedError
        elif opt == "Exit":
            print(cli.cols, f"Logging out user: {userData['name']}...")
            break
    
    cli.log('S', "Successfully logged out!")
    print(cli.cols, "Thank you for using our application. See you soon!")

if conn.is_connected():
    cur = conn.cursor()

    print(cli.colors.clear)
    cli.printBanner("Welcome to Cafeteria Management System")
    uname = input(cli.cols + "Enter Username: ")
    pswd = input(cli.cols + "Enter password: ")
    cur.execute(f"SELECT name, passwd FROM staff WHERE username = '{uname}' AND status = 1")
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

