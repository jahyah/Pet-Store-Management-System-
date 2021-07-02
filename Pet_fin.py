import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
#from PIL import Image, ImageTk
import tkinter.messagebox
import csv
import os
import sqlite3


LARGE_FONT= ("Verdana", 20)

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)
        
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Customer, Appointment, Pet):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Customer)

    def show_frame(self, page_number):

        frame = self.frames[page_number]
        frame.tkraise()


class Customer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Pet Store Management System")
                        
        leftcolor = tk.Label(self,height = 5,width=250, bg= "powder blue")
        leftcolor.place(x=0,y=0)
        
        label2 = tk.Label(self, text="Pet Store Management System", font=LARGE_FONT, bg= "powder blue", fg= "gray")
        label2.place(x=15,y=10)
               
        CustomerID= StringVar()
        Customer_name = StringVar()
        Customer_mno = StringVar()
        SearchBar_Var = StringVar()
        
        ##=======================Functions=====================###
        
        
        def connectCustomer():
            conn = sqlite3.connect("petstore.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS customer (CustomerID VARCHAR PRIMARY KEY, Customer_Name VARCHAR, Customer_mno VARCHAR),FOREIGN KEY(CustomerID)") 
            conn.commit() 
            conn.close()
            
        def addCustomer():
            #conn = sqlite3.connect("petstore.db")
            #c = conn.cursor()         
            #Insert Table
            #c.execute("INSERT INTO customer(CustomerID,Customer_name,Customer_mno) VALUES (?,?,?)",\
                      #(CustomerID.get(),Customer_name.get(),Customer_mno.get()))        
            #conn.commit()           
            #conn.close()
            #CustomerID.set('')
            #Customer_name.set('')
            #Customer_mno.set('') 
            #tkinter.messagebox.showinfo("Pet Store Management System", "Customer Recorded Successfully")
            #displayCustomer()
            if CustomerID.get() == "" or Customer_name.get() == "" or Customer_mno.get() == "": 
                tkinter.messagebox.showinfo("Pet Store Management System", "Please fill in the box with *")
            else:
                try:
                    conn = sqlite3.connect("petstore.db")
                    c = conn.cursor() 
                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                    c.execute("INSERT INTO customer(CustomerID,Customer_name,Customer_mno) VALUES (?,?,?)",\
                              (CustomerID.get(),Customer_name.get(),Customer_mno.get()))                                     
                                                                       
                    tkinter.messagebox.showinfo("Pet Store Management System", "Customer Recorded Successfully")
                    conn.commit() 
                    clear()
                    displayCustomer()
                    conn.close()
                except:
                    tkinter.messagebox.showerror("Pet Store Management System", "ID already existed")
                    
        def displayCustomer():
            self.customerlist.delete(*self.customerlist.get_children())
            conn = sqlite3.connect("petstore.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM customer")
            rows = cur.fetchall()
            for row in rows:
                self.customerlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
            
        def updateCustomer():
            for selected in self.customerlist.selection():
                conn = sqlite3.connect("petstore.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE customer SET CustomerID=?, Customer_name=?, Customer_mno=? WHERE CustomerID=?", \
                            (CustomerID.get(),Customer_name.get(),Customer_mno.get(), self.customerlist.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Pet Store Management System", "Customer Updated Successfully")
                displayCustomer()
                conn.close()
                
        def editCustomer():
            x = self.customerlist.focus()
            if x == "":
                tkinter.messagebox.showerror("Pet Store Management System", "Please select a record from the table.")
                return
            values = self.customerlist.item(x, "values")
            CustomerID.set(values[0])
            Customer_name.set(values[1])
            Customer_mno.set(values[2])
            
        def deleteCustomer():
            messageDelete = tkinter.messagebox.askyesno("PSMS", "Do you want to permanently delete this record?")
            if messageDelete > 0:   
                con = sqlite3.connect("petstore.db")
                cur = con.cursor()
                x = self.customerlist.selection()[0]
                c_id = self.customerlist.item(x)["values"][0]
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("DELETE FROM customer WHERE CustomerID = ?",(c_id,))                   
                con.commit()
                self.customerlist.delete(x)
                tkinter.messagebox.askyesno("Pet Store Management System", "Customer Record Deleted Successfully")
                displayCustomer()
                con.close()                    
            
        
        def searchCustomer():
            CustomerID = SearchBar_Var.get()                
            con = sqlite3.connect("petstore.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM customer WHERE CustomerID = ?",(CustomerID,))
            con.commit()
            self.customerlist.delete(*self.customerlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.customerlist.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
        
        def Refresh():
            pass
            displayCustomer()
            
            
        def clear():
            CustomerID.set('')
            Customer_name.set('')
            Customer_mno.set('')
        ##=======================================================###
        

        button2 = tk.Button(self, text="Customer",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg= "powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Customer))
        button2.place(x=200,y=50)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="Appointment",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg="powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Appointment))
        button3.place(x=100,y=50)
        button3.config(cursor= "hand2")

        button4 = tk.Button(self, text="Pet",font=("Verdana",10,"bold"),bd=0,
                            width = 6,
                            bg="powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Pet))
        button4.place(x=290,y=50)
        button4.config(cursor= "hand2")
        
        
        ## Label and Entry
        
        self.lblCustomer_ID = Label(self, font=("Poppins", 12, "bold"), text="CUSTOMER ID:", padx=5, pady=5)
        self.lblCustomer_ID.place(x=15,y=144)
        self.txtCustomer_ID = Entry(self, font=("Poppins", 13), textvariable=CustomerID, width=32)
        self.txtCustomer_ID.place(x=190,y=150)
        

        self.lblCustomername = Label(self, font=("Poppins", 12,"bold"), text="CUSTOMER NAME:", padx=5, pady=5)
        self.lblCustomername.place(x=15,y=205)
        self.txtCustomername = Entry(self, font=("Poppins", 13), textvariable=Customer_name, width=32)
        self.txtCustomername.place(x=190,y=210)
        
        self.lblCustomermno = Label(self, font=("Poppins", 12,"bold"), text="CONTACT NUMBER:", padx=5, pady=5)
        self.lblCustomermno.place(x=15,y=266)
        self.txtCustomermno = Entry(self, font=("Poppins", 13), textvariable=Customer_mno, width=32)
        self.txtCustomermno.place(x=190,y=270)
        
        self.SearchBar = Entry(self, font=("Poppins", 11), textvariable=SearchBar_Var, width=21)
        self.SearchBar.place(x=515,y=110)
        self.SearchBar.insert(0,'Search customer id here')
        

        ##==================================================Treeview========================================##
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1250,y=140,height=430)

        self.customerlist = ttk.Treeview(self,
                                        columns=("Customer ID","Customer Name", "Contact Number"),
                                        height = 20,
                                        yscrollcommand=scrollbar.set)

        self.customerlist.heading("Customer ID", text="Customer ID", anchor=W)
        self.customerlist.heading("Customer Name", text="Customer Name",anchor=W)
        self.customerlist.heading("Contact Number", text="Contact Number",anchor=W)
        self.customerlist['show'] = 'headings'

        self.customerlist.column("Customer ID", width=200, anchor=W, stretch=False)
        self.customerlist.column("Customer Name", width=330, stretch=False)
        self.customerlist.column("Contact Number", width=200, stretch=False)


        self.customerlist.place(x=510,y=140)
        scrollbar.config(command=self.customerlist.yview)
            
        ##===================================================Buttons=======================================##

        self.btnAddID = Button(self, text="ADD", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                               bg="powder blue", fg="gray", command=addCustomer)
        self.btnAddID.place(x=200,y=320)
        
        self.btnUpdate = Button(self, text="UPDATE", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                                bg="powder blue", fg="gray", command=updateCustomer) 
        self.btnUpdate.place(x=350,y=320)
        
        self.btnClear = Button(self, text="CLEAR", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                               bg="powder blue", fg="gray", command=clear)
        self.btnClear.place(x=200,y=370)
        
        self.btnDelete = Button(self, text="DELETE", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                                bg="powder blue", fg="gray", command=deleteCustomer)
        self.btnDelete.place(x=350,y=370)
        
        self.btnSelect = Button(self, text="Select", font=('Poppins', 10, 'bold'), height=1, width=11,
                              bg="powder blue", fg="gray", command=editCustomer)
        self.btnSelect.place(x=1010,y=103)
        
        self.btnSearch = Button(self, text="Search", font=('Poppins', 10, 'bold'), height=1, width=10,
                                bg="powder blue", fg="gray", command=searchCustomer)
        self.btnSearch.place(x=695,y=103)
        
        self.btnRefresh = Button(self, text="Show All", font=('Poppins', 10, 'bold'), height=1, width=11,
                              bg="powder blue", fg="gray", command=Refresh)
        self.btnRefresh.place(x=1135,y=103)
        
        #connectCustomer()
        displayCustomer()
        
class Pet(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Pet Store Management System")
                        
        leftcolor = tk.Label(self,height = 5,width=250, bg= "powder blue")
        leftcolor.place(x=0,y=0)
        
        label2 = tk.Label(self, text="Pet Store Management System", font=LARGE_FONT, bg= "powder blue", fg= "gray")
        label2.place(x=15,y=10)
               
        PetID= StringVar()
        Breed = StringVar()
        Pet_type = StringVar()
        CustomerID = StringVar()
        SearchBar_Var = StringVar()
        
        ##=======================Functions=====================###
        #cur.execute("CREATE TABLE IF NOT EXISTS customer (CustomerID VARCHAR PRIMARY KEY, Customer_Name VARCHAR, Customer_mno VARCHAR)") 
        
        def connectPet():
            conn = sqlite3.connect("petstore.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS pet (PetID VARCHAR PRIMARY KEY, Breed VARCHAR, Pet_type VARCHAR, CustomerID VARCHAR),FOREIGN KEY(CustomerID)REFERENCES customer(CustomerID) ON UPDATE CASCADE ON DELETE CASCADE") 
            conn.commit() 
            conn.close()    
        
        def addPet():
            
            #conn = sqlite3.connect("petstore.db")
            #c = conn.cursor() 
            #c.execute("INSERT INTO pet(PetID,Breed,Pet_type,CustomerID) VALUES (?,?,?,?)",\
                     #(PetID.get(),Breed.get(),Pet_type.get(),CustomerID.get()))                                       
            #conn.commit()           
            #conn.close()
            #PetID.set('')
            #Breed.set('')
            #Pet_type.set('')
            #CustomerID.set('')
            #tkinter.messagebox.showinfo("Pet Store Management System", "Pet Recorded Successfully")
            #displayPet()
        
            if PetID.get() == "" or Breed.get() == "" or Pet_type.get() == "" or CustomerID.get() == "": 
                tkinter.messagebox.showinfo("Pet Store Management System", "Please fill in the box with *")
            else:
                try:
                    conn = sqlite3.connect("petstore.db")
                    c = conn.cursor() 
                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                    c.execute("INSERT INTO pet(PetID,Breed,Pet_type,CustomerID) VALUES (?,?,?,?)",\
                              (PetID.get(),Breed.get(),Pet_type.get(),CustomerID.get()))                                  
                    tkinter.messagebox.showinfo("Pet Store Management System", "Pet Recorded Successfully")
                    conn.commit() 
                    clear()
                    displayPet()
                    conn.close()
                except:
                    tkinter.messagebox.showerror("Pet Store Management System", "Customer ID not registered")
                    
        def displayPet():
            self.petlist.delete(*self.petlist.get_children())
            conn = sqlite3.connect("petstore.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM pet")
            rows = cur.fetchall()
            for row in rows:
                self.petlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
            
        def updatePet():
            for selected in self.petlist.selection():
                conn = sqlite3.connect("petstore.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE pet SET PetID=?, Breed=?, Pet_type=?, CustomerID=? WHERE CustomerID=?", \
                            (PetID.get(),Breed.get(),Pet_type.get(),CustomerID.get(), self.petlist.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Pet Store Management System", "Pet Record Updated Successfully")
                displayPet()
                conn.close()

                
        def editPet():
            x = self.petlist.focus()
            if x == "":
                tkinter.messagebox.showerror("Pet Store Management System", "Please select a record from the table.")
                return
            values = self.petlist.item(x, "values")
            PetID.set(values[0])
            Breed.set(values[1])
            Pet_type.set(values[2])
            CustomerID.set(values[3])
        
        def deletePet():
            messageDelete = tkinter.messagebox.askyesno("PSMS", "Do you want to permanently delete this record?")
            if messageDelete > 0:   
                con = sqlite3.connect("petstore.db")
                cur = con.cursor()
                x = self.petlist.selection()[0]
                P_id = self.petlist.item(x)["values"][0]
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("DELETE FROM pet WHERE PetID = ?",(P_id,))                   
                con.commit()
                self.petlist.delete(x)
                tkinter.messagebox.askyesno("Pet Store Management System", "Pet Record Deleted Successfully")
                displayPet()
                con.close() 
                
        
        def searchPet():
            CustomerID = SearchBar_Var.get()                
            con = sqlite3.connect("petstore.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM pet WHERE CustomerID = ?",(CustomerID,))
            con.commit()
            self.petlist.delete(*self.petlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.petlist.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
         
            
        def Refresh():
            pass
            displayPet()
            
        def clear():
            PetID.set('')
            Breed.set('')
            Pet_type.set('')
            CustomerID.set('')
        ##=======================================================###
        

        button2 = tk.Button(self, text="Customer",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg= "powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Customer))
        button2.place(x=200,y=50)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="Appointment",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg="powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Appointment))
        button3.place(x=100,y=50)
        button3.config(cursor= "hand2")
        
        button4 = tk.Button(self, text="Pet",font=("Verdana",10,"bold"),bd=0,
                            width = 6,
                            bg="powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Pet))
        button4.place(x=290,y=50)
        button4.config(cursor= "hand2")

        ## Label and Entry
        
        self.lblPet_ID = Label(self, font=("Poppins", 12, "bold"), text="PET ID:", padx=5, pady=5)
        self.lblPet_ID.place(x=25,y=144)
        self.txtPet_ID = Entry(self, font=("Poppins", 13), textvariable=PetID, width=34)
        self.txtPet_ID.place(x=155,y=150)
        

        self.lblPet_Breed = Label(self, font=("Poppins", 12,"bold"), text="BREED:", padx=5, pady=5)
        self.lblPet_Breed.place(x=25,y=205)
        self.txtPet_Breed = Entry(self, font=("Poppins", 13), textvariable=Breed, width=34)
        self.txtPet_Breed.place(x=155,y=210)
        
        self.lblPettype = Label(self, font=("Poppins", 12,"bold"), text="PET TYPE:", padx=5, pady=5)
        self.lblPettype.place(x=25,y=266)
        self.txtPettype = Entry(self, font=("Poppins", 13), textvariable=Pet_type, width=34)
        self.txtPettype.place(x=155,y=270)
        
        self.lblCustomer_iD = Label(self, font=("Poppins", 12, "bold"), text="CUSTOMER ID:", padx=5, pady=5)
        self.lblCustomer_iD.place(x=25,y=327)
        self.txtCustomer_iD = Entry(self, font=("Poppins", 13), textvariable=CustomerID, width=34)
        self.txtCustomer_iD.place(x=155,y=330)
        
        self.SearchBar = Entry(self, font=("Poppins", 11), textvariable=SearchBar_Var, width=21)
        self.SearchBar.place(x=515,y=110)
        self.SearchBar.insert(0,'Search customer id here')
        

        ##==================================================Treeview========================================##
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1250,y=140,height=430)

        self.petlist = ttk.Treeview(self,
                                        columns=("Pet ID","Breed", "Pet Type","Customer ID"),
                                        height = 20,
                                        yscrollcommand=scrollbar.set)

        
        self.petlist.heading("Pet ID", text="Pet ID", anchor=W)
        self.petlist.heading("Breed", text="Breed",anchor=W)
        self.petlist.heading("Pet Type", text="Pet Type",anchor=W)
        self.petlist.heading("Customer ID", text="Customer ID", anchor=W)
        self.petlist['show'] = 'headings'

        self.petlist.column("Customer ID", width=100, anchor=W, stretch=False)
        self.petlist.column("Pet ID", width=100, anchor=W, stretch=False)
        self.petlist.column("Breed", width=330, stretch=False)
        self.petlist.column("Pet Type", width=200, stretch=False)
        self.petlist.column("Customer ID", width=100, anchor=W, stretch=False)


        self.petlist.place(x=510,y=140)
        scrollbar.config(command=self.petlist.yview)
            
        ##===================================================Buttons=======================================##

        self.btnAddID = Button(self, text="ADD", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                               bg="powder blue", fg="gray", command=addPet)
        self.btnAddID.place(x=170,y=390)
        
        self.btnUpdate = Button(self, text="UPDATE", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                                bg="powder blue", fg="gray", command=updatePet) 
        self.btnUpdate.place(x=300,y=390)
        
        self.btnClear = Button(self, text="CLEAR", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                               bg="powder blue", fg="gray", command=clear)
        self.btnClear.place(x=170,y=450)
        
        self.btnDelete = Button(self, text="DELETE", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                                bg="powder blue", fg="gray",command=deletePet)
        self.btnDelete.place(x=300,y=450)
        
        self.btnSelect = Button(self, text="Select", font=('Poppins', 10, 'bold'), height=1, width=11,
                              bg="powder blue", fg="gray", command=editPet)
        self.btnSelect.place(x=1010,y=103)
        
        self.btnSearch = Button(self, text="Search", font=('Poppins', 10, 'bold'), height=1, width=10,
                                bg="powder blue", fg="gray", command=searchPet)
        self.btnSearch.place(x=695,y=103)
        
        self.btnRefresh = Button(self, text="Show All", font=('Poppins', 10, 'bold'), height=1, width=11,
                              bg="powder blue", fg="gray", command=Refresh)
        self.btnRefresh.place(x=1135,y=103)
        
        #connectPet()
        displayPet()

class Appointment(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Pet Store Management System")        
        
        leftcolor = tk.Label(self,height = 5,width=250, bg= "powder blue")
        leftcolor.place(x=0,y=0)
        
        label2 = tk.Label(self, text=" Pet Store Management System", font=LARGE_FONT, bg= "powder blue", fg= "gray")
        label2.place(x=15,y=10)
        
        

        ##=============================================WindowBtn=====================================##
        button2 = tk.Button(self, text="Customer",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg= "powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Customer))
        button2.place(x=200,y=50)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="Appointment",font=("Verdana",10,"bold"),bd=0,
                            width = 10,
                            bg="powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Appointment))
        button3.place(x=100,y=50)
        button3.config(cursor= "hand2")
        
        button4 = tk.Button(self, text="Pet",font=("Verdana",10,"bold"),bd=0,
                            width = 6,
                            bg="powder blue",
                            fg="gray",
                            command=lambda: controller.show_frame(Pet))
        button4.place(x=290,y=50)
        button4.config(cursor= "hand2")
        
        
        ##=====================================================Functions================================##
        AppointmentID = StringVar()
        Appointment_details = StringVar()
        Status = StringVar()
        Appointment_Date = StringVar()
        CustomerID = StringVar()
        SearchBar_Var = StringVar()
        
        def connectAppointment():
            conn = sqlite3.connect("petstore.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS appointment (AppointmentID VARCHAR PRIMARY KEY, Appointment_details VARCHAR, Status VARCHAR, Appointment_date VARCHAR, CustomerID VARCHAR),FOREIGN KEY(CustomerID)REFERENCES customer(CustomerID) ON UPDATE CASCADE ON DELETE CASCADE") 
            conn.commit() 
            conn.close()    
        
        def addAppointment():
            
            #conn = sqlite3.connect("petstore.db")
            #c = conn.cursor() 
            #c.execute("INSERT INTO appointment(AppointmentID,Appointment_details,Status,Appointment_date,CustomerID) VALUES (?,?,?,?,?)",\
                     #(AppointmentID.get(),Appointment_details.get(),Status.get(),Appointment_Date.get(),CustomerID.get()))                                       
            #conn.commit()           
            #conn.close()
            #AppointmentID.set('')
            #Appointment_details.set('')
            #Status.set('')
            #Appointment_Date.set('')
            #CustomerID.set('')
            #tkinter.messagebox.showinfo("Pet Store Management System", "Appointment Recorded Successfully")
            #displayAppointment()
        
            if AppointmentID.get() == "" or Appointment_details.get() == "" or Status.get() == ""  or Appointment_Date.get() == "" or CustomerID.get() == "": 
                tkinter.messagebox.showinfo("Pet Store Management System", "Please fill in the box with *")
            else:
                try:
                    conn = sqlite3.connect("petstore.db")
                    c = conn.cursor() 
                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                    c.execute("INSERT INTO appointment(AppointmentID,Appointment_details,Status,Appointment_date,CustomerID) VALUES (?,?,?,?,?)",\
                              (AppointmentID.get(),Appointment_details.get(),Status.get(),Appointment_Date.get(),CustomerID.get()))                                  
                    tkinter.messagebox.showinfo("Pet Store Management System", "Appointment Recorded Successfully")
                    conn.commit() 
                    clear()
                    displayAppointment()
                    conn.close()
                except:
                    tkinter.messagebox.showerror("Pet Store Management System", "Customer ID not registered")
                    
        def displayAppointment():
            self.appolist.delete(*self.appolist.get_children())
            conn = sqlite3.connect("petstore.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM appointment")
            rows = cur.fetchall()
            for row in rows:
                self.appolist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
       
        def updateAppointment():
            for selected in self.appolist.selection():
                conn = sqlite3.connect("petstore.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE appointment SET AppointmentID=?, Appointment_details=?, Status=?, Appointment_Date=?, CustomerID=? WHERE AppointmentID=?", \
                            (AppointmentID.get(),Appointment_details.get(),Status.get(),Appointment_Date.get(),CustomerID.get(), self.appolist.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Pet Store Management System", "Appointment Record Updated Successfully")
                displayAppointment()
                clear()
                conn.close()
                

        def editAppointment():
            x = self.appolist.focus()
            if x == "":
                tkinter.messagebox.showerror("Pet Store Management System", "Please select a record from the table.")
                return
            values = self.appolist.item(x, "values")
            AppointmentID.set(values[0])
            Appointment_details.set(values[1])
            Status.set(values[2])
            Appointment_Date.set(values[3])
            CustomerID.set(values[4])
            
        def deleteAppointment():
            messageDelete = tkinter.messagebox.askyesno("PSMS", "Do you want to permanently delete this record?")
            if messageDelete > 0:   
                con = sqlite3.connect("petstore.db")
                cur = con.cursor()
                x = self.appolist.selection()[0]
                a_id = self.appolist.item(x)["values"][0]
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("DELETE FROM appointment WHERE AppointmentID = ?",(a_id,))                   
                con.commit()
                self.appolist.delete(x)
                tkinter.messagebox.askyesno("Pet Store Management System", "Appointment Record Deleted Successfully")
                displayAppointment()
                con.close()      
                
                
        def searchAppointment():
            CustomerID = SearchBar_Var.get()                
            con = sqlite3.connect("petstore.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM appointment WHERE CustomerID = ?",(CustomerID,))
            con.commit()
            self.appolist.delete(*self.appolist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.appolist.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
         
            
        def Refresh():
            pass
            displayAppointment()
            
        def clear():
            AppointmentID.set('')
            Appointment_details.set('')
            Status.set('')
            Appointment_Date.set('')
            CustomerID.set('')
        ##=====================================Label and Entry=====================================##
        
        self.lblAppointment_ID = Label(self, font=("Poppins", 12, "bold"), text="APPOINTMENT ID:", padx=5, pady=5)
        self.lblAppointment_ID.place(x=15,y=144)
        self.txtAppointment_ID = Entry(self, font=("Poppins", 13), textvariable=AppointmentID, width=33)
        self.txtAppointment_ID.place(x=170,y=150)
        

        self.lblAppointmentdet = Label(self, font=("Poppins", 12,"bold"), text="ORDER DETAILS:", padx=5, pady=5)
        self.lblAppointmentdet.place(x=15,y=205)
        self.txtAppointmentdet = Entry(self, font=("Poppins", 13), textvariable=Appointment_details, width=33)
        self.txtAppointmentdet.place(x=170,y=210)
        
        self.lblStatu = Label(self, font=("Poppins", 12,"bold"), text="STATUS:", padx=5, pady=5)
        self.lblStatu.place(x=15,y=266)
        self.txtStatu = ttk.Combobox(self, value=["Completed", "Cancelled"], font=("Poppins", 13),
                                             state="readonly", textvariable=Status, width=31)
        self.txtStatu.place(x=170,y=270)
        
        
        self.lbldt = Label(self, font=("Poppins", 12,"bold"), text="DATE:", padx=5, pady=5)
        self.lbldt.place(x=15,y=327)
        self.txtdt = Entry(self, font=("Poppins", 13), textvariable=Appointment_Date, width=33)
        self.txtdt.place(x=170,y=327)
        self.lbldtFormat = Label(self, font=("Poppins", 12,"bold"),
                                          text="(MM-DD-YYYY)")
        self.lbldtFormat.place(x=170,y=350)
        
        self.lblCustomer_id = Label(self, font=("Poppins", 12, "bold"), text="CUSTOMER ID:", padx=5, pady=5)
        self.lblCustomer_id.place(x=15,y=387)
        self.txtCustomer_id= Entry(self, font=("Poppins", 13), textvariable=CustomerID, width=34)
        self.txtCustomer_id.place(x=170,y=387)
        
        self.SearchBar = Entry(self, font=("Poppins", 11), textvariable=SearchBar_Var, width=21)
        self.SearchBar.place(x=515,y=110)
        self.SearchBar.insert(0,'Search Customer ID here')
        
        
        
        

        ##=========================Treeview==============================##
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1250,y=140,height=420)

        self.appolist = ttk.Treeview(self,
                                        columns=("Appointment ID", "Appointment Details", "Status", "Date", "Customer ID"),
                                        height = 20,
                                        yscrollcommand=scrollbar.set)

        
        self.appolist.heading("Appointment ID", text="Appointment ID", anchor=W)
        self.appolist.heading("Appointment Details", text="Appointment Details",anchor=W)
        self.appolist.heading("Status", text="Status",anchor=W)
        self.appolist.heading("Date", text="Date",anchor=W)
        self.appolist.heading("Customer ID", text="Customer ID", anchor=W)
        self.appolist['show'] = 'headings'

    
        self.appolist.column("Appointment ID", width=130, anchor=W, stretch=False)
        self.appolist.column("Appointment Details", width=280, stretch=False)
        self.appolist.column("Status", width=120, anchor=W, stretch=False)
        self.appolist.column("Date", width=100, anchor=W, stretch=False)
        self.appolist.column("Customer ID", width=100, anchor=W, stretch=False)

        self.appolist.place(x=510,y=140)
        scrollbar.config(command=self.appolist.yview)
        
        ##========================Buttons=================================##
        
        self.btnAddID = Button(self, text="ADD", font=('Poppins', 11, 'bold'), height=1, width=10, bd=0, 
                               bg="powder blue", fg="gray", command=addAppointment)
        self.btnAddID.place(x=200,y=440)
        self.btnAddID.config(cursor= "hand2")
        
        self.btnUpdate = Button(self, text="UPDATE", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                                bg="powder blue", fg="gray", command=updateAppointment)
        self.btnUpdate.place(x=335,y=440)
        self.btnUpdate.config(cursor= "hand2")
        
        self.btnClear = Button(self, text="CLEAR", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                               bg="powder blue", fg="gray", command=clear)
        self.btnClear.place(x=200,y=490)
        self.btnClear.config(cursor= "hand2")
        
        self.btnDelete = Button(self, text="DELETE", font=('Poppins', 11, 'bold'), height=1, width=10, bd=1,
                                bg="powder blue", fg="gray", command=deleteAppointment)
        self.btnDelete.place(x=335,y=490)
        self.btnDelete.config(cursor= "hand2")
        
        self.btnSelect = Button(self, text="Select", font=('Poppins', 10, 'bold'), height=1, width=11,
                              bg="powder blue", fg="gray", command=editAppointment)
        self.btnSelect.place(x=1010,y=103)
        self.btnSelect.config(cursor= "hand2")
        
        self.btnSearch = Button(self, text="Search", font=('Poppins', 10, 'bold'), height=1, width=10,
                                bg="powder blue", fg="gray",command=searchAppointment)
        self.btnSearch.place(x=695,y=103)
        self.btnSearch.config(cursor= "hand2")
        
        self.btnRefresh = Button(self, text="Show All", font=('Poppins', 10, 'bold'), height=1, width=11,
                              bg="powder blue", fg="gray", command=Refresh)
        self.btnRefresh.place(x=1135,y=103)
        self.btnRefresh.config(cursor= "hand2")
        
        #connect()
        displayAppointment()
        #searchData()
        
        
            
        
app = App()
app.geometry("1280x600")
app.mainloop()


