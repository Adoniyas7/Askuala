#==========================================================================
#                      Student Registration System                        #
#==========================================================================
#                             developed by:-                              #
#                          Adoniyas and Rediet                            #
#==========================================================================

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from gui import main


ASSETS_PATH = Path(__file__).resolve().parent / 'assets/login'
print(ASSETS_PATH)

def assets(path):
    return ASSETS_PATH / Path(path)

#username and password
user_name = 'Admin'
password = '12345'


def login():
    #check if the username and password is correct
    if username_entry.get().strip() == user_name and password_entry.get() == password:
        #destroy the current window and run the main function from the main app
        window.destroy()
        main()
    else:
        messagebox.showerror(title='Error', message='Please enter the correct credentials.')


window = Tk()

window.geometry("1012x506")
#remove the title bar
window.wm_attributes('-type', 'splash')


canvas = Canvas(
    window,
    bg = "#0017FF",
    height = 506,
    width = 1012,
    bd = 0,
    highlightthickness = 0
)

canvas.place(x = 0, y = 0)

#--------------LOGO------------------
askuala_img = PhotoImage(
    file=assets("askuala_logo.png"))
logo = canvas.create_image(
    234.0,
    84.0,
    image=askuala_img
)

#--------------BG picture-------------
bg_image = PhotoImage(
    file=assets("login_bg.png"))
    
login_bg = canvas.create_image(
    227.0,
    273.0,
    image=bg_image
)

#---------------right side-------
canvas.create_rectangle(
    469.0,
    0.0,
    1012.0,
    506.0,
    fill="#232B2D",
    outline="")


###############----Entries----###############
entry_image = PhotoImage(
    file=assets("entry_1.png"))


username_bg = canvas.create_image(
    736.0,
    241.0,
    image=entry_image
)
username_entry = Entry(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
username_entry.place(
    x=568.0,
    y=215.0,
    width=336.0,
    height=50.0
)


password_bg = canvas.create_image(
    736.0,
    348.0,
    image=entry_image
)
password_entry = Entry(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0,
    show='*'
)
password_entry.place(
    x=568.0,
    y=322.0,
    width=336.0,
    height=50.0
)


###############----TEXT----###############


canvas.create_text(
    553.0,
    66.0,
    anchor="nw",
    text="Enter your login details",
    fill="#0DA0FF",
    font=("Montserrat Bold", -26)
)

canvas.create_text(
    553.0,
    109.0,
    anchor="nw",
    text="Enter the username and password",
    fill="#CCCCCC",
    font=("Montserrat SemiBold", -16)
)

canvas.create_text(
    553.0,
    130.0,
    anchor="nw",
    text="that was given to you.",
    fill="#CCCCCC",
    font=("Montserrat SemiBold", -16)
)

canvas.create_text(
    567.0,
    191.0,
    anchor="nw",
    text="Username",
    fill="#0DA0FF",
    font=("Montserrat Bold", -14)
)

canvas.create_text(
    567.0,
    298.0,
    anchor="nw",
    text="Password",
    fill="#0DA0FF",
    font=("Montserrat Bold", -14)
)

canvas.create_text(
    115.0,
    431.0,
    anchor="nw",
    text="© Adoniyas & Rediet, 2023",
    fill="#FFFFFF",
    font=("Montserrat Bold", -18)
)


###############----Buttons----###############

#----------------show/hide password------------

hide_pass= True
def toggle():

    global hide_pass
    #if hidepass is true show pass
    if hide_pass:
        password_entry.config(show='')
        show_pass.config(image=hide_pass_img)
        hide_pass = False

    #if hide pass is false hide pass
    else:
        password_entry.config(show='*')
        show_pass.config(image=show_pass_img)
        hide_pass = True

show_pass_img = PhotoImage(
    file=assets("show_pass.png"))
hide_pass_img = PhotoImage(
    file=assets("hide_pass.png"))
show_pass = Button(
    image=show_pass_img,
    borderwidth=0,
    highlightthickness=0,
    command= toggle,
    relief="flat",
    background='#EFEFEF'
)
show_pass.place(
    x=870.0,
    y=329.0,
    width=35.0,
    height=38.0
)


#----------login------------------
login_button_img = PhotoImage(
    file=assets("login_btn.png"))
login_btn_hover_img = PhotoImage(
    file=assets("login_hover.png"))

login_button = Button(
    image=login_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=login,
    relief="flat",
    background='#242B2E',
    activebackground='#242B2E'
)
login_button.place(
    x=673.0,
    y=413.0,
    width=118.0,
    height=39.0
)

def login_hover(e):
    login_button.config(
        image=login_btn_hover_img
    )
def login_leave(e):
    login_button.config(
        image=login_button_img
    )

login_button.bind('<Enter>', login_hover)
login_button.bind('<Leave>', login_leave)


#------------close--------------------

close_button_img = PhotoImage(
    file=assets("close.png"))
close_btn_hover_img = PhotoImage(
    file=assets("close_hover.png"))
close_button = Button(
    image=close_button_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: window.destroy(),
    relief="flat",
    background='#242B2E',
    activebackground='#242B2E'
)
close_button.place(
    x=925.0,
    y=465.0,
    width=79.0,
    height=30.0
)


def close_hover(e):
    close_button.config(
        image=close_btn_hover_img
    )

def close_leave(e):
    close_button.config(
        image=close_button_img
    )

close_button.bind('<Enter>', close_hover)
close_button.bind('<Leave>', close_leave)


#binding the window to the enter button to login 
window.bind('<Return>', lambda event: login())
window.resizable(False, False)
window.mainloop()
