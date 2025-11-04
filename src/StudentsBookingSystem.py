from tkinter import *
from tkinter import ttk
from tkinter import messagebox as ms
from time import strftime
from datetime import *
import sqlite3

datetime_now = date.today()
now_week = datetime_now.strftime("%W")
now_year = datetime_now.strftime("%Y")

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user_db
              (username_db              TEXT,
               password_db              TEXT,
               firstname_db             TEXT,
               lastname_db              TEXT,
               phone_number_db          TEXT,
               email_address_db         TEXT,
               user_status_db           INT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS appointment_db
              (username_db              TEXT,
               date_db                  TEXT,
               time_db                  TEXT,
               subject_db               TEXT,
               qualification_db         TEXT,
               text_db                  TEXT,
               helper_db                TEXT)''')


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.screen.title('Students Booking System')
        self.screen.geometry("1000x500")
        self.screen.resizable(0, 0)

        self.admin_username = StringVar()
        self.admin_password = StringVar()
        self.admin_confirm_password = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.phone_number = StringVar()
        self.email_address = StringVar()
        self.user_status = IntVar()
        self.selection_db = IntVar()
        self.username_verify = StringVar()
        self.password_verify = StringVar()
        self.current_username = StringVar()
        self.day_selection = IntVar()
        self.week_delta = timedelta(days=7)
        self.week_date = datetime.strptime('{}-W{}-{}'.format(now_year, now_week, 1), "%Y-W%W-%w").date()
        self.week_counter = 0
        self.selected_index = ''
        self.username_index = ''
        self.date_index = ''
        self.time_index = ''

        ''' screen --------------------------------------------------------------------------------------------------'''
        self.screen_lbl = Label(self.screen, text="Students Booking System", bg="AntiqueWhite3",
                                height="1", font=("Calibri", 26))
        self.time_lbl = Label(self.screen, bg="AntiqueWhite1", font=("Calibri", 14))

        ''' screen_admin --------------------------------------------------------------------------------------------'''
        self.screen_admin = Frame(self.screen)

        Label(self.screen_admin, text="Please enter details below to set up an Administrator account:",
              font=("Calibri", 22)).grid(column=0, columnspan=4, row=0, pady=(40, 80), padx=0)
        Label(self.screen_admin, text="Username:",
              font=("Calibri", 16)).grid(column=0, row=1, sticky=W, padx=(50, 0), pady=5)
        Entry(self.screen_admin, textvariable=self.admin_username, width=30, font=("Calibri", 14),
              fg='red').grid(column=1, columnspan=2, row=1, sticky=W)
        Label(self.screen_admin, text="Password:",
              font=("Calibri", 16)).grid(column=0, row=2, sticky=W, padx=(50, 0), pady=5)
        Entry(self.screen_admin, textvariable=self.admin_password, width=30, show="*", font=("Calibri", 14),
              fg='red').grid(column=1, columnspan=2, row=2, sticky=W)
        Label(self.screen_admin, text="Confirm password:",
              font=("Calibri", 16)).grid(column=0, row=3, sticky=W, padx=(50, 0), pady=5)
        Entry(self.screen_admin, textvariable=self.admin_confirm_password, width=30, fg='red', show="*",
              font=("Calibri", 14)).grid(column=1, columnspan=2, row=3, sticky=W)
        Button(self.screen_admin, text="Register", width=10, height=1, font=("Calibri", 16),
               command=self.register_admin).grid(column=1, row=4, sticky=W, pady=20)

        ''' screen_main ---------------------------------------------------------------------------------------------'''
        self.screen_main = Frame(self.screen, bg="AntiqueWhite1")

        Button(self.screen_main, text="Login", height="2", width="30", font=("Calibri", 14), bg="AntiqueWhite2",
               command=self.login).pack(pady=(70, 10))
        Button(self.screen_main, text="Register", height="2", width="30", font=("Calibri", 14),
               bg="AntiqueWhite2", command=self.register).pack(pady=10)
        Button(self.screen_main, text="Exit", height="2", width="30", font=("Calibri", 14), bg="AntiqueWhite2",
               command=exit).pack(pady=10)

        ''' screen_login --------------------------------------------------------------------------------------------'''
        self.screen_login = Frame(self.screen, bg="AntiqueWhite1")

        Label(self.screen_login, text="Please enter details below to login:", font=("Calibri", 18),
              bg="AntiqueWhite1").grid(column=0, columnspan=2, row=0, padx=20, pady=(70, 20))
        Label(self.screen_login, text="Username:", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=1, sticky=W, columnspan=1, padx=(50, 0), pady=5)
        Entry(self.screen_login, textvariable=self.username_verify,
              font=("Calibri", 12)).grid(column=1, row=1, sticky=W, columnspan=1)
        Label(self.screen_login, text="Password:", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=2, sticky=W, columnspan=1, padx=(50, 0), pady=5)
        Entry(self.screen_login, textvariable=self.password_verify, font=("Calibri", 12),
              show="*").grid(column=1, row=2, sticky=W, columnspan=2)
        Button(self.screen_login, text="Login", width=10, height=1, bg="AntiqueWhite2", font=("Calibri", 14),
               command=self.login_verify).grid(column=0, row=3, columnspan=1, pady=(40, 0))
        Button(self.screen_login, text="Go back", width=10, height=1, bg="AntiqueWhite2", font=("Calibri", 14),
               command=self.main_screen).grid(column=1, row=3, columnspan=1, pady=(40, 0))

        ''' screen_register -----------------------------------------------------------------------------------------'''
        self.screen_register = Frame(self.screen, bg="AntiqueWhite1")

        Label(self.screen_register, text="Please enter details below to register:", font=("Calibri", 18),
              bg="AntiqueWhite1").grid(column=0, columnspan=3, row=0, pady=20, padx=20)
        Label(self.screen_register, text="Username: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=1, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.username, width=30,
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=1, sticky=W)
        Label(self.screen_register, text="Password: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=2, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.password, width=30, show="*",
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=2, sticky=W)
        Label(self.screen_register, text="Confirm password: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=3, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.confirm_password, width=30, show="*",
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=3, sticky=W)
        Label(self.screen_register, text="First name: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=4, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.firstname, width=30,
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=4, sticky=W)
        Label(self.screen_register, text="Last name: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=5, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.lastname, width=30,
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=5, sticky=W)
        Label(self.screen_register, text="Phone number: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=6, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.phone_number, width=30,
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=6, sticky=W)
        Label(self.screen_register, text="Email address: ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=7, sticky=W, padx=(20, 0), pady=0)
        Entry(self.screen_register, textvariable=self.email_address, width=30,
              font=("Calibri", 12)).grid(column=1, columnspan=2, row=7, sticky=W)
        Label(self.screen_register, text="Register as a ", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(column=0, row=8, sticky=W, padx=(20, 0))

        Radiobutton(self.screen_register, text="student", font=("Calibri", 14), bg="AntiqueWhite1",
                    variable=self.user_status, value=1).grid(column=1, row=8, sticky=W)
        Radiobutton(self.screen_register, text="helper", font=("Calibri", 14), bg="AntiqueWhite1",
                    variable=self.user_status, value=2).grid(column=2, row=8, sticky=W)

        Button(self.screen_register, text="Register", width=10, height=1, bg="AntiqueWhite2", font=("Calibri", 14),
               command=self.register_user).grid(column=1, row=9, sticky=W, pady=20)
        Button(self.screen_register, text="Go back", width=10, height=1, bg="AntiqueWhite2", font=("Calibri", 14),
               command=self.main_screen).grid(column=2, row=9, sticky=E, pady=(0, 0))

        ''' screen_gallery ------------------------------------------------------------------------------------------'''
        self.screen_session = Frame(self.screen, bg="AntiqueWhite1")
        self.tv_session_frame = Frame(self.screen_session, bg="AntiqueWhite1")
        self.text_session_frame = Frame(self.screen_session, bg="AntiqueWhite1")
        self.btn_frame = Frame(self.screen_session, bg="AntiqueWhite1")

        Label(self.screen_session, text="Please select one of the appointments:", bg="AntiqueWhite1",
              font=("Calibri", 16)).grid(column=0, row=0, padx=10)

        self.tv_session_frame.grid(column=0, row=1, pady=10, padx=10)
        self.sb_tv_session = Scrollbar(self.tv_session_frame)
        tv_session_columns = ('Username', 'Firstname', 'Lastname', 'Date', 'Time', 'Subject', 'Qualification')
        self.tv_session = ttk.Treeview(self.tv_session_frame, columns=tv_session_columns, show='headings',
                                       height=10, yscrollcommand=self.sb_tv_session.set)
        self.tv_session.bind('<<TreeviewSelect>>', self.view_text)
        self.tv_session.pack(side=LEFT)
        self.sb_tv_session.config(command=self.tv_session.yview)
        self.sb_tv_session.pack(side=RIGHT, fill=Y)
        for i in range(7):
            self.tv_session.column(tv_session_columns[i], width=120)
            self.tv_session.heading(tv_session_columns[i], text=tv_session_columns[i])

        self.text_session_frame.grid(column=0, row=2, columnspan=1)
        self.sb_text_session = Scrollbar(self.text_session_frame)
        self.text_session = Text(self.text_session_frame, height=4, width=105, font=("Calibri", 12), state="disabled",
                                 yscrollcommand=self.sb_text_session.set)
        self.text_session.pack(side=LEFT)
        self.sb_text_session.config(command=self.text_session.yview)
        self.sb_text_session.pack(side=RIGHT, fill=Y)

        self.btn_frame.grid(column=0, row=3, pady=10, padx=10, columnspan=1)
        self.create_btn = Button(self.btn_frame, text="Create Appointment", bg="AntiqueWhite2", height="1", width="20",
                                 font=("Calibri", 14), command=self.create_appointment)
        self.help_btn = Button(self.btn_frame, text="Help Student", bg="AntiqueWhite2", height="1", width="20",
                               font=("Calibri", 14), command=self.help_appointment)
        self.view_btn = Button(self.btn_frame, text="View your Appointments", bg="AntiqueWhite2", height="1",
                               width="20", font=("Calibri", 14), command=self.view_appointments)
        self.delete_btn = Button(self.btn_frame, text="Delete Appointment", bg="AntiqueWhite2", height="1", width="20",
                                 font=("Calibri", 14), command=self.delete_appointment)
        self.view_users_btn = Button(self.btn_frame, text="View Users", bg="AntiqueWhite2", height="1", width="20",
                                     font=("Calibri", 14), command=self.view_users)
        self.clear_db_btn = Button(self.btn_frame, text="Clear Database", bg="AntiqueWhite2", height="1", width="20",
                                   font=("Calibri", 14), command=self.clear_db)
        self.logout_btn = Button(self.btn_frame, text="Logout", bg="AntiqueWhite2", height="1", width="20",
                                 font=("Calibri", 14), command=self.main_screen)

        ''' screen_create -------------------------------------------------------------------------------------------'''
        self.screen_create = Frame(self.screen, bg="AntiqueWhite1")
        self.week_frame = Frame(self.screen_create, bg="AntiqueWhite1")
        self.cb_frame = Frame(self.screen_create, bg="AntiqueWhite1")
        self.text_create_frame = Frame(self.screen_create, bg="AntiqueWhite1")

        Label(self.screen_create, text="Please choose a day for the appointment:", bg="AntiqueWhite1",
              font=("Calibri", 16)).grid(row=0, column=0, columnspan=3, padx=0, pady=(20, 10))

        self.previous_week_btn = Button(self.screen_create, text="Previous week", bg="AntiqueWhite2",
                                        font=("Calibri", 12), command=self.previous_week)
        self.previous_week_btn.grid(row=1, column=0, pady=(0, 0))
        self.date_lbl = Label(self.screen_create, text=self.week_date, bg="AntiqueWhite1", font=("Calibri", 14))
        self.date_lbl.grid(row=1, column=1)
        self.next_week_btn = Button(self.screen_create, text="Next week", bg="AntiqueWhite2",
                                    font=("Calibri", 12), command=self.next_week)
        self.next_week_btn.grid(row=1, column=2)

        self.week_frame.grid(row=2, column=0, columnspan=3, sticky=W, padx=0, pady=10)
        week_value = (("Monday", 1), ("Tuesday", 2), ("Wednesday", 3), ("Thursday", 4), ("Friday", 5),
                      ("Saturday", 6), ("Sunday", 0))
        for day in week_value:
            Radiobutton(self.week_frame, text=day[0], value=day[1], variable=self.day_selection, font=("Calibri", 12),
                        bg="AntiqueWhite1", command=self.cb_change_time).pack(fill="none", ipady=5, side="left")

        self.cb_frame.grid(row=3, column=0, columnspan=3, pady=0, sticky=W)
        self.weekday_time = ("15:15 to 16:15", "16:15 to 17:15", "17:15 to 18:15", "18:15 to 19:15", "19:15 to 20:15")
        self.weekend_time = ("10:00 to 11:00", "11:00 to 12:00", "12:00 to 13:00", "13:00 to 14:00", "14:00 to 15:00",
                             "15:00 to 16:00", "16:00 to 17:00")
        self.cb_time = ttk.Combobox(self.cb_frame, state='readonly')
        self.cb_time.grid(row=0, column=0, padx=15)
        subjects = ("Biology", "Business", "Chemistry", "Computer science", "Economics", "English", "French",
                    "Geography", "History", "Law", "Maths", "Philosophy", "Physics", "Politics", "Psychology",
                    "Religious Studies", "Sociology", "Spanish")
        self.cb_subject = ttk.Combobox(self.cb_frame, values=subjects)
        self.cb_subject.grid(row=0, column=1, padx=15)
        qualifications = ("GCSE", "AS level", "A level")
        self.cb_qualification = ttk.Combobox(self.cb_frame, values=qualifications, state='readonly')
        self.cb_qualification.grid(row=0, column=3, padx=15)

        Label(self.screen_create, text="Work to do :", bg="AntiqueWhite1",
              font=("Calibri", 14)).grid(row=4, column=0, sticky=W, padx=(0, 0), pady=10)
        self.text_create_frame.grid(row=5, column=0, columnspan=3)
        self.sb_text_create = Scrollbar(self.text_create_frame)
        self.text_create = Text(self.text_create_frame, height=5, font=("Calibri", 12),
                                yscrollcommand=self.sb_text_create.set)
        self.text_create.pack(side=LEFT)
        self.sb_text_create.config(command=self.text_create.yview)
        self.sb_text_create.pack(side=RIGHT, fill=Y)

        Button(self.screen_create, text="Save", bg="AntiqueWhite2", width="10", font=("Calibri", 13),
               command=self.save_appointment).grid(row=6, column=1, pady=20)
        Button(self.screen_create, text="Go back", bg="AntiqueWhite2", width="10", font=("Calibri", 13),
               command=self.session).grid(row=6, column=2, padx=0)

        ''' screen_users --------------------------------------------------------------------------------------------'''
        self.screen_users = Frame(self.screen, bg="AntiqueWhite1")
        self.tv_users_frame = Frame(self.screen_users, bg="AntiqueWhite1")

        Label(self.screen_users, text="Please select one of the users:", bg="AntiqueWhite1",
              font=("Calibri", 16)).grid(row=0, column=0, columnspan=2, pady=(20, 10))

        self.tv_users_frame.grid(row=1, column=0, columnspan=2, padx=0)
        tv_users_columns = ('Username', 'Password', 'First name', 'Last name', 'Phone number', 'Email address',
                            'User status')
        self.sb_tv_users = Scrollbar(self.tv_users_frame)
        self.tv_users = ttk.Treeview(self.tv_users_frame, columns=tv_users_columns, show='headings', height=10,
                                     yscrollcommand=self.sb_tv_users.set)
        self.tv_users.pack(side=LEFT)
        self.sb_tv_users.config(command=self.tv_users.yview)
        self.sb_tv_users.pack(side=RIGHT, fill=Y)
        for i in range(7):
            self.tv_users.column(tv_users_columns[i], width=120)
            self.tv_users.heading(tv_users_columns[i], text=tv_users_columns[i])
        self.db_users()

        Button(self.screen_users, text="Delete User", bg="AntiqueWhite2", height="1", width="20",
               font=("Calibri", 14), command=self.delete_user).grid(row=2, column=0, columnspan=1, sticky=E, pady=20)

        Button(self.screen_users, command=self.session, text="Go back", width="10", font=("Calibri", 14),
               bg="AntiqueWhite2").grid(row=2, column=1, columnspan=1, padx=0)

        ''' screen_view ---------------------------------------------------------------------------------------------'''
        self.screen_view = Frame(self.screen, bg="AntiqueWhite1")
        self.tv_view_frame = Frame(self.screen_view, bg="AntiqueWhite1")

        self.tv_view_frame.pack(pady=20)
        tv_view_columns = ('Student first name', 'Student last name', 'Date', 'Time', 'Subject', 'Qualification',
                           'Helper first name', 'Helper last name')
        self.sb_tv_view = Scrollbar(self.tv_view_frame)
        self.tv_view = ttk.Treeview(self.tv_view_frame, columns=tv_view_columns, show='headings', height=10,
                                    yscrollcommand=self.sb_tv_view.set)
        self.tv_view.pack(side=LEFT)
        self.sb_tv_view.config(command=self.tv_view.yview)
        self.sb_tv_view.pack(side=RIGHT, fill=Y)
        for i in range(8):
            self.tv_view.column(tv_view_columns[i], width=120)
            self.tv_view.heading(tv_view_columns[i], text=tv_view_columns[i])
        self.db_view()

        Button(self.screen_view, command=self.session, text="Go back", width="10",
               font=("Calibri", 14), bg="AntiqueWhite2").pack(pady=10)

        '''----------------------------------------------------------------------------------------------------------'''
        cursor.execute("SELECT * FROM user_db WHERE user_status_db = 3")
        if not cursor.fetchall():
            self.screen_admin.pack()
        else:
            self.screen.configure(bg="AntiqueWhite1")
            self.screen_widgets()

    def register_admin(self):
        if self.admin_confirm_password.get() == self.admin_password.get():
            cursor.execute('INSERT INTO user_db(username_db, password_db, user_status_db) VALUES(?,?,?)',
                           [self.admin_username.get(), self.admin_password.get(), 3])
            db.commit()
            ms.showinfo("Info", "Registration success!")
            self.screen_admin.forget()
            self.screen.configure(bg="AntiqueWhite1")
            self.screen_widgets()
        else:
            ms.showinfo("Error", "Passwords don't match!")
            self.admin_confirm_password.set("")

    def screen_widgets(self):
        self.screen_lbl.pack(pady=0, fill=X)
        self.time_lbl.pack(side=BOTTOM, anchor=SE)
        self.main_screen()

    def db_users(self):
        cursor.execute("SELECT * FROM user_db WHERE user_status_db != 3 ORDER BY username_db")
        for tv_row in cursor.fetchall():
            self.tv_users.insert("", END, values=tv_row)

    def db_view(self):
        self.tv_view.delete(*self.tv_view.get_children())
        cursor.execute('''SELECT student.firstname_db, student.lastname_db, appointment_db.date_db, 
                                 appointment_db.time_db, appointment_db.subject_db, appointment_db.qualification_db, 
                                 helper.firstname_db, helper.lastname_db 
                          FROM appointment_db 
                          INNER JOIN user_db as student ON student.username_db = appointment_db.username_db 
                          INNER JOIN user_db as helper ON helper.username_db = appointment_db.helper_db 
                          WHERE (appointment_db.username_db=? OR appointment_db.helper_db=?)
                          AND appointment_db.date_db >= ? ORDER BY appointment_db.date_db, appointment_db.time_db''',
                       [self.current_username.get(), self.current_username.get(), datetime_now])
        for tv_row in cursor.fetchall():
            self.tv_view.insert("", END, values=tv_row)

    def db_student(self):
        self.tv_session.delete(*self.tv_session.get_children())

        cursor.execute('''SELECT user_db.username_db, user_db.firstname_db, user_db.lastname_db, 
                                 appointment_db.date_db, appointment_db.time_db, appointment_db.subject_db, 
                                 appointment_db.qualification_db 
                          FROM appointment_db 
                          INNER JOIN user_db ON user_db.username_db = appointment_db.username_db 
                          WHERE appointment_db.username_db = ? AND appointment_db.date_db >= ? 
                          AND appointment_db.helper_db IS NULL 
                          ORDER BY appointment_db.date_db, appointment_db.time_db''',
                       [self.current_username.get(), datetime_now])
        for tv_row in cursor.fetchall():
            self.tv_session.insert("", END, values=tv_row)

    def db_helper(self):
        self.tv_session.delete(*self.tv_session.get_children())

        cursor.execute('''SELECT user_db.username_db, user_db.firstname_db, user_db.lastname_db, 
                                 appointment_db.date_db, appointment_db.time_db, appointment_db.subject_db, 
                                 appointment_db.qualification_db 
                          FROM appointment_db 
                          INNER JOIN user_db ON user_db.username_db = appointment_db.username_db 
                          WHERE appointment_db.date_db >= ? AND appointment_db.helper_db IS NULL 
                          ORDER BY appointment_db.date_db, appointment_db.time_db''',
                       [datetime_now])
        for tv_row in cursor.fetchall():
            self.tv_session.insert("", END, values=tv_row)

    def db_admin(self):
        self.tv_session.delete(*self.tv_session.get_children())

        cursor.execute('''SELECT user_db.username_db, user_db.firstname_db, user_db.lastname_db, 
                                 appointment_db.date_db, appointment_db.time_db, appointment_db.subject_db, 
                                 appointment_db.qualification_db 
                          FROM appointment_db 
                          INNER JOIN user_db ON user_db.username_db = appointment_db.username_db 
                          ORDER BY appointment_db.date_db, appointment_db.time_db''')

        for tv_row in cursor.fetchall():
            self.tv_session.insert("", END, values=tv_row)

    def save_appointment(self):
        if self.cb_time.current() == -1:
            ms.showerror("Error", "Please select a schedule")
        elif self.cb_subject.current() == -1:
            ms.showerror("Error", "Please select a subject")
        elif self.cb_qualification.current() == -1:
            ms.showerror("Error", "Please select a qualification")
        else:
            if self.week_date < datetime_now:
                ms.showerror("Error", "Date unavailable")
            else:
                cursor.execute(
                    'SELECT * FROM appointment_db WHERE username_db = ? AND date_db = ? AND time_db = ?',
                    [self.current_username.get(), self.week_date, self.cb_time.get()])
                if cursor.fetchall():
                    ms.showerror("Error", "You have already made an appointment at this time slot")
                else:
                    cursor.execute('''INSERT INTO appointment_db(username_db, date_db, time_db, subject_db, 
                                      qualification_db, text_db) VALUES(?,?,?,?,?,?)''',
                                   [self.current_username.get(), self.week_date, self.cb_time.get(),
                                    self.cb_subject.get(), self.cb_qualification.get(),
                                    self.text_create.get('1.0', 'end')])
                    db.commit()

                    self.db_student()

                    ms.showinfo("Saved", "Appointment saved")
                    self.session()

    def update_week_date(self):
        self.week_date = datetime.strptime(
            '{}-W{}-{}'.format(now_year, now_week, self.day_selection.get()), "%Y-W%W-%w").date()
        self.week_date = self.week_date + self.week_counter * self.week_delta
        self.date_lbl['text'] = self.week_date

    def cb_change_time(self):
        if self.day_selection.get() != 6 and self.day_selection.get() != 0:
            self.cb_time['values'] = self.weekday_time
        elif self.day_selection.get() == 6 or self.day_selection.get() == 0:
            self.cb_time['values'] = self.weekend_time
        self.cb_time.set("Select a Schedule")

        self.update_week_date()

    def previous_week(self):
        self.week_counter = self.week_counter - 1
        if self.week_counter <= 0:
            self.previous_week_btn["state"] = DISABLED
        self.update_week_date()

    def next_week(self):
        self.week_counter = self.week_counter + 1
        self.previous_week_btn["state"] = NORMAL
        self.update_week_date()

    def create_appointment(self):
        self.screen.title("Create")
        self.screen_session.forget()
        self.screen_create.pack()

        self.week_counter = 0
        self.previous_week_btn["state"] = DISABLED
        self.day_selection.set(1)
        self.cb_change_time()
        self.cb_subject.set("Select a Subject")
        self.cb_qualification.set("Select a Qualification")
        self.text_create.delete('1.0', END)

    def tv_session_selection(self):
        self.selected_index = self.tv_session.selection()
        self.username_index = self.tv_session.item(self.selected_index)['values'][0]
        self.date_index = self.tv_session.item(self.selected_index)['values'][3]
        self.time_index = self.tv_session.item(self.selected_index)['values'][4]

    def view_text(self, _):
        if len(self.tv_session.selection()) > 0:
            self.tv_session_selection()

            fetch_text = cursor.execute('''SELECT text_db FROM appointment_db WHERE username_db = ? AND date_db = ? 
                                           AND time_db = ?''',
                                        [self.username_index, self.date_index, self.time_index]).fetchone()

            self.text_session.configure(state="normal")
            self.text_session.delete('1.0', END)
            self.text_session.insert(END, fetch_text[0])
            self.text_session.configure(state="disabled")

    def help_appointment(self):
        if len(self.tv_session.selection()) > 0:
            self.tv_session_selection()

            ms_help = ms.askyesno('Confirm Appointment', 'Are you sure you want to attend this appointment?')
            if ms_help:
                cursor.execute('''UPDATE appointment_db SET helper_db = ? WHERE username_db = ? 
                                  AND date_db = ? AND time_db = ?''',
                               [self.current_username.get(), self.username_index, self.date_index, self.time_index])
                db.commit()
                self.tv_session.delete(self.selected_index)
                self.text_session.configure(state="normal")
                self.text_session.delete('1.0', END)
                self.text_session.configure(state="disabled")
                ms.showinfo('Confirm Appointment', 'Appointment confirmed successfully')

    def delete_appointment(self):
        if len(self.tv_session.selection()) > 0:
            self.tv_session_selection()

            ms_delete = ms.askyesno('Delete Appointment', 'Are you sure you want to delete this appointment?')
            if ms_delete:
                cursor.execute("DELETE FROM appointment_db WHERE username_db = ? AND date_db = ? AND time_db = ?",
                               [self.username_index, self.date_index, self.time_index])
                db.commit()
                self.tv_session.delete(self.selected_index)
                self.text_session.configure(state="normal")
                self.text_session.delete('1.0', END)
                self.text_session.configure(state="disabled")
                ms.showinfo('Delete Appointment', 'Appointment deleted successfully')

    def view_appointments(self):
        self.screen.title("View your appointments")
        self.db_view()
        if len(self.tv_view.selection()) > 0:
            self.tv_view.selection_remove(self.tv_view.selection()[0])
        self.screen_session.forget()
        self.screen_view.pack()

    def delete_user(self):
        if len(self.tv_users.selection()) > 0:
            selected_index = self.tv_users.selection()
            username_index = self.tv_users.item(selected_index)['values'][0]

            ms_delete = ms.askyesno('Delete User',
                                    'All appointments related to this user will also be deleted. Continue?')
            if ms_delete:
                cursor.execute("DELETE FROM user_db WHERE username_db = ?",
                               [username_index])
                cursor.execute("DELETE FROM appointment_db WHERE username_db = ? OR helper_db = ?",
                               [username_index, username_index])
                db.commit()
                self.tv_users.delete(selected_index)
                ms.showinfo('Delete User', 'User deleted successfully')
                self.db_admin()

    def view_users(self):
        self.screen.title("View Users")
        if len(self.tv_users.selection()) > 0:
            self.tv_users.selection_remove(self.tv_users.selection()[0])
        self.screen_session.forget()
        self.screen_users.pack()

    def clear_db(self):
        ms_clear = ms.askyesno('Clear Database', 'All past appointments will be deleted from the database. Continue?')
        if ms_clear:
            cursor.execute("DELETE FROM appointment_db WHERE appointment_db.date_db < ?",
                           [datetime_now])
            db.commit()
            self.db_admin()
            ms.showinfo('Clear Database', 'Database cleared successfully')

    def session_student(self):
        self.screen_lbl['text'] = "Welcome to the dashboard, Student"
        self.create_btn.pack(side=LEFT, padx=0)
        self.view_btn.pack(side=LEFT, padx=0)
        self.delete_btn.pack(side=LEFT, padx=0)
        self.logout_btn.pack(side=LEFT, padx=0)

    def session_helper(self):
        self.screen_lbl['text'] = "Welcome to the dashboard, Helper"
        self.help_btn.pack(side=LEFT, padx=0)
        self.view_btn.pack(side=LEFT, padx=0)
        self.logout_btn.pack(side=LEFT, padx=0)

    def session_admin(self):
        self.screen_lbl['text'] = "Welcome to the dashboard, Administrator"
        self.delete_btn.pack(side=LEFT, padx=0)
        self.view_users_btn.pack(side=LEFT, padx=0)
        self.clear_db_btn.pack(side=LEFT, padx=0)
        self.logout_btn.pack(side=LEFT, padx=0)

    def session(self):
        self.screen.title("Dashboard")

        self.screen_create.forget()
        self.screen_view.forget()
        self.screen_users.forget()

        if len(self.tv_session.selection()) > 0:
            self.tv_session.selection_remove(self.tv_session.selection()[0])

        self.text_session.configure(state="normal")
        self.text_session.delete('1.0', END)
        self.text_session.configure(state="disabled")

        self.screen_session.pack()

    def session_selection(self):
        self.screen_login.forget()

        for child in self.btn_frame.winfo_children():
            child.forget()

        self.selection_db = cursor.execute("SELECT user_status_db FROM user_db WHERE username_db = ?",
                                           [self.current_username.get()]).fetchone()

        if self.selection_db[0] == 1:
            self.db_student()
            self.session_student()
        elif self.selection_db[0] == 2:
            self.db_helper()
            self.session_helper()
        elif self.selection_db[0] == 3:
            self.db_admin()
            self.tv_users.delete(*self.tv_users.get_children())
            self.db_users()
            self.session_admin()

        self.session()

    def login_verify(self):
        cursor.execute("SELECT username_db FROM user_db WHERE username_db = ?", [(self.username_verify.get())])
        if cursor.fetchone():
            cursor.execute("SELECT * FROM user_db WHERE username_db = ? AND password_db = ?",
                           [(self.username_verify.get()), (self.password_verify.get())])
            if cursor.fetchone():
                self.current_username.set(self.username_verify.get())
                self.username_verify.set("")
                self.password_verify.set("")
                self.session_selection()
            else:
                ms.showerror("Error", "Password error!")
        else:
            ms.showerror("Error", "User not found!")
            self.username_verify.set("")
            self.password_verify.set("")

    def login(self):
        self.screen.title("Login")
        self.username_verify.set("")
        self.password_verify.set("")
        self.screen_main.forget()
        self.screen_login.pack()

    def register_user(self):
        if self.username.get() == '':
            ms.showerror("Error", "Please enter your username")
        else:
            cursor.execute('SELECT username_db FROM user_db WHERE username_db = ?', [self.username.get()])
            if cursor.fetchall():
                ms.showerror("Error", "Username taken!")
                self.username.set("")
            elif self.confirm_password.get() != self.password.get():
                ms.showerror("Error", "Passwords don't match!")
                self.confirm_password.set("")
            elif self.firstname.get() == '':
                ms.showerror("Error", "Please enter your first name")
            elif self.lastname.get() == '':
                ms.showerror("Error", "Please enter your last name")
            elif self.user_status.get() == 0:
                ms.showerror("Error", "Please select an option between student and helper")
            else:
                cursor.execute('INSERT INTO user_db VALUES(?,?,?,?,?,?,?)',
                               [self.username.get(), self.password.get(), self.firstname.get(), self.lastname.get(),
                                self.phone_number.get(), self.email_address.get(), self.user_status.get()])
                db.commit()
                ms.showinfo("Info", "Registration success!")
                self.main_screen()

    def register(self):
        self.screen.title("Register")
        self.username.set("")
        self.password.set("")
        self.confirm_password.set("")
        self.firstname.set("")
        self.lastname.set("")
        self.phone_number.set("")
        self.email_address.set("")
        self.user_status.set(0)

        self.screen_main.forget()
        self.screen_register.pack()

    def time(self):
        self.time_lbl.configure(text=strftime('%H:%M:%S %p'))
        self.time_lbl.after(1000, self.time)

    def main_screen(self):
        self.screen_register.forget()
        self.screen_login.forget()
        self.screen_session.forget()
        self.time()

        self.screen.title('Students Booking System')
        self.screen_lbl['text'] = "Students Booking System"
        self.screen_main.pack()


if __name__ == '__main__':
    root = Tk()
    Main(root)
    root.mainloop()
