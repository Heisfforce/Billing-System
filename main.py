import customtkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import date
import database

def handle_login():
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()
    
    if username and password:
        try:
            with open('users.txt', 'r') as file:
                users = file.read().strip()
                if not users:
                    raise FileNotFoundError("No users found.")
                
                user_entries = users.split("====================\n")
                for user_entry in user_entries:
                    if user_entry.strip():
                        lines = user_entry.strip().split("\n")
                        if len(lines) < 2:  
                            continue
                        stored_username_line = lines[0].split(": ")
                        stored_password_line = lines[1].split(": ")
                        if len(stored_username_line) < 2 or len(stored_password_line) < 2:
                            continue
                        stored_username = stored_username_line[1].strip()
                        stored_password = stored_password_line[1].strip()
                        if username == stored_username and password == stored_password:
                            messagebox.showinfo("Success", "Login successful!")
                            login_window.destroy()
                            app.deiconify()
                            return
                messagebox.showerror("Error", "Invalid username or password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No users found. Please sign up.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Both fields are required.")

def handle_signup():
    username = signup_username_entry.get().strip()
    password = signup_password_entry.get().strip()
    confirm_password = signup_confirm_password_entry.get().strip()
    
    if username and password and confirm_password:
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        try:
            with open('users.txt', 'a') as file:
                file.write(f"username: {username}\npassword: {password}\n====================\n")
            messagebox.showinfo("Success", "Sign-up successful! Please log in.")
            signup_window.destroy()
            show_login_window()  
        except Exception as e:
            messagebox.showerror("Error", f"Error saving user: {e}")
    else:
        messagebox.showerror("Error", "All fields are required.")

def show_login_window():
    global login_window, login_username_entry, login_password_entry, signup_window, signup_username_entry, signup_password_entry, signup_confirm_password_entry
    
    app.withdraw()
    login_window = customtkinter.CTkToplevel(app)
    login_window.title("BON APPETIT!")
    login_window.geometry("400x350")
    login_window.configure(fg_color="#2E8B57")

    Label(login_window, text="BON APPETIT!", font=("Arial", 20, "bold"), fg="#FFFFFF", bg="#2E8B57").pack(pady=10)
    Label(login_window, text="Username:", font=("Arial", 14), fg="#FFFFFF", bg="#2E8B57").pack(pady=5)
    login_username_entry = customtkinter.CTkEntry(login_window, font=("Arial", 14), text_color='#000000', fg_color="#F0FFF0", border_width=2)
    login_username_entry.pack(pady=5)
    Label(login_window, text="Password:", font=("Arial", 14), fg="#FFFFFF", bg="#2E8B57").pack(pady=5)
    login_password_entry = customtkinter.CTkEntry(login_window, font=("Arial", 14), text_color='#000000', fg_color="#F0FFF0", border_width=2, show="*")
    login_password_entry.pack(pady=5)
    
    Button(login_window, text="Login", font=("Arial", 14), fg="#FFFFFF", bg="#228B22", command=handle_login).pack(pady=10)
    Button(login_window, text="Sign Up", font=("Arial", 14), fg="#FFFFFF", bg="#8B0000", command=lambda: show_signup_window(login_window)).pack(pady=10)

def show_signup_window(parent):
    parent.destroy()
    global signup_window
    signup_window = customtkinter.CTkToplevel(app)
    signup_window.title("Sign Up")
    signup_window.geometry("400x400")
    signup_window.configure(fg_color="#2E8B57")

    Label(signup_window, text="Sign Up", font=("Arial", 20, "bold"), fg="#FFFFFF", bg="#2E8B57").pack(pady=10)
    Label(signup_window, text="Username:", font=("Arial", 14), fg="#FFFFFF", bg="#2E8B57").pack(pady=5)
    global signup_username_entry, signup_password_entry, signup_confirm_password_entry
    signup_username_entry = customtkinter.CTkEntry(signup_window, font=("Arial", 14), text_color='#000000', fg_color="#F0FFF0", border_width=2)
    signup_username_entry.pack(pady=5)
    Label(signup_window, text="Password:", font=("Arial", 14), fg="#FFFFFF", bg="#2E8B57").pack(pady=5)
    signup_password_entry = customtkinter.CTkEntry(signup_window, font=("Arial", 14), text_color='#000000', fg_color="#F0FFF0", border_width=2, show="*")
    signup_password_entry.pack(pady=5)
    Label(signup_window, text="Confirm Password:", font=("Arial", 14), fg="#FFFFFF", bg="#2E8B57").pack(pady=5)
    signup_confirm_password_entry = customtkinter.CTkEntry(signup_window, font=("Arial", 14), text_color='#000000', fg_color="#F0FFF0", border_width=2, show="*")
    signup_confirm_password_entry.pack(pady=5)
    
    Button(signup_window, text="Sign Up", font=("Arial", 14), fg="#FFFFFF", bg="#228B22", command=handle_signup).pack(pady=10)

app = customtkinter.CTk()
app.title('Bon Appetit Billing System')
app.geometry('900x400')
app.configure(fg_color="#0A0B0C")

show_login_window()

font1 = ('Arial', 20, "bold")
font2 = ('Arial', 24, "bold")

def receipt():
    customer_name = customer_name_entry.get().strip()
    if not customer_name:
        messagebox.showerror('Error', 'Customer name is required.')
        return

    meals_entries = [Risotto_entry, Braciole_entry, Arancini_entry]
    drinks_entries = [Orange_entry, Strawberry_entry, Lemonade_entry]
    meals_prices, drinks_prices = database.get_product_prices()

    try:
        meals_quantities = [int(entry.get()) if entry.get().isdigit() else 0 for entry in meals_entries]
        drinks_quantities = [int(entry.get()) if entry.get().isdigit() else 0 for entry in drinks_entries]
        meals_total = sum(quantity * price for quantity, price in zip(meals_quantities, meals_prices))
        drinks_total = sum(quantity * price for quantity, price in zip(drinks_quantities, drinks_prices))
        total = meals_total + drinks_total
        todays_date = date.today().strftime('%m/%d/%Y')

        if total == 0:
            messagebox.showerror('Error', 'Choose at least 1 product.')
        else:
            customer_label.configure(text=f'Customer: {customer_name}')
            meals_total_label.configure(text=f'Meals Total: ₱{meals_total:.2f}')
            drinks_total_label.configure(text=f'Drinks Total: ₱{drinks_total:.2f}')
            total_label.configure(text=f'Total Price: ₱{total:.2f}')
            date_label.configure(text=f'Date: {todays_date}')
            return customer_name, meals_total, drinks_total, total, todays_date
    except ValueError:
        messagebox.showerror('Error', 'Entered values should be integers.')

def new():
    customer_name_entry.delete(0, END)
    Risotto_entry.delete(0, END)
    Braciole_entry.delete(0, END)
    Arancini_entry.delete(0, END)
    Orange_entry.delete(0, END)
    Strawberry_entry.delete(0, END)
    Lemonade_entry.delete(0, END)
    customer_label.configure(text='')
    meals_total_label.configure(text='')
    drinks_total_label.configure(text='')
    total_label.configure(text='')
    date_label.configure(text='')

def save():
    receipt_data = receipt()
    if receipt_data is not None:
        customer_name, meals_total, drinks_total, total, todays_date = receipt_data
        with open('receipts.txt', 'a', encoding='utf-8') as file:
            file.write(f"Customer: {customer_name}\n")
            file.write(f"Meals Total: ₱{meals_total:.2f}\n")
            file.write(f"Drinks Total: ₱{drinks_total:.2f}\n")
            file.write(f"Total Price: ₱{total:.2f}\n")
            file.write(f"Date: {todays_date}\n")
            file.write("=" * 22 + "\n")
        messagebox.showinfo('Success', 'Receipt has been saved.')


customer_frame = customtkinter.CTkFrame(app, bg_color='#000000', fg_color='#7B68EE', corner_radius=10, border_width=5, border_color='#FFFFFF', width=576, height=70)
customer_frame.place(x=16, y=10)

customer_name_label = customtkinter.CTkLabel(customer_frame, font=font1, text='Customer Name:', text_color='#FFFFFF')
customer_name_label.place(x=25, y=20)

customer_name_entry = customtkinter.CTkEntry(customer_frame, font=font1, text_color='#000', fg_color='#F5F5E6', border_width=2, width=340)
customer_name_entry.place(x=200, y=20)

meals_frame = customtkinter.CTkFrame(app, bg_color='#000000', fg_color='#7B3F00', corner_radius=10, border_width=5, border_color='#FFFFFF', width=280, height=250)
meals_frame.place(x=15, y=90)

title1_label = customtkinter.CTkLabel(meals_frame, font=font2, text='MEALS', text_color='#FF69B4', bg_color='#7B3F00')
title1_label.place(x=60, y=40)

image1 = Image.open('algie.png')  
image1 = image1.resize((90,80))  
image1 = ImageTk.PhotoImage(image1)

image1_label = Label(meals_frame, image=image1, bg='#7B3F00')
image1_label.image = image1  
image1_label.place(x=165, y=5)

Risotto_label = customtkinter.CTkLabel(meals_frame, font=font1, text='Risotto:', text_color='#90EE90')
Risotto_label.place(x=50, y=100)

Risotto_entry = customtkinter.CTkEntry(meals_frame, font=font1, text_color='#000', fg_color='#F5F5E6', border_width=2, width=90)
Risotto_entry.place(x=160, y=100)

Braciole_label = customtkinter.CTkLabel(meals_frame, font=font1, text='Braciole:', text_color='#B0E0E6')
Braciole_label.place(x=50, y=140)

Braciole_entry = customtkinter.CTkEntry(meals_frame, font=font1, text_color='#000', fg_color='#F5F5E6', border_width=2, width=90)
Braciole_entry.place(x=160, y=140)

Arancini_label = customtkinter.CTkLabel(meals_frame, font=font1, text='Arancini:', text_color='#FFD700')
Arancini_label.place(x=50, y=180)

Arancini_entry = customtkinter.CTkEntry(meals_frame, font=font1, text_color='#000', fg_color='#F5F5E6', border_width=2, width=90)
Arancini_entry.place(x=160, y=180)

drinks_frame = customtkinter.CTkFrame(app, bg_color='#000000', fg_color='#D2B48C', corner_radius=10, border_width=5, border_color='#FFFFFF', width=280, height=250)
drinks_frame.place(x=310, y=90)

title2_label = customtkinter.CTkLabel(drinks_frame, font=font2, text='DRINKS', text_color='#0000FF', bg_color='#D2B48C')
title2_label.place(x=60, y=40)

image2 = Image.open('heir.png')  
image2 = image2.resize((90,80))  
image2 = ImageTk.PhotoImage(image2)

image2_label = Label(drinks_frame, image=image2, bg='#D2B48C')
image2_label.image = image2  
image2_label.place(x=165, y=5)

Orange_label = customtkinter.CTkLabel(drinks_frame, font=font1, text='Orange Juice:', text_color='#D2691E')
Orange_label.place(x=20, y=100)

Orange_entry = customtkinter.CTkEntry(drinks_frame, font=font1, text_color='#000', fg_color='#D2691E', border_width=2, width=60)
Orange_entry.place(x=200, y=100)

Strawberry_label = customtkinter.CTkLabel(drinks_frame, font=font1, text='Strawberry Juice:', text_color='#8B0000')
Strawberry_label.place(x=20, y=140)

Strawberry_entry = customtkinter.CTkEntry(drinks_frame, font=font1, text_color='#000', fg_color='#8B0000', border_width=2, width=60)
Strawberry_entry.place(x=200, y=140)

Lemonade_label = customtkinter.CTkLabel(drinks_frame, font=font1, text='Lemonade Juice:', text_color='#228B22')
Lemonade_label.place(x=20, y=180)

Lemonade_entry = customtkinter.CTkEntry(drinks_frame, font=font1, text_color='#000', fg_color='#228B22', border_width=2, width=60)
Lemonade_entry.place(x=200, y=180)

receipt_frame = customtkinter.CTkFrame(app, bg_color='#000000', fg_color='#FFFFF0', corner_radius=10, border_width=5, border_color='#818181', width=280, height=350)
receipt_frame.place(x=605, y=10)

title3_label = customtkinter.CTkLabel(receipt_frame, font=font2, text='  RECEIPT  ', text_color='#FFFFFF', bg_color='#818181')
title3_label.place(x=78, y=20)

customer_label = customtkinter.CTkLabel(receipt_frame, font=font1, text='', text_color='#000000', bg_color='#FFFFF0')
customer_label.place(x=20, y=60)

meals_total_label = customtkinter.CTkLabel(receipt_frame, font=font1, text='', text_color='#000000', bg_color='#FFFFF0')
meals_total_label.place(x=20, y=100)

drinks_total_label = customtkinter.CTkLabel(receipt_frame, font=font1, text='', text_color='#000000', bg_color='#FFFFF0')
drinks_total_label.place(x=20, y=140)

total_label = customtkinter.CTkLabel(receipt_frame, font=font1, text='', text_color='#000000', bg_color='#FFFFF0')
total_label.place(x=20, y=180)

date_label = customtkinter.CTkLabel(receipt_frame, font=font1, text='', text_color='#000000', bg_color='#FFFFF0')
date_label.place(x=20, y=220)

receipt_button = customtkinter.CTkButton(app, command=receipt, font=font2, text_color='#FFFFFF', text='Receipt', fg_color='#088561', hover_color='#047152', bg_color='#000000', cursor='hand2', corner_radius=25, width=200)
receipt_button.place(x=60, y=350)

save_button = customtkinter.CTkButton(app, command=save, font=font2, text_color='#FFFFFF', text='Save', fg_color='#4E4E4E', hover_color='#343434', bg_color='#FFFFF0', cursor='hand2', corner_radius=25, width=200)
save_button.place(x=645, y=300)

new_button = customtkinter.CTkButton(app, command=new, font=font2, text_color='#FFFFFF', text='New', fg_color='#E93E05', hover_color='#A82A00', bg_color='#000000', cursor='hand2', corner_radius=25, width=200)
new_button.place(x=360, y=350)

app.mainloop()
