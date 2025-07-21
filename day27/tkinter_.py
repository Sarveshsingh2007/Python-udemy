from tkinter import *

#window
window = Tk()
window.title("My First GUI")
window.minsize(500, 300)
window.config(padx=100, pady=200)

def button_clicked():
    print("Button was clicked!")
    new_text = input.get()
    my_label.config(text=new_text)

# Label
my_label = Label(text="Hello, Tkinter!", font=("Arial", 12, "bold"))
my_label.grid(column=0, row=0)

# Button
button = Button(text="Click Me", command=button_clicked)
button.grid(column=2,row=0)



# Entry
input = Entry(width=10)
input.grid(column=3,row=2)
print(input.get())


window.mainloop()
