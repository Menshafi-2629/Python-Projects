import mysql.connector
from datetime import date,datetime

while True:
    try:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Super_Market")

        c=db.cursor()
        break
    except:
        print("Unable to connect database")
        while True:
            try:
                a=input("Do you want to try again('y','n'): ").lower()
            except:
                print("Please enter 'y' or 'n'\n")
                continue
            if a!='y' and a!='n':
                print("Please enter 'y' or 'n'\n")
                continue
            else:
                break
        if a=='n':
            exit()
        else:
            print("\n")

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
        print(f"{'ID':>5} | {'Name':<13} | {'Price':>11} | {'Quantity':>8} | {'E.C':<13}")
        print("="*63)
        print(f"{d[0]:>5} | {d[1]:<13} | {d[3]:>11} | {z:>8} | ",end='')
        expiry(q)
    else:
        p.append([d,z])
        print(f"{'ID':>5} | {'Name':<13} | {'Price':>11} | {'Quantity':>8} | {'E.C':<13}")
        print("="*63)
        print(f"{d[0]:>5} | {d[1]:<13} | {d[3]:>11} | {z:>8} | ",end='')
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
            except:
                print("Please enter a proper quantity\n")
                continue
            if z<=0:
                print("Quantity must be greater than 0")
                continue
            else:
                break

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
                                print("\nOnly", d[2]-k[1], "more items available")
                                k[1]=d[2]
                            else:
                                k[1] += z
                            break
                else:
                    print("Quantity not updated")
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
            print(f"{'ID':>5} | {'Name':<13} | {'Price':>12} | {'Quantity':>8} | {'E.C':<13}")
            print("="*64)
            for i,z in p:
                print(f"{i[0]:>5} | {i[1]:<13} | {i[3]:>12} | {z:>8} | ",end='')
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
                n=input("\nEnter the product name: ").strip().title()
            except:
                print("Please enter a proper name")
                continue
            if n=="":
                print("Product name cannot be empty")
                continue
            else:
                break
        c.execute("select * from Products where Product_Name=%s",(n,))
        d=c.fetchone()
        if d is not None:
            print("Product already available\n")
            while True:
                while True:
                    try:
                        f=input("Do you want to increase the product's quantity instead('y','n'): ").lower()
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
                        t=int(input("\nEnter the total quantity: "))
                    except:
                        print("Please enter a proper quantity")
                        continue
                    if t<0:
                        print("Quantity must not be in negative")
                        continue
                    else:
                        break
                c.execute("update products set Total_Quantity_Available=%s where Product_Name=%s",(d[2]+t,n))
                db.commit()
                print("\nProduct's Quantity has be successfully Increased\n")
            else:
                print("\n")
        else:
            while True:
                try:
                    t=int(input("Enter the total quantity: "))
                except:
                    print("Please enter a proper quantity\n")
                    continue
                if t<0:
                    print("Quantity must not be in negative")
                    continue
                else:
                    break
            while True:
                try:
                    p=float(input("Enter the individual product price: "))
                except:
                    print("Please enter a proper price value\n")
                    continue
                if p<=0:
                    print("Price must be greater than 0")
                    continue
                else:
                    break
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
                r=input("\nEnter the product name or ID to be removed: ").strip().title()
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
            print("\n")
            break  

def search_product():
    while True:
        try:
            s=input("\nEnter the product name or ID to search for it: ").strip().title()
            break
        except:
            print("Please enter a proper ID or name")
    if s.isdigit():
        c.execute("select * from Products where Product_ID=%s",(s,))
    else:
        c.execute("select * from Products where Product_Name=%s",(s,))
    d=c.fetchone()
    if d is not None:
        print("\n")
        print(f"{'ID':>5} | {'Name':<13} | {'Total Quantity':<14} | {'Price':<11} | {'Expiry Date':<13}")
        print("="*66)
        if d[4] is not None:
            expiry_date =d[4]
        else:
            expiry_date ="N/A"
        print(f"{d[0]:>5} | {d[1]:<13} | {d[2]:<14} | {d[3]:<11} | {expiry_date:<13}")
        print("\n")
    else:
        print("Product not available\n")

def expiry_checker():
    c.execute("select * from products where Expiry_Date<=curdate()")
    d=c.fetchall()
    if d:
        print("\n")
        print(f"{'ID':>5} | {'Name':<13} | {'Total Quantity':>14} | {'Price':>11} | {'Expiry Date':<13} | {'E.C':<15}")
        print("="*78)
        for i in d:
            expiry_date=str(i[4])
            print(f"{i[0]:>5} | {i[1]:<13} | {i[2]:>14} | {i[3]:>11} | {expiry_date:<13} | {'Expired':<15}")
        print("\n")
    else:
        print("\nNo expired products\n")

def view_products():
    c.execute("select * from products")
    d=c.fetchall()
    print("\n")
    print(f"{'ID':>5} | {'Name':<13} | {'Total Quantity':>14} | {'Price':>11} | {'Expiry Date':<13}")
    print("="*66)
    if d:
        for i in d:
            if i[4] is not None:
                expiry_date =str(i[4])
            else:
                expiry_date ="N/A"
            print(f"{i[0]:>5} | {i[1]:<13} | {i[2]:>14} | {i[3]:>11} | {expiry_date:<13}")
        print("\n")
    else:
        print("\nNo products\n")

def product_data_update():
    while True:
        while True:
            try:
                v=input("\nEnter the product ID or name to be updated in the database of the Super Market: ").strip().title()
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
                except:
                    print("Please enter the proper integer\n")
                    continue
                n=range(1,4)
                if p not in n:
                    print("Please enter a proper integer from the given option\n")
                    continue
                else:
                    break
            if p==1:
                while True:
                    try:
                        q=int(input("\nEnter the quantity to be be updated: "))
                    except:
                        print("Please enter a proper quantity")
                        continue
                    if q<0:
                        print("Quantity must not be negative")
                        continue
                    else:
                        break
                c.execute("update products set Total_Quantity_Available=%s where Product_ID=%s",(q,d[0]))
                print("\nQuantity of the product",d[1],"has been successfully updated")
            elif p==2:
                while True:
                    try:
                        q=float(input("\nEnter the price to be be updated: "))
                    except:
                        print("Please enter a proper price value")
                        continue
                    if q<=0:
                        print("Price must be greater than 0")
                        continue
                    else:
                        break
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
