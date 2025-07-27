from tkinter import *
import requests

def get_quote():
    response = requests.get("https://api.kanye.rest")
    data = response.json()
    quote = data['quote']
    canvas.itemconfig(quote_text, text=quote)


window = Tk()
window.title("Kanye Says..")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file=r"udemy\day33\Kanye_Quotes\background.png")
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(150, 207, text="Kanye Quote goes HERE", width=250, font=("Arial", 20, "bold"), fill="white")
canvas.grid(column=0 ,row=0)

kanye_img = PhotoImage(file=r"udemy\day33\Kanye_Quotes\kanye.png")
kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
kanye_button.grid(column=0, row=1)

window.mainloop()
