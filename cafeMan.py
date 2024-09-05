# The School Cafeteria Management System
# Written by M.V.Harish Kumar - Grade 12 'A' 
# on 05-09-2024
import mysql.connector as ms
import cliElem as cli

conn = ms.connect(host="localhost", user="cafeAdmin", passwd="cafe@p$wd", db="cafeteria")

def staffMan(dbCur, userData):
    options = ["Add new user", "Edit User Details", "View Users", "Delete User"]
    opt = cli.inputLOV("How would you like to manage staffs?", options)
    if opt == "Add new user":
        print("-"*10)
        print(cli.colors.bold + "Adding new user", cli.colors.reset)
        name = input("Enter name of the user: ")
        uname = input("Enter username for user: ")
        passwd = input("Enter password for user: ")
        query = """ INSERT INTO staff
        SELECT MAX(id)+1, '{}', '{}', '{}', 1 FROM staff""".format(name, uname, passwd)
        print(query)
        dbCur.execute(query)
        conn.commit()
        cli.log('S', "Added new user sucessfully!")
    
    elif opt == "Edit User Details":
        raise NotImplementedError
    elif opt == "View Users":
        opt = cli.inputLOV("How would you like to view users?", ["All", "Search"])
        if opt == "All":
            query = "SELECT * FROM staff"
        elif opt == "Search":
            uid = input("Enter the user id: ")
            query = "SELECT * FROM staff WHERE id = {}".format(uid)
        dbCur.execute(query)
        data = dbCur.fetchall()
        if data == []:
            cli.log('I', f"No such user with id {uid} found")
        else:
            print(cli.genTable(data, ('id', 'name', 'username', 'password', 'status')))


    elif opt == "Delete User":
        raise NotImplementedError
        
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
            raise NotImplementedError
        elif opt == "Add new Item":
            raise NotImplementedError
        elif opt == "Manage Daily Stock":
            raise NotImplementedError
        elif opt == "Manage Sales":
            raise NotImplementedError
        elif opt == "Exit":
            print(f"Logging out user: {userData['name']}...")
            break
    
    cli.log('S', "Successfully logged out!")
    print("Thank you for using our application. See you soon!")

            

if conn.is_connected():
    cur = conn.cursor()

    cli.printBanner("Welcome to Cafeteria Management System")
    uname = input("Enter Username: ")
    pswd = input("Enter password: ")
    cur.execute(f"SELECT name, passwd FROM staff WHERE username = '{uname}' AND status = 1")
    data = cur.fetchall()
    if data != []:
        if data[0][1] == pswd:
            userData = {"name": data[0][0], "username": uname}
            cli.log('I', 'Logon Success')
            print(cli.colors.bold, f"Welcome, {userData['name']}", cli.colors.reset)
            mainMenu(cur, userData)
        else:
            cli.log('E', "Invalid password for user:", uname)
    else:
        cli.log('E', "No such user in database:", uname)


conn.close()


