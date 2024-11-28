from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
import time
import datetime
import re
from pathlib import Path
from tkcalendar import DateEntry
import os
import pickle
import sqlite3
from tkinter import colorchooser

"""
    function to be add

    1. Entry with pre-populated data
    2. Request book
    3. Recycle bin 
    4. 


"""

db = sqlite3.connect("Lib_Management.sqlite")
# r = r"(^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]
# |1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$)"

r = r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"


# r = r"^(0[1-9]|[12][0-9]|3[01])[- /.] (0[1-9]|1[012])[- /.] (19|20)\d\d$"


def get_binary_img(path):
    with open(path, 'rb') as f:
        binary_data = f.read()

    return binary_data


def get_img(b_data, filename):
    with open(filename, 'wb') as f:
        f.write(b_data)


def get_settings() -> dict:
    cwd = os.getcwd()
    file = cwd + r'\settings.pickle'
    setting_file = Path(file)
    if setting_file.is_file():
        with open('settings.pickle', 'br') as fp:
            try:
                return pickle.load(fp)
            except EOFError:
                return dict()
    else:
        settings = {
            'screen_state': 'fullscreen',
            'primary_bg_color': '#28282B',
            'secondary_bg_color': '#303841',
            'lab_heading_font': 'Lucida 20',
            'primary_font': 'Helvetica 12',
            'btn_primary_bg_color': '#FFFFFF',
            'btn_active_bg_color': '#28282B',
            'btn_font': 'Helvetica 12',
            'btn_foreground': '#28282B',
            'btn_active_foreground': '#FFFFFF',
            'lab_foreground': '#FFFFFF',
            'clock_font': 'Helvetica 15',
            'clock_foreground': '#28282B',
            'clock_background': '#FFFFFF',
        }
        # Please Delete < settings.pickle > after editing settings-dict
        setting_file = 'settings.pickle'
        with open(setting_file, 'bw') as fp:
            pickle.dump(settings, fp, protocol=0)
        return settings


def change_settings(setting_name: str, new_value: str):
    cwd = os.getcwd()
    file = cwd + r'\settings.pickle'
    setting_file = Path(file)
    if setting_file.is_file():
        try:
            with open('settings.pickle', 'br') as fp:
                settings = pickle.load(fp)
                settings[setting_name] = new_value

            with open('settings.pickle', 'bw') as fp1:
                pickle.dump(settings, fp1)

        except (EOFError, ValueError):
            print("Setting could not be found")
    else:
        return None


def show_message(message: str, message_type: str, title="Title"):
    """
        This function
    :param message: What message you want to display on the screen
    :param message_type: Type of message
    :param title: Title for the message box
    :return: None
    """
    if message_type == "showinfo":
        messagebox.showinfo(title, message)
    elif message_type == "showwarning":
        messagebox.showwarning(title, message)
    elif message_type == "showerror":
        messagebox.showerror(title, message)
    elif message_type == "askquestion":
        messagebox.askquestion(title, message)
    elif message_type == "askokcancel":
        messagebox.askokcancel(title, message)
    elif message_type == "askyesno":
        messagebox.askyesno(title, message)
    elif message_type == "askretrycancel":
        messagebox.askretrycancel(title, message)


def get_conformation(message: str) -> bool:
    ans = askyesno(title='Confirmation', message=message)
    return ans


class AppTk:
    def __init__(self, master):
        self.admin_nm = None
        self.settings = get_settings()
        self.master = master
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.master.geometry(f'{self.screen_width}x{self.screen_height}')
        self.master.title("Library System_1.1.1")
        self.master.configure(bg=self.settings['primary_bg_color'])
        # self.master.attributes('-fullscreen', True)
        self.welcome_screen()

        # global type manage_book variables
        self.frame_add_book = None
        self.frame_change_details = None
        self.frame_remove_book = None

        # global type manage_student variables
        self.frame_add_student = None
        self.frame_change_student_details = None
        self.frame_remove_student = None

        # ISBN number for only change_details section for auto refresh
        self.isbn_change_details = None

        self.back_img = PhotoImage(file=r"C:\My_Data\Projects\Library_Management_1.5\back_img.png")

    # ------------------------------------------- Heading functionalites -------------------------------------------- #

    def main_logo(self):
        frame_logo = Frame(self.master, background='#ffffff')
        frame_logo.pack(fill=X)
        Label(frame_logo, text='Library Manager', font='Helvetica 20', background='#ffffff',
              foreground='#303841').pack(anchor=W, pady=5, padx=10)

    def date_time_frame(self):
        frame_date_time = Frame(self.master, background=self.settings['clock_background'])
        frame_date_time.pack(fill=X, anchor=S, side=BOTTOM)

        frame_inside = Frame(frame_date_time, background=self.settings['clock_background'])
        frame_inside.pack(anchor=E)

        def get_date_time():
            hour = time.strftime("%I")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            am_pm = time.strftime("%p")
            day = time.strftime("%A")
            date = datetime.datetime.now()
            date = str(date)[:10]

            # rearranging date -------------------------------

            year = date[:4]
            month = date[5:7]
            date = date[8:]

            date = date + '-' + month + '-' + year

            lab_time.config(text=hour + ":" + minute + ":" + second + ":" + am_pm)
            lab_time.after(1000, get_date_time)

            lab_day.config(text=day)

            lab_date.config(text=date)

        lab_time = Label(frame_inside, text="", font=self.settings['clock_font'],
                         foreground=self.settings['clock_foreground'], background=self.settings['clock_background'])
        lab_time.grid(row=0, column=0, padx=5)

        lab_day = Label(frame_inside, text="", font=self.settings['clock_font'],
                        foreground=self.settings['clock_foreground'], background=self.settings['clock_background'])
        lab_day.grid(row=0, column=1, padx=5)

        lab_date = Label(frame_inside, text="", font=self.settings['clock_font'],
                         foreground=self.settings['clock_foreground'], background=self.settings['clock_background'])
        lab_date.grid(row=0, column=2, padx=5)

        get_date_time()

    # This function is to quit the whole software.
    def quit_program(self):
        if get_conformation('Do you really want to quit'):
            self.master.destroy()

    # --------------------------------------------- Login functionalities ------------------------------------------- #

    def welcome_screen(self):
        """
                    This method creates multiple frames to welcome user(admin)
                :return: None
                """
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()
        frame_options = Frame(self.master, background=self.settings['primary_bg_color'])
        frame_options.pack(pady=self.screen_height // 5)

        def toggle_screen(e):
            """
            type e: For internal working
            """
            if self.settings['screen_state'] == 'fullscreen':
                self.master.attributes('-fullscreen', False)
                self.settings['screen_state'] = 'non_fullscreen'
            else:
                self.master.attributes('-fullscreen', True)
                self.settings['screen_state'] = 'fullscreen'

        self.master.bind('<F11>', toggle_screen)

        Button(frame_options, text='Login', font=self.settings['primary_font'],
               activeforeground=self.settings['btn_active_foreground'],
               activebackground=self.settings['btn_active_bg_color'],
               background=self.settings['btn_primary_bg_color'],
               command=self.login)
        Button(frame_options, text='Create Administrator', font=self.settings['primary_font'],
               activeforeground=self.settings['btn_active_foreground'],
               activebackground=self.settings['btn_active_bg_color'],
               background=self.settings['btn_primary_bg_color'],
               command=self.create_admin)
        Button(frame_options, text='Settings', font=self.settings['primary_font'],
               activeforeground=self.settings['btn_active_foreground'],
               activebackground=self.settings['btn_active_bg_color'],
               background=self.settings['btn_primary_bg_color'],
               command=self.edit_settings)
        Button(frame_options, text='Contact Us', font=self.settings['primary_font'],
               activeforeground=self.settings['btn_active_foreground'],
               activebackground=self.settings['btn_active_bg_color'],
               background=self.settings['btn_primary_bg_color'],
               command=self.contact_us)
        Button(frame_options, text='Help', font=self.settings['primary_font'],
               activeforeground=self.settings['btn_active_foreground'],
               activebackground=self.settings['btn_active_bg_color'],
               background=self.settings['btn_primary_bg_color'],
               command=self.help)

        Button(frame_options, text='Exit', font=self.settings['primary_font'],
               activeforeground=self.settings['btn_active_foreground'],
               activebackground=self.settings['btn_active_bg_color'],
               background=self.settings['btn_primary_bg_color'], command=self.quit_program)

        row_no = 0
        for widget in frame_options.winfo_children():
            Grid.rowconfigure(frame_options, row_no, weight=1)
            row_no += 1

        col_no = 0
        for widget in frame_options.winfo_children():
            Grid.columnconfigure(frame_options, col_no, weight=1)
            col_no += 1

        row_no = 0
        for widget in frame_options.winfo_children():
            widget.grid(row=row_no, column=0, ipadx=self.screen_width // 15, pady=self.screen_height // 100, sticky=EW)
            row_no += 1

        Label(self.master, text='')

        self.date_time_frame()

    def navbar_welcome(self, non_required_button: str) -> None:
        frame_nav_bar = Frame(self.master, )
        frame_nav_bar.pack(anchor=W, fill=X, pady=1)

        if non_required_button != 'login':
            Button(frame_nav_bar, text='Login', relief=FLAT,
                   background=self.settings['btn_primary_bg_color'],
                   font=self.settings['primary_font'],
                   activebackground=self.settings['btn_active_bg_color'],
                   activeforeground=self.settings['btn_active_foreground'],
                   command=self.login)

        if non_required_button != 'create_admin':
            Button(frame_nav_bar, text='Create Administrator', relief=FLAT,
                   background=self.settings['btn_primary_bg_color'],
                   font=self.settings['primary_font'],
                   activebackground=self.settings['btn_active_bg_color'],
                   activeforeground=self.settings['btn_active_foreground'],
                   command=self.create_admin)

        if non_required_button != 'settings':
            Button(frame_nav_bar, text='Settings', relief=FLAT,
                   background=self.settings['btn_primary_bg_color'],
                   font=self.settings['primary_font'],
                   activebackground=self.settings['btn_active_bg_color'],
                   activeforeground=self.settings['btn_active_foreground'],
                   command=self.edit_settings)

        if non_required_button != 'contact_us':
            Button(frame_nav_bar, text='Contact Us', relief=FLAT,
                   background=self.settings['btn_primary_bg_color'],
                   font=self.settings['primary_font'],
                   activebackground=self.settings['btn_active_bg_color'],
                   activeforeground=self.settings['btn_active_foreground'], )

        if non_required_button != 'help':
            Button(frame_nav_bar, text='Help', relief=FLAT,
                   background=self.settings['btn_primary_bg_color'],
                   font=self.settings['primary_font'],
                   activebackground=self.settings['btn_active_bg_color'],
                   activeforeground=self.settings['btn_active_foreground'], )

        Button(frame_nav_bar, text='Quit', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'],
               activebackground='Red',
               activeforeground=self.settings['btn_active_foreground'],
               command=self.welcome_screen)

        # Now making 'em responsive

        col_no = 0
        for widget in frame_nav_bar.winfo_children():
            Grid.columnconfigure(frame_nav_bar, col_no, weight=1)
            col_no += 1

        row_no = 0
        for widget in frame_nav_bar.winfo_children():
            Grid.columnconfigure(frame_nav_bar, row_no, weight=1)
            row_no += 1

        col_ = 0
        for widget in frame_nav_bar.winfo_children():
            widget.grid(row=0, column=col_, sticky='new')
            col_ += 1

    def login(self):
        for child in self.master.winfo_children():
            child.destroy()

        # Calling main logo
        self.main_logo()

        # Calling Nav-bar
        self.navbar_welcome('login')

        # Create frame for login
        frame_login = Frame(self.master, background=self.settings['secondary_bg_color'])
        frame_login.pack()

        def verify_admin():
            admin_ = admin_name.get()
            pass_ = password.get()

            # taking admin name to self.admin_nm to access the table of that particular admin

            admin_info = None
            i = 1
            # print("View Mode is on...")
            with open('admin_details_file.pickle', 'br') as fo:
                while True:
                    try:
                        admin_info = pickle.load(fo)
                    except EOFError:
                        break

            print(admin_info)

            if admin_info['admin_name'] == admin_:
                if admin_info['password'] == pass_:
                    self.library_options()
                else:
                    show_message('Wrong Password', 'showerror', 'Login Error')
            else:
                show_message('Wrong Administrator Name', 'showerror', 'Login Error')

        label_login = Label(frame_login, text='Login', font='lucida 15', foreground=self.settings['lab_foreground'],
                            background=self.settings['secondary_bg_color'])

        label_admin_name = Label(frame_login, text='Administrator Name', font=self.settings['primary_font'],
                                 foreground=self.settings['lab_foreground'],
                                 background=self.settings['secondary_bg_color'], )
        label_pass = Label(frame_login, text='Password', font=self.settings['primary_font'],
                           foreground=self.settings['lab_foreground'],
                           background=self.settings['secondary_bg_color'], )
        admin_name = ttk.Entry(frame_login, font=self.settings['primary_font'])
        password = ttk.Entry(frame_login, font=self.settings['primary_font'], show='*')

        # Signup Button --------------------------

        btn_login = ttk.Button(frame_login, text='Login', command=verify_admin)
        btn_cancel = ttk.Button(frame_login, text='Cancel', command=self.welcome_screen)

        lst = [label_login, label_admin_name, label_pass, admin_name, password]

        col_no = 0
        for button in lst:
            Grid.columnconfigure(frame_login, col_no, weight=1)
            col_no += 1

        # row_no = 0
        # for button in lst:
        #     Grid.rowconfigure(frame_login, row_no, weight=1)
        #     row_no += 1

        label_login.grid(row=0, column=0, columnspan=2, padx=self.screen_width // 50, pady=self.screen_height // 50, )
        label_admin_name.grid(row=1, column=0, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50, )
        label_pass.grid(row=2, column=0, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50, )
        admin_name.grid(row=1, column=1, padx=self.screen_width // 50, pady=self.screen_height // 50, )
        password.grid(row=2, column=1, padx=self.screen_width // 50, pady=self.screen_height // 50, )
        btn_login.grid(row=3, column=0, padx=self.screen_width // 50, pady=self.screen_height // 50, )
        btn_cancel.grid(row=3, column=1, padx=self.screen_width // 50, pady=self.screen_height // 50, )

        admin_name.focus()

        self.date_time_frame()

    def create_admin(self):
        # Destroying all child in root
        for child in self.master.winfo_children():
            child.destroy()

        # Adding top frame for logo

        self.main_logo()

        # Calling Navbar-welcome

        self.navbar_welcome('create_admin')

        cwd = os.getcwd()
        file = cwd + r'\admin_details_file.pickle'
        admin_details_file = Path(file)

        if admin_details_file.is_file():
            frame_create_admin = Frame(self.master, background=self.settings['secondary_bg_color'])
            frame_create_admin.pack()

            # Adding admin functionality

            Label(frame_create_admin, font=self.settings['primary_font'],
                  text='Administrator Space has already been created!\nPlease Login...', ).pack(padx=50, pady=50,
                                                                                                ipadx=100, ipady=100)
        else:
            # Create admin frame handling
            frame_create_admin = Frame(self.master, background=self.settings['secondary_bg_color'])
            frame_create_admin.pack()

            # Adding admin functionality

            Label(frame_create_admin, text='Create Administrator Space', )

            label_signup = Label(frame_create_admin, text='Signup', font='lucida 15',
                                 foreground=self.settings['lab_foreground'],
                                 background=self.settings['secondary_bg_color'])

            label_admin_name = Label(frame_create_admin, text='Enter Library Username',
                                     font=self.settings['primary_font'],
                                     background=self.settings['secondary_bg_color'],
                                     foreground=self.settings['lab_foreground'])
            admin_name = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_password = Label(frame_create_admin, text='Enter password', font=self.settings['primary_font'],
                                   background=self.settings['secondary_bg_color'],
                                   foreground=self.settings['lab_foreground'])
            password = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_password_confirm = Label(frame_create_admin, text='Confirm password',
                                           font=self.settings['primary_font'],
                                           background=self.settings['secondary_bg_color'],
                                           foreground=self.settings['lab_foreground'])
            password_confirm = ttk.Entry(frame_create_admin, font=self.settings['primary_font'], show='*')

            label_librarian_name = Label(frame_create_admin, text='Enter Librarian name',
                                         font=self.settings['primary_font'],
                                         background=self.settings['secondary_bg_color'],
                                         foreground=self.settings['lab_foreground'])
            librarian_name = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_email = Label(frame_create_admin, text='Enter email address', font=self.settings['primary_font'],
                                background=self.settings['secondary_bg_color'],
                                foreground=self.settings['lab_foreground'])
            email = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_contact_no = Label(frame_create_admin, text='Enter Contact No.', font=self.settings['primary_font'],
                                     background=self.settings['secondary_bg_color'],
                                     foreground=self.settings['lab_foreground'])
            contact_no = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_shop_name = Label(frame_create_admin, text='Enter School Name', font=self.settings['primary_font'],
                                    background=self.settings['secondary_bg_color'],
                                    foreground=self.settings['lab_foreground'])
            school_name = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_school_code = Label(frame_create_admin, text='Enter School code/id',
                                      font=self.settings['primary_font'],
                                      background=self.settings['secondary_bg_color'],
                                      foreground=self.settings['lab_foreground'])
            school_code = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_school_address = Label(frame_create_admin, text='Enter School Address',
                                         font=self.settings['primary_font'],
                                         background=self.settings['secondary_bg_color'],
                                         foreground=self.settings['lab_foreground'])
            school_address = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            label_extra_details = Label(frame_create_admin, text='Enter any Extra details',
                                        font=self.settings['primary_font'],
                                        background=self.settings['secondary_bg_color'],
                                        foreground=self.settings['lab_foreground'])
            extra_details = ttk.Entry(frame_create_admin, font=self.settings['primary_font'])

            # Verify details

            def verify_details():
                all_ok = True
                var_password = password.get()
                var_password_confirm = password_confirm.get()
                var_contact_no = contact_no.get()

                while True:
                    if len(password.get()) < 1:
                        show_message("Password length must be more than 1 character", "showerror", "Error")
                        all_ok = False
                        break
                    elif var_password != var_password_confirm:
                        show_message("Entered Passwords are not same", "showerror", "Error")
                        all_ok = False
                        break
                    if not var_contact_no.isnumeric():
                        all_ok = False
                        show_message("Contact no should be numeric", "showerror", "Error")
                        break
                    elif len(var_contact_no) != 10:
                        show_message("Contact no. must be 10 digits", "showerror", "Error")
                        all_ok = False
                        break
                    else:
                        break

                if all_ok:
                    # If this condition gets true then we will call a function which will be responsible
                    # for the database
                    today_date = str(datetime.datetime.now())
                    time_ = today_date[11:19]
                    today_date = today_date[:10]
                    ad_name = admin_name.get()

                    admin_details = dict()

                    admin_details['admin_name'] = admin_name.get()
                    admin_details['password'] = password.get()
                    admin_details['librarian_name'] = librarian_name.get()
                    admin_details['email'] = email.get()
                    admin_details['contact'] = contact_no.get()
                    admin_details['school_name'] = school_name.get()
                    admin_details['school_code'] = school_code.get()
                    admin_details['school_admin'] = school_address.get()
                    admin_details['extra_admin'] = extra_details.get()

                    with open('admin_details_file.pickle', 'ba') as fo:
                        pickle.dump(admin_details, fo, protocol=0)

                    self.login()

            btn_signup = ttk.Button(frame_create_admin, text='Signup', command=verify_details)
            btn_cancel = ttk.Button(frame_create_admin, text='Cancel', command=self.welcome_screen)

            lst = [
                label_signup,
                label_admin_name, admin_name,
                label_password, password,
                label_password_confirm, password_confirm,
                label_librarian_name, librarian_name,
                label_email, email,
                label_contact_no, contact_no,
                label_shop_name, school_name,
                label_school_code, school_code,
                label_school_address, school_address,
                label_extra_details, extra_details,
                btn_signup, btn_cancel
            ]

            col_no = 0
            for button in lst:
                Grid.columnconfigure(frame_create_admin, col_no, weight=1)
                col_no += 1

            row_no = 0
            for button in lst:
                Grid.rowconfigure(frame_create_admin, col_no, weight=1)
                row_no += 1

            # Taking label into grid ----------------------

            label_signup.grid(row=0, column=0, columnspan=2, padx=self.screen_width // 50,
                              pady=self.screen_height // 50)
            label_admin_name.grid(row=1, column=0, sticky=W, padx=self.screen_width // 70,
                                  pady=self.screen_height // 70)
            label_password.grid(row=2, column=0, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            label_password_confirm.grid(row=3, column=0, sticky=W, padx=self.screen_width // 70,
                                        pady=self.screen_height // 70)
            label_librarian_name.grid(row=4, column=0, sticky=W, padx=self.screen_width // 70,
                                      pady=self.screen_height // 70)
            label_email.grid(row=5, column=0, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            label_contact_no.grid(row=6, column=0, sticky=W, padx=self.screen_width // 70,
                                  pady=self.screen_height // 70)

            label_shop_name.grid(row=7, column=0, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)

            label_school_code.grid(row=8, column=0, sticky=W, padx=self.screen_width // 70,
                                   pady=self.screen_height // 70)
            label_school_address.grid(row=9, column=0, sticky=W, padx=self.screen_width // 70,
                                      pady=self.screen_height // 70)
            label_extra_details.grid(row=10, column=0, sticky=W, padx=self.screen_width // 70,
                                     pady=self.screen_height // 70)

            # Taking entry into grid

            admin_name.grid(row=1, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            password.grid(row=2, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            password_confirm.grid(row=3, column=1, sticky=W, padx=self.screen_width // 70,
                                  pady=self.screen_height // 70)
            librarian_name.grid(row=4, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            email.grid(row=5, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            contact_no.grid(row=6, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)

            school_name.grid(row=7, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)

            school_code.grid(row=8, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            school_address.grid(row=9, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)
            extra_details.grid(row=10, column=1, sticky=W, padx=self.screen_width // 70, pady=self.screen_height // 70)

            # Taking button into grid

            btn_signup.grid(row=11, column=0, sticky=EW, padx=self.screen_width // 70, pady=self.screen_height // 70)
            btn_cancel.grid(row=11, column=1, sticky=EW, padx=self.screen_width // 70, pady=self.screen_height // 70)

            # Adding focus

            admin_name.focus()

        # Adding date-time frame

        self.date_time_frame()

    def edit_settings(self):
        for child in self.master.winfo_children():
            child.destroy()

        with open('settings.pickle', 'rb') as settings:
            all_settings = pickle.load(settings)

        # for i in all_settings:
        #     print(f"'{i}' = '{all_settings[i]}'")
        # - ------------------------

        # Calling main logo
        self.main_logo()

        # Calling Nav-bar
        self.navbar_welcome('settings')

        # Create frame for settings page
        frame_edit_settings = Frame(self.master, background=self.settings['secondary_bg_color'])
        frame_edit_settings.pack(pady=10, fill=X)

        label_settings = Label(frame_edit_settings, text='Settings', font='lucida 25',
                               foreground=self.settings['lab_foreground'],
                               background=self.settings['secondary_bg_color'])
        label_settings.pack()

        # Frame for white line
        Frame(frame_edit_settings, ).pack(fill=X)

        frame_grid = Frame(frame_edit_settings, background=self.settings['secondary_bg_color'])
        frame_grid.pack(side=LEFT)

        # Settings

        # Function to choose color.

        def choose_color(color_for):

            # variable to store hexadecimal code of color
            color_code = colorchooser.askcolor(title="Choose color")

            # variable to store hexadecimal code of color
            if color_for == 'primary_bg_color':
                all_settings['primary_bg_color'] = color_code[1]
                frame_show_select_primary_color.config(background=color_code[1])

            if color_for == 'secondary_bg_color':
                all_settings['secondary_bg_color'] = color_code[1]
                frame_show_select_secondary_color.config(background=color_code[1])

            if color_for == 'btn_primary_bg_color':
                all_settings['btn_primary_bg_color'] = color_code[1]
                frame_show_button_color.config(background=color_code[1])

        label_primary_color = Label(frame_grid, text='Primary Color', font='lucida 15',
                                    foreground=self.settings['lab_foreground'],
                                    background=self.settings['secondary_bg_color'])

        frame_show_select_primary_color_border = None
        if all_settings['secondary_bg_color'] != '#FFFFFF':
            frame_show_select_primary_color_border = Frame(frame_grid, background='#FFFFFF')
        else:
            frame_show_select_primary_color_border = Frame(frame_grid, background='#000000')

        frame_show_select_primary_color = Frame(frame_show_select_primary_color_border,
                                                background=all_settings['primary_bg_color'])

        frame_show_select_primary_color.pack(ipadx=self.screen_width // 55, ipady=self.screen_height // 55, padx=2,
                                             pady=2)

        btn_primary_color_picker = ttk.Button(frame_grid, text="Select color",
                                              command=lambda: (choose_color('primary_bg_color')))

        label_secondary_color = Label(frame_grid, text='Secondary Color', font='lucida 15',
                                      foreground=self.settings['lab_foreground'],
                                      background=self.settings['secondary_bg_color'])

        frame_show_select_secondary_color_border = None
        if all_settings['secondary_bg_color'] != '#FFFFFF':
            frame_show_select_secondary_color_border = Frame(frame_grid, background='#FFFFFF', )
        else:
            frame_show_select_secondary_color_border = Frame(frame_grid, background='#000000', )

        frame_show_select_secondary_color = Frame(frame_show_select_secondary_color_border,
                                                  background=all_settings['secondary_bg_color'])
        frame_show_select_secondary_color.pack(ipadx=self.screen_width // 55,
                                               ipady=self.screen_height // 55, padx=2,
                                               pady=2)

        btn_secondary_color_picker = ttk.Button(frame_grid, text="Select color",
                                                command=lambda: (choose_color('secondary_bg_color')))

        label_btn_color = Label(frame_grid, text='Button Color', font='lucida 15',
                                foreground=self.settings['lab_foreground'],
                                background=self.settings['secondary_bg_color'])
        frame_show_button_color_border = None
        if all_settings['secondary_bg_color'] != '#FFFFFF':
            frame_show_button_color_border = Frame(frame_grid, background='#FFFFFF', )
        else:
            frame_show_button_color_border = Frame(frame_grid, background='#000000', )

        frame_show_button_color = Frame(frame_show_button_color_border, background=all_settings['btn_primary_bg_color'])
        frame_show_button_color.pack(ipadx=self.screen_width // 55,
                                     ipady=self.screen_height // 55, padx=2,
                                     pady=2)
        btn_button_color_picker = ttk.Button(frame_grid, text="Select color",
                                             command=lambda: (choose_color('btn_primary_bg_color')))

        def restore_default():
            if get_conformation('Do you really to want restore defualt settings'):
                os.remove("settings.pickle")
                self.__init__(self.master)

        # Restore default button
        btn_restore_settings = ttk.Button(frame_grid, text="Restore Default Settings",
                                          command=lambda: (restore_default()))

        # Grid

        label_primary_color.grid(row=2, column=0, sticky=W, pady=self.screen_height // 50)
        frame_show_select_primary_color_border.grid(row=2, column=1, sticky=W, pady=self.screen_height // 50)
        btn_primary_color_picker.grid(row=2, column=2, sticky=W, padx=self.screen_width // 50,
                                      pady=self.screen_height // 50)

        label_secondary_color.grid(row=3, column=0, sticky=W, pady=self.screen_height // 50)
        frame_show_select_secondary_color_border.grid(row=3, column=1, sticky=W, pady=self.screen_height // 50)
        btn_secondary_color_picker.grid(row=3, column=2, sticky=W, padx=self.screen_width // 50,
                                        pady=self.screen_height // 50)

        label_btn_color.grid(row=4, column=0, sticky=W, pady=self.screen_height // 50)
        frame_show_button_color_border.grid(row=4, column=1, sticky=W, pady=self.screen_height // 50)
        btn_button_color_picker.grid(row=4, column=2, sticky=W, padx=self.screen_width // 50,
                                     pady=self.screen_height // 50)

        btn_restore_settings.grid(row=8, column=2, sticky=W, padx=self.screen_width // 50,
                                  pady=self.screen_height // 50)

        # Upload all settings

        def upload_settings():
            ans = get_conformation('Restart is required to apply the settings.\n'
                                   'Do you want to restart the application')

            if ans:
                os.remove("settings.pickle")
                setting_file = 'settings.pickle'
                with open(setting_file, 'bw') as fp:
                    pickle.dump(all_settings, fp, protocol=0)
                self.__init__(self.master)

        ttk.Button(frame_edit_settings, text="Save", command=lambda: (upload_settings())).pack(
            pady=self.screen_height // 50, side=BOTTOM
        )

        #

        self.date_time_frame()

    def contact_us(self):
        for child in self.master.winfo_children():
            child.destroy()

        # Calling main logo
        self.main_logo()

        # Calling Nav-bar
        self.navbar_welcome('contact_us')

        # Create frame for login
        frame_contact_us = Frame(self.master, background=self.settings['secondary_bg_color'])
        frame_contact_us.pack()

        frame_inside = Frame(frame_contact_us, background=self.settings['secondary_bg_color'])
        frame_inside.pack(pady=20)

        Frame(frame_inside, ).grid(row=1, column=0, columnspan=2, pady=self.screen_height // 50, sticky=EW)

        label_contact_us = Label(frame_inside, text='Contact Us', font='lucida 25',
                                 foreground=self.settings['lab_foreground'],
                                 background=self.settings['secondary_bg_color'])
        label_contact_us.grid(row=0, column=0, columnspan=2)

        email = 'iamayush@gmail.com'
        phone = '8012312484'
        address = '3rd floor, House No. 34, 5th Street, Betul Ganj, Betul, Madhya Pradesh, India'

        label_email = Label(frame_inside, text='Email:', font='lucida 15',
                            foreground=self.settings['lab_foreground'],
                            background=self.settings['secondary_bg_color'])
        label_email_ans = Label(frame_inside, text=email, font='lucida 15',
                                foreground=self.settings['lab_foreground'],
                                background=self.settings['secondary_bg_color'])

        label_phone = Label(frame_inside, text='Phone:', font='lucida 15',
                            foreground=self.settings['lab_foreground'],
                            background=self.settings['secondary_bg_color'])

        label_phone_ans = Label(frame_inside, text=phone, font='lucida 15',
                                foreground=self.settings['lab_foreground'],
                                background=self.settings['secondary_bg_color'])

        label_address = Label(frame_inside, text='Address:', font='lucida 15',
                              foreground=self.settings['lab_foreground'],
                              background=self.settings['secondary_bg_color'])

        label_address_ans = Label(frame_inside, text=address, font='lucida 15',
                                  foreground=self.settings['lab_foreground'],
                                  background=self.settings['secondary_bg_color'])

        # Griding

        label_email.grid(row=2, column=0, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50)
        label_email_ans.grid(row=2, column=1, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50)

        label_phone.grid(row=3, column=0, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50)
        label_phone_ans.grid(row=3, column=1, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50)

        label_address.grid(row=4, column=0, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50)
        label_address_ans.grid(row=4, column=1, sticky=W, padx=self.screen_width // 50, pady=self.screen_height // 50)

        #

    def help(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()
        self.navbar_welcome('help')
        frame_help = Frame(self.master, background=self.settings['secondary_bg_color'])
        frame_help.pack(pady=10, ipady=self.screen_height // 50)

        Label(frame_help, text='Help Desk',
              font=self.settings['lab_heading_font'],
              bg=self.settings['secondary_bg_color'],
              foreground=self.settings['lab_foreground']).grid(row=0, column=0, pady=self.screen_height // 50,
                                                               padx=self.screen_width // 50)

        def show_shortcuts():
            pass

        def how_to():
            pass

        Button(frame_help, text='Learn ShortCuts', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff',
               activeforeground='White', command=show_shortcuts).grid(row=1, column=0,
                                                                      pady=self.screen_height // 50)
        Button(frame_help, text='How this software works?', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff',
               activeforeground='White', command=how_to).grid(row=2, column=0, padx=self.screen_width // 50)

    # -------------------------------------------- Library functionalities ------------------------------------------- #

    def main_options(self):
        for child in self.master.winfo_children():
            child.destroy()

            # Adding top frame for logo

        self.main_logo()
        frame_manage_books_ = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_manage_books_.pack(pady=1)

        Label(frame_manage_books_, text='Management',
              font=self.settings['lab_heading_font'],
              bg=self.settings['secondary_bg_color'],
              foreground=self.settings['lab_foreground']).grid(row=0, column=0, ipadx=self.screen_width // 15,
                                                               padx=self.screen_width // 10, sticky='new')

        Frame(frame_manage_books_, ).grid(row=1, column=0, pady=self.screen_height // 50, sticky=EW, )

        Button(frame_manage_books_, text='Library Management', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.management_options)

        Button(frame_manage_books_, text='Issue Book', relief=FLAT, background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.issue_book)
        Button(frame_manage_books_, text='Submit Book', relief=FLAT, background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.submit_book)

        Button(frame_manage_books_, text='Logout', relief=FLAT, background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.login)
        Button(frame_manage_books_, relief=FLAT, text='Help', background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White', )
        Button(frame_manage_books_, text='Quit', relief=FLAT, background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'],
               activebackground='Red', activeforeground='White', command=self.quit_program)

        row_no = 0
        for widget in frame_manage_books_.winfo_children():
            Grid.rowconfigure(frame_manage_books_, row_no, weight=1)
            row_no += 1

        col_no = 0
        for widget in frame_manage_books_.winfo_children():
            Grid.columnconfigure(frame_manage_books_, col_no, weight=1)
            col_no += 1

        row_no = 2
        cnt = 1
        for widget in frame_manage_books_.winfo_children():
            if cnt == 1 or cnt == 2:
                cnt += 1
                continue
            else:
                widget.grid(row=row_no, column=0, ipadx=self.screen_width // 15, padx=self.screen_width // 10,
                            pady=self.screen_height // 95, sticky='new')
                row_no += 1

    def library_options(self):
        self.main_options()

    def issue_book(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()
        frame_issue_book = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_issue_book.pack(pady=1)

        Label(frame_issue_book, text='Issue Book',
              font=self.settings['lab_heading_font'],
              bg=self.settings['secondary_bg_color'],
              foreground=self.settings['lab_foreground']).grid(row=0, column=0, ipadx=self.screen_width // 15,
                                                               padx=self.screen_width // 10, sticky='new', columnspan=3)

        Frame(frame_issue_book, ).grid(row=1, column=0, pady=self.screen_height // 50, sticky=EW, columnspan=6)

        frame_inside = Frame(frame_issue_book, bg=self.settings['secondary_bg_color'])
        frame_inside.grid(row=2, column=0, pady=self.screen_height // 50, sticky=EW, columnspan=6)
        lab_student_id = Label(frame_inside, text='Student ID*', font=self.settings['primary_font'],
                               bg='#FFFFFF')
        ent_student_id = ttk.Entry(frame_inside, font=self.settings['primary_font'])

        lab_book_isbn = Label(frame_inside, text='ISBN*', font=self.settings['primary_font'],
                              bg='#FFFFFF')
        ent_book_isbn = ttk.Entry(frame_inside, font=self.settings['primary_font'])

        from_date = None

        def get_date(par_cal):
            nonlocal from_date
            dt = par_cal.get()
            arr = dt.split("/")

            new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

            match = re.search(r, new_date)
            if match is None:
                print("\n\nError\n\n")
            else:
                from_date = match.group()

                # print(adding_date)

        # Frame_adding_date is frame in which all date related component are packed()

        lab_from_date = Label(frame_inside, text='Issue from*', font=self.settings['primary_font'],
                              bg='#FFFFFF')

        frame_from_date = Frame(frame_inside)

        Label(frame_from_date, text="Format:MM/DD/YY").grid(row=0, column=0)

        cal_from_data = DateEntry(frame_from_date, width=16, background="#28282B", foreground="white", bd=2,
                                  font="lucida 10")
        cal_from_data.grid(row=0, column=1, padx=self.screen_width // 100)
        btn_get_from_date = ttk.Button(frame_from_date, command=lambda: get_date(cal_from_data), text="SELECT", )
        btn_get_from_date.grid(row=0, column=2, padx=10)

        to_date = None

        def get_date2(par_cal):
            nonlocal to_date
            dt = par_cal.get()
            arr = dt.split("/")

            new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

            match = re.search(r, new_date)
            if match is None:
                print("\n\nError\n\n")
            else:
                print(match.group())
                to_date = match.group()

                # print(adding_date)

        # Frame_adding_date is frame in which all date related component are packed()

        lab_to_date = Label(frame_inside, text='Issued to*', font=self.settings['primary_font'],
                            bg='#FFFFFF')

        frame_to_date = Frame(frame_inside)

        Label(frame_to_date, text="Format:MM/DD/YY").grid(row=0, column=0)

        cal_to_date = DateEntry(frame_to_date, width=16, background="#28282B", foreground="white", bd=2,
                                font="lucida 10")
        cal_to_date.grid(row=0, column=1, padx=self.screen_width // 100)
        btn_get_to_date = ttk.Button(frame_to_date, command=lambda: get_date2(cal_to_date), text="SELECT", )
        btn_get_to_date.grid(row=0, column=2, padx=10)

        # ________________________________________________

        def add_issue_record():
            book_isbn = ent_book_isbn.get()
            student_id = ent_student_id.get()

            nonlocal from_date
            nonlocal to_date

            # print(book_isbn, student_id, from_date, to_date)
            # print("Issue Called")

            # checking wheahter this book is already issued to student or not

            cur8 = db.cursor()
            cur8.execute(f'SELECT * FROM book_record WHERE isbn="{book_isbn}"')
            is_already_issued = False
            for i in cur8:
                if i[5] == None or i[5] == '':
                    is_already_issued = True
                    break

            if book_isbn == '':
                show_message("Please enter ISBN", 'showerror', 'Enter ISBN')
            elif student_id == '':
                show_message("Please enter Student Id", 'showerror', 'Enter ISBN')

            elif from_date is None:
                show_message("Please select Issue Date", 'showerror', 'Date Error')
            elif to_date is None:
                show_message("Please select Date till book is Issued", 'showerror', 'Date Error')
            elif from_date == to_date:
                show_message("Issue Date and Issued to Date cannot be same", 'showerror', 'Date Error')
            elif is_already_issued:
                show_message(f"This book is already issued to student", 'showerror', 'Date Error')


            else:
                all_ok = 0

                cur3 = db.cursor()

                cur3.execute(f'SELECT * FROM students where id = "{student_id}"')
                for i in cur3:
                    all_ok += 1
                    break

                if all_ok == 0:
                    show_message("Invalid Student ID", 'showerror', 'Invalid Error')

                cur3.execute(f'SELECT * FROM books where isbn = "{book_isbn}"')

                student_name = ''

                for i in cur3:
                    all_ok += 1
                    student_name = i[0]
                    break

                if all_ok == 1:
                    show_message("Invalid Book ISBN", 'showerror', 'Invalid Error')

                if all_ok == 2:
                    cur3 = db.cursor()

                    # Getting sno from book_record

                    cur3.execute('SELECT * FROM book_record')
                    book_name = ''
                    last_sno = 0
                    for i in cur3:

                        book_name = i[0]
                        last_sno = i[0]

                    last_sno += 1
                    print('last_no = ', last_sno)

                    cur3.execute(f"INSERT INTO book_record (Sno, id, isbn, issue_from, issue_to) VALUES "
                                 f"({last_sno}, '{student_id}', '{book_isbn}', '{from_date}', '{to_date}')")

                    db.commit()
                    show_message(f'{book_name} has been successfully issued to\n {student_name}', 'showinfo')
                    self.issue_book()

        btn_add_issue_record = ttk.Button(frame_inside, text='Issue Book', command=lambda: (add_issue_record(),
                                                                                            get_date(cal_from_data),
                                                                                            get_date2(cal_to_date)))
        btn_add_issue_record.grid(row=5, column=0, ipadx=self.screen_width // 50, padx=self.screen_width // 50,
                                  pady=self.screen_height // 20, sticky=W)

        btn_go_back = ttk.Button(frame_inside, image=self.back_img, command=lambda: (self.main_options(),
                                                                                     frame_issue_book.destroy()))
        btn_go_back.grid(row=5, column=1, pady=self.screen_height // 20, sticky=W)

        btn_get_student_id = ttk.Button(frame_inside, text='Get Student Details', command=lambda: (
        ))
        btn_get_student_id.grid(row=5, column=2, ipadx=self.screen_width // 50, padx=self.screen_width // 50,
                                pady=self.screen_height // 20, sticky=W)

        btn_get_isbn = ttk.Button(frame_inside, text='Get ISBN details', command=lambda:
        (self.view_books('issue_book')))
        btn_get_isbn.grid(row=5, column=3, ipadx=self.screen_width // 50, padx=self.screen_width // 50,
                          pady=self.screen_height // 20, sticky=W)

        # Adding to grid

        lab_student_id.grid(row=3, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        ent_student_id.grid(row=3, column=1, pady=self.screen_height // 100, sticky=W)

        lab_book_isbn.grid(row=4, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        ent_book_isbn.grid(row=4, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=E)

        lab_from_date.grid(row=3, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        frame_from_date.grid(row=3, column=3, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)

        lab_to_date.grid(row=4, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        frame_to_date.grid(row=4, column=3, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)

        # -----------------------

        self.date_time_frame()

    def submit_book(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()
        frame_submit_book = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_submit_book.pack(pady=1)

        Label(frame_submit_book, text='Submit Book',
              font=self.settings['lab_heading_font'],
              bg=self.settings['secondary_bg_color'],
              foreground=self.settings['lab_foreground']).grid(row=0, column=0, ipadx=self.screen_width // 15,
                                                               padx=self.screen_width // 10, sticky='new', columnspan=3)

        Frame(frame_submit_book, ).grid(row=1, column=0, pady=self.screen_height // 50, sticky=EW, columnspan=6)

        lab_student_id = Label(frame_submit_book, text='Student ID*', font=self.settings['primary_font'],
                               bg='#FFFFFF')
        ent_student_id = Entry(frame_submit_book, font=self.settings['primary_font'])

        lab_book_isbn = Label(frame_submit_book, text='ISBN*', font=self.settings['primary_font'],
                              bg='#FFFFFF')
        ent_book_isbn = Entry(frame_submit_book, font=self.settings['primary_font'])

        return_date = None

        def get_date11(par_cal):
            try:
                print('Inside the gate ')
                nonlocal return_date
                dt = par_cal.get()
                arr = dt.split("/")

                new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

                match = re.search(r, new_date)
                if match is None:
                    print("\n\nError\n\n")
                else:
                    print("\nActual Date: ")
                    print(match.group())
                    return_date = match.group()
            except:
                print('Exception')

                # print(adding_date)

        # Frame_adding_date is frame in which all date related component are packed()

        lab_return_date = Label(frame_submit_book, text='Returning on*', font=self.settings['primary_font'],
                                bg='#FFFFFF')

        frame_return_date = Frame(frame_submit_book)

        Label(frame_return_date, text="Format:MM/DD/YY").grid(row=0, column=0)

        cal_returned_data = DateEntry(frame_return_date, width=16, background="#28282B", foreground="white", bd=2,
                                      font="lucida 10")
        cal_returned_data.grid(row=0, column=1, padx=self.screen_width // 100)
        btn_get_from_date = ttk.Button(frame_return_date, command=lambda: get_date11(cal_returned_data), text="SELECT", )
        btn_get_from_date.grid(row=0, column=2, padx=10)

        def add_submit_record():

            nonlocal return_date
            print(return_date)

            student_id = ent_student_id.get()
            isbn = ent_book_isbn.get()

            cur = db.cursor()

            cur.execute(f'SELECT * FROM book_record where id="{student_id}" and isbn="{isbn}"')

            is_record_in_db = False
            for i in cur:
                is_record_in_db = True
                break

            if is_record_in_db:
                cur.execute(F'UPDATE book_record SET returned_at="{return_date}" where id="{student_id}" and  isbn="{isbn}"')

                show_message("Book has been successfully submitted", 'showinfo',
                             'Date Error')

                db.commit()
                self.submit_book()

        btn_return_book = ttk.Button(frame_submit_book, text='Return Book',
                                     command=lambda: (add_submit_record(), get_date11(cal_returned_data)))

        btn_go_back = ttk.Button(frame_submit_book, text='Go Back', command=lambda: (self.main_options()))

        # Grid

        lab_student_id.grid(row=3, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        ent_student_id.grid(row=3, column=1, pady=self.screen_height // 100, sticky=W)

        lab_book_isbn.grid(row=4, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        ent_book_isbn.grid(row=4, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        lab_return_date.grid(row=3, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)
        frame_return_date.grid(row=3, column=3, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=W)

        btn_return_book.grid(row=5, column=3, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        btn_go_back.grid(row=6, column=3, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)

        # Display date and time

        self.date_time_frame()

    def management_options(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()
        frame_management_options = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_management_options.pack(pady=1)

        Label(frame_management_options, text='Library Management',
              font=self.settings['lab_heading_font'],
              bg=self.settings['secondary_bg_color'],
              foreground=self.settings['lab_foreground']).grid(row=0, column=0, ipadx=self.screen_width // 15,
                                                               padx=self.screen_width // 10, sticky='new')

        Frame(frame_management_options, ).grid(row=1, column=0, pady=self.screen_height // 50, sticky=EW, )

        Button(frame_management_options, text='Mange Books', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.manage_books)
        Button(frame_management_options, text='Manage Students', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.manage_student)
        Button(frame_management_options, text='Track Student', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.track_student)
        Button(frame_management_options, text='Track Book', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White', )
        Button(frame_management_options, text='View Students', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.view_student)
        Button(frame_management_options, text='View Books', relief=FLAT,
               background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.view_books)
        Button(frame_management_options, text='Go Back', relief=FLAT, background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
               command=self.main_options)

        row_no = 0
        for widget in frame_management_options.winfo_children():
            Grid.rowconfigure(frame_management_options, row_no, weight=1)
            row_no += 1

        col_no = 0
        for widget in frame_management_options.winfo_children():
            Grid.columnconfigure(frame_management_options, col_no, weight=1)
            col_no += 1

        row_no = 2
        cnt = 1
        for widget in frame_management_options.winfo_children():
            if cnt == 1 or cnt == 2:
                cnt += 1
                continue
            else:
                widget.grid(row=row_no, column=0, ipadx=self.screen_width // 15, padx=self.screen_width // 10,
                            pady=self.screen_height // 95, sticky='new')
                row_no += 1

        self.date_time_frame()

    # ------------------------------------------ Manage Books functionalities ---------------------------------------- #

    def get_list(self, frame):
        pass

    def manage_books(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()

        frame_manage_books_logo = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_manage_books_logo.pack(pady=1, fill=X)

        Label(frame_manage_books_logo, text='Manage Books', font=self.settings['lab_heading_font'],
              foreground=self.settings['lab_foreground'],
              bg=self.settings['secondary_bg_color']).pack(pady=self.screen_height // 80)

        # Adding Nav-bar

        global frame_manage_books
        frame_manage_books = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_manage_books.pack(pady=1, fill=X)

        global btn_add_book
        global btn_change_details
        global btn_remove_book

        btn_add_book = Button(frame_manage_books, text='Add Book', relief=FLAT,
                              background=self.settings['btn_primary_bg_color'],
                              font=self.settings['primary_font'], activebackground='#66b3ff', activeforeground='White',
                              command=self.add_book)
        btn_change_details = Button(frame_manage_books, text='Change Details', relief=FLAT,
                                    background=self.settings['btn_primary_bg_color'],
                                    font=self.settings['primary_font'], activebackground='#66b3ff',
                                    activeforeground='White', command=self.change_details)
        btn_remove_book = Button(frame_manage_books, text='Remove Book', relief=FLAT,
                                 background=self.settings['btn_primary_bg_color'],
                                 font=self.settings['primary_font'], activebackground='#66b3ff',
                                 activeforeground='White', command=self.remove_book)
        Button(frame_manage_books, image=self.back_img, relief=FLAT, background=self.settings['btn_primary_bg_color'],
               font=self.settings['primary_font'], activebackground='Yellow', activeforeground='Black',
               command=self.management_options)

        row_no = 0
        for widget in frame_manage_books.winfo_children():
            Grid.rowconfigure(frame_manage_books, row_no, weight=1)
            row_no += 1

        col_no = 0
        for widget in frame_manage_books.winfo_children():
            Grid.columnconfigure(frame_manage_books, col_no, weight=1)
            col_no += 1

        col_no = 0
        for widget in frame_manage_books.winfo_children():
            widget.grid(row=0, column=col_no, ipadx=self.screen_width // 15, padx=10, pady=self.screen_height // 100,
                        sticky='new')
            col_no += 1

        # Adding clock

        self.date_time_frame()

    def add_book(self):
        # Making button disable
        btn_add_book['state'] = 'disable'
        btn_change_details['state'] = 'normal'
        btn_remove_book['state'] = 'normal'

        btn_add_book.config(foreground=self.settings['lab_foreground'], bg=self.settings['secondary_bg_color'])

        btn_change_details.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])
        btn_remove_book.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        # removing other frames if they exists
        if self.frame_change_details is not None:
            self.frame_change_details.destroy()

        if self.frame_remove_book is not None:
            self.frame_remove_book.destroy()

        # Main frame for the add_book functionality
        self.frame_add_book = Frame(self.master, bg=self.settings['secondary_bg_color'])
        self.frame_add_book.pack(ipadx=self.screen_width // 20, ipady=self.screen_height // 100, anchor=W, fill=X)

        lab_logo = Label(self.frame_add_book, text='Add Book Details', font=self.settings['lab_heading_font'],
                         background=self.settings['secondary_bg_color'], foreground=self.settings['lab_foreground'])

        # Adding element

        lab_book_name = Label(self.frame_add_book, text='Book Name*', font=self.settings['primary_font'], bg='#FFFFFF')
        ent_book_name = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_isbn_type = Label(self.frame_add_book, text='ISBN Type*', font=self.settings['primary_font'], bg='#FFFFFF')
        lst_isbn_type = ['Select', '10', '13', 'None']

        isbn_type = None

        def get_isbn_type(e):
            nonlocal isbn_type
            isbn_type = combo_isbn_type.get()

        combo_isbn_type = ttk.Combobox(self.frame_add_book, value=lst_isbn_type, font=self.settings['primary_font'])
        combo_isbn_type.current(0)
        combo_isbn_type.bind('<<ComboboxSelected>>', get_isbn_type)

        lab_isbn_number = Label(self.frame_add_book, text='ISBN*', font=self.settings['primary_font'], bg='#FFFFFF')
        ent_isbn_number = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_number_of_books = Label(self.frame_add_book, text='Number of Books*', font=self.settings['primary_font'],
                                    bg='#FFFFFF')
        ent_number_of_books = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_author_name = Label(self.frame_add_book, text='Author Name', font=self.settings['primary_font'],
                                bg='#FFFFFF')
        ent_author_name = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_edition = Label(self.frame_add_book, text='Edition', font=self.settings['primary_font'], bg='#FFFFFF')
        ent_edition = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_publication_name = Label(self.frame_add_book, text='Publication Name', font=self.settings['primary_font'],
                                     bg='#FFFFFF')
        ent_publication_name = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_publication_year = Label(self.frame_add_book, text='Year of Publication',
                                     font=self.settings['primary_font'], bg='#FFFFFF')

        years = ['Select']

        # Appending the range in list_ year
        for i in range(2030, 1800, -1):
            years.append(str(i))

        publication_year = None

        def get_year(e):
            nonlocal publication_year
            publication_year = combox_publication_year.get()

        combox_publication_year = ttk.Combobox(self.frame_add_book, value=years, font=self.settings['primary_font'])
        combox_publication_year.current(0)
        combox_publication_year.bind('<<ComboboxSelected>>', get_year)

        # Publication date:

        lab_adding_date = Label(self.frame_add_book, text='Date',
                                font=self.settings['primary_font'], bg='#FFFFFF')

        adding_date = None

        def get_date(par_cal):
            nonlocal adding_date
            dt = par_cal.get()
            arr = dt.split("/")

            new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

            match = re.search(r, new_date)
            if match is None:
                print("\n\nError\n\n")
            else:
                print("\nActual Date: ")
                print(match.group())
                adding_date = match.group()

                # print(adding_date)

        # Frame_adding_date is frame in which all date related component are packed()
        frame_adding_date = Frame(self.frame_add_book)

        Label(frame_adding_date, text="Format:MM/DD/YY").grid(row=0, column=0)

        cal_adding_data = DateEntry(frame_adding_date, width=16, background="#28282B", foreground="white", bd=2,
                                    font="lucida 10")
        cal_adding_data.grid(row=0, column=1, padx=self.screen_width // 100)
        btn_get_date = ttk.Button(frame_adding_date, command=lambda: get_date(cal_adding_data), text="SELECT", )
        btn_get_date.grid(row=0, column=2, )

        lab_price = Label(self.frame_add_book, text='Price', font=self.settings['primary_font'], bg='#FFFFFF')
        ent_price = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_pages = Label(self.frame_add_book, text='Pages', font=self.settings['primary_font'], bg='#FFFFFF')
        ent_pages = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        lab_about = Label(self.frame_add_book, text='About', font=self.settings['primary_font'], bg='#FFFFFF')
        ent_about = ttk.Entry(self.frame_add_book, font=self.settings['primary_font'])

        # Function to add image.
        image_path = None

        def get_image():
            nonlocal image_path
            path = filedialog.askopenfilename(title="Select an Image",
                                              filetype=(('image    files', '*.jpg'), ('all files', '*.*')))
            image_path = path
            img = Image.open(path)
            resize_image = img.resize((100, 100))

            img = ImageTk.PhotoImage(resize_image)
            lab_book_img = Label(self.frame_add_book, image=img, width=100, height=100)
            lab_book_img.image = img
            lab_book_img.grid(row=7, column=3, rowspan=3, sticky=W)

            print('\nPath = ', image_path)

        btn_add_img = Button(self.frame_add_book, text='Add Image', font=self.settings['primary_font'],
                             command=get_image)

        # Buttons

        def verify_book_details():

            all_ok = True

            nonlocal isbn_type
            nonlocal publication_year
            nonlocal adding_date

            book_name = ent_book_name.get()
            isbn_number = ent_isbn_number.get()
            number_of_books = ent_number_of_books.get()
            author_name = ent_author_name.get()
            edition = ent_edition.get()
            publication_name = ent_publication_name.get()
            price = ent_price.get()
            pages = ent_pages.get()
            about = ent_about.get()

            try:
                book_name = book_name.strip()
                isbn_number = isbn_number.strip()

                author_name = author_name.strip()
                edition = edition.strip()
                price = price.strip()
                pages = pages.strip()
                about = about.strip()
                isbn_type = isbn_type.strip()
            except AttributeError:
                show_message('Complete the all necessary fields before adding book in database', 'showerror',
                             'Field Error')
                all_ok = False

            # adding_date is direct variable

            if all_ok:
                if len(book_name) == 0:
                    all_ok = False
                    show_message('Book name cannot be empty', 'showerror', 'Value Error')

                if isbn_type == 'Select' or isbn_type == '':
                    all_ok = False
                    show_message('Please Select ISBN Type', 'showerror', 'Value Error')

                try:
                    isbn_number = int(isbn_number)
                except ValueError:
                    show_message('ISBN of Books must be Integer', 'showerror', 'Value Error')
                    all_ok = False

                if len(number_of_books) != 0:
                    try:
                        number_of_books = int(number_of_books)
                    except ValueError:
                        show_message('Quantity of Books must be Integer', 'showerror', 'Value Error')
                        all_ok = False
                else:
                    show_message('Please enter quantity of Books', 'showerror', 'Value Error')

                try:
                    if publication_year is not None:
                        if publication_year == 'Select':
                            publication_year = 'NULL'
                        else:
                            publication_year = int(publication_year)
                    else:
                        show_message('Publication cannot be a empty', 'showerror', 'Error')
                        all_ok = False
                except ValueError:
                    show_message('Publication year must be a year', 'showerror', 'Error')
                    all_ok = False

                # Giving default value

                if author_name == '':
                    author_name = 'NULL'

                if edition == '':
                    edition = 'NULL'

                if price == '':
                    price = 0.0
                else:
                    try:
                        price = float(price)
                    except ValueError:
                        show_message('Enter a valid price for book', 'showerror', 'Value Error')
                        all_ok = False

                if pages == '':
                    pages = 0
                else:
                    try:
                        pages = int(pages)
                    except ValueError:
                        show_message('Pages of book must be Integer', 'showerror', 'Value Error')
                        all_ok = False

                if about == '':
                    about = 'NULL'

                if all_ok:
                    cursor_ = db.cursor()

                    # Creating binary data for the image.
                    if image_path is not None:
                        binary_book_img = get_binary_img(image_path)

                        cursor_.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                        (book_name, isbn_type, str(isbn_number), number_of_books, author_name, edition,
                                         publication_name, str(publication_year), adding_date, price, pages, about,
                                         binary_book_img))
                    else:
                        # Inserting book table
                        image_path_ = os.getcwd()
                        image_path_ += r'\book_default_img.png'

                        # img = Image.open(image_path_)
                        # resize_image = img.resize((100, 100))
                        #
                        # img = ImageTk.PhotoImage(resize_image)

                        binary_book_img = get_binary_img(image_path_)

                        cursor_.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                        (book_name, isbn_type, str(isbn_number), number_of_books, author_name, edition,
                                         publication_name, str(publication_year), adding_date, price, pages, about,
                                         binary_book_img))

                        # cursor_.execute('INSERT INTO books (name, isbn_type, isbn, number_of_books, author, edition,\
                        #                  publication_name, publication_year, date_of_adding, price, pages, about \
                        #                  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        #                (book_name, isbn_type, str(isbn_number), number_of_books, author_name, edition,
                        #                  publication_name, str(publication_year), adding_date, price, pages, about))
                    db.commit()
                    # Condition = Good, Avg, Bad, Worst

                    # table_name = 'isbn_' + str(ent_isbn_number.get()).strip()

                    # db.execute(f'CREATE TABLE {table_name} (serial_no INTEGER, is_available TEXT,condition TEXT)')

                    # number_of_books_ = number_of_books + 1
                    # for serial_no in range(1, number_of_books_):
                    #    cursor_.execute(f'INSERT INTO {str(table_name)} VALUES ( ?, ?, ?)', (serial_no, is_available,
                    #                                                                       condition))
                    db.commit()

                    self.frame_add_book.destroy()
                    self.add_book()

                    show_message(f'{book_name} has been successfully added.', 'showinfo')

        btn_add = ttk.Button(self.frame_add_book, text='Add', command=lambda: (get_date(cal_adding_data),
                                                                               verify_book_details()))
        btn_reset = ttk.Button(self.frame_add_book, text='Reset',
                               command=lambda: (self.frame_add_book.destroy(), self.add_book()))

        # Adding grid
        lab_logo.grid(row=0, column=0, columnspan=2, padx=self.screen_width // 50, pady=self.screen_height // 50,
                      sticky=W, )

        lab_book_name.grid(row=1, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_book_name.grid(row=1, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        lab_isbn_type.grid(row=2, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        combo_isbn_type.grid(row=2, column=1, pady=self.screen_height // 100, sticky=W)

        lab_isbn_number.grid(row=3, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_isbn_number.grid(row=3, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        lab_number_of_books.grid(row=4, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                 sticky=EW)
        ent_number_of_books.grid(row=4, column=1, pady=self.screen_height // 100, sticky=W)

        lab_author_name.grid(row=5, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_author_name.grid(row=5, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        lab_edition.grid(row=6, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_edition.grid(row=6, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        lab_publication_name.grid(row=7, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                  sticky=EW)
        ent_publication_name.grid(row=7, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                                  sticky=W)

        lab_publication_year.grid(row=1, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                  sticky=EW)
        combox_publication_year.grid(row=1, column=3, pady=self.screen_height // 100, sticky=W)

        lab_adding_date.grid(row=2, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        frame_adding_date.grid(row=2, column=3, pady=self.screen_height // 100, sticky=W)

        lab_price.grid(row=3, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_price.grid(row=3, column=3, pady=self.screen_height // 100, sticky=W)

        lab_pages.grid(row=4, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_pages.grid(row=4, column=3, pady=self.screen_height // 100, sticky=W)

        lab_about.grid(row=5, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_about.grid(row=5, column=3, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        btn_add_img.grid(row=7, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)

        btn_add.grid(row=11, column=0, padx=self.screen_width // 50, pady=self.screen_height // 20, sticky=EW)
        btn_reset.grid(row=11, column=1, pady=self.screen_height // 100, sticky=W)

        row_no = 0
        for widget in self.frame_add_book.winfo_children():
            Grid.rowconfigure(self.frame_add_book, row_no, weight=1)
            row_no += 1

        col_no = 0
        for widget in self.frame_add_book.winfo_children():
            Grid.columnconfigure(self.frame_add_book, col_no, weight=1)
            col_no += 1

        ent_book_name.focus()

        # Assigning None again for smooth transition

    def change_details(self):
        # Deleting other/previous frame
        if self.frame_add_book is not None:
            self.frame_add_book.destroy()

        if self.frame_remove_book is not None:
            self.frame_remove_book.destroy()

        # Making button disable
        btn_add_book['state'] = 'normal'
        btn_change_details['state'] = 'disable'
        btn_remove_book['state'] = 'normal'

        # record var to keep what's selected

        record = None

        btn_change_details.config(foreground=self.settings['lab_foreground'], bg=self.settings['secondary_bg_color'])

        btn_add_book.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])
        btn_remove_book.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        # Change details frame
        self.frame_change_details = Frame(self.master, bg=self.settings['secondary_bg_color'])
        self.frame_change_details.pack(fill=Y)

        # Giving 2 options 1. Direct by isbn and 2. by list

        frame_change_details_option = Frame(self.frame_change_details, background=self.settings['secondary_bg_color'])
        frame_change_details_option.pack(fill=Y)

        Label(frame_change_details_option, text='Change Book details',
              font=self.settings['lab_heading_font']).grid(column=0, row=0, columnspan=2, padx=self.screen_width // 10,
                                                           pady=self.screen_height // 50, sticky='new')

        # -----------------------------------

        frame_change_by_isbn = Frame(self.frame_change_details)
        frame_change_by_isbn.pack(anchor=W, pady=10, expand=True, ipadx=self.screen_width // 60)

        Label(frame_change_by_isbn, text='Enter ISBN',
              font=self.settings['primary_bg_color']).grid(column=0, row=0,  padx=self.screen_width // 100,
                                                           pady=self.screen_height // 100, )

        ent_isbn = ttk.Entry(frame_change_by_isbn, font=self.settings['primary_font'])
        ent_isbn.grid(column=1, row=0, padx=self.screen_width // 40, ipadx=self.screen_width // 20,
                      pady=self.screen_height // 100, sticky=EW)

        btn_change_details_by_isbn = ttk.Button(frame_change_by_isbn, text='Chnage details',
                                                command=lambda: (change_details()), )

        btn_change_details_by_isbn.grid(column=2, row=0,
                                        pady=self.screen_height // 100)

        # self.frame_change_details.forget()
        #
        # self.frame_change_details = Frame(self.master, bg=self.settings['secondary_bg_color'])
        # self.frame_change_details.pack(fill=Y)

        # Getting data from database
        frame_change_by_lst = Frame(self.frame_change_details)
        frame_change_by_lst.pack(anchor=CENTER)

        treeview_y_scrollbar = Scrollbar(frame_change_by_lst)
        treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

        # adding a x-scrollbar to treeview
        treeview_x_scrollbar = Scrollbar(frame_change_by_lst, orient='horizontal')
        treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

        treeview_books = ttk.Treeview(frame_change_by_lst, yscrollcommand=treeview_y_scrollbar.set,
                                      xscrollcommand=treeview_x_scrollbar.set)

        lst_book_row = list()

        def make_changes():

            print(record)

            # complete row record from tree to pre populate the entry

            selected_row = treeview_books.focus()
            selected_row = treeview_books.item(selected_row)['values']


            print('selected_row_dic', selected_row)


            self.frame_change_details.forget()

            self.frame_change_details = Frame(self.master, bg=self.settings['secondary_bg_color'])
            self.frame_change_details.pack(fill=Y)

            frame_change_books_details = Frame(self.frame_change_details)
            frame_change_books_details.pack(anchor=CENTER)

            Label(frame_change_books_details, text='Change Details',
                  font=self.settings['lab_heading_font']).pack()

            # --------------------------------------------------

            frame_changing_fields = Frame(frame_change_books_details)
            frame_changing_fields.pack()

            lab_book_name = Label(frame_changing_fields, text='Book Name*', font=self.settings['primary_font'],
                                  bg='#FFFFFF')
            ent_book_name = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_book_name.insert(0, selected_row[0])

            lab_number_of_books = Label(frame_changing_fields, text='Number of Books*',
                                        font=self.settings['primary_font'], bg='#FFFFFF')
            ent_number_of_books = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_number_of_books.insert(0, selected_row[1])

            lab_author_name = Label(frame_changing_fields, text='Author Name',
                                    font=self.settings['primary_font'],
                                    bg='#FFFFFF')
            ent_author_name = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_author_name.insert(0, selected_row[5])

            lab_edition = Label(frame_changing_fields, text='Edition', font=self.settings['primary_font'],
                                bg='#FFFFFF')
            ent_edition = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_edition.insert(0, selected_row[6])

            lab_publication_name = Label(frame_changing_fields, text='Publication Name',
                                         font=self.settings['primary_font'],
                                         bg='#FFFFFF')
            ent_publication_name = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_publication_name.insert(0, selected_row[4])

            lab_publication_year = Label(frame_changing_fields, text='Year of Publication',
                                         font=self.settings['primary_font'], bg='#FFFFFF')

            years = [selected_row[8]]

            # Appending the range in list_ year
            for i in range(2030, 1800, -1):
                years.append(str(i))

            publication_year = None

            def get_year(e):
                nonlocal publication_year
                publication_year = combox_publication_year.get()

            combox_publication_year = ttk.Combobox(frame_changing_fields, value=years,
                                                   font=self.settings['primary_font'])
            combox_publication_year.current(0)
            combox_publication_year.bind('<<ComboboxSelected>>', get_year)

            # Publication date:

            lab_adding_date = Label(frame_changing_fields, text='Date',
                                    font=self.settings['primary_font'], bg='#FFFFFF')

            adding_date = None

            def get_date(par_cal):
                nonlocal adding_date
                dt = par_cal.get()
                arr = dt.split("/")

                new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

                match = re.search(r, new_date)
                if match is None:
                    print("\n\nError\n\n")
                else:
                    print(match.group())
                    adding_date = match.group()

                    # print(adding_date)

            # Frame_adding_date is frame in which all date related component are packed()
            frame_adding_date = Frame(frame_changing_fields)

            Label(frame_adding_date, text="Format:MM/DD/YY").grid(row=0, column=0)

            cal_adding_data = DateEntry(frame_adding_date, width=16, background="#28282B", foreground="white",
                                        bd=2,
                                        font="lucida 10")
            cal_adding_data.grid(row=0, column=1, padx=self.screen_width // 100)
            btn_get_date = ttk.Button(frame_adding_date, command=lambda: get_date(cal_adding_data),
                                      text="SELECT", )
            btn_get_date.grid(row=0, column=2, )

            lab_price = Label(frame_changing_fields, text='Price', font=self.settings['primary_font'],
                              bg='#FFFFFF')
            ent_price = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_price.insert(0, selected_row[10])

            lab_pages = Label(frame_changing_fields, text='Pages', font=self.settings['primary_font'],
                              bg='#FFFFFF')
            ent_pages = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_pages.insert(0, selected_row[11])

            lab_about = Label(frame_changing_fields, text='About', font=self.settings['primary_font'],
                              bg='#FFFFFF')
            ent_about = ttk.Entry(frame_changing_fields, font=self.settings['primary_font'])
            ent_about.insert(0, selected_row[12])


            # Function to add image.
            image_path = None

            def get_image():
                nonlocal image_path
                path = filedialog.askopenfilename(title="Select an Image",
                                                  filetype=(('image    files', '*.jpg'), ('all files', '*.*')))
                image_path = path
                img = Image.open(path)
                resize_image = img.resize((100, 100))

                img = ImageTk.PhotoImage(resize_image)
                lab_book_img = Label(frame_changing_fields, image=img, width=100, height=100)
                lab_book_img.image = img
                lab_book_img.grid(row=7, column=3, rowspan=3, sticky=W)

                print('\nPath = ', image_path)

            btn_add_img = Button(frame_changing_fields, text='Change Image', font=self.settings['primary_font'],
                                 command=get_image)

            # Buttons
            lst_all_books = list()

            def verify_book_details():

                all_ok = True
                nonlocal publication_year
                nonlocal adding_date

                book_name = ent_book_name.get()

                number_of_books = ent_number_of_books.get()
                author_name = ent_author_name.get()
                edition = ent_edition.get()
                publication_name = ent_publication_name.get()
                price = ent_price.get()
                pages = ent_pages.get()
                about = ent_about.get()

                try:
                    book_name = book_name.strip()
                    author_name = author_name.strip()
                    edition = edition.strip()
                    price = price.strip()
                    pages = pages.strip()
                    about = about.strip()

                except AttributeError:
                    show_message('Complete the all necessary fields before adding book in database',
                                 'showerror',
                                 'Field Error')
                    all_ok = False

                # adding_date is direct variable

                cur1 = db.cursor()
                cur1.execute('SELECT * FROM books')

                for tp in cur1:
                    lst_all_books.append(tp)

                if all_ok:
                    cur1 = db.cursor()
                    if book_name != '':
                        cur1.execute(
                            f'UPDATE books SET name = "{book_name}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    if len(number_of_books) != 0:
                        try:
                            number_of_books = int(number_of_books)
                            cur1.execute(
                                f'UPDATE books SET number_of_books = {number_of_books} where isbn = {int(lst_all_books[int(record) - 1][2])}')

                        except ValueError:
                            show_message('Quantity of Books must be Integer', 'showerror', 'Value Error')
                            all_ok = False
                    if author_name != '':
                        cur1.execute(
                            f'UPDATE books SET author = "{author_name}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    if edition != '':
                        cur1.execute(
                            f'UPDATE books SET edition = "{edition}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    if publication_name != '':
                        cur1.execute(
                            f'UPDATE books SET publication_name = "{publication_name}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    try:
                        if publication_year is not None:
                            if publication_year == 'Select':
                                publication_year = 'NULL'
                            else:
                                publication_year = int(publication_year)
                                cur1.execute(
                                    f'UPDATE books SET publication_year = "{publication_year}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    except ValueError:
                        show_message('Publication year must be a year', 'showerror', 'Error')
                        all_ok = False

                    if adding_date != '':
                        cur1.execute(
                            f'UPDATE books SET date_of_adding = "{adding_date}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    if price != '':
                        try:
                            price = float(price)
                            cur1.execute(
                                f'UPDATE books SET price = "{price}" where isbn = {int(lst_all_books[int(record) - 1][2])}')
                        except ValueError:
                            show_message('Enter a valid price for book', 'showerror', 'Value Error')
                            all_ok = False

                    if pages != '':
                        try:
                            pages = int(pages)
                            cur1.execute(
                                f'UPDATE books SET pages = "{pages}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                        except ValueError:
                            show_message('Pages of book must be Integer', 'showerror', 'Value Error')
                            all_ok = False

                    if about != '':
                        cur1.execute(
                            f'UPDATE books SET about = "{about}" where isbn = {int(lst_all_books[int(record) - 1][2])}')

                    db.commit()

            btn_add = ttk.Button(frame_changing_fields, text='Change',
                                 command=lambda: (get_date(cal_adding_data),
                                                  verify_book_details(),
                                                  show_message(
                                                      f"Record for Book: {lst_all_books[int(record) - 1][2]}",
                                                      "showinfo", "Record Changed")))
            btn_reset = ttk.Button(frame_changing_fields, text='Reset',
                                   command=lambda: (self.frame_change_details.destroy(), self.change_details()))

            btn_go_back = ttk.Button(frame_changing_fields, image=self.back_img,
                                     command=lambda: (frame_change_books_details.destroy(),
                                                      self.frame_change_details.destroy(),
                                                      self.change_details(),))

            # Adding grid

            lab_book_name.grid(row=1, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                               sticky=EW)
            ent_book_name.grid(row=1, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                               sticky=W)

            lab_number_of_books.grid(row=2, column=0, padx=self.screen_width // 50,
                                     pady=self.screen_height // 100,
                                     sticky=EW)
            ent_number_of_books.grid(row=2, column=1, pady=self.screen_height // 100, sticky=W)

            lab_author_name.grid(row=3, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                 sticky=EW)
            ent_author_name.grid(row=3, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                                 sticky=W)

            lab_edition.grid(row=4, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                             sticky=EW)
            ent_edition.grid(row=4, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                             sticky=W)

            lab_publication_name.grid(row=5, column=0, padx=self.screen_width // 50,
                                      pady=self.screen_height // 100,
                                      sticky=EW)
            ent_publication_name.grid(row=5, column=1, ipadx=self.screen_width // 20,
                                      pady=self.screen_height // 100,
                                      sticky=W)

            lab_publication_year.grid(row=1, column=2, padx=self.screen_width // 50,
                                      pady=self.screen_height // 100,
                                      sticky=EW)
            combox_publication_year.grid(row=1, column=3, pady=self.screen_height // 100, sticky=W)

            #

            lab_adding_date.grid(row=2, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                 sticky=EW)
            frame_adding_date.grid(row=2, column=3, pady=self.screen_height // 100, sticky=W)

            lab_price.grid(row=3, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                           sticky=EW)
            ent_price.grid(row=3, column=3, pady=self.screen_height // 100, sticky=W)

            lab_pages.grid(row=4, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                           sticky=EW)
            ent_pages.grid(row=4, column=3, pady=self.screen_height // 100, sticky=W)

            lab_about.grid(row=5, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                           sticky=EW)
            ent_about.grid(row=5, column=3, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                           sticky=W)

            btn_add_img.grid(row=8, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                             sticky=EW)

            btn_add.grid(row=11, column=0, padx=self.screen_width // 50, pady=self.screen_height // 20,
                         sticky=EW)
            btn_reset.grid(row=11, column=1, pady=self.screen_height // 100, sticky=W)

            btn_go_back.grid(row=11, column=1, pady=self.screen_height // 100, sticky=E)

            row_no = 0
            for widget in frame_changing_fields.winfo_children():
                Grid.rowconfigure(frame_changing_fields, row_no, weight=1)
                row_no += 1

            col_no = 0
            for widget in frame_changing_fields.winfo_children():
                Grid.columnconfigure(frame_changing_fields, col_no, weight=1)
                col_no += 1

            ent_book_name.focus()

            # ---------------------------------------------------

            mes = '** The fields that you are filling, will be changed in ' \
                  'database rest will be the same as before **'
            Label(frame_change_books_details, text=mes, ).pack()


        def change_details():
            print(ent_isbn.get() + "-->>")

            if ent_isbn.get() != "":
                print(ent_isbn.get() + "--<<")

                cur9 = db.cursor()

                cur9.execute(f'select * from books where isbn = "{ent_isbn.get().strip()}"')

                for i in cur9:
                    print('this is it')

            else:
                try:
                    nonlocal record
                    record = treeview_books.selection()[0]

                    make_changes()


                except IndexError:
                    print('Error')

                # Some button for the extra functionality.

        Label(frame_change_by_lst, text='Select the book to change the details',
              font=self.settings['lab_heading_font']).pack()

        btn_change_book_det = ttk.Button(frame_change_by_lst, text='Change Book Details', command=change_details)
        btn_change_book_det.pack(pady=25)

        cursor = db.cursor()
        cursor.execute('SELECT * FROM books')

        lst_book_availability = list()

        # for i in cursor:
        #     lst_book_row.append(i[:len(i) - 1])
        #
        #     cur = db.cursor()
        #     cur.execute(f'SELECT COUNT(is_available) FROM {"isbn_" + i[2]} where is_available="yes"')
        #
        #     for y in cur:
        #         lst_book_availability.append(y[0])

        # Here we are taking data from every books table that how many books are available in lib

        # We are going to make an extra column space for the available books since the books table doesn't have
        # and therefore we have to take that the data from that specific table so fourth.

        # It column will be just after the total books column

        # configuring scroll bar
        treeview_y_scrollbar.configure(command=treeview_books.yview)
        treeview_x_scrollbar.configure(command=treeview_books.xview)

        # Defining columns
        treeview_books['columns'] = (
            'name', 'isbn_type', 'isbn', 'number_of_books', 'books_available', 'author', 'edition',
            'publication_name', 'publication_year', 'date_of_adding', 'price', 'pages', 'about'
        )

        # Format our column # this is for the parent-child column
        treeview_books.column('#0', anchor=CENTER, width=60, minwidth=50)
        treeview_books.column('name', anchor=W, width=170, minwidth=150)
        treeview_books.column('isbn_type', anchor=W, width=80, minwidth=50)
        treeview_books.column('isbn', anchor=W, width=120)
        treeview_books.column('number_of_books', anchor=W, width=120)
        treeview_books.column('books_available', anchor=W, width=120)
        treeview_books.column('author', anchor=W, width=120)
        treeview_books.column('edition', anchor=W, width=120)
        treeview_books.column('publication_name', anchor=W, width=120)
        treeview_books.column('publication_year', anchor=W, width=120)
        treeview_books.column('date_of_adding', anchor=W, width=120)
        treeview_books.column('price', anchor=W, width=120)
        treeview_books.column('pages', anchor=W, width=120)
        treeview_books.column('about', anchor=W, width=120)

        # Create heading
        treeview_books.heading('#0', text='Label', anchor=W)
        treeview_books.heading('name', text='Name', anchor=W)
        treeview_books.heading('isbn_type', text='ISBN Type', anchor=W)
        treeview_books.heading('isbn', text='ISBN', anchor=W)
        treeview_books.heading('number_of_books', text='Books Available', anchor=W)
        treeview_books.heading('books_available', text='Number of Books', anchor=W, )
        treeview_books.heading('author', text='Author', anchor=W, )
        treeview_books.heading('edition', text='Edition', anchor=W, )
        treeview_books.heading('publication_name', text='Publication Name', anchor=W, )
        treeview_books.heading('publication_year', text='Publication Year', anchor=W, )
        treeview_books.heading('date_of_adding', text='Adding Date', anchor=W, )
        treeview_books.heading('price', text='Price', anchor=W, )
        treeview_books.heading('pages', text='Pages', anchor=W, )
        treeview_books.heading('about', text='About', anchor=W, )

        # Rows

        treeview_books.tag_configure('oddrow', background='White')
        treeview_books.tag_configure('evenrow', background='Light Blue')

        style = ttk.Style()
        style.configure('Treeview', rowheight=80, )

        lst_book_main = list()

        cursor.execute('SELECT * from books')

        # Converting data into usable format
        lst_book_rows = list()

        count = 1

        for row in cursor:
            lst_tem = list()
            lst_tem.append(row[len(row) - 1])
            lst_tem += row[:len(row) - 1]
            lst_book_main.append(lst_tem)

        for tpl in lst_book_main:

            lst_with_available_books = list()

            cur = db.cursor()
            cur.execute('SELECT count(isbn) from book_record where isbn = "' + tpl[3] + '"')

            books_available = 0

            for distributed_book in cur:
                books_available = tpl[4] - distributed_book[0]

            for i in range(1, len(tpl)):
                if i == 4:
                    lst_with_available_books.append(books_available)

                lst_with_available_books.append(tpl[i])

            if count % 2 == 0:
                treeview_books.insert(parent='', index='end', iid=count, text=count,
                                      values=tuple(lst_with_available_books),
                                      tags=('evenrow',))
            else:
                treeview_books.insert(parent='', index='end', iid=count, text=count,
                                      values=tuple(lst_with_available_books),
                                      tags=('oddrow',))

            count += 1

        treeview_books.pack(pady=10, fill=BOTH, expand=1, )

    def remove_book(self):
        btn_add_book['state'] = 'normal'
        btn_change_details['state'] = 'normal'
        btn_remove_book['state'] = 'disable'

        btn_remove_book.config(foreground=self.settings['lab_foreground'], bg=self.settings['secondary_bg_color'])

        btn_change_details.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])
        btn_add_book.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        # removing other frames if they exists
        if self.frame_change_details is not None:
            self.frame_change_details.destroy()

        if self.frame_add_book is not None:
            self.frame_add_book.destroy()

        # ---------------------------------------------------------------

        self.frame_remove_book = Frame(self.master, bg=self.settings['secondary_bg_color'])
        self.frame_remove_book.pack(fill=Y)

        # Giving 2 options 1. Direct by isbn and 2. by list

        frame_remove_option = Frame(self.frame_remove_book, background=self.settings['secondary_bg_color'])
        frame_remove_option.pack(fill=Y)

        Label(frame_remove_option, text='Select an option remove the book',
              font=self.settings['lab_heading_font']).grid(column=0, row=0, columnspan=2, padx=self.screen_width // 10,
                                                           pady=self.screen_height // 20, sticky='new')

        # Functions

        def remove_by_list():
            self.frame_remove_book.forget()

            self.frame_remove_book = Frame(self.master, bg=self.settings['secondary_bg_color'])
            self.frame_remove_book.pack(fill=Y)

            # Getting data from database
            frame_remove_by_lst = Frame(self.frame_remove_book)
            frame_remove_by_lst.pack(anchor=CENTER)

            treeview_y_scrollbar = Scrollbar(frame_remove_by_lst)
            treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

            # adding a x-scrollbar to treeview
            treeview_x_scrollbar = Scrollbar(frame_remove_by_lst, orient='horizontal')
            treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

            treeview_books = ttk.Treeview(frame_remove_by_lst, yscrollcommand=treeview_y_scrollbar.set,
                                          xscrollcommand=treeview_x_scrollbar.set)

            lst_book_row = list()

            def remove_book1():
                cur = db.cursor()
                cur.execute("SELECT * FROM books")

                record = treeview_books.selection()[0]

                lst_books_record = list()
                for i in cur:
                    lst_books_record.append(i)

                cur1 = db.cursor()

                # if lst_books_record[2] ==
                #

                cur1.execute(
                    'SELECT count(isbn) from book_record where isbn = "' + lst_books_record[int(record) - 1][2] + '"')
                book_not_lib = 0

                print("lst_books_record[int(record)-1][2] = ", lst_books_record[int(record) - 1][2])

                for i in cur1:
                    book_not_lib = i[0]

                if book_not_lib == 0:
                    print("??Inside if")
                    db.execute("DELETE FROM books where isbn= '" + lst_books_record[int(record) - 1][2] + "'")
                    frame_remove_by_lst.destroy()
                    remove_by_list()
                    db.commit()
                    show_message("Successfully removed book: " + str(lst_books_record[int(record) - 1][2]), "showinfo",
                                 "Operation Successful")
                else:
                    show_message("Cannot delete this book", "showerror", "Invalid Operation")

            Label(frame_remove_by_lst, text='Select the book to change the details',
                  font=self.settings['lab_heading_font']).pack()

            btn_change_book_det = ttk.Button(frame_remove_by_lst, text='Remove book/s', command=remove_book1)
            btn_change_book_det.pack(pady=25)

            cursor = db.cursor()
            cursor.execute('SELECT * FROM books')

            # Here we are taking data from every books table that how many books are available in lib

            # We are going to make an extra column space for the available books since the books table doesn't have
            # and therefore we have to take that the data from that specific table so fourth.

            # It column will be just after the total books column

            # configuring scroll bar
            treeview_y_scrollbar.configure(command=treeview_books.yview)
            treeview_x_scrollbar.configure(command=treeview_books.xview)

            # Defining columns
            treeview_books['columns'] = (
                'name', 'isbn_type', 'isbn', 'number_of_books', 'books_available', 'author', 'edition',
                'publication_name', 'publication_year', 'date_of_adding', 'price', 'pages', 'about'
            )

            # Format our column # this is for the parent-child column
            treeview_books.column('#0', anchor=CENTER, width=60, minwidth=50)
            treeview_books.column('name', anchor=W, width=170, minwidth=150)
            treeview_books.column('isbn_type', anchor=W, width=80, minwidth=50)
            treeview_books.column('isbn', anchor=W, width=120)
            treeview_books.column('number_of_books', anchor=W, width=120)
            treeview_books.column('books_available', anchor=W, width=120)
            treeview_books.column('author', anchor=W, width=120)
            treeview_books.column('edition', anchor=W, width=120)
            treeview_books.column('publication_name', anchor=W, width=120)
            treeview_books.column('publication_year', anchor=W, width=120)
            treeview_books.column('date_of_adding', anchor=W, width=120)
            treeview_books.column('price', anchor=W, width=120)
            treeview_books.column('pages', anchor=W, width=120)
            treeview_books.column('about', anchor=W, width=120)

            # Create heading
            treeview_books.heading('#0', text='Label', anchor=W)
            treeview_books.heading('name', text='Name', anchor=W)
            treeview_books.heading('isbn_type', text='ISBN Type', anchor=W)
            treeview_books.heading('isbn', text='ISBN', anchor=W)
            treeview_books.heading('number_of_books', text='Books Available', anchor=W)
            treeview_books.heading('books_available', text='Number of Books', anchor=W, )
            treeview_books.heading('author', text='Author', anchor=W, )
            treeview_books.heading('edition', text='Edition', anchor=W, )
            treeview_books.heading('publication_name', text='Publication Name', anchor=W, )
            treeview_books.heading('publication_year', text='Publication Year', anchor=W, )
            treeview_books.heading('date_of_adding', text='Adding Date', anchor=W, )
            treeview_books.heading('price', text='Price', anchor=W, )
            treeview_books.heading('pages', text='Pages', anchor=W, )
            treeview_books.heading('about', text='About', anchor=W, )

            # Rows

            treeview_books.tag_configure('oddrow', background='White')
            treeview_books.tag_configure('evenrow', background='Light Blue')

            style = ttk.Style()
            style.configure('Treeview', rowheight=80, )

            lst_book_main = list()

            count = 1

            for row in cursor:
                lst_tem = list()
                lst_tem.append(row[len(row) - 1])
                lst_tem += row[:len(row) - 1]
                lst_book_main.append(lst_tem)

            for tpl in lst_book_main:

                lst_with_available_books = list()

                cur = db.cursor()
                cur.execute('SELECT count(isbn) from book_record where isbn = "' + tpl[3] + '"')

                books_available = 0

                for distributed_book in cur:
                    books_available = tpl[4] - distributed_book[0]

                for i in range(1, len(tpl)):
                    if i == 4:
                        lst_with_available_books.append(books_available)

                    lst_with_available_books.append(tpl[i])

                if count % 2 == 0:
                    treeview_books.insert(parent='', index='end', iid=count, text=count,
                                          values=tuple(lst_with_available_books),
                                          tags=('evenrow',))
                else:
                    treeview_books.insert(parent='', index='end', iid=count, text=count,
                                          values=tuple(lst_with_available_books),
                                          tags=('oddrow',))

                count += 1

            treeview_books.pack(pady=10, fill=BOTH, expand=1, )

        #

        btn_remove_by_isbn = Button(frame_remove_option, text='Change details by INBN', relief=FLAT,
                                    background='White', font=self.settings['primary_font'], activebackground='#66b3ff',
                                    activeforeground='White', command=self.add_book)
        btn_remove_by_isbn.grid(column=0, row=1, padx=self.screen_width // 10,
                                pady=self.screen_height // 30, )

        btn_remove_by_list = Button(frame_remove_option, text='Change details by List', relief=FLAT,
                                    background='White', font=self.settings['primary_font'], activebackground='#66b3ff',
                                    activeforeground='White', command=remove_by_list)
        btn_remove_by_list.grid(column=1, row=1, padx=self.screen_width // 10,
                                pady=self.screen_height // 30, sticky=EW, )

    # ---------------------------------------- Manage Student functionalities ---------------------------------------- #

    def manage_student(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()

        frame_manage_student_logo = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_manage_student_logo.pack(pady=1, fill=X)

        Label(frame_manage_student_logo, text='Manage Students', font=self.settings['lab_heading_font'],
              foreground=self.settings['lab_foreground'],
              bg=self.settings['secondary_bg_color']).pack(pady=self.screen_height // 80)

        global frame_manage_student
        frame_manage_student = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_manage_student.pack(pady=1, fill=X)

        global btn_add_student
        global btn_change_student_details
        global btn_remove_student

        btn_add_student = Button(frame_manage_student, text='Add Student', relief=FLAT, background='White',
                                 font=self.settings['primary_font'], activebackground='#66b3ff',
                                 activeforeground='White',
                                 command=self.add_student)

        btn_change_student_details = Button(frame_manage_student, text='Change Student Details', relief=FLAT,
                                            background='White',
                                            font=self.settings['primary_font'], activebackground='#66b3ff',
                                            activeforeground='White', command=self.change_student_details)
        btn_remove_student = Button(frame_manage_student, text='Remove Student', relief=FLAT, background='White',
                                    font=self.settings['primary_font'], activebackground='#66b3ff',
                                    activeforeground='White', command=self.remove_student)
        Button(frame_manage_student, text='Go Back', relief=FLAT, background='White',
               font=self.settings['primary_font'], activebackground='Yellow', activeforeground='Black',
               command=self.management_options)

        row_no = 0
        for widget in frame_manage_student.winfo_children():
            Grid.rowconfigure(frame_manage_student, row_no, weight=1)
            row_no += 1

        col_no = 0
        for widget in frame_manage_student.winfo_children():
            Grid.columnconfigure(frame_manage_student, col_no, weight=1)
            col_no += 1

        col_no = 0
        for widget in frame_manage_student.winfo_children():
            widget.grid(row=0, column=col_no, ipadx=self.screen_width // 15, padx=10, pady=self.screen_height // 100,
                        sticky='new')
            col_no += 1

        # Adding clock

        self.date_time_frame()

    def add_student(self):
        btn_add_student['state'] = 'disable'
        btn_change_student_details['state'] = 'normal'
        btn_remove_student['state'] = 'normal'

        btn_add_student.config(foreground=self.settings['lab_foreground'], bg=self.settings['secondary_bg_color'])

        btn_change_student_details.config(foreground=self.settings['secondary_bg_color'],
                                          bg=self.settings['lab_foreground'])
        btn_remove_student.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        # removing other frames if they exists
        if self.frame_change_student_details is not None:
            self.frame_change_student_details.destroy()

        if self.frame_remove_student is not None:
            self.frame_remove_student.destroy()

        # Main frame for the add_book functionality
        self.frame_add_student = Frame(self.master, bg=self.settings['secondary_bg_color'])
        self.frame_add_student.pack(ipadx=self.screen_width // 20, ipady=self.screen_height // 100, anchor=W, fill=X)

        lab_logo = Label(self.frame_add_student, text='Add Student Details', font=self.settings['lab_heading_font'],
                         background=self.settings['secondary_bg_color'], foreground=self.settings['lab_foreground'])

        # Adding element

        lab_student_name = Label(self.frame_add_student, text='Student Name*',
                                 font=self.settings['primary_font'], bg='#FFFFFF')
        ent_student_name = ttk.Entry(self.frame_add_student, font=self.settings['primary_font'])

        lab_student_id = Label(self.frame_add_student, text='Student Id*',
                               font=self.settings['primary_font'], bg='#FFFFFF')
        ent_student_id = ttk.Entry(self.frame_add_student, font=self.settings['primary_font'])

        lab_student_roll_no = Label(self.frame_add_student, text='Student Roll no',
                                    font=self.settings['primary_font'], bg='#FFFFFF')
        ent_student_roll_no = ttk.Entry(self.frame_add_student, font=self.settings['primary_font'])

        lab_student_class = Label(self.frame_add_student, text='Class*',
                                  font=self.settings['primary_font'], bg='#FFFFFF')
        lst_class = ['Select', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        student_class = None

        def get_class(e):
            nonlocal student_class
            student_class = combox_class.get()

        combox_class = ttk.Combobox(self.frame_add_student, value=lst_class, font=self.settings['primary_font'])
        combox_class.current(0)
        combox_class.bind('<<ComboboxSelected>>', get_class)

        lab_student_section = Label(self.frame_add_student, text='Section*',
                                    font=self.settings['primary_font'], bg='#FFFFFF')
        ent_student_section = ttk.Entry(self.frame_add_student, font=self.settings['primary_font'])

        lab_student_date_of_birth = Label(self.frame_add_student, text='Date of Birth*',
                                          font=self.settings['primary_font'], bg='#FFFFFF')

        student_date_of_birth = None

        def get_date(par_cal):
            nonlocal student_date_of_birth
            dt = par_cal.get()
            arr = dt.split("/")

            new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

            match = re.search(r, new_date)
            if match is None:
                print("\n\nError\n\n")
            else:
                print("\nActual Date: ")
                print(match.group())
                student_date_of_birth = match.group()

        # Frame_adding_date is frame in which all date related component are packed()
        frame_date_of_birth = Frame(self.frame_add_student)

        Label(frame_date_of_birth, text="Format:MM/DD/YY").grid(row=0, column=0)

        cal_data_of_birth = DateEntry(frame_date_of_birth, width=16, background="#28282B", foreground="white", bd=2,
                                      font="lucida 10")

        cal_data_of_birth.grid(row=0, column=1, padx=self.screen_width // 100)
        btn_get_date = ttk.Button(frame_date_of_birth, command=lambda: get_date(cal_data_of_birth), text="SELECT", )
        btn_get_date.grid(row=0, column=2, )

        image_path = None

        def get_image():
            nonlocal image_path
            path = filedialog.askopenfilename(title="Select an Image",
                                              filetype=(('image    files', '*.jpg'), ('all files', '*.*')))
            image_path = path
            img = Image.open(path)
            resize_image = img.resize((100, 100))

            img = ImageTk.PhotoImage(resize_image)
            lab_book_img = Label(self.frame_add_student, image=img, width=100, height=100)
            lab_book_img.image = img
            lab_book_img.grid(row=7, column=3, rowspan=3, sticky=W)

            print('\nPath = ', image_path)

        btn_add_img = Button(self.frame_add_student, text='Add Image', font=self.settings['primary_font'],
                             command=get_image)

        def verify_student_details():
            all_ok = True

            nonlocal student_class
            nonlocal student_date_of_birth

            student_name = ent_student_name.get()
            student_id = ent_student_id.get()
            student_roll_no = ent_student_roll_no.get()
            student_section = ent_student_section.get()

            try:
                student_name = student_name.strip()
                student_id = student_id.strip()
                student_roll_no = student_roll_no.strip()
                student_section = student_section.strip()
            except AttributeError:
                show_message('Complete the all necessary fields before adding book in database', 'showerror',
                             'Field Error')
                all_ok = False

            if all_ok:
                if len(student_name) == 0:
                    all_ok = False
                    show_message('Student Name cannot be empty', 'showerror', 'Invalid Input')

                if len(student_id) == 0:
                    all_ok = False
                    show_message('Student ID cannot be empty', 'showerror', 'Invalid Input')

                try:
                    if len(student_roll_no) == 0 and student_roll_no:
                        all_ok = False
                        show_message('Student roll no. cannot be empty', 'showerror', 'Invalid Input')
                    student_roll_no = int(student_roll_no)
                except ValueError:
                    show_message('Student roll no. must be Integer', 'showerror', 'Value Error')
                    all_ok = False

                # if len(student_roll_no) == 0:
                #     all_ok = False
                #     show_message('Student roll no. cannot be empty', 'showerror', 'Invalid Input')

                print("student_roll_no = ", student_roll_no, "\ntype = ", type(student_roll_no))

                if len(student_section) == 0:
                    all_ok = False
                    show_message('Student section cannot be empty', 'showerror', 'Invalid Input')

                # try:
                #     if student_date_of_birth is not None:
                #         if student_date_of_birth == 'Select':
                #             student_date_of_birth = 'NULL'
                #         else:
                #             student_date_of_birth = int(student_date_of_birth)
                #     else:
                #         show_message('Date of birth cannot be a empty', 'showerror', 'Error')
                #         all_ok = False
                # except ValueError:
                #     show_message('Date of birth must be a date', 'showerror', 'Error')
                #     all_ok = False

                if all_ok:
                    cursor = db.cursor()
                    binary_student_img = None
                    if image_path is not None:
                        binary_student_img = get_binary_img(image_path)
                    else:
                        # Inserting book table
                        image_path_ = os.getcwd()
                        image_path_ += r'\user_icon.jpeg'

                        binary_student_img = get_binary_img(image_path_)

                    cursor.execute('INSERT INTO students VALUES (?, ? , ?, ?, ?, ? , ?)',
                                   (student_name, str(student_id), student_roll_no, student_class,
                                    str(student_section), str(student_date_of_birth), binary_student_img))

                    db.commit()
                    self.frame_add_student.destroy()
                    self.add_student()

                    show_message(f'{student_name} has been successfully added.', 'showinfo')

        btn_add = ttk.Button(self.frame_add_student, text='Add', command=lambda: (get_date(cal_data_of_birth),
                                                                                  verify_student_details()))
        btn_reset = ttk.Button(self.frame_add_student, text='Reset',
                               command=lambda: (self.frame_add_student.destroy(), self.add_student()))

        # Adding to grid

        lab_student_name.grid(row=1, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_student_name.grid(row=1, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100, sticky=W)

        lab_student_id.grid(row=2, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100, sticky=EW)
        ent_student_id.grid(row=2, column=1, pady=self.screen_height // 100, sticky=W)

        lab_student_roll_no.grid(row=3, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                 sticky=EW)
        ent_student_roll_no.grid(row=3, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                                 sticky=W)

        lab_student_date_of_birth.grid(row=4, column=0, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                       sticky=EW)
        frame_date_of_birth.grid(row=4, column=1, ipadx=self.screen_width // 20, pady=self.screen_height // 100,
                                 sticky=W)

        lab_student_class.grid(row=1, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                               sticky=EW)
        combox_class.grid(row=1, column=3, pady=self.screen_height // 100, sticky=W)

        lab_student_section.grid(row=2, column=2, padx=self.screen_width // 50, pady=self.screen_height // 100,
                                 sticky=EW)
        ent_student_section.grid(row=2, column=3, pady=self.screen_height // 100, sticky=W)

        btn_add_img.grid(row=4, column=3, pady=self.screen_height // 100, sticky=W)

        btn_add.grid(row=11, column=0, padx=self.screen_width // 50, pady=self.screen_height // 20, sticky=EW)
        btn_reset.grid(row=11, column=1, pady=self.screen_height // 100, sticky=W)

    def change_student_details(self):
        btn_add_student['state'] = 'normal'
        btn_change_student_details['state'] = 'disable'
        btn_remove_student['state'] = 'normal'

        btn_add_student.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        btn_change_student_details.config(foreground=self.settings['lab_foreground'],
                                          bg=self.settings['secondary_bg_color'])
        btn_remove_student.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        # removing other frames if they exists
        if self.frame_add_student is not None:
            self.frame_add_student.destroy()

        if self.frame_remove_student is not None:
            self.frame_remove_student.destroy()

        # Change details frame
        self.frame_change_student_details = Frame(self.master, bg=self.settings['secondary_bg_color'])
        self.frame_change_student_details.pack(fill=Y)

        # Giving 2 options 1. Direct by isbn and 2. by list

        frame_change_student_details_option = Frame(self.frame_change_student_details,
                                                    background=self.settings['secondary_bg_color'])
        frame_change_student_details_option.pack(fill=Y)

        Label(frame_change_student_details_option, text='Select an option to change details',
              font=self.settings['lab_heading_font']).grid(column=0, row=0, columnspan=2, padx=self.screen_width // 10,
                                                           pady=self.screen_height // 20, sticky='new')

        def change_student_details_by_id():
            pass

        def change_student_details_by_list():
            self.frame_change_student_details.forget()

            self.frame_change_student_details = Frame(self.master, bg=self.settings['secondary_bg_color'])
            self.frame_change_student_details.pack(fill=Y)

            # Getting data from database
            frame_change_student_details_by_lst = Frame(self.frame_change_student_details)
            frame_change_student_details_by_lst.pack(anchor=CENTER)

            treeview_y_scrollbar = Scrollbar(frame_change_student_details_by_lst)
            treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

            # adding a x-scrollbar to treeview
            treeview_x_scrollbar = Scrollbar(frame_change_student_details_by_lst, orient='horizontal')
            treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

            treeview_students = ttk.Treeview(frame_change_student_details_by_lst,
                                             yscrollcommand=treeview_y_scrollbar.set,
                                             xscrollcommand=treeview_x_scrollbar.set)

            def change_st_details():
                try:
                    selected_row = treeview_students.focus()

                    if selected_row == '':
                        show_message("Please select a student!", "showerror", "Selection Error")
                    else:
                        print(treeview_students.item(selected_row))
                        print(type(treeview_students.item(selected_row)))

                        selected_row_dic = treeview_students.item(selected_row)

                        """
                            Here cur_item is a dictionary which has almost every 
                            information about the tree view row.
                            Ex - 

                            {
                                'text': '', 
                                'image': ['pyimage3'], 
                                'values': ['Student_3', 3, 3, 7, 'A', '28/5/23'], 'open': 0, 'tags': ['oddrow']
                            }

                        """
                        self.frame_change_student_details.forget()

                        self.frame_change_student_details = Frame(self.master, bg=self.settings['secondary_bg_color'])
                        self.frame_change_student_details.pack(fill=Y)

                        frame_change_student_details = Frame(self.frame_change_student_details)
                        frame_change_student_details.pack(anchor=CENTER)

                        # ----------------------------------------------------

                        lab_student_name = Label(frame_change_student_details, text='Student Name*',
                                                 font=self.settings['primary_font'], bg='#FFFFFF')
                        ent_student_name = ttk.Entry(frame_change_student_details, font=self.settings['primary_font'])

                        lab_student_id = Label(frame_change_student_details, text='Student Id*',
                                               font=self.settings['primary_font'], bg='#FFFFFF')
                        ent_student_id = ttk.Entry(frame_change_student_details, font=self.settings['primary_font'])

                        lab_student_roll_no = Label(frame_change_student_details, text='Student Roll no',
                                                    font=self.settings['primary_font'], bg='#FFFFFF')
                        ent_student_roll_no = ttk.Entry(frame_change_student_details,
                                                        font=self.settings['primary_font'])

                        lab_student_date_of_birth = Label(frame_change_student_details, text='Date of Birth*',
                                                          font=self.settings['primary_font'], bg='#FFFFFF')

                        student_date_of_birth = None

                        def get_date(par_cal):
                            nonlocal student_date_of_birth
                            dt = par_cal.get()
                            arr = dt.split("/")

                            new_date = str(arr[1]) + '/' + arr[0] + '/' + arr[2]

                            match = re.search(r, new_date)
                            if match is None:
                                print("\n\nError\n\n")
                            else:
                                print("\nActual Date: ")
                                print(match.group())
                                student_date_of_birth = match.group()

                        # Frame_adding_date is frame in which all date related component are packed()
                        frame_date_of_birth = Frame(frame_change_student_details)

                        Label(frame_date_of_birth, text="Format:MM/DD/YY").grid(row=0, column=0)

                        cal_data_of_birth = DateEntry(frame_date_of_birth, width=16, background="#28282B",
                                                      foreground="white", bd=2,
                                                      font="lucida 10")

                        cal_data_of_birth.grid(row=0, column=1, padx=self.screen_width // 100)
                        btn_get_date = ttk.Button(frame_date_of_birth, command=lambda: get_date(cal_data_of_birth),
                                                  text="SELECT", )
                        btn_get_date.grid(row=0, column=2, )

                        lab_student_class = Label(frame_change_student_details, text='Class*',
                                                  font=self.settings['primary_font'], bg='#FFFFFF')
                        lst_class = ['Select', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

                        student_class = None

                        def get_class(e):
                            nonlocal student_class
                            student_class = combox_class.get()

                        combox_class = ttk.Combobox(frame_change_student_details, value=lst_class,
                                                    font=self.settings['primary_font'])
                        combox_class.current(0)
                        combox_class.bind('<<ComboboxSelected>>', get_class)

                        lab_student_section = Label(frame_change_student_details, text='Section*',
                                                    font=self.settings['primary_font'], bg='#FFFFFF')
                        ent_student_section = ttk.Entry(frame_change_student_details,
                                                        font=self.settings['primary_font'])

                        image_path = None

                        def get_image():
                            nonlocal image_path
                            path = filedialog.askopenfilename(title="Select an Image",
                                                              filetype=(
                                                                  ('image    files', '*.jpg'), ('all files', '*.*')))
                            image_path = path
                            img = Image.open(path)
                            resize_image1 = img.resize((100, 100))
                            img = ImageTk.PhotoImage(resize_image1)
                            lab_book_img = Label(frame_change_student_details, image=img, width=100, height=100)
                            lab_book_img.image = img
                            lab_book_img.grid(row=7, column=2, rowspan=3, sticky=W)

                            print('\nPath = ', image_path)

                        btn_add_img = Button(frame_change_student_details, text='Add Image',
                                             font=self.settings['primary_font'],
                                             command=get_image)

                        def verify_student_details():
                            all_ok = True

                            nonlocal student_class
                            nonlocal student_date_of_birth

                            student_name = ent_student_name.get()
                            student_id = ent_student_id.get()
                            student_roll_no = ent_student_roll_no.get()
                            student_section = ent_student_section.get()

                            try:
                                student_name = student_name.strip()
                                student_id = student_id.strip()
                                student_roll_no = student_roll_no.strip()
                                student_section = student_section.strip()
                            except AttributeError:
                                show_message('Complete the all necessary fields before adding book in database',
                                             'showerror',
                                             'Field Error')
                                all_ok = False

                            cur1 = db.cursor()
                            cur1.execute('SELECT * FROM students')

                            if all_ok:
                                cur1 = db.cursor()

                                if student_id != '':
                                    change_id_confirmation = get_conformation("Do you really "
                                                                              "want to change the Id of this student?\n"
                                                                              "Changing Student ID may cause some errors!")
                                    if not change_id_confirmation:
                                        all_ok = False

                                update_roll_no = False
                                if len(student_roll_no) != 0:
                                    try:
                                        student_roll_no = int(student_roll_no)
                                        update_roll_no = True
                                    except ValueError:
                                        show_message('Student Roll No. must be integer', 'showerror', 'Invalid Input')
                                        all_ok = False

                                update_class = False
                                if student_class != '' and student_class != None:
                                    try:
                                        print("what class = ", student_class)
                                        student_class = int(student_class)
                                        update_class = True
                                    except ValueError:
                                        show_message('Student class must be integer', 'showerror', 'Invalid Input')
                                        all_ok = False

                                print(all_ok)

                                if all_ok:
                                    if student_name != '':
                                        print(
                                            f'UPDATE students SET name="{student_name}" where id={int(selected_row_dic["values"][1])}')
                                        cur1.execute(
                                            f'UPDATE students SET name="{student_name}" where id={int(selected_row_dic["values"][1])}'
                                        )

                                        db.commit()

                                    if update_roll_no:
                                        print(f'UPDATE students SET roll_no={student_roll_no}  \
                                              where id={int(selected_row_dic["values"][1])}')
                                        cur1.execute(
                                            f'UPDATE students SET roll_no={student_roll_no}  \
                                              where id={int(selected_row_dic["values"][1])}'
                                        )

                                        db.commit()

                                    if update_class and student_class is not None:
                                        cur1.execute(
                                            f'UPDATE students SET class={student_class}  \
                                              where id={int(selected_row_dic["values"][1])}'
                                        )

                                        db.commit()

                                    if student_section != '':
                                        cur1.execute(
                                            f'UPDATE students SET section="{student_section}"  \
                                              where id={int(selected_row_dic["values"][1])}'
                                        )

                                        db.commit()

                                    if student_date_of_birth is not None:
                                        cur1.execute(
                                            f'UPDATE students SET date_of_birth="{student_date_of_birth}"  \
                                              where id={int(selected_row_dic["values"][1])}'
                                        )

                                        db.commit()

                                    if image_path is not None:
                                        binary_st_img = get_binary_img(image_path)
                                        cur1.execute(
                                            'UPDATE students SET student_image= ? where id=?', (binary_st_img,
                                                                                                int(selected_row_dic
                                                                                                    ["values"][1]))
                                        )

                                    # Placing student_id replacement at last so when user changes student_id along
                                    # with other detail, the other details got changed first then the primary key.
                                    # It protects from ambiguity.
                                    # If we keep the change student command in b/w the commands below the student_id
                                    # don't get executed as primary key got changed before them.

                                    if student_id != '':
                                        cur1.execute(
                                            f'UPDATE students SET id="{student_id}"  \
                                              where id={int(selected_row_dic["values"][1])}'
                                        )

                                        db.commit()

                                    db.commit()
                                    show_message("Changes have been successfully made...", "showinfo", "Success")
                                    change_student_details_by_list()

                            #  --

                        btn_change = ttk.Button(frame_change_student_details, text='Change',
                                                command=lambda: (verify_student_details()))
                        btn_reset = ttk.Button(frame_change_student_details, text='Reset',
                                               command=lambda: (
                                                   self.frame_change_student_details.destroy(), self.add_student()))

                        # Adding to grid

                        lab_student_name.grid(row=1, column=0, padx=self.screen_width // 50,
                                              pady=self.screen_height // 100,
                                              sticky=EW)
                        ent_student_name.grid(row=1, column=1, ipadx=self.screen_width // 20,
                                              pady=self.screen_height // 100, sticky=W)

                        lab_student_id.grid(row=2, column=0, padx=self.screen_width // 50,
                                            pady=self.screen_height // 100,
                                            sticky=EW)
                        ent_student_id.grid(row=2, column=1, pady=self.screen_height // 100, sticky=W)

                        lab_student_roll_no.grid(row=3, column=0, padx=self.screen_width // 50,
                                                 pady=self.screen_height // 100,
                                                 sticky=EW)
                        ent_student_roll_no.grid(row=3, column=1, ipadx=self.screen_width // 20,
                                                 pady=self.screen_height // 100,
                                                 sticky=W)

                        lab_student_date_of_birth.grid(row=4, column=0, padx=self.screen_width // 50,
                                                       pady=self.screen_height // 100,
                                                       sticky=EW)
                        frame_date_of_birth.grid(row=4, column=1, ipadx=self.screen_width // 20,
                                                 pady=self.screen_height // 100,
                                                 sticky=W)

                        lab_student_class.grid(row=1, column=2,
                                               pady=self.screen_height // 100,
                                               sticky=W)
                        combox_class.grid(row=1, column=2, padx=self.screen_width // 20,
                                          pady=self.screen_height // 100, sticky=E)

                        lab_student_section.grid(row=2, column=2, pady=self.screen_height // 100,
                                                 sticky=W)

                        # lab_student_section.grid(row=2, column=2, padx=self.screen_width // 50,
                        #                          pady=self.screen_height // 100,
                        #                          sticky=EW)
                        ent_student_section.grid(row=2, column=2, padx=self.screen_width // 20,
                                                 pady=self.screen_height // 100, sticky=E)

                        btn_add_img.grid(row=4, column=2, pady=self.screen_height // 100, sticky=W)

                        btn_change.grid(row=11, column=0, padx=self.screen_width // 50, pady=self.screen_height // 20,
                                        sticky=EW)
                        btn_reset.grid(row=11, column=1, pady=self.screen_height // 100, sticky=W)

                except IndexError:
                    print('Error')

            Label(frame_change_student_details_by_lst, text='Select the student to change its details',
                  font=self.settings['lab_heading_font']).pack()

            btn_change_book_det = ttk.Button(frame_change_student_details_by_lst, text='Change Student Details',
                                             command=change_st_details)
            btn_change_book_det.pack(pady=25)

            cursor = db.cursor()
            cursor.execute('SELECT * FROM students')

            # It column will be just after the total books column

            # configuring scroll bar
            treeview_y_scrollbar.configure(command=treeview_students.yview)
            treeview_x_scrollbar.configure(command=treeview_students.xview)

            # Defining columns
            treeview_students['columns'] = (
                'name', 'id', 'roll_no', 'class', 'section', 'date_of_birth'
            )

            # Format our column # this is for the parent-child column
            treeview_students.column('name', anchor=W, width=170, minwidth=150)
            treeview_students.column('id', anchor=W, width=80, minwidth=50)
            treeview_students.column('roll_no', anchor=W, width=120)
            treeview_students.column('class', anchor=W, width=120)
            treeview_students.column('section', anchor=W, width=120)
            treeview_students.column('date_of_birth', anchor=W, width=120)

            # Create heading
            treeview_students.heading('name', text='Name', anchor=W)
            treeview_students.heading('id', text='Student Id', anchor=W)
            treeview_students.heading('roll_no', text='Roll no.', anchor=W)
            treeview_students.heading('class', text='Class', anchor=W)
            treeview_students.heading('section', text='Section', anchor=W, )
            treeview_students.heading('date_of_birth', text='Birth Date', anchor=W)

            # Rows

            treeview_students.tag_configure('oddrow', background='White')
            treeview_students.tag_configure('evenrow', background='Light Blue')

            style = ttk.Style()
            style.configure('Treeview', rowheight=120, )

            lst_student_main = list()

            cursor.execute('SELECT * from students')

            count = 1

            for row in cursor:
                lst_tem = list()
                lst_tem.append(row[len(row) - 1])
                lst_tem += row[:len(row) - 1]
                lst_student_main.append(lst_tem)

            self.images_all_student = []

            for tpl in lst_student_main:
                cwd = os.getcwd()

                # # Directory ----------------------------------------
                # directory = "stduent_imgs"
                # parent_dir = cwd + "/"
                # # Path
                # path = os.path.join(parent_dir, directory)
                #
                # if count == 1 and not os.path.exists(path):
                #     os.mkdir(path)

                # ---------------------------------------------------

                img_path = cwd + r'\tem_student.jpeg'
                get_img(tpl[0], img_path)

                self.images_all_student.append(Image.open(img_path))
                resize_image = self.images_all_student[count - 1].resize((70, 90))
                self.images_all_student[count - 1] = ImageTk.PhotoImage(resize_image)

                if count % 2 == 0:
                    treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                             values=(
                                                 tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                             ), tags=('evenrow'))
                else:
                    treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                             values=(
                                                 tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                             ), tags=('oddrow'))
                count += 1

            # ---------------------------------------- pack for tree

            treeview_students.pack(pady=10, fill=BOTH, expand=1)

        btn_change_student_details_by_id = Button(frame_change_student_details_option, text='Change details by ID',
                                                  relief=FLAT,
                                                  background='White', font=self.settings['primary_font'],
                                                  activebackground='#66b3ff',
                                                  activeforeground='White', command=change_student_details_by_id)
        btn_change_student_details_by_id.grid(column=0, row=1, padx=self.screen_width // 10,
                                              pady=self.screen_height // 30, )

        btn_change_student_details_by_list = Button(frame_change_student_details_option, text='Change details by List',
                                                    relief=FLAT,
                                                    background='White', font=self.settings['primary_font'],
                                                    activebackground='#66b3ff',
                                                    activeforeground='White', command=change_student_details_by_list)
        btn_change_student_details_by_list.grid(column=1, row=1, padx=self.screen_width // 10,
                                                pady=self.screen_height // 30, sticky=EW, )

    def remove_student(self):
        btn_add_student['state'] = 'normal'
        btn_change_student_details['state'] = 'normal'
        btn_remove_student['state'] = 'disable'

        btn_add_student.config(foreground=self.settings['secondary_bg_color'], bg=self.settings['lab_foreground'])

        btn_change_student_details.config(foreground=self.settings['secondary_bg_color'],
                                          bg=self.settings['lab_foreground'])
        btn_remove_student.config(foreground=self.settings['lab_foreground'],
                                  bg=self.settings['secondary_bg_color'])

        # removing other frames if they exists
        if self.frame_add_student is not None:
            self.frame_add_student.destroy()
            self.frame_add_student.destroy()

        if self.frame_change_student_details is not None:
            self.frame_change_student_details.destroy()

        # Remove students

        self.frame_remove_student = Frame(self.master, bg=self.settings['secondary_bg_color'])
        self.frame_remove_student.pack(fill=Y)

        # Giving 2 options 1. Direct by isbn and 2. by list

        frame_remove_student_details_option = Frame(self.frame_remove_student,
                                                    background=self.settings['secondary_bg_color'])
        frame_remove_student_details_option.pack(fill=Y)

        Label(frame_remove_student_details_option, text='Select an option to remove student',
              font=self.settings['lab_heading_font']).grid(column=0, row=0, columnspan=2, padx=self.screen_width // 10,
                                                           pady=self.screen_height // 20, sticky='new')

        def remove_student_by_id():
            pass

        def remove_student_by_list():
            self.frame_remove_student.forget()

            self.frame_remove_student = Frame(self.master, bg=self.settings['secondary_bg_color'])
            self.frame_remove_student.pack(fill=Y)

            # Getting Data from database

            frame_remove_student_by_lst = Frame(self.frame_remove_student)
            frame_remove_student_by_lst.pack(anchor=CENTER)

            treeview_y_scrollbar = Scrollbar(frame_remove_student_by_lst)
            treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

            # adding a x-scrollbar to treeview
            treeview_x_scrollbar = Scrollbar(frame_remove_student_by_lst, orient='horizontal')
            treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

            treeview_students = ttk.Treeview(frame_remove_student_by_lst,
                                             yscrollcommand=treeview_y_scrollbar.set,
                                             xscrollcommand=treeview_x_scrollbar.set)

            def remove_student_from_database():
                try:
                    selected_row = treeview_students.focus()

                    if selected_row == '':
                        show_message("Please select a student first!", "showerror", "Selection Error")
                    else:
                        selected_row_dic = treeview_students.item(selected_row)

                        cur1 = db.cursor()

                        all_ok = True

                        print(f'SELECT * FROM book_record WHERE id = "{selected_row_dic["values"][1]}"')
                        cur1.execute(f'SELECT * FROM book_record WHERE id = "{selected_row_dic["values"][1]}"')
                        for i in cur1:
                            print("inside for")
                            show_message("You cannot remove this student as this student have some book!"
                                         "\nClear the record of this student first and then reomve it.", "showerror",
                                         "Record Error")
                            all_ok = False
                            break

                        #
                        if all_ok and get_conformation("Do you really want to remove this student"):
                            cur1.execute(f'DELETE FROM students where id = "{selected_row_dic["values"][1]}"')

                        remove_student_by_list()
                        db.commit()

                except IndexError:
                    print('Error')

            Label(frame_remove_student_by_lst, text='Select the student to remove him/her from database',
                  font=self.settings['lab_heading_font']).pack()

            btn_change_book_det = ttk.Button(frame_remove_student_by_lst, text='Remove Student',
                                             command=remove_student_from_database)
            btn_change_book_det.pack(pady=25)

            cursor = db.cursor()
            cursor.execute('SELECT * FROM students')

            # It column will be just after the total books column

            # configuring scroll bar
            treeview_y_scrollbar.configure(command=treeview_students.yview)
            treeview_x_scrollbar.configure(command=treeview_students.xview)

            # Defining columns
            treeview_students['columns'] = (
                'name', 'id', 'roll_no', 'class', 'section', 'date_of_birth'
            )

            # Format our column # this is for the parent-child column
            treeview_students.column('name', anchor=W, width=170, minwidth=150)
            treeview_students.column('id', anchor=W, width=80, minwidth=50)
            treeview_students.column('roll_no', anchor=W, width=120)
            treeview_students.column('class', anchor=W, width=120)
            treeview_students.column('section', anchor=W, width=120)
            treeview_students.column('date_of_birth', anchor=W, width=120)

            # Create heading
            treeview_students.heading('name', text='Name', anchor=W)
            treeview_students.heading('id', text='Student Id', anchor=W)
            treeview_students.heading('roll_no', text='Roll no.', anchor=W)
            treeview_students.heading('class', text='Class', anchor=W)
            treeview_students.heading('section', text='Section', anchor=W, )
            treeview_students.heading('date_of_birth', text='Birth Date', anchor=W)

            # Rows

            treeview_students.tag_configure('oddrow', background='White')
            treeview_students.tag_configure('evenrow', background='Light Blue')

            style = ttk.Style()
            style.configure('Treeview', rowheight=120, )

            lst_student_main = list()

            cursor.execute('SELECT * from students')

            # Converting data into usable format
            lst_student_rows = list()

            count = 1

            for row in cursor:
                lst_tem = list()
                lst_tem.append(row[len(row) - 1])
                lst_tem += row[:len(row) - 1]
                lst_student_main.append(lst_tem)

            self.images_all_student = []

            for tpl in lst_student_main:
                cwd = os.getcwd()

                # # Directory ----------------------------------------
                # directory = "stduent_imgs"
                # parent_dir = cwd + "/"
                # # Path
                # path = os.path.join(parent_dir, directory)
                #
                # if count == 1 and not os.path.exists(path):
                #     os.mkdir(path)

                # ---------------------------------------------------

                img_path = cwd + r'\tem_student.jpeg'
                get_img(tpl[0], img_path)

                self.images_all_student.append(Image.open(img_path))
                resize_image = self.images_all_student[count - 1].resize((70, 90))
                self.images_all_student[count - 1] = ImageTk.PhotoImage(resize_image)

                if count % 2 == 0:
                    treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                             values=(
                                                 tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                             ), tags=('evenrow'))
                else:
                    treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                             values=(
                                                 tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                             ), tags=('oddrow'))
                count += 1

                # ---------------------------------------- pack for tree

            treeview_students.pack(pady=10, fill=BOTH, expand=1, )

            # ---------------

        btn_remove_student_by_id = Button(frame_remove_student_details_option, text='Change details by ID',
                                          relief=FLAT,
                                          background='White', font=self.settings['primary_font'],
                                          activebackground='#66b3ff',
                                          activeforeground='White', command=remove_student_by_id)
        btn_remove_student_by_id.grid(column=0, row=1, padx=self.screen_width // 10,
                                      pady=self.screen_height // 30, )

        btn_remove_student_by_list = Button(frame_remove_student_details_option, text='Change details by List',
                                            relief=FLAT,
                                            background='White', font=self.settings['primary_font'],
                                            activebackground='#66b3ff',
                                            activeforeground='White', command=remove_student_by_list)
        btn_remove_student_by_list.grid(column=1, row=1, padx=self.screen_width // 10,
                                        pady=self.screen_height // 30, sticky=EW, )

    # ---------------------------------------- View All Books functionalities ---------------------------------------- #

    def track_student(self):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()

        frame_track_student = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_track_student.pack(fill=Y)

        Label(frame_track_student, text='Select the student to track',
              font=self.settings['lab_heading_font']).grid(row=0, column=0)

        def track(coming_from):
            student_id = ''

            all_ok = False
            if coming_from == 'by_id':
                student_id = ent_stuent_id.get().strip()

                cur22 = db.cursor()
                cur22.execute(f'SELECT * FROM students WHERE id="{student_id}"')

                for i in cur22:
                    all_ok = True
                    break

            else:
                selected_row = treeview_students.focus()
                if selected_row == '':
                    show_message("Please select a student!", "showerror", "Selection Error")
                else:
                    selected_row_dic = treeview_students.item(selected_row)

                    student_id = selected_row_dic["values"][1]
                    print(student_id)
                    all_ok = True

            if all_ok:
                for child2 in frame_track_student.winfo_children():
                    child2.destroy()

                frame_show_track_record = Frame(frame_track_student, bg=self.settings['secondary_bg_color'])
                frame_show_track_record.pack(fill=Y)

                lab_heading = Label(frame_show_track_record, text='', font=self.settings['lab_heading_font'])

                lab_heading.pack(padx=self.screen_width // 50, pady=self.screen_height // 50)

                frame_about = Frame(frame_show_track_record, bg=self.settings['secondary_bg_color'])
                frame_about.pack(fill=Y)

                cur234 = db.cursor()
                cur234.execute(f'SELECT * FROM students where id = "{student_id}"')

                student_details = None
                for i in cur234:
                    student_details = i
                    break

                heading = 'Track Record: ' + student_details[0]
                lab_heading.config(text=heading)

                img_path1 = cwd + r'\tem_student.jpeg'
                get_img(student_details[len(student_details) - 1], img_path1)

                img = Image.open(img_path1)
                resize_image2 = img.resize((170, 190))
                img = ImageTk.PhotoImage(resize_image2)

                lab_img = Label(frame_about, image=img, width=170, height=190)
                lab_img.image = img
                lab_img.grid(row=1, column=0, rowspan=4, sticky=W, padx=self.screen_width // 25,
                             pady=self.screen_height // 50
                             )

                txt = 'ID: ' + student_details[1]
                Label(frame_about, text=txt,
                      font=self.settings['primary_font']).grid(row=1, column=1, padx=10, pady=10, sticky=EW,
                                                               ipadx=self.screen_width // 50)
                txt = 'Roll No. : ' + str(student_details[2])
                Label(frame_about, text=txt,
                      font=self.settings['primary_font']).grid(row=2, column=1, padx=10, pady=10, sticky=EW,
                                                               ipadx=self.screen_width // 50)
                txt = 'Class: ' + str(student_details[3])
                Label(frame_about, text=txt,
                      font=self.settings['primary_font']).grid(row=3, column=1, padx=10, pady=10, sticky=EW,
                                                               ipadx=self.screen_width // 50)

                txt = 'Section: ' + student_details[4]
                Label(frame_about, text=txt,
                      font=self.settings['primary_font']).grid(row=1, column=2, padx=10, pady=10, sticky=EW,
                                                               ipadx=self.screen_width // 50)
                txt = 'DOB: ' + student_details[5]
                Label(frame_about, text=txt,
                      font=self.settings['primary_font']).grid(row=2, column=2, padx=10, pady=10, sticky=EW,
                                                               ipadx=self.screen_width // 50)

                ttk.Button(frame_about, text='Back', command=lambda: (frame_show_track_record.forget(),
                                                                      self.track_student())).grid(row=3, column=4,
                                                                                                  padx=self.screen_width // 30,
                                                                                                  pady=10, sticky=EW,
                                                                                                  ipadx=self.screen_width // 30,
                                                                                                  )

                # For all history
                frame_history = Frame(frame_show_track_record, bg=self.settings['secondary_bg_color'])
                frame_history.pack(fill=Y)

                cur234.execute(f'SELECT * FROM book_record WHERE id="{student_id}"')

                # Treeview to show the history

                treeview_y_scrollbar = Scrollbar(frame_history)
                treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

                # adding a x-scrollbar to treeview
                treeview_x_scrollbar = Scrollbar(frame_history, orient='horizontal')
                treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

                treeview_history = ttk.Treeview(frame_history, yscrollcommand=treeview_y_scrollbar.set,
                                                xscrollcommand=treeview_x_scrollbar.set)

                treeview_y_scrollbar.configure(command=treeview_history.yview)
                treeview_x_scrollbar.configure(command=treeview_history.xview)

                treeview_history['columns'] = (
                    'isbn', 'issue_from', 'issue_to', 'returned_at'
                )

                treeview_history.column('isbn', anchor=W, width=170, minwidth=150)
                treeview_history.column('issue_from', anchor=W, width=120)
                treeview_history.column('issue_to', anchor=W, width=120)
                treeview_history.column('returned_at', anchor=W, width=120)

                treeview_history.heading('isbn', text='ISBN', anchor=W)
                treeview_history.heading('issue_from', text='Issued From', anchor=W)
                treeview_history.heading('issue_to', text='Issue Till', anchor=W)
                treeview_history.heading('returned_at', text='Returned At', anchor=W)

                treeview_history.tag_configure('oddrow', background='White')
                treeview_history.tag_configure('evenrow', background='Light Blue')

                style = ttk.Style()
                style.configure('Treeview', rowheight=80, )

                # Getting all the image of books for tree view
                cur2344 = db.cursor()
                cur2344.execute('SELECT isbn, book_image FROM books')
                lst_book_image = list()  # This list format = [(id, image), ...]

                for i in cur2344:
                    lst_book_image.append(i)

                # Creating a dictionary

                dict_book_image = dict()  # format = dict =>  ['id': image]

                for i in lst_book_image:
                    dict_book_image[i[0]] = i[1]

                list_record = list()
                for i in cur234:
                    lst_tem2 = list()
                    lst_tem2 += i[2:]
                    list_record.append(lst_tem2)

                count2 = 1

                self.lst_all_book_images = list()

                for tpl2 in list_record:

                    img_path12 = cwd + r'\tem_student.jpeg'
                    get_img(dict_book_image[tpl2[0]], img_path12)

                    self.lst_all_book_images.append(Image.open(img_path12))
                    resize_image12 = self.lst_all_book_images[count2 - 1].resize((70, 90))
                    self.lst_all_book_images[count2 - 1] = ImageTk.PhotoImage(resize_image12)

                    if count2 % 2 == 0:
                        treeview_history.insert(parent='', index='end',
                                                image=self.lst_all_book_images[count2 - 1],
                                                values=(
                                                    tpl2[0], tpl2[1], tpl2[2], tpl2[3]
                                                ),
                                                tags=('evenrow',))
                    else:
                        treeview_history.insert(parent='', index='end',
                                                image=self.lst_all_book_images[count2 - 1],
                                                values=(
                                                    tpl2[0], tpl2[1], tpl2[2], tpl2[3]
                                                ),
                                                tags=('oddrow',))
                    count2 += 1

                treeview_history.pack(pady=10, fill=BOTH, expand=1, ipadx=self.screen_width // 15)

        frame_track_by_id = Frame(frame_track_student, bg=self.settings['primary_bg_color'])
        frame_track_by_id.grid(row=1, column=0, sticky=EW, pady=self.screen_height // 70)

        Label(frame_track_by_id, text='Enter Student ID: ',
              font=self.settings['primary_font']).grid(row=0, column=0, padx=self.screen_width // 50,
                                                       pady=self.screen_height // 50)
        ent_stuent_id = ttk.Entry(frame_track_by_id,
                                  font=self.settings['primary_font'])
        ent_stuent_id.grid(row=0, column=1)

        ttk.Button(frame_track_by_id, text='Track',
                   command=track('by_id')).grid(row=0, column=2, padx=self.screen_width // 50, )

        ttk.Button(frame_track_by_id, text='Back', command=lambda: (frame_track_student.destroy(),
                                                                    self.management_options())
                   ).grid(row=0, column=3, padx=self.screen_width // 20, )

        frame_track_by_list = Frame(frame_track_student, bg=self.settings['secondary_bg_color'])
        frame_track_by_list.grid(row=2, column=0)

        treeview_y_scrollbar = Scrollbar(frame_track_by_list)
        treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

        # adding a x-scrollbar to treeview
        treeview_x_scrollbar = Scrollbar(frame_track_by_list, orient='horizontal')
        treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

        treeview_students = ttk.Treeview(frame_track_by_list,
                                         yscrollcommand=treeview_y_scrollbar.set,
                                         xscrollcommand=treeview_x_scrollbar.set)

        btn_change_book_det = ttk.Button(frame_track_by_list, text='Select Student',
                                         command=lambda: track('by_list'))
        btn_change_book_det.pack(pady=25)

        cursor = db.cursor()
        cursor.execute('SELECT * FROM students')

        # It column will be just after the total books column

        # configuring scroll bar
        treeview_y_scrollbar.configure(command=treeview_students.yview)
        treeview_x_scrollbar.configure(command=treeview_students.xview)

        # Defining columns
        treeview_students['columns'] = (
            'name', 'id', 'roll_no', 'class', 'section', 'date_of_birth'
        )

        # Format our column # this is for the parent-child column
        treeview_students.column('name', anchor=W, width=170, minwidth=150)
        treeview_students.column('id', anchor=W, width=80, minwidth=50)
        treeview_students.column('roll_no', anchor=W, width=120)
        treeview_students.column('class', anchor=W, width=120)
        treeview_students.column('section', anchor=W, width=120)
        treeview_students.column('date_of_birth', anchor=W, width=120)

        # Create heading
        treeview_students.heading('name', text='Name', anchor=W)
        treeview_students.heading('id', text='Student Id', anchor=W)
        treeview_students.heading('roll_no', text='Roll no.', anchor=W)
        treeview_students.heading('class', text='Class', anchor=W)
        treeview_students.heading('section', text='Section', anchor=W, )
        treeview_students.heading('date_of_birth', text='Birth Date', anchor=W)

        # Rows

        treeview_students.tag_configure('oddrow', background='White')
        treeview_students.tag_configure('evenrow', background='Light Blue')

        style = ttk.Style()
        style.configure('Treeview', rowheight=120, )

        lst_student_main = list()

        cursor.execute('SELECT * from students')

        count = 1

        for row in cursor:
            lst_tem = list()
            lst_tem.append(row[len(row) - 1])
            lst_tem += row[:len(row) - 1]
            lst_student_main.append(lst_tem)

        self.images_all_student = []

        for tpl in lst_student_main:
            cwd = os.getcwd()

            # # Directory ----------------------------------------
            # directory = "stduent_imgs"
            # parent_dir = cwd + "/"
            # # Path
            # path = os.path.join(parent_dir, directory)
            #
            # if count == 1 and not os.path.exists(path):
            #     os.mkdir(path)

            # ---------------------------------------------------

            img_path = cwd + r'\tem_student.jpeg'
            get_img(tpl[0], img_path)

            self.images_all_student.append(Image.open(img_path))
            resize_image = self.images_all_student[count - 1].resize((70, 90))
            self.images_all_student[count - 1] = ImageTk.PhotoImage(resize_image)

            if count % 2 == 0:
                treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                         values=(
                                             tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                         ), tags=('evenrow'))
            else:
                treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                         values=(
                                             tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                         ), tags=('oddrow'))
            count += 1

        # ---------------------------------------- pack for tree

        treeview_students.pack(pady=10, fill=BOTH, expand=1, )

    def view_student(self, coming_from='None'):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()

        frame_view_student = Frame(self.master, bg=self.settings['secondary_bg_color'])
        frame_view_student.pack(fill=Y)

        # Getting data from database
        frame_show_students = Frame(frame_view_student)
        frame_show_students.pack(anchor=CENTER)

        treeview_y_scrollbar = Scrollbar(frame_show_students)
        treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

        # adding a x-scrollbar to treeview
        treeview_x_scrollbar = Scrollbar(frame_show_students, orient='horizontal')
        treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

        treeview_students = ttk.Treeview(frame_show_students,
                                         yscrollcommand=treeview_y_scrollbar.set,
                                         xscrollcommand=treeview_x_scrollbar.set)

        #

        Label(frame_show_students, text='Select the student to change its details',
              font=self.settings['lab_heading_font']).pack()

        cursor = db.cursor()
        cursor.execute('SELECT * FROM students')

        # configuring scroll bar
        treeview_y_scrollbar.configure(command=treeview_students.yview)
        treeview_x_scrollbar.configure(command=treeview_students.xview)

        treeview_students['columns'] = (
            'name', 'id', 'roll_no', 'class', 'section', 'date_of_birth'
        )

        # Format our column # this is for the parent-child column
        treeview_students.column('name', anchor=W, width=170, minwidth=150)
        treeview_students.column('id', anchor=W, width=80, minwidth=50)
        treeview_students.column('roll_no', anchor=W, width=120)
        treeview_students.column('class', anchor=W, width=120)
        treeview_students.column('section', anchor=W, width=120)
        treeview_students.column('date_of_birth', anchor=W, width=120)

        # Create heading
        treeview_students.heading('name', text='Name', anchor=W)
        treeview_students.heading('id', text='Student Id', anchor=W)
        treeview_students.heading('roll_no', text='Roll no.', anchor=W)
        treeview_students.heading('class', text='Class', anchor=W)
        treeview_students.heading('section', text='Section', anchor=W, )
        treeview_students.heading('date_of_birth', text='Birth Date', anchor=W)

        # Rows

        treeview_students.tag_configure('oddrow', background='White')
        treeview_students.tag_configure('evenrow', background='Light Blue')

        style = ttk.Style()
        style.configure('Treeview', rowheight=120, )

        lst_student_main = list()

        cursor.execute('SELECT * from students')

        count = 1

        for row in cursor:
            lst_tem = list()
            lst_tem.append(row[len(row) - 1])
            lst_tem += row[:len(row) - 1]
            lst_student_main.append(lst_tem)

        self.images_all_student = []

        for tpl in lst_student_main:
            cwd = os.getcwd()

            # # Directory ----------------------------------------
            # directory = "stduent_imgs"
            # parent_dir = cwd + "/"
            # # Path
            # path = os.path.join(parent_dir, directory)
            #
            # if count == 1 and not os.path.exists(path):
            #     os.mkdir(path)

            # ---------------------------------------------------

            img_path = cwd + r'\tem_student.jpeg'
            get_img(tpl[0], img_path)

            self.images_all_student.append(Image.open(img_path))
            resize_image = self.images_all_student[count - 1].resize((70, 90))
            self.images_all_student[count - 1] = ImageTk.PhotoImage(resize_image)

            if count % 2 == 0:
                treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                         values=(
                                             tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                         ), tags=('evenrow'))
            else:
                treeview_students.insert(parent='', index='end', image=self.images_all_student[count - 1],
                                         values=(
                                             tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], tpl[5], tpl[6]
                                         ), tags=('oddrow'))
            count += 1

        # ---------------------------------------- pack for tree

        if coming_from == 'issue_book':
            Button(frame_show_students, text='Go Back', command=lambda: (frame_show_students.destroy(),
                                                                         self.issue_book())).pack(side=RIGHT)
        else:
            Button(frame_show_students, text='Go Back', command=lambda: (frame_show_students.destroy(),
                                                                         self.management_options())).pack()

        treeview_students.pack(pady=10, fill=BOTH, expand=1, )

    def view_books(self, coming_from='None'):
        for child in self.master.winfo_children():
            child.destroy()

        self.main_logo()

        # Adding label
        lab_heading = Label(self.master, text='Books in Library', font=self.settings['lab_heading_font'],
                            bg=self.settings['secondary_bg_color'], foreground=self.settings['lab_foreground'])
        lab_heading.pack(fill=X, pady=self.screen_height // 80, anchor=N)

        # Main view frame
        frame_view_books = Frame(self.master, width=1000, height=1000)
        frame_view_books.pack(expand=True, fill=BOTH)

        treeview_y_scrollbar = Scrollbar(frame_view_books)
        treeview_y_scrollbar.pack(side=RIGHT, fill=Y)

        # adding a x-scrollbar to treeview
        treeview_x_scrollbar = Scrollbar(frame_view_books, orient='horizontal')
        treeview_x_scrollbar.pack(side=BOTTOM, fill=X)

        treeview_books = ttk.Treeview(frame_view_books,
                                      yscrollcommand=treeview_y_scrollbar.set,
                                      xscrollcommand=treeview_x_scrollbar.set)

        cursor = db.cursor()
        cursor.execute('SELECT * FROM books')

        # configuring scroll bar
        treeview_y_scrollbar.configure(command=treeview_books.yview)
        treeview_x_scrollbar.configure(command=treeview_books.xview)

        treeview_books['columns'] = (
            'name', 'isbn_type', 'isbn', 'number_of_books', 'available_books', 'author', 'edition', 'publication_name',
            'publication_year', 'date_of_adding', 'price', 'pages', 'about'
        )

        treeview_books.column('name', anchor=W, width=170, minwidth=150)
        treeview_books.column('isbn_type', anchor=W, width=80, minwidth=50)
        treeview_books.column('isbn', anchor=W, width=120)
        treeview_books.column('number_of_books', anchor=W, width=120)
        treeview_books.column('available_books', anchor=W, width=120)
        treeview_books.column('author', anchor=W, width=120)
        treeview_books.column('edition', anchor=W, width=120)
        treeview_books.column('publication_name', anchor=W, width=120)
        treeview_books.column('date_of_adding', anchor=W, width=120)
        treeview_books.column('price', anchor=W, width=120)
        treeview_books.column('pages', anchor=W, width=120)
        treeview_books.column('about', anchor=W, width=120)

        # Create heading
        treeview_books.heading('name', text='Name', anchor=W)
        treeview_books.heading('isbn_type', text='ISBN Type', anchor=W)
        treeview_books.heading('isbn', text='ISBN', anchor=W)
        treeview_books.heading('number_of_books', text='Total Books', anchor=W)
        treeview_books.heading('available_books', text='Available Books', anchor=W, )
        treeview_books.heading('author', text='Author', anchor=W)
        treeview_books.heading('edition', text='Edition', anchor=W)
        treeview_books.heading('publication_name', text='Publication Name', anchor=W)
        treeview_books.heading('publication_year', text='Publication Year', anchor=W)
        treeview_books.heading('date_of_adding', text='Adding Date in Library', anchor=W)
        treeview_books.heading('price', text='Price', anchor=W)
        treeview_books.heading('pages', text='Pages', anchor=W)
        treeview_books.heading('about', text='About', anchor=W)

        # Rows

        treeview_books.tag_configure('oddrow', background='White')
        treeview_books.tag_configure('evenrow', background='Light Blue')

        #

        style = ttk.Style()
        style.configure('Treeview', rowheight=120, )

        lst_student_main = list()

        cursor.execute('SELECT * from books')

        count = 1

        lst_book_main = list()

        for row in cursor:
            lst_tem = list()
            lst_tem.append(row[len(row) - 1])
            lst_tem += row[:len(row) - 1]
            lst_book_main.append(lst_tem)

        self.images_all_books = []

        for tpl in lst_book_main:

            cwd = os.getcwd()
            img_path = cwd + r'\tem_book.jpeg'
            get_img(tpl[0], img_path)

            self.images_all_books.append(Image.open(img_path))
            resize_image = self.images_all_books[count - 1].resize((70, 90))
            self.images_all_books[count - 1] = ImageTk.PhotoImage(resize_image)

            cur2 = db.cursor()
            cur2.execute(f'SELECT COUNT(*) FROM book_record WHERE isbn = "{tpl[3]}"')

            available_book = tpl[4]

            for i in cur2:
                available_book = available_book - int(i[0])
                print(i)

            if count % 2 == 0:
                treeview_books.insert(parent='', index='end', image=self.images_all_books[count - 1],
                                      values=(
                                          tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], available_book, tpl[5], tpl[6],
                                          tpl[7], tpl[8], tpl[9], tpl[10], tpl[11], tpl[12]
                                      ), tags=('evenrow'))
            else:
                treeview_books.insert(parent='', index='end', image=self.images_all_books[count - 1],
                                      values=(
                                          tpl[1], str(tpl[2]), str(tpl[3]), tpl[4], available_book, tpl[5], tpl[6],
                                          tpl[7], tpl[8], tpl[9], tpl[10], tpl[11], tpl[12]
                                      ), tags=('oddrow'))
            count += 1

        # -----------------------------------------------------------------------------------------

        if coming_from == 'issue_book':
            Button(frame_view_books, image=self.back_img, font=self.settings['btn_font'],
                   command=lambda: (frame_view_books.destroy(), self.issue_book())).pack(pady=20)
        else:
            Button(frame_view_books, image=self.back_img, font=self.settings['btn_font'],
                   command=lambda: (frame_view_books.destroy(), self.management_options())).pack(pady=20, side=BOTTOM)

        treeview_books.pack(pady=10, fill=X)


def destroy_root(e):
    root.destroy()


def create_tables():
    # Here id_collection is representing the ids of exact similar books

    # For id_serial_no, in add_book we are running a for loop, number_of_book times and feeding data of all similar
    # books by adding [ serial number + id_collection ] as unique id

    # All Book Collection Table
    db.execute('CREATE TABLE IF NOT EXISTS books (name TEXT, isbn_type TEXT, isbn TEXT, number_of_books INTEGER, '
               'author TEXT, edition TEXT, publication_name TEXT, publication_year TEXT,  date_of_adding TEXT, '
               'price REAL, pages INTEGER, about TEXT, book_image BLOB)')

    # All Student Table
    db.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, id TEXT PRIMARY KEY, roll_no INTEGER, class INTEGER, '
               'section TEXT, date_of_birth TEXT, student_image BLOB)')

    db.execute('CREATE TABLE IF NOT EXISTS book_record (Sno INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL, isbn '
               'TEXT NOT NULL, issue_from Text, issue_to Text, returned_at TEXT, FOREIGN KEY (id) '
               'REFERENCES students(id),FOREIGN KEY(isbn) REFERENCES books(isbn) )')


root = Tk()
create_tables()

root.bind('<Escape>', destroy_root)

obj = AppTk(root)
obj.main_options()
root.mainloop()
