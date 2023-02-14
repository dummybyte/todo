# importing the required modules  
import tkinter as tk            # importing the tkinter module as tk  
from tkinter import ttk         # importing the ttk module from the tkinter library  
from tkinter import messagebox  # importing the messagebox module from the tkinter library  
from tkinter import Grid
import sqlite3 as sql           # importing the sqlite3 module as sql  

# defining an empty list  
tasks = []
task_buttons = []
task_labels = []

task_font_color_code = "#fdfefe"
window_bg_color_code = "#454545"
button_bg_color_code = "#3d3c3e"
button_highlight_color_code = "#454545"
task_field_bg_color_code = "#2A7BDE"
text_font = ("Roboto Bold", "12")


# defining the function to add tasks to the list  
def add_task(event):  
    # getting the string from the entry field  
    task_string = task_field.get()  
    # checking whether the string is empty or not  
    if len(task_string) == 0:  
        # displaying a message box with 'Empty Field' message  
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:  
        # adding the string to the tasks list  
        tasks.append(task_string)  
        # using the execute() method to execute a SQL statement  
        the_cursor.execute('insert into tasks values (?)', (task_string,))  
        # calling the function to update the list  
        list_update()  
        # deleting the entry in the entry field  
        task_field.delete(0, 'end')


# defining the function to delete a task from the list  
def delete_task(the_value):  
    try:  
        if the_value in tasks:  
            # removing the task from the list  
            tasks.remove(the_value)
            
            list_update()
            # using the execute() method to execute a SQL statement  
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:  
        # displaying the message box with 'No Item Selected' message for an exception  
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')  

# def button_enter(event):
#     event.widget['background'] = button_highlight_color_code

# def button_leave(event):
#     event.widget['background'] = button_highlight_color_code


def list_update():
    for widget in task_buttons:
        widget.destroy()
    task_pos_y = 10
    for task in tasks:
        task_button = tk.Button(
            main_frame,
            text = task,
            font= text_font,
            width = 40,
            bg = button_bg_color_code,
            fg = task_font_color_code,
            border=0,
            borderwidth=0,
            highlightcolor=button_highlight_color_code,
            highlightbackground=button_highlight_color_code,
            command = lambda x=task: delete_task(x)
        )
        task_button.pack()
        task_button.grid(row=0,column=0,sticky="NSEW")
        task_button.place(x = 0, y = task_pos_y)
        task_buttons.append(task_button)
        task_pos_y = task_pos_y + 50
    
    
# function to retrieve data from the database  
def retrieve_database():  
    # using the while loop to iterate through the elements in the tasks list  
    while(len(tasks) != 0):  
        # using the pop() method to pop out the elements from the list  
        tasks.pop()  
    # iterating through the rows in the database table  
    for row in the_cursor.execute('select title from tasks'):  
        # using the append() method to insert the titles from the table to the list  
        tasks.append(row[0])


# main function  
if __name__ == "__main__":  
    # creating an object of the Tk() class  
    guiWindow = tk.Tk()  
    # setting the title of the window  
    guiWindow.title("Simple Todo")  
    # setting the geometry of the window  
    guiWindow.geometry("750x750")

    # # disabling the resizable option  
    guiWindow.resizable(0, 0)  
    # setting the background color to #FAEBD7  
    guiWindow.configure(bg = window_bg_color_code)  

        # using the connect() method to connect to the database  
    the_connection = sql.connect('listOfTasks.db')  
    # creating an object of the cursor class  
    the_cursor = the_connection.cursor()  
    # using the execute() method to execute a SQL statement  
    the_cursor.execute('create table if not exists tasks (title text)')  

    main_frame = tk.Frame(guiWindow, bg = window_bg_color_code)
    main_frame.pack(side="bottom", expand=True, fill="both")

    
    
    task_field = tk.Entry(  
        main_frame,  
        font = text_font,  
        width = 40,
        foreground = task_font_color_code,
        background = button_bg_color_code,
        border=0,
        borderwidth=0,
        highlightbackground=task_field_bg_color_code,
        highlightcolor=task_field_bg_color_code,
    )
    task_field.place(x = 0, y = 700)  
    task_field.bind('<Return>', add_task)

    retrieve_database()  
    list_update()  
    # using the mainloop() method to run the application  
    guiWindow.mainloop()  
    # establishing the connection with database  
    the_connection.commit()  
    the_cursor.close()  