from tkinter import *
import pymysql
from tkinter import messagebox,filedialog
from tkinter import ttk
from datetime import datetime
taz=Tk()

width=taz.winfo_screenwidth()
#print(width)
height=taz.winfo_screenheight()
#print(height)

###### database connection #######


tazTV=ttk.Treeview(height=10,columns=('Item Name''Rate','mkType'))
tazTV1=ttk.Treeview(height=10,columns=('Date''Name','Type','Rate','Total'))
####### for char input

###def only_char_input(p):
   # if p.isalpha() or p=='':
        #return True
    #return False
#callback=taz.register(only_char_input)
## for digit
#def only_numeric_input(p):
    #if p.isdigit() or p=='':
        #return True
   # return False
#callback2=taz.register(only_numeric_input)#



def dbconfig():
    global conn, mycursor
    conn=pymysql.connect(host="localhost",user="root",db="myhotel")
    mycursor=conn.cursor()
######## clear screen ########
def clear_screen():
    global taz
    for widgets in taz.winfo_children():
        widgets.grid_remove()
######## logout #######
def logout():
    clear_screen()
    mainheading()
    loginwindow()

def mainheading():
    label = Label(taz, text="Restaurant Management System", fg="yellow", bg="purple", font=("comic sans Ms", 40, "bold"),
                  padx=270, pady=0)

    label.grid(row=0, columnspan=4)
usernameVar=StringVar()
passwordVar=StringVar()

def adminLogin():
    dbconfig()
    username=usernameVar.get()
    password=passwordVar.get()
    que="select * from user_info where user_id=%s and user_Pass=%s"
    val=(username,password)
    mycursor.execute(que,val)
    data=mycursor.fetchall()
    flag=False
    for row in data:
        flag=True
    conn.close()

    if flag==True:
        welcomewindow()
    else:
        messagebox.showerror("invalid user credential","either user name or password is incorrect ")
        usernameVar.set("")
        passwordVar.set("")



def loginwindow():
    usernameVar.set("")
    passwordVar.set("")

    labellogin=Label(taz, text="Admin Login",  font=("ariel", 25, "bold"))
    labellogin.grid(row=1,column=1,columnspan=2,padx=50,pady=10)
    usernamelabel=Label(taz,text="User Name",font=("ariel", 12, "bold"))
    usernamelabel.grid(row=2,column=1,padx=20,pady=5)
    passwordlabel = Label(taz, text="User password",font=("ariel", 12, "bold"))
    passwordlabel.grid(row=3, column=1, padx=20, pady=5)
    usernameEntry=Entry(taz,textvariable=usernameVar)
    usernameEntry.grid(row=2,column=2,padx=20,pady=5)
    passwordEntry=Entry(taz,show="*",textvariable=passwordVar)
    passwordEntry.grid(row=3,column=2,padx=20,pady=5)
    loginButton=Button(taz,text="login",width=20,height=2,fg="green",bg="pink",bd=10,command=adminLogin)
    loginButton.grid(row=4, column=1,columnspan=2, padx=20, pady=5)
def welcomewindow():
    clear_screen()
    mainheading()
    welcome =Label(taz, text=" welcome Admin ",  font=("ariel", 25, "bold"))
    welcome.grid(row=1,column=1,columnspan=2,padx=50,pady=10)
    logoutButton = Button(taz, text="logout", width=20, height=2, fg="green",bg="pink", bd=10, command=logout)
    logoutButton.grid(row=4, column=1, columnspan=2, padx=20, pady=5)


    manageRest=Button(taz,text="Manage Restaurant", width=20,height=2,fg="green",bg="pink",bd=10,command=addItemWindow)
    manageRest.grid(row=5,column=1,columnspan=2,padx=20,pady=5)

    billGen = Button(taz, text="Bill Generation", width=20, height=2, fg="red",bg="yellow", bd=10, command=billWindow)
    billGen.grid(row=6, column=1, columnspan=2, padx=20, pady=5)





###### back button ######

def back():
    clear_screen()
    mainheading()
    welcomewindow()

def additemprocess():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    query="insert into itemlist(item_name,item_rate,item_type)values(%s,%s,%s)"
    val=(name,rate,type)
    mycursor.execute(query,val)
    conn.commit()
    messagebox.showinfo("save item","item saved successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemrateVar.set("")
    getItemInTreeview()




###########
def  getItemInTreeview():
    # to delete alredy inserted  data
    records=tazTV.get_children()
    for x in records:
        tazTV.delete(x)

    conn=pymysql.connect(host="localhost",user="root",db="myhotel")
    mycursor=conn.cursor(pymysql.cursors.DictCursor)
    query1="select * from itemlist"
    mycursor.execute(query1)
    data=mycursor.fetchall()
    #print(data)
    for row in data:
        tazTV.insert('','end',text=row['item_name'],values=(row["item_rate"],row['item_type']))
    conn.close()
    tazTV.bind("<Double-1>",OnDoubleClick)
###### double click #####
def OnDoubleClick(event):
    item=tazTV.selection()
    itemnameVar1=tazTV.item(item,"text")
    item_detail =tazTV.item(item,"values")
    itemnameVar.set(itemnameVar1)
    itemrateVar.set(item_detail[0])
    itemtypeVar.set(item_detail[1])



#########

######## update item ######
def updateItem():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    que="update itemlist set item_rate=%s,item_type=%s where item_name=%s"
    val=(rate,type,name)
    mycursor.execute(que,val)
    conn.commit()
    messagebox.showinfo("Updation confirmation","Item updated Successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemtypeVar.set("")
    getItemInTreeview()
########## Delete item ########

def deleteItem():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    que1="delete from itemlist where item_name=%s"
    val=(name)
    mycursor.execute(que1,val)
    conn.commit()
    messagebox.showinfo("delete confirmation","Item deleted Successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemtypeVar.set("")
    getItemInTreeview()
########## bill window #########
global x
x=datetime.now()

datetimeVar=StringVar()
datetimeVar.set(x)
customerNameVar=StringVar()
mobileVar=StringVar()
combovaraiable=StringVar()
baserate=StringVar()
cost=StringVar()
qtyvariable=StringVar()

################# combo data #333333
def combo_input():
    dbconfig()
    mycursor.execute('select item_name from itemlist')
    data=[]
    for row in mycursor.fetchall():
        data.append(row[0])
    return data
###### optionalCallBack ####
def optionCallBack(*args):
    global itemname
    itemname=combovaraiable.get()
    #print(itemname)
    aa=ratelist()
    #print(aa)
    baserate.set(aa) #TODO : Fix Rate
    global v
    for i in aa:
        for j in i:
            v=j
            # baserate.set(v)
            # break
###### optionCallBack2 ######
def optionCallBack2(*args):
    global qty
    qty=qtyvariable.get()
    final=int(v)*int(qty)
    cost.set(final)


######### ratelist():
def ratelist():
    dbconfig()
    que2="select item_rate from itemlist where item_name=%s"
    val=(itemname)
    mycursor.execute(que2,val)
    data=mycursor.fetchall()
    print(data)
    return data

def billWindow():
    clear_screen()
    mainheading()
    billitem = Label(taz, text="Generate Bill ", font=("ariel", 25, "bold"))
    billitem.grid(row=1, column=1, columnspan=2, padx=50, pady=10)
    logoutButton = Button(taz, text="logout", width=20, height=2, fg="green",bg="pink", bd=10, command=logout)
    logoutButton.grid(row=3, column=0, columnspan=1)

    backButton = Button(taz, text="Back", width=20, height=2, fg="green",bg="pink", bd=10, command=back)
    backButton.grid(row=4, column=0, columnspan=1)

    printButton = Button(taz, text="print Bill", width=20, height=2, fg="green",bg="pink", bd=10, command=printBill)
    printButton.grid(row=5, column=0, columnspan=1)


    dateTimeLabel=Label(taz,text="date & Time",font=("ariel",15,"bold"))
    dateTimeLabel.grid(row=2,column=1,padx=20,pady=5)

    dateTimeEntry=Entry(taz,textvariable=datetimeVar,font=("ariel",15,"bold"))
    dateTimeEntry.grid(row=2,column=2,padx=20,pady=5)

    customerNameLabel = Label(taz, text="Customer Name / Table No.", font=("ariel", 15, "bold"))
    customerNameLabel.grid(row=3, column=1, padx=20, pady=5)

    customerNameEntry = Entry(taz, textvariable=customerNameVar, font=("ariel", 15, "bold"))
    customerNameEntry.grid(row=3, column=2, padx=20, pady=5)

    mobileLabel = Label(taz, text="Contact no", font=("ariel", 15, "bold"))
    mobileLabel.grid(row=4, column=1, padx=20, pady=5)

    mobileEntry = Entry(taz, textvariable=mobileVar, font=("ariel", 15, "bold"))
    mobileEntry.grid(row=4, column=2, padx=20, pady=5)

    selectLabel = Label(taz, text="Select item", font=("ariel", 15, "bold"))
    selectLabel.grid(row=5, column=1, padx=20, pady=5)

    l=combo_input()
    c=ttk.Combobox(taz,values=l,textvariable=combovaraiable, font=("ariel", 15, "bold"))
    c.set("select item")
    combovaraiable.trace('w',optionCallBack)
    c.grid(row=5,column=2,padx=20,pady=5)

    rateLabel = Label(taz, text="Item Rate", font=("ariel", 15, "bold"))
    rateLabel.grid(row=6, column=1, padx=20, pady=5)

    rateEntry = Entry(taz, textvariable=baserate, font=("ariel", 15, "bold"))
    rateEntry.grid(row=6, column=2, padx=20, pady=5)

    qtyLabel = Label(taz, text="Select Quantity", font=("ariel", 15, "bold"))
    qtyLabel.grid(row=7, column=1, padx=20, pady=5)

    global qtyvariable
    l2=[1,2,3,4,5,6,7,8,9,10]
    qty = ttk.Combobox(taz, values=l2, textvariable=qtyvariable, font=("ariel", 15, "bold"))
    qty.set("select Quantity")
    qtyvariable.trace('w', optionCallBack2)
    qty.grid(row=7, column=2, padx=20, pady=5)

    costLabel = Label(taz, text="Cost", font=("ariel", 15, "bold"))
    costLabel.grid(row=8, column=1, padx=20, pady=5)

    costEntry = Entry(taz, textvariable=cost, font=("ariel", 15, "bold"))
    costEntry.grid(row=8, column=2, padx=20, pady=5)

    billButton=Button(taz,text="Save Bill",width=20,height=2,bd=10,fg="red",bg="yellow",command=saveBill)

    billButton.grid(row=9,column=2,padx=20,pady=5)
######### save bill ##########

def saveBill():
    dt=datetimeVar.get()
    custname=customerNameVar.get()
    mobile=mobileVar.get()
    item_name=itemname
    itemrate=v
    itemqty=qtyvariable.get()
    total=cost.get()
    print(dt,custname)
    dbconfig()
    insqu="insert into bill(datetime,customer_name,contact_no,item_name,item_rate,item_qty,cost) values(%s,%s,%s,%s,%s,%s,%s)"
    val=(dt,custname,mobile,item_name,itemrate,itemqty,total)
    mycursor.execute(insqu,val)
    conn.commit()
    messagebox.showinfo("Save Data","Bill Saved successfully")
    customerNameVar.set("")
    mobileVar.set("")
    itemnameVar.set("")
    cost.set("")

######printBill#######
def printBill():
    clear_screen()
    mainheading()
    printitem=Label(taz,text="Bill Details",font=("ariel",25,"bold"))
    printitem.grid(row=1,column=1,columnspan=2,padx=50,pady=10)

    logoutButton = Button(taz, text="logout", width=20, height=2, fg="green",bg="pink", bd=10, command=logout)
    logoutButton.grid(row=1, column=0, columnspan=1)


    backButton = Button(taz, text="Back", width=20, height=2, fg="green",bg="pink", bd=10, command=back)
    backButton.grid(row=1, column=3, columnspan=1)

    clickitem = Button(taz, text="Double Click to TreeView To Print Bill", font=("ariel", 25, "bold"))
    clickitem.grid(row=2, column=1, columnspan=23, padx=50, pady=10)

    # treeview
    tazTV1.grid(row=5, column=0, columnspan=4)
    style = ttk.Style(taz)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="green")
    scrollBar = Scrollbar(taz, orient="vertical", command=tazTV1.yview)
    scrollBar.grid(row=5, column=5, sticky="NSE")

    tazTV1.configure(yscrollcommand=scrollBar.set)
    tazTV1.heading('#0', text="Date/Time")
    tazTV1.heading('#1', text="Name")
    tazTV1.heading('#2', text="mobile")
    tazTV1.heading('#3', text="Selected Food")
    tazTV1.heading('#4', text="Total Cost")
    displaybill()

    #getItemInTreeview()
##################################
######### display bill ############
def displaybill():
    # to delete alredy inserted  data
    records = tazTV1.get_children()
    for x in records:
        tazTV1.delete(x)

    conn = pymysql.connect(host="localhost", user="root", db="myhotel")
    mycursor = conn.cursor(pymysql.cursors.DictCursor)
    query1 = "select * from bill"
    mycursor.execute(query1)
    data = mycursor.fetchall()
    # print(data)
    for row in data:
        tazTV1.insert('', 'end', text=row['datetime'], values=(row["customer_name"], row['contact_no'],row['item_name'],row['cost']))
    conn.close()
    tazTV1.bind("<Double-1>", OnDoubleClick2)

############## OnDoubleClick2 ########333
def  OnDoubleClick2(event):
    item = tazTV1.selection()
    global itemNameVar11
    itemNameVar11 = tazTV1.item(item, "text")
    item_detail1 = tazTV1.item(item, "values")
    receipt()




###################################


############ receipt() ########
def  receipt():
    billstring=""
    billstring+="===================MY Restaurant BILL=====================\n\n"
    billstring += "===================CUSTOMER DETAILS=====================\n\n"

    dbconfig()
    query="select * from bill where datetime='{}';".format(itemNameVar11)
    mycursor.execute(query)
    data=mycursor.fetchall()
    print(data)
    for row in data:
        billstring+="{}{:<20}{:<10}\n".format("Date/Time","",row[1])
        billstring += "{}{:<20}{:<10}\n".format("Customer Name / Table No.", "", row[2])
        billstring += "{}{:<20}{:<10}\n".format("Contact No", "", row[3])
        billstring += "\n================= Item Details=======================\n"
        billstring +="{:<10}{:<10}{:<15}{:<15}".format("Item Name","Rate","Quantity","Total Cost")
        billstring+="\n{:<10}{:<10}{:<25}{:<25}".format(row[4],row[5],row[6],row[7],)
        billstring+="===============================================================\n"
        billstring+="{}{:<10}{:<15}{:<10}\n".format("Total Cost"," "," ",row[7])
        billstring+="\n\n ======================== Thanks Please Visit Again============\n"

    bilFile=filedialog.asksaveasfile(mode="w",defaultextension=".txt")
    if bilFile is None:
        messagebox.showerror("File Name Error","Invalid File Name")
    else:
        bilFile.write(billstring)
        bilFile.close()


itemnameVar = StringVar()
itemrateVar = StringVar()
itemtypeVar = StringVar()


def addItemWindow():
    clear_screen()
    mainheading()

    itemnameLabel = Label(taz, text="Item Name", font=("ariel", 20, "bold"))
    itemnameLabel.grid(row=2, column=1, padx=20, pady=5)

    itemrateLabel = Label(taz, text="Item Rate (INR)", font=("ariel", 20, "bold"))
    itemrateLabel.grid(row=3, column=1, padx=20, pady=5)

    itemtypeLabel = Label(taz, text="Item Type", font=("ariel", 20, "bold"))
    itemtypeLabel.grid(row=4, column=1, padx=20, pady=5)

    itemnameEntry = Entry(taz, textvariable=itemnameVar)
    itemnameEntry.grid(row=2, column=2, padx=20, pady=5)
    # for validation
    # itemnameEntry.configure(validate="key",validatecommand=(callback,"%p"))
    itemrateEntry = Entry(taz, textvariable=itemrateVar)
    itemrateEntry.grid(row=3, column=2, padx=20, pady=5)
    # itemrateEntry.configure(validate="key", validatecommand=(callback2, "%p"))

    itemtypeEntry = Entry(taz, textvariable=itemtypeVar)
    itemtypeEntry.grid(row=4,column=2,padx=20,pady=5)

    additemButton = Button(taz, text="Add Item", width=20, height=2, fg="green",bg="pink", bd=10, command=additemprocess)
    additemButton.grid(row=3, column=3, columnspan=1)

    updateButton = Button(taz, text="UPDATE Item", width=20, height=2, fg="green",bg="pink", bd=10, command=updateItem)
    updateButton.grid(row=4, column=3, columnspan=1)

    deleteButton = Button(taz, text="DELETE Item", width=20, height=2, fg="green",bg="pink", bd=10, command=deleteItem)
    deleteButton.grid(row=5, column=3, columnspan=1)

    logoutButton = Button(taz, text="logout", width=20, height=2, fg="green",bg="pink", bd=10, command=logout)
    logoutButton.grid(row=3, column=0, columnspan=1)
    backButton = Button(taz, text="Back", width=20, height=2, fg="green",bg="pink", bd=10, command=back)
    backButton.grid(row=4, column=0, columnspan=1)

    # treeview
    tazTV.grid(row=5, column=0, columnspan=4)
    style = ttk.Style(taz)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="green")
    scrollBar = Scrollbar(taz, orient="vertical", command=tazTV.yview)
    scrollBar.grid(row=5, column=5, sticky="NSE")

    tazTV.configure(yscrollcommand=scrollBar.set)
    tazTV.heading('#0', text="Item Name")
    tazTV.heading('#1', text="Rate")
    tazTV.heading('#2', text="Type")

    getItemInTreeview()




def additem():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemtypeVar.get()
    dbconfig()
    query="insert into itemlist(item_name,item_rate,item_type)values(%s,%s,%s)"
    val=(name,rate,type)
    mycursor.execute(query,val)
    conn.commit()
    messagebox.showinfo("save item","item saved successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemrateVar.set("")














mainheading()

loginwindow()
taz.title("Restaurant Management System")
taz.geometry("%dx%d+0+0"%(width,height))

taz.mainloop()




