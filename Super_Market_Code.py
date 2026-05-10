import mysql.connector
from datetime import date,datetime

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="shafi_@62(",
    database="Super_Market")

c=db.cursor()

def expiry(x):
    c.execute("select Expiry_Date from products where Product_ID=%s",(x,))
    d=c.fetchone()
    if d and d[0] is not None:
        if d[0]>date.today():
            print("Not Expired")
        elif d[0]<=date.today():
            print("Expired")
    else:
        print("No Expiry date")

def billing_system():
    p=[]
    t=0
    while True:
        while True:
            try:
                q=int(input("Enter the product ID: "))
                break
            except:
                print("Please enter a proper ID")
                continue

        while True:
            try:
                z=int(input("Enter the number of Quantity: "))
                break
            except:
                print("Please enter a proper Quantity")
                continue

        c.execute("select * from Products where Product_ID=%s",(q,))
        d=c.fetchone()
        
        if d is not None:
            if z>d[2]:
                z=d[2]
            p.append([d,z])
            print(d[0],"\t",d[1],"\t",d[3],"\t",z,"\t",end='\t')
            expiry(q)
        else:
            print("Product not available")
        while True:
            a=input("Do you want to add another Product(y,n): ").lower()
            if a!='y' and a!='n':
                print("Please enter a proper decision")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            print("\nFinal bill is:\n")
            for i,z in p:
                print(i[0],"\t",i[1],"\t",i[3],"\t",z,"\t",end='\t')
                expiry(i[0])

                t+=float(i[3]*z)

                c.execute("update products set Total_Quantity_Available=%s where Product_ID=%s",(i[2]-z,i[0]))
                db.commit()

                c.execute("select Total_Quantity_Available from Products where Product_ID=%s",(i[0],))
                w=c.fetchone()
                if w[0]==0:
                    c.execute("delete from Products where Product_ID=%s",(i[0],))
                    db.commit()

            print("\nTotal Price:",t)
            p.clear()
            t=0
            break

def add_product():
    while True:
        n=input("Enter the Product name: ")
        while True:
            try:
                t=int(input("Enter the total quantity of the Product: "))
                break
            except:
                print("Please enter the proper quantity")
        while True:
            try:
                p=float(input("Enter the Individual Product price: "))
                break
            except:
                print("Please enter a proper price value")
        while True:
            try:
                e=input("Enter the Expiry date of the Product(YYYY-MM-DD): ")
                if e=="":
                    e=None
                    break
                e=datetime.strptime(e,"%Y-%m-%d").date()
                break
            except:
                print("Invalid Date Format")
                continue
        c.execute("insert into Products(Product_Name, Total_Quantity_Available, Individual_Product_Price, Expiry_Date) values(%s,%s,%s,%s)",(n,t,p,e))
        db.commit()
        while True:
            a=input("Do you have to add another Product(y,n): ").lower()
            if a!='y' and a!='n':
                print("Please enter a proper decision")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            break

def remove_product():
    while True:
        r=input("Enter the product name or ID to be removed: ")
        if r.isdigit():
            c.execute("delete from Products where Product_ID=%s",(r,))
            print("Product with ID",r,"is succesfully removed")
        else:
            c.execute("delete from Products where Product_Name=%s",(r,))
            print("Product with Name",r,"is succesfully removed")
        db.commit()
        while True:
            a=input("Do you want to remove another Product(y,n): ").lower()
            if a!='y' and a!='n':
                print("Please enter a proper decision")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            break  

def search_product():
    s=input("Enter the product name or ID to search for it: ")
    if s.isdigit():
        c.execute("select * from Products where Product_ID=%s",(s,))
    else:
        c.execute("select * from Products where Product_Name=%s",(s,))
    d=c.fetchone()
    if d is not None:
        print(d[0],"\t",d[1],"\t",d[2],"\t",d[3],"\t",d[4])
    else:
        print("Product not available")

def expiry_checker():
    c.execute("select * from products where Expiry_Date<=curdate()")
    d=c.fetchall()
    if d:
        for i in d:
            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4],"\t", "Expired")
    else:
        print("No Expired Products")

def view_products():
    c.execute("select * from products")
    d=c.fetchall()
    if d:
        for i in d:
            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4])
    else:
        print("No Products")
