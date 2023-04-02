#==========================================================================
#                      Student Registration System                        #
#==========================================================================
#                             developed by:-                              #
#                          Adoniyas and Rediet                            #
#==========================================================================

from tkinter import *
from pathlib import Path
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from backend import *
from datetime import datetime


ASSETS_PATH = Path(__file__).parent.resolve() / Path("assets")

#initialized the selected id to 0 to check if a row is selected
selected_id = 0

def main():

    #create table in the database
    create_table() #its from the backend

    def select_row(event):
        global selected_id
        global selected_row
        global selected_student
        # style.map('Treeview', background=[('selected', '#575A7B')])

        try:
            selected_row = table.focus()
            values = table.item(selected_row, 'values')
            selected_id = values[0]
            first_name_entry.delete(0, END)
            middle_name_entry.delete(0, END)
            last_name_entry.delete(0, END)
            address_entry.delete(0, END)
            nationality_entry.delete(0, END)
            
            first_name_entry.insert(0, values[1])
            middle_name_entry.insert(0, values[2])
            last_name_entry.insert(0, values[3])
            gender_var.set(values[4])
            date_entry.set_date(values[5])
            address_entry.insert(0, values[6])
            nationality_entry.insert(0, values[7])
            dept_var.set(values[8])

            selected_student = (
                values[1],
                values[2],
                values[3],
                values[4],
                values[5],
                values[6],
                values[7],
                values[8]
            )
        except IndexError:
            pass
            # values = table.item(selected_row, 'values')
            #Unselecting all rows to handle the index error
            # for item in selected_row:
            #     table.selection_remove(item)

        #if a row is selected remove the add button
        if selected_id != 0:
            add_button.place_forget()
        else:
            add_button.place(
            x=26.0,
            y=635.40478515625,
            width=130.0,
            height=43.0
    )

    def check_entries():
        #returns true if the entries are not empty or default
        if (first_name_entry.get() == '' or  
            middle_name_entry.get() == '' or  
            last_name_entry.get() == '' or 
            gender_var.get() == 'Select Gender' or 
            date_entry.get_date()== datetime.now().date() or 
            address_entry.get()== '' or  
            nationality_entry.get()== '' or 
            dept_var.get() == 'Select Department'):

            return False
        else:
            return True

    def empty_field_error_msg():
        messagebox.showerror(title='Error', message='Please Fill All Fields!!!')

    def selection_error_msg():
        messagebox.showerror(title ='Error!!!', message='Please select a student')

    def check_row_selection():

        #if selected id is not 0 then it means arow is selected
        if selected_id == 0:
            return False
        else:
            return True

    def check_date():
        #calculate age and chek if it between 18 and 40
        age = datetime.now().year - date_entry.get_date().year
        if 18 <= age <= 40:
            return True
        else:
            return False

    def refresh_table(sort_by = 'Default'):

        global selected_id
        #clear the table
        for row in table.get_children():
            table.delete(row)
        #reset the selction by setting the student id to 0
        selected_id = 0
        view_command(sort_by)

    def view_command(sort_by ='Default'):

        #view_data() is the data from the database backend which returns rows of the db
        if sort_by == 'Default':
            for row in view_data():
                table.insert('', END, values=row)
        else:
            for row in sort(sort_by):
                table.insert('', END, values=row)

    def add_command():
        global selected_id
        date = datetime.now()

        #check if the entries are not empty
        if check_entries():
            #check the date
            if check_date():
                #insert_data is from the backend
                insert_data(
                            first_name_entry.get().title().strip(),
                            middle_name_entry.get().title().strip(), 
                            last_name_entry.get().title().strip(),
                            gender_var.get(),
                            date_entry.get_date(),
                            address_entry.get().title().strip(),
                            nationality_entry.get().title().strip(),
                            dept_var.get(),
                            date
                            )
                
                #refresh the table to show the new student at the top and refresh and reset entry then show success message
                refresh_table(sort_by='Date')
                reset_entry()
                messagebox.showinfo(title='Sucess', message='Student added sucessfully')
            else:
                messagebox.showerror(title='Error', message='"Age must be between 18-40"')
        else:
            empty_field_error_msg()

    def reset_entry():

        #clear the entries
        first_name_entry.delete(0,END)
        last_name_entry.delete(0,END)
        middle_name_entry.delete(0,END)
        gender_var.set('Select Gender')
        address_entry.delete(0,END)
        date_entry.delete(0,END)
        date_entry.insert(0,'Select Date')
        nationality_entry.delete(0,END)
        dept_var.set('Select Department')

        #if a row is not selected show the add button
        if selected_id != 0:
            add_button.place(
            x=26.0,
            y=635.40478515625,
            width=130.0,
            height=43.0
        )

    def edit_command():

        edited_student = (
            first_name_entry.get().title(),
            middle_name_entry.get().title(), 
            last_name_entry.get().title(),
            gender_var.get(),
            date_var.get(),
            address_entry.get().title(),
            nationality_entry.get().title(),
            dept_var.get()
        )

        #check if a row is selected or not
        if check_row_selection():
            #check if all the entries are filled
            if check_entries():
                # check if a value is not changed
                if selected_student != edited_student:
                    #Update the database
                    update_data(
                                first_name_entry.get().title(),
                                middle_name_entry.get().title(), 
                                last_name_entry.get().title(),
                                gender_var.get(),
                                date_entry.get_date(),
                                address_entry.get().title(),
                                nationality_entry.get().title(),
                                dept_var.get(),
                                selected_id
                                )
                    #Update the treeview
                    refresh_table()
                    messagebox.showinfo(title='Edited', message='Student info edited sucessfully')
                    reset_entry()
                else:
                    messagebox.showwarning(title='Nothing to edit', message='Nothing changed')
            else:
                empty_field_error_msg()
        else:
            selection_error_msg()

    def delete_command():

        #check if row is selected
        if check_row_selection():

            #show a yes or no pop up
            sure = messagebox.askyesno(title='Are you sure??', message='Are you sure you want to delete student?')

            #if the user clicked yes delete the student and refresh the table
            if sure:
                delete_data(selected_id)
                refresh_table()
                reset_entry()
                messagebox.showinfo(title='Deleted', message='Student deleted sucessfully')
        else:
            selection_error_msg()

    def search_command():
        
        #if search entry is not empty search value
        if search_box.get() != '' or gen_search_var.get() != 'Select Gender' or dept_search_var.get() != 'Select Department':
            if search_by.get() == 'Id':
                #search by id
                #store the result and view the result
                result = search_data(id=search_box.get(), search_by = search_by.get())
                view_search_result(result)
            elif search_by.get() == 'First Name':
                #search by first name
                result = search_data(fname=search_box.get(), search_by = search_by.get())
                view_search_result(result)
            elif search_by.get() == 'Middle Name':
                #search by miidle name
                result = search_data(mname=search_box.get(), search_by = search_by.get())
                view_search_result(result)
            elif search_by.get() == 'Last Name':
                #search by last name
                result = search_data(lname=search_box.get(), search_by = search_by.get())
                view_search_result(result)
            elif search_by.get() == 'Gender':
                #search by gender
                result = search_data(gen=gen_search_var.get(), search_by = search_by.get())
                view_search_result(result)
            elif search_by.get() == 'Department':
                #search by department
                result = search_data(dept=dept_search_var.get(), search_by = search_by.get())
                view_search_result(result)
            else:
                #if search by is defaul or all...seratch by all
                result = search_data(all = search_box.get())
                view_search_result(result)

        #if search box is empty sort
        else:
            view_search_result(sort(search_by.get()))


    def view_search_result(data):

        #clear the table
        for row in table.get_children():
            table.delete(row) 

        #check if student is found
        if check_result(data):

        #display the new result
            for row in data:
                table.insert('', END, values=row)


    def check_result(result):
        #check if the result is empty or not
        if result == []:
            return False
        else:
            return True

    def sort(value):

        #Search by value and the corresponding databse value {serachbye: database value}
        db_values = {'Id':'id',
                'First Name': 'First_name',
                'Middle Name': 'Middle_name',
                'Last Name': 'Last_name',
                'Gender':'Gender',
                'Department':'Department',
                'Search By : All':'First_name',
                'All':'First_name',
                'Search By : All':'First_name',
                'Date':'Date_added'                }
        row = sort_data(db_values[value])  #sort_data is from the backend
        return row     

    def clear_search():

        #clear search result and reset search by to its default value
        search_by.set('Search By : All')
        dept_search_var.set('Select Department')
        search_box.delete(0,END)

        #show the search icon
        right_canv.itemconfigure(4, state = 'normal')
        try:
            gen_search_option.destroy()
        except NameError:
            pass

        try:
            dept_search_option.destroy()
        except NameError:
            pass

        reset_entry()
        refresh_table()

    def save_command():

        #show file dialog box and store the path given to save the file
        path = filedialog.asksaveasfilename(initialfile='Students_data.xlsx' ,title="Save file",
                        filetypes=(("xlsx files", "*.xlsx"),("all files", "*.*")), defaultextension=".xlsx")

        #Check if the path is not empty 
        if path != () and path  != '':

            #save the data as excel file on the given path
            save_db(path) #save_db is from the backend
            messagebox.showinfo(title='Error',  message='Saved sucessfully')

    def assets(path):
        #returns the assets path
        return ASSETS_PATH / Path(path)


    window = Tk()
    window.title('Askuala')

    window.geometry("1366x768")
    window.configure(bg = "#0017FF")


    #This the main canvas 
    canvas = Canvas(
        window,
        bg = "#0017FF",
        height = 768,
        width = 1366,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)


   #---------LOGO----------
    askuala_img = PhotoImage(
    file=assets("askuala_logo.png"))
    logo = canvas.create_image(
    234.0,
    80.0,
    image=askuala_img
    )

    #-------TEXTS-----------
    canvas.create_text(
        110.0,
        130.0,
        anchor="nw",
        text="Student Registration Form",
        fill="#FFFFFF",
        font=("Montserrat Bold", -20)
    )

    canvas.create_text(
        33.0,
        206.0,
        anchor="nw",
        text="First Name\n",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )

    canvas.create_text(
        282.0,
        206.0,
        anchor="nw",
        text="Middle Name\n",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )


    canvas.create_text(
        33.0,
        295.0,
        anchor="nw",
        text="Last Name\n",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )


    canvas.create_text(
        282.0,
        295.0,
        anchor="nw",
        text="Gender",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )


    canvas.create_text(
        33.0,
        392.0,
        anchor="nw",
        text="Date Of Birth",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )

    canvas.create_text(
        282.0,
        392.0,
        anchor="nw",
        text="Address",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )


    canvas.create_text(
        33.0,
        481.0,
        anchor="nw",
        text="Nationality",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )


    canvas.create_text(
        282.0,
        481.0,
        anchor="nw",
        text="Department\n",
        fill="#FFFFFF",
        font=("Montserrat Bold", -14)
    )


    ###########----Frames----############

    rightFrm = Frame(window, width= 856, height= 768)
    rightFrm.place(x= 510, y=0)

    tableFrm = Frame(window, width=856, height=486, bg= '#FFFFFF')
    tableFrm.place(x = 510, y =161)

    #********Right Canvas*****************

    right_canv = Canvas(rightFrm, width= 856, height=768, bg="#FFFFFF")
    right_canv.place(x = 0 , y= 0)

    right_canv.create_rectangle(
        0.0,
        118.0,
        856.0,
        124.0,
        fill="#EFEFEF",
        outline="")

    #--------Table and scroller----------

    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri',9)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 10,'bold')) # Modify the font of the headings
    columns = ('ID', 'First Name', 'Middle Name', 'Last Name', 'Gender', 'Date of Birth', 'Address', 'Nationality', 'Department')
    table = ttk.Treeview(
        tableFrm,
        columns= columns,
        show= "headings",
        selectmode='extended',
        style= 'mystyle.Treeview'
        
    )
    table.place(x = 0, y =0, relheight=0.975)

    #Setting up the column heading and id
    for column in columns:
        table.heading(column=column, text= column)

    table.column('ID',stretch=False, width=30, minwidth=20)
    table.column('First Name',stretch=False, width=102, minwidth=20)
    table.column('Last Name',stretch=False, width=102, minwidth=20)
    table.column('Middle Name',stretch=False, width=102, minwidth=20)
    table.column('Gender',stretch=False, width=60, minwidth=20, anchor="center")
    table.column('Date of Birth',stretch=False, width=100, minwidth=20, anchor='center')
    table.column('Address',stretch=False, width=80, minwidth=20)
    table.column('Nationality',stretch=False, width=85, minwidth=20)
    table.column('Department',stretch=False, width=182, minwidth=20)

    #bind the table to select_row function to enable selcting a row
    table.bind('<<TreeviewSelect>>', select_row)


    #vertical scroll bar (vsb)
    vsb = Scrollbar(tableFrm, command=table.yview, orient="vertical")
    vsb.place(relx = 1, rely= 0, relheight=0.975, anchor='ne')

    #horizontal scroll var (hsb)
    hsb = Scrollbar(tableFrm, orient='horizontal', command= table.xview)
    hsb.place(relx= 1, rely = 0.975, relwidth=1, anchor='ne')

    table.config(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

    #----------------------------------------------------------------


    ###################---ENTRIES----#####################

    entry_image = PhotoImage(
        file=assets("entry_1.png"))


    #----------first name----------------------

    first_name_entry_bg = canvas.create_image(
        129.5,
        250.0,
        image=entry_image
    )
    first_name_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    first_name_entry.place(
        x=41.0,
        y=230.0,
        width=177.0,
        height=38.0
    )


    #-------------middle name-----------------


    middle_name_entry_bg = canvas.create_image(
        379.5,
        250.0,
        image=entry_image
    )
    middle_name_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    middle_name_entry.place(
        x=290.0,
        y=230.0,
        width=179.0,
        height=38.0
    )

    #-------------last name-----------------

    last_name_entry_bg = canvas.create_image(
        129.5,
        339.0,
        image=entry_image
    )
    last_name_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    last_name_entry.place(
        x=41.0,
        y=319.0,
        width=177.0,
        height=38.0
    )

    #-------------gender-----------------

    gender_entry_bg = canvas.create_image(
        379.5,
        339.0,
        image=entry_image
    )

    gender_var = StringVar()
    gender_var.set('Select Gender')
    gender_option = OptionMenu(window, gender_var, 'Male', 'Female')
    gender_option.config(
        bd=0,
        bg='#FFFFFF',
        highlightthickness=0,
        cursor='hand1'
    )
    gender_option.place(
        x=290.0,
        y=320.0,
        width=180.0,
        height=38.0
    )

    #-----------date of birth-----------------

    dob_entry_bg = canvas.create_image(
        129.5,
        436.0,
        image=entry_image
    )

    date_var = StringVar()
    date_entry = DateEntry(window,
                          textvariable = date_var, 
                          selectmode = 'day', 
                          date_pattern = 'y-mm-dd', 
                          cursor = 'hand1', 
                          background = 'blue',
                          foreground ='yellow' ,
                          calendar_cursor='hand1'
                          )
    date_entry.place(
        x=41.0,
        y=416.0,
        width=177.0,
        height=39.0 
    )

    #clear todays date and show select date
    date_entry.delete(0,END)
    date_entry.insert(0,'Select Date')



    #---------address-------------

    address_entry_bg = canvas.create_image(
        379.5,
        436.0,
        image=entry_image
    )
    address_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    address_entry.place(
        x=290.0,
        y=416.0,
        width=179.0,
        height=38.0
    )

    #---------nationality----------

    nationality_entry_bg = canvas.create_image(
        129.5,
        524.5,
        image=entry_image
    )
    nationality_entry = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    nationality_entry.place(
        x=41.0,
        y=506.0,
        width=177.0,
        height=39.0
    )


    #--------department--------

    department_entry_bg = canvas.create_image(
        379.5,
        524.5,
        image=entry_image
    )

    dept_var = StringVar()
    dept_var.set('Select Department')

    department_choice = OptionMenu(
                                    window,
                                    dept_var,
                                    'Software Engineering(Bsc)',
                                    'IT and Systems(Bsc)',
                                    'IT management(Msc)'
                                    )                                

    department_choice.place(
        x=290.0,
        y=506.0,
        width=180.0,
        height=39.0
    )

    department_choice.config(
        bd = 0,
        bg='#FFFFFF',
        highlightthickness=0,
        cursor= 'hand1'
    )



    #----------9--------------

    def show_options(event):
        
        #clear the search box
        search_box.delete(0, END)
        #if there is a selection reset entry
        if selected_id != 0:
            reset_entry()

        #sort the table by search_by
        refresh_table(search_by.get())


        global gen_search_option
        global dept_search_option


        #if search by gender is selected
        if search_by.get() == 'Gender':

            #hide the search icon
            right_canv.itemconfigure(4, state = 'hidden')
            
            #destroy department entry if it exist
            try:
                dept_search_var.set('Select Department')
                dept_search_option.destroy()
            except NameError:
                print('x')

            gen_search_option = OptionMenu(rightFrm, gen_search_var, 'Male', 'Female', command=lambda e: search_command())

            gen_search_option.config(
                bd=0,
                bg='#FFFFFF',
                fg='#000000',
                highlightthickness=0
            )

            gen_search_option.place(
                    x=323.0,
                    y=54.0,
                    width=173.0,
                    height=38.0
            )


        #if search by department is selected
        elif search_by.get() == 'Department':
            
            #hide the search icon 
            right_canv.itemconfigure(4, state= 'hidden')

            #destroy gender entry if it exist
            try:
                gen_search_var.set('Select Gender')
                gen_search_option.destroy()
            except NameError:
                pass
            dept_search_option = OptionMenu(
                                            rightFrm,
                                            dept_search_var,
                                            'Software Engineering(Bsc)',
                                            'IT and Systems(Bsc)',
                                            'IT management(Msc)',
                                            command=lambda e: search_command()
                                            )
            
            dept_search_option.config(
                bd=0,
                bg='#FFFFFF',
                fg='#000000',
                highlightthickness=0
            )        

            dept_search_option.place(
                x=323.0,
                y=54.0,
                width=173.0,
                height=38.0
            )
        
        #if neither of search by gender or department is selected
        else:

            #Show the search icon in the search box
            right_canv.itemconfigure(4, state = 'normal')
            gen_search_var.set('Select Gender')
            dept_search_var.set('Select Department')

            #reset gender and department variables to their defaul and destroy them
            try:
                gen_search_option.destroy()
            except NameError:
                pass
            try:
                dept_search_option.destroy()
            except NameError:
                pass

    entry_image_2 = PhotoImage(
        file=assets("entry_2.png"))

    serach_by_bg = right_canv.create_image(
        187,
        73,
        image = entry_image_2
        
    )   

    search_by = StringVar()
    search_by.set('Search By : All')

    gen_search_var = StringVar()
    gen_search_var.set('Select Gender')

    dept_search_var = StringVar()
    dept_search_var.set('Select Department')


    search_by_option = OptionMenu(
                    rightFrm,
                    search_by,
                    'Id',
                    'First Name',
                    'Middle Name',
                    'Last Name',
                    'Gender',
                    'Department',
                    'All',
                    command= show_options
                    )

    search_by_option.place(
        x=101.0,
        y=54.0,
        width=173.0,
        height=38.0

    )


    search_by_option.config(
        bd = 0,
        bg='#FFFFFF',
        highlightthickness=0,
        highlightcolor='#FFFFFF'
    )

    #--------10---Search box-------------

    search_box_bg = right_canv.create_image(
        410,
        73,
        image = entry_image_2
    )


    search_icon_img = PhotoImage(
    file=assets("search_icon.png"))
    search_icon_hov_img = PhotoImage(
    file=assets("search_icon_hov.png"))
    search_icon = right_canv.create_image(
    329,
    73,
    image=search_icon_img
    )


    search_box_var = StringVar()
    search_box = Entry(
        rightFrm,
        textvariable= search_box_var,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )

    search_box.place(
        x=345.0,
        y=54.0,
        width=145.0,
        height=38.0
    )

    #change the colorof the serach icon when focusing on it
    def focus_in(e):
        right_canv.itemconfigure(4, image = search_icon_hov_img)
    def focus_out(e):
        right_canv.itemconfigure(4, image = search_icon_img)

    #change the color of serach icon when the cursor is on it
    search_box.bind('<FocusIn>', focus_in)
    search_box.bind('<FocusOut>', focus_out)

    def search_auto(*argz):
        search_command()

    #Trace each character written in the search box and auto search
    search_box_var.trace('w', search_auto)

    ###################################---Buttons---##################################

    #----------ADD BUTTON----------

    #change the button's appearance when hovering on it
    def add_hover(e):
        add_button.config(
            image= add_hover_image
        )

    def add_leave(e):
        add_button.config(
            image=add_button_image
        )

    add_button_image = PhotoImage(
        file=assets("add_btn.png"))

    add_hover_image = PhotoImage(
        file=assets('add_hover.png'))

    add_button = Button(
        image=add_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=add_command,
        relief="flat",
        background='#0017FF',
        activebackground='#0017FF'
    )
    add_button.place(
        x=26.0,
        y=635.40478515625,
        width=130.0,
        height=43.0
    )

    #bind the button to add a hover effect
    add_button.bind('<Enter>', add_hover)
    add_button.bind('<Leave>', add_leave)

    #---------- edit-------------------

    def edit_hover(e):
        edit_button.config(
            image= edit_hover_image
        )

    def edit_leave(e):
        edit_button.config(
            image=edit_button_image
        )

    edit_button_image = PhotoImage(
        file=assets("edit_button.png"))

    edit_hover_image = PhotoImage(
        file=assets('edit_hover.png'))

    edit_button = Button(
        image=edit_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=edit_command,
        relief="flat",
        background='#0017FF',
        activebackground='#0017FF'
    )
    edit_button.place(
        x=183.3814697265625,
        y=635.40478515625,
        width=130.0,
        height=43.0
    )

    #bind the button to add a hover effect
    edit_button.bind('<Enter>', edit_hover)
    edit_button.bind('<Leave>', edit_leave)

    #----------reset-------------------

    def reset_hover(e):
        reset_button.config(
            image=reset_hover_image
        )

    def reset_leave(e):
        reset_button.config(
            image=reset_button_image
        )

    reset_button_image = PhotoImage(
        file=assets("reset_button.png"))

    reset_hover_image = PhotoImage(
        file=assets('reset_hover.png'))

    reset_button = Button(
        image=reset_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=reset_entry,
        relief="flat",
        background='#0017FF',
        activebackground='#0017FF'
    )
    reset_button.place(
        x=340.76318359375,
        y=635.40478515625,
        width=130.0,
        height=43.0
    )

    #bind the button to add a hover effect
    reset_button.bind('<Enter>', reset_hover)
    reset_button.bind('<Leave>', reset_leave)


    #-------SAVE DATA button------------------------

    def save_hover(e):
        save_button.config(
            image = save_hover_image
        )

    def save_leave(e):
        save_button.config(
            image=save_button_image
        )

    save_button_image = PhotoImage(
        file=assets("export_data.png"))

    save_hover_image = PhotoImage(
        file=assets('export_hover.png'))

    save_button = Button(
        rightFrm,
        image=save_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=save_command,
        relief="flat",
        background='#FFFFFF',
        activebackground='#FFFFFF'
    )
    save_button.place(
        x=700.26,
        y=53.472412109375,
        width=131.0,
        height=43.0
    )

    save_button.bind('<Enter>', save_hover)
    save_button.bind('<Leave>', save_leave)


    #---------clear button----------


    def clear_hover(e):
        clear_button.config(
            image=clear_hover_image
        )

    def clear_leave(e):
        clear_button.config(
            image=clear_button_image
        )

    clear_button_image = PhotoImage(
        file=assets("reset_search.png"))

    clear_hover_image = PhotoImage(
        file=assets('reset_search_hov.png'))

    clear_button = Button(
        rightFrm,
        image=clear_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=clear_search,
        relief="flat",
        background='#FFFFFF',
        activebackground='#FFFFFF'
    )
    clear_button.place(
        x=550.26,
        y=53.472412109375,
        width=130.0,
        height=43.0
    )

    clear_button.bind('<Enter>', clear_hover)
    clear_button.bind('<Leave>', clear_leave)


    #----------Delete button------------------

    def delete_hover(e):
        delete_button.config(
            image = delete_hover_image
        )

    def delete_leave(e):
        delete_button.config(
            image= delete_button_image
        )

    delete_button_image = PhotoImage(
        file=assets("delete_btn.png"))

    delete_hover_image = PhotoImage(
        file=assets('delete_hover.png'))

    delete_button = Button(
        rightFrm,
        image=delete_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=delete_command,
        relief="flat",
        background='#FFFFFF',
        activebackground='#FFFFFF'
    )
    delete_button.place(
        x=700.26,
        y=685.0,
        width=130.0,
        height=43.0
    )

    delete_button.bind('<Enter>', delete_hover)
    delete_button.bind('<Leave>', delete_leave)


    #----------Close button--------------------------

    def close_hover(e):
        close_button.config(
            image = close_hover_image
        )

    def close_leave(e):
        close_button.config(
            image=close_button_image
        )

    close_button_image = PhotoImage(
        file=assets("close_btn.png"))

    close_hover_image = PhotoImage(
        file=assets('close_hover.png'))

    close_button = Button(
        rightFrm,
        image=close_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: window.destroy(),
        relief="flat",
        background='#FFFFFF',
        activebackground='#FFFFFF'
    )
    close_button.place(
        x=550.26,
        y=685.0,
        width=130.0,
        height=43.0
    )

    close_button.bind('<Enter>', close_hover)
    close_button.bind('<Leave>', close_leave)


    #-----------------------------------------------
    #run the view command to show registered students eerytime the program runs
    view_command()
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    main()