from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
conn = sqlite3.connect("storage.db")
cursor = conn.cursor()
cursor.execute(

"""
    CREATE TABLE IF NOT EXISTS storage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
"""
)


def start_button(back):
    global ascii_text_ch,listbox,back_button

    if back == "new_entry":
        ascii_text_new.place_forget()
        website_name.place_forget()
        website_entry.place_forget()
        user_name.place_forget()
        username_entry.place_forget()
        password_name.place_forget()
        password_entry.place_forget()
        back_button_save.place_forget()
        button_4.place_forget()
    if back == "edit_entry":
        ascii_text_ch.place_forget()
        listbox.place_forget()
        back_button.place_forget()
        scrollbar.place_forget()
    global ascii_text,welcome_text,button_imag,button_1,button_2,button_3,ascii_text_hi
    ascii_text.place_forget() 
    welcome_text.place_forget()
    button_imag.place_forget() 

    ascii_art_hi = """
     _   _ _____   _ 
    | | | |_   _| | |
    | |_| | | |   | |
    |  _  | | |   | |
    | | | |_| |_  |_|
    \_| |_/\___/  (_)
                     
                     
    """

    button_1.place(x=150, y=300)
    button_2.place(x=150, y=400)
    button_3.place(x=150, y=500)

    ascii_text_hi = Label(root, text=ascii_art_hi, font=("Courier", 10), bg="#2a0f46", fg="white")
    ascii_text_hi.place(x=170, y=70)

edit_window = None
def open_edit_window(selected_website):
    global edit_window
    if edit_window is not None and edit_window.winfo_exists():
        # If an edit window is already open, focus on it instead of opening a new one
        edit_window.focus()
        return

    edit_window = Toplevel()
    edit_window.title("Edit Entry")

    cursor.execute("SELECT website_name, username, password FROM storage WHERE website_name=?", (selected_website,))
    data = cursor.fetchone()

    new_website_name = StringVar(value=data[0])
    new_username = StringVar(value=data[1])
    new_password = StringVar(value=data[2])

    website_entry = Entry(edit_window, textvariable=new_website_name)
    username_entry = Entry(edit_window, textvariable=new_username)
    password_entry = Entry(edit_window, textvariable=new_password)

    website_label = Label(edit_window, text="Website Name:")
    username_label = Label(edit_window, text="Username:")
    password_label = Label(edit_window, text="Password:")

    def update_record():
        new_data = (new_website_name.get(), new_username.get(), new_password.get(), selected_website)
        cursor.execute("UPDATE storage SET website_name=?, username=?, password=? WHERE website_name=?", new_data)
        conn.commit()
        messagebox.showinfo("Success", "Updated Successfully")
        edit_window.destroy()

    update_button = Button(edit_window, text="Update", command=update_record)

    website_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    website_entry.grid(row=0, column=1, padx=10, pady=5)
    username_entry.grid(row=1, column=1, padx=10, pady=5)
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    update_button.grid(row=3, column=1, pady=10)
    edit_window.protocol("WM_DELETE_WINDOW", on_edit_window_close)

def on_edit_window_close():
    global edit_window
    if messagebox.askokcancel("Quit", "Do you want to close this window?"):
        edit_window.destroy()
        edit_window = None  # Reset the variable to None when the window is closed


def save_exit():
    global root
    cursor.execute("SELECT * FROM storage")
    data = cursor.fetchall()

    file_path = os.path.join(os.getcwd(), "exported_data.txt")

    with open(file_path, 'w') as file:
        for entry in data:
            file.write(f"Website: {entry[1]}\n")
            file.write(f"Username: {entry[2]}\n")
            file.write(f"Password: {entry[3]}\n")
            file.write("\n")

    conn.close()
    root.destroy()

def change_entry():

    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    ascii_text_hi.place_forget()

    global ascii_text_ch,listbox,back_button,scrollbar
    ascii_change_entry = """
 _____  _   _   ___   _   _ _____  _____      _____ _   _ _____________   __
/  __ \| | | | / _ \ | \ | |  __ \|  ___|    |  ___| \ | |_   _| ___ \ \ / /
| /  \/| |_| |/ /_\ \|  \| | |  \/| |__      | |__ |  \| | | | | |_/ /\ V / 
| |    |  _  ||  _  || . ` | | __ |  __|     |  __|| . ` | | | |    /  \ /  
| \__/\| | | || | | || |\  | |_\ \| |___     | |___| |\  | | | | |\ \  | |  
 \____/\_| |_/\_| |_/\_| \_/\____/\____/     \____/\_| \_/ \_/ \_| \_| \_/  
"""


    ascii_text_ch= Label(root, text=ascii_change_entry, font=("Courier", 8), bg="#2a0f46", fg="white")
    ascii_text_ch.place(x=20, y=70)

    # Set the background color of the Listbox
    listbox = Listbox(root, width=33, height=12, font=("", 17, "bold"), bg="#3C1C5E", fg="white")
    listbox.place(x=10, y=200)

    scrollbar = Scrollbar(root, orient=VERTICAL, command=listbox.yview)
    scrollbar.place(x=540, y=200, height=350)

    listbox.config(yscrollcommand=scrollbar.set)

    cursor.execute("SELECT website_name FROM storage")
    website_names = cursor.fetchall()
    for website_name in website_names:
        listbox.insert(END, website_name[0])

    def on_mousewheel(event):
        listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")

    listbox.bind("<MouseWheel>", on_mousewheel)

    def on_listbox_click(event):
        selected_index = listbox.curselection()
        if selected_index:
            selected_website = listbox.get(selected_index)
            open_edit_window(selected_website)

    listbox.bind("<Button-1>", on_listbox_click)
    # Back button
    back_button = Button(root, text="Back",cursor="hand2" ,command=lambda:start_button(back='edit_entry'))
    back_button.place(x=450, y=580)

def new_entry_save():
    print(web_name.get())
    print(username.get())
    print(password.get())
    website_name_value = web_name.get()
    username_value = username.get()
    password_value = password.get()

    cursor.execute('''INSERT INTO storage (website_name, username, password) VALUES (?, ?, ?)''', (website_name_value, username_value, password_value))
    conn.commit()
    messagebox.showinfo("Success", "New Entry Stored Successfully!.")

    web_name.set('')
    username.set('')
    password.set('')
    
def Save_new_entry():
    
    global root,button_1,button_2,button_3,button_4
    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    ascii_text_hi.place_forget()

    ascii_new_entry = """
_   _  _____ _    _      _____ _   _ _____________   __
| \ | ||  ___| |  | |    |  ___| \ | |_   _| ___ \ \ / /
|  \| || |__ | |  | |    | |__ |  \| | | | | |_/ /\ V / 
| . ` ||  __|| |/\| |    |  __|| . ` | | | |    /  \ /  
| |\  || |___\  /\  /    | |___| |\  | | | | |\ \  | |  
\_| \_/\____/ \/  \/     \____/\_| \_/ \_/ \_| \_| \_/  
                                                    
                                                    
"""
    global web_name,username,password, ascii_text_new, website_name, website_entry, user_name,username_entry,password_name,password_entry,back_button_save
    web_name = StringVar()
    username = StringVar()
    password = StringVar()
    ascii_text_new = Label(root, text=ascii_new_entry, font=("Courier", 10), bg="#2a0f46", fg="white")
    ascii_text_new.place(x=80, y=70)
    website_name = Label(root, text=f"Website", fg="white",font=("Arial", 20,"bold"), bg="#2A0F46")
    website_name.place(x=60,y=230)
    website_entry=Entry(root,font=("Arial", 16,"bold"),width=25, textvariable=web_name)
    website_entry.place(x=220,y=235)
    user_name = Label(root, text=f"Username", fg="white",font=("Arial", 20,"bold"), bg="#2A0F46")
    user_name.place(x=60,y=300)
    username_entry = Entry(root,font=("Arial", 16,"bold"),width=25, textvariable=username)
    username_entry.place(x=220,y=305)
    password_name = Label(root, text=f"Password", fg="white",font=("Arial", 20,"bold"), bg="#2A0F46")
    password_name.place(x=60,y=370)
    password_entry = Entry(root,font=("Arial", 16,"bold"),width=25, textvariable=password)
    password_entry.place(x=220,y=375)
    
    button_4.place(x=250, y=470)
    back_button_save = Button(root, text="Back",cursor="hand2" ,command=lambda:start_button(back='new_entry'))
    back_button_save.place(x=480, y=20)


def welcomeScreen():
    global root,frame_label,ascii_text,welcome_text,button_imag,button_1,button_2,button_3,button_4
    root = Tk()
    root.geometry("558x650")
    root.title("Secure App")
    # Set the fixed size of the window
    root.minsize(558, 650)
    root.maxsize(558, 650)

    ascii_art = """
_    _ _____ _     _____ ________  ___ _____ 
| |  | |  ___| |   /  __ \  _  |  \/  ||  ___|
| |  | | |__ | |   | /  \/ | | | .  . || |__  
| |/\| |  __|| |   | |   | | | | |\/| ||  __| 
\  /\  / |___| |___| \__/\ \_/ / |  | || |___ 
 \/  \/\____/\_____/\____/\___/\_|  |_/\____/ 
                    

"""

    img = Image.open("background.png")
    frame_photo = ImageTk.PhotoImage(img)

    frame_label = Label(root, image=frame_photo, border=2, bg="black")
    frame_label.pack(fill=BOTH, expand=True)

    ascii_text = Label(root, text=ascii_art, font=("Courier", 10), bg="#2a0f46", fg="white")
    ascii_text.place(x=100, y=70)

    welcome_text = Label(root, text="Welcome to Secure Pass", font=("Arial", 25, "bold"), bg="#2A0F46", fg="white")
    welcome_text.place(x=100, y=220)

    img_button = Image.open("button_start.png")

    img_button = ImageTk.PhotoImage(img_button)
    img_label = Label(image=img_button)
    button_imag = Button(root, image=img_button, command=lambda:start_button(back=False), relief="flat", bd=0, highlightthickness=0,
                    borderwidth=0, bg="#2a0f46", cursor="hand2")

    button_imag.place(x=170, y=350)
    img_button_1 = Image.open("button_save-a-new-entry.png")
    img_button_1 = img_button_1.resize((260, 70), Image.Resampling.LANCZOS)

    img_button_1 = ImageTk.PhotoImage(img_button_1)
    button_1 = Button(root, image=img_button_1, relief="flat", bd=0, highlightthickness=0, borderwidth=0,
                        bg="#2a0f46", cursor="hand2", command=Save_new_entry)
    img_button_2 = Image.open("button_edit-entry.png")
    img_button_2 = ImageTk.PhotoImage(img_button_2)
    button_2 = Button(root, image=img_button_2, relief="flat", bd=0, highlightthickness=0, borderwidth=0,
                        bg="#2a0f46", cursor="hand2", command=change_entry)
    img_button_3 = Image.open("button_save-exit.png")
    img_button_3 = ImageTk.PhotoImage(img_button_3)
    button_3 = Button(root, image=img_button_3, relief="flat", bd=0, highlightthickness=0, borderwidth=0,
                        bg="#2a0f46", cursor="hand2",command=save_exit)

    img_button_4 = Image.open("button_save.png")
    img_button_4 = img_button_4.resize((100, 40), Image.Resampling.LANCZOS)

    img_button_4 = ImageTk.PhotoImage(img_button_4)
    button_4 = Button(root, image=img_button_4, relief="flat", bd=0, highlightthickness=0, borderwidth=0, bg="#2a0f46", cursor="hand2",command=new_entry_save)
    root.mainloop()

welcomeScreen()