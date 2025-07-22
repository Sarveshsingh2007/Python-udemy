from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# Password generator
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*']


    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
def save():

    website = website_entry.get()
    email = mail_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="opps",message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}" 
                                                    f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            with open(r"udemy\day29\data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)




window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file=r"udemy\day29\logo.png")
canvas.create_image(100, 100, image= logo_img)
canvas.grid(column=1, row=0)

# LABELS
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# ENTRIES
website_entry = Entry(width=52)
website_entry.grid(row=1,column=1, columnspan=2)
website_entry.focus()

mail_entry = Entry(width=52)
mail_entry.grid(row=2,column=1, columnspan=2)
mail_entry.insert(0, "sarveshsingh9381@gmail.com")
password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)


# BUTTONS
pass_gen = Button(text="Generate Password", command=generate_password)
pass_gen.grid(column=2, row=3)

add = Button(text="Add", width=44, command=save)
add.grid(row=4, column=1, columnspan=2)

window.mainloop()
