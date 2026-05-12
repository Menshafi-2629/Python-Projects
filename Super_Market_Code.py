import mysql.connector
from datetime import date,datetime

while True:
    try:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="shafi_@62(",
            database="Super_Market")

        c=db.cursor()
        break
    except:
        print("Unable to to connect database")
        while True:
            try:
                a=input("Do you want to try again('y','n'): ")
                break
            except:
                print("Please enter 'y' or 'n'")
        if a=='n':
            exit()
            break

print("SUPER MARKET APPLICATION\n")

def expiry(x):
    c.execute("select Expiry_Date from products where Product_ID=%s",(x,))
    d=c.fetchone()
    if d and d[0] is not None:
        if d[0]>date.today():
            print("Not expired")
        elif d[0]<=date.today():
            print("Expired")
    else:
        print("No expiry date")

def add_to_list(d,z,q,p):
    if d[2] == 0:
        print("\nProduct out of stock")
    elif z>d[2]:
        print("\nOnly", d[2], "items available")
        z=d[2]
        p.append([d,z])
        print("\n",d[0],"\t",d[1],"\t",d[3],z,end='\t')
        expiry(q)
    else:
        p.append([d,z])
        print("\n",d[0],"\t",d[1],"\t",d[3],z,end='\t')
        expiry(q)

def billing_system():
    p=[]
    t=0
    while True:
        while True:
            try:
                q=int(input("\nEnter the product ID: "))
                break
            except:
                print("Please enter a proper ID")
                continue
 
        while True:
            try:
                z=int(input("Enter the quantity: "))
                break
            except:
                print("Please enter a proper quantity\n")
                continue

        c.execute("select * from Products where Product_ID=%s",(q,))
        d=c.fetchone()
        if d is not None:
            if d[0] in (i[0][0] for i in p):
                print("Product already added to the list")
                while True:
                    while True:
                        try:
                            a=input("\nDo you want to increase the quantity of this product(y,n): ").lower()
                            break
                        except:
                            print("Please enter 'y' or 'n'")
                    if a!='y' and a!='n':
                        print("Please enter 'y' or 'n'")
                        continue
                    else:
                        break
                if a=='y':
                    for k in p:
                        if k[0][0] == d[0]:
                            if k[1]+z >d[2]:
                                print("\nOnly", d[2], "items available")
                                k[1]=d[2]
                            else:
                                k[1] += z
                            break
            else:
                add_to_list(d,z,q,p)
        else:
            print("\nProduct not available")
        while True:
            while True:
                try:
                    a=input("\n\nDo you want to add another product(y,n): ").lower()
                    break
                except:
                    print("Please enter 'y' or 'n'")
            if a!='y' and a!='n':
                print("Please enter 'y' or 'n'")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            print("\nFinal bill is:\n")
            for i,z in p:
                print(i[0],"\t",i[1],"\t",i[3],z,end='\t')
                expiry(i[0])

                t+=i[3]*z
                current_quantity = i[2] - z
                c.execute("update Products set Total_Quantity_Available=%s where Product_ID=%s",(current_quantity, i[0]))
                db.commit()
            print("\nTotal Price:",t)
            p.clear()
            t=0
            print("\n")
            break

def add_product():
    while True:
        while True:
            try:
                n=input("\nEnter the product name: ").title()
                break
            except:
                print("Please enter a proper name")
        c.execute("select * from Products where Product_Name=%s",(n,))
        d=c.fetchone()
        if d is not None:
            print("Product already available\n")
            while True:
                while True:
                    try:
                        f=input("Do you want to increase the product's quantity instead('y','n'): ")
                        break
                    except:
                        print("Please enter 'y' or 'n'")
                        continue
                if f!='y' and f!='n':
                    print("Please enter 'y' or 'n'\n")
                    continue
                else:
                    break
            if f=='y':
                while True:
                    try:
                        t=int(input("\nEnter the total quantity: ")).title()
                        break
                    except:
                        print("Please enter a proper quantity")
                c.execute("update products set Total_Quantity_Available=%s where Product_Name=%s",(d[2]+t,n))
                db.commit()
                print("\nProduct's Quantity has be successfully Increased\n")
            else:
                print("\n")
        else:
            while True:
                try:
                    t=int(input("Enter the total quantity: "))
                    break
                except:
                    print("Please enter a proper quantity\n")
            while True:
                try:
                    p=float(input("Enter the individual product price: "))
                    break
                except:
                    print("Please enter a proper price value\n")
            while True:
                try:
                    e=input("Enter the expiry date of the product(YYYY-MM-DD): ")
                    if e=="":
                        e=None
                        break
                    e=datetime.strptime(e,"%Y-%m-%d").date()
                    break
                except:
                    print("Invalid date format\n")
                    continue
            c.execute("insert into Products(Product_Name, Total_Quantity_Available, Individual_Product_Price, Expiry_Date) values(%s,%s,%s,%s)",(n,t,p,e))
            db.commit()
            print("\nProduct",n,"successfully added to the database of the Super Market\n\n")
        while True:
            while True:
                try:
                    a=input("Do you want to add another product(y,n): ").lower()
                    break
                except:
                    print("Please enter 'y' or 'n'")
            if a!='y' and a!='n':
                print("Please enter 'y' or 'n'\n")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            print("\n")
            break

def remove_product():
    while True:
        while True:
            try:
                r=input("Enter the product name or ID to be removed: ").title()
                break
            except:
                print("Please enter a proper ID or name")
        if r.isdigit():
            c.execute("select * from Products where Product_ID=%s",(r,))
            d=c.fetchone()
            if d:
                c.execute("delete from Products where Product_ID=%s",(r,))
                print("\nProduct with ID",r,"is successfully removed from the database of the Super Market\n\n")
            else:
                print("Product not available\n")
        else:
            c.execute("select * from Products where Product_Name=%s",(r,))
            d=c.fetchone()
            if d:
                c.execute("delete from Products where Product_Name=%s",(r,))
                print("\nProduct with name",r,"is successfully removed from the database of the Super Market\n\n")
            else:
                print("Product not available\n")
        db.commit()
        while True:
            while True:
                try:
                    a=input("Do you want to remove another product(y,n): ").lower()
                    break
                except:
                    print("Please enter 'y' or 'n'")
            if a!='y' and a!='n':
                print("Please enter 'y' or 'n'\n")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            break  

def search_product():
    while True:
        try:
            s=input("\nEnter the product name or ID to search for it: ").title()
            break
        except:
            print("Please enter a proper ID or name")
    if s.isdigit():
        c.execute("select * from Products where Product_ID=%s",(s,))
    else:
        c.execute("select * from Products where Product_Name=%s",(s,))
    d=c.fetchone()
    if d is not None:
        print("\n",d[0],"\t",d[1],"\t",d[2],"\t",d[3],"\t",d[4])
        print("\n")
    else:
        print("Product not available\n")

def expiry_checker():
    c.execute("select * from products where Expiry_Date<=curdate()")
    d=c.fetchall()
    if d:
        print("\n")
        for i in d:
            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4],"\t", "Expired")
        print("\n")
    else:
        print("\nNo expired products\n")

def view_products():
    c.execute("select * from products")
    d=c.fetchall()
    if d:
        print("\n")
        for i in d:
            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4],)
        print("\n")
    else:
        print("\nNo products\n")

def product_data_update():
    while True:
        while True:
            try:
                v=input("\nEnter the product ID or name to be updated in the database of the Super Market: ").title()
                break
            except:
                print("Please enter a proper ID or name")
        if v.isdigit():
            c.execute("select * from Products where Product_ID=%s",(v,))
        else:
            c.execute("select * from Products where Product_Name=%s",(v,))
        d=c.fetchone()
        if d is not None:
            print("\n1= Total quantity available")
            print("2= Individual product price")
            print("3= Expiry date\n")
            while True:
                try:
                    p=int(input("Enter the integer of the data need to be updated for the product in the database of the Super Market: "))
                    break
                except:
                    print("Please enter the proper integer\n")
                    continue
            if p==1:
                while True:
                    try:
                        q=int(input("\nEnter the quantity to be be updated: "))
                        break
                    except:
                        print("Please enter a proper quantity")
                c.execute("update products set Total_Quantity_Available=%s where Product_ID=%s",(q,d[0]))
                print("\nQuantity of the product",d[1],"has been successfully updated")
            elif p==2:
                while True:
                    try:
                        q=float(input("\nEnter the price to be be updated: "))
                        break
                    except:
                        print("Please enter a proper price value")
                c.execute("update products set Individual_Product_Price=%s where Product_ID=%s",(q,d[0]))
                print("\nIndividual product price of the product",d[1],"has been successfully updated")
            elif p==3:
                while True:
                    try:
                        q=input("\nEnter the expiry date of the product(YYYY-MM-DD): ")
                        if q=="":
                            q=None
                            break
                        q=datetime.strptime(q,"%Y-%m-%d").date()
                        break
                    except:
                        print("Invalid date format\n")
                        continue
                c.execute("update products set Expiry_Date=%s where Product_ID=%s",(q,d[0]))
                print("\nExpiry date of the product",d[1],"has been successfully updated")
            db.commit()
        else:
            print("Product not available\n")
        while True:
            while True:
                try:
                    a=input("\nDo you want to update another product(y,n): ").lower()
                    break
                except:
                    print("Please enter 'y' or 'n'\n")
            if a!='y' and a!='n':
                print("Please enter 'y' or 'n'\n")
                continue
            else:
                break
        if a=='y':
            continue
        else:
            print("\n")
            break

k=range(1,9)

while True:
    print("1= Billing")
    print("2= Add products")
    print("3= Remove product")
    print("4= Search products")
    print("5= Show expired products")
    print("6= Show all available products")
    print("7= Update product data")
    print("8= Exit Super Market\n")
    try:
        l=int(input("Which Super Market operation do you want to perform(Enter the integer): "))
    except:
        print("Please enter the proper integer\n")
        continue
    if l not in k:
        print("Please enter the integer from the given data\n")
        continue
    if l==1:
        billing_system()
    elif l==2:
        add_product()
    elif l==3:
        remove_product()
    elif l==4:
        search_product()
    elif l==5:
        expiry_checker()
    elif l==6:
        view_products()
    elif l==7:
        product_data_update()
    elif l==8:
        print("\nThank you for using the Super Market Application")
        break
c.close()
db.close()
