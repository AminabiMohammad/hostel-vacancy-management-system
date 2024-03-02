from tkinter import Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, messagebox, Toplevel,ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import scrolledtext
import csv

# Establishing connection to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Amina@123',
    database='mydatabase'
)
cursor = conn.cursor()

fonts = ('Calibri', 25, 'bold')
font1 = ('Calibri', 20, 'bold')


class Login:
    def __init__(self, root,cursor):
        self.root = root
        self.login_frame = Frame(self.root, bg='Light yellow')
        self.login_frame.pack(fill='both', expand=True)

        logo_image = Image.open("newlogo.bmp")
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = Label(self.login_frame, image=self.logo_photo, bg='Light yellow')
        logo_label.pack(side="left", padx=5, pady=5)
        logo_label.pack(anchor="nw", padx=5, pady=5)

        college_label = Label(self.login_frame, text='SHRI VISHNU ENGINEERING COLLEGE FOR WOMEN \n BHIMAVARAM',
                              font=('Calibri', 30, 'bold'), bg='Light Yellow', fg='Dark orange')
        college_label.pack(padx=5, pady=5)

        student_login_frame = Frame(self.login_frame, width=600, height=500, bg='Light Yellow')
        student_login_frame.pack(side='left', fill='both', expand=True)

        title_label = Label(student_login_frame, text='Student Login', font=font1, bg='Dark Orange', fg='White')
        title_label.place(x=(student_login_frame.winfo_reqwidth() - title_label.winfo_reqwidth()) / 1.5, y=70)

        self.user_name = Label(student_login_frame, text='USER NAME  : ', font=fonts, bg='white', fg='Orange', width=12)
        self.user_name.place(x=50, y=150)
        self.user_name_entry = Entry(student_login_frame, width=13, font=font1, bg='white')
        self.user_name_entry.place(x=280, y=150)

        self.user_pass = Label(student_login_frame, text='PASSWORD  : ', font=fonts, bg='white', fg='Orange', width=12)
        self.user_pass.place(x=50, y=200)
        self.user_pass_entry = Entry(student_login_frame, width=13, font=font1, bg='white', show=".")
        self.user_pass_entry.place(x=280, y=200)

        self.submit_btn = Button(student_login_frame, text='Student Login', fg='White', bg='Dark Orange', font=font1,
                                 command=self.check_student_login, cursor='hand2', activebackground='Light Yellow')
        self.submit_btn.place(x=220, y=300)

        self.student_photo_label = Label(student_login_frame)
        self.student_photo_label.place(x=90, y=300)

        self.user_name_entry.bind("<Return>", lambda event: self.user_pass_entry.focus())
        self.user_pass_entry.bind("<Return>", lambda event: self.check_student_login())

        admin_login_frame = Frame(self.login_frame, width=600, height=500, bg='Light Yellow')
        admin_login_frame.pack(side='right', fill='both', expand=True)

        title_label = Label(admin_login_frame, text='Admin Login', font=font1, bg='Dark Orange', fg='White')
        title_label.place(x=(admin_login_frame.winfo_reqwidth() - title_label.winfo_reqwidth()) / 1.5, y=60)

        self.admin_user_name = Label(admin_login_frame, text='USER NAME  : ', font=fonts, bg='white', fg='Orange',
                                      width=12)
        self.admin_user_name.place(x=100, y=150)
        self.admin_user_name_entry = Entry(admin_login_frame, width=13, font=font1, bg='white')
        self.admin_user_name_entry.place(x=350, y=150)

        self.admin_user_pass = Label(admin_login_frame, text='PASSWORD  : ', font=fonts, bg='white', fg='Orange',
                                      width=12)
        self.admin_user_pass.place(x=100, y=200)
        self.admin_user_pass_entry = Entry(admin_login_frame, width=13, font=font1, bg='white', show=".")
        self.admin_user_pass_entry.place(x=350, y=200)

        self.admin_submit_btn = Button(admin_login_frame, text='Admin Login', fg='White', bg='Dark Orange', font=font1,
                                       command=self.check_admin_login, cursor='hand2', activebackground='Light Yellow')
        self.admin_submit_btn.place(x=250, y=300)

        self.admin_photo_label = Label(admin_login_frame)
        self.admin_photo_label.place(x=110, y=300)

        self.admin_user_name_entry.bind("<Return>", lambda event: self.admin_user_pass_entry.focus())
        self.admin_user_pass_entry.bind("<Return>", lambda event: self.check_admin_login())

        self.resize_images()

    def resize_images(self):
        student_photo = Image.open("student1.jpg")
        student_photo = student_photo.resize((105, 95), Image.LANCZOS)
        self.student_photo = ImageTk.PhotoImage(student_photo)
        self.student_photo_label.config(image=self.student_photo)

        admin_photo = Image.open("admin.jpg")
        admin_photo = admin_photo.resize((95, 87), Image.LANCZOS)
        self.admin_photo = ImageTk.PhotoImage(admin_photo)
        self.admin_photo_label.config(image=self.admin_photo)

    def check_student_login(self):
        name = self.user_name_entry.get()
        password = self.user_pass_entry.get()
    
        

        if password != "svecw":
            messagebox.showerror('WRONG PASSWORD', 'Incorrect password. Please try again.')
            return

        cursor.execute("SELECT * FROM student WHERE name = %s", (name,))
        user = cursor.fetchone()

        if user:  
            messagebox.showinfo('WELCOME', 'WELCOME USER')
            self.login_frame.destroy()
            self.student_dashboard()
        else:  
            cursor.execute("INSERT INTO student (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            messagebox.showinfo('WELCOME', 'WELCOME USER')
            self.login_frame.destroy()
            dashboard = Dashboard(self.root, admin=False)

    def student_dashboard(self):
        student_dashboard_frame = Frame(self.root, bg='Light Green')
        student_dashboard_frame.pack(fill='both', expand=True)

        logout_btn = Button(student_dashboard_frame, text="Logout", command=self.logout, bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1, activebackground='Dark Orange', bd=0, cursor='hand2')
        logout_btn.pack(pady=10)

        hostel_label = Label(student_dashboard_frame, text="Select Hostel:", font=('Calibri', 14, 'bold'),
                             bg='Light Green')
        hostel_label.pack(pady=10)

        self.search_var = Entry(student_dashboard_frame, font=('Calibri', 14), bg='white')
        self.search_var.pack(pady=5, padx=10)
        self.search_var.bind('<KeyRelease>', self.filter_hostel_list)

        self.hostel_listbox = Listbox(student_dashboard_frame, font=('Calibri', 14), bg='white', height=5)
        self.hostel_listbox.pack(pady=5, padx=10)
        scrollbar = Scrollbar(student_dashboard_frame, orient="vertical")
        scrollbar.config(command=self.hostel_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.hostel_listbox.config(yscrollcommand=scrollbar.set)

        hostel_names =["Sarada", "Medha", "Vaishnavi", "Yashoda", "Manasa", "Padmavathi", "Nirmala", "Sita", "Bhargavi"]
        for hostel in hostel_names:
            self.hostel_listbox.insert('end', hostel)

        self.hostel_listbox.bind("<<ListboxSelect>>", self.display_hostel_details)

        self.hostel_details_frame = Frame(student_dashboard_frame, bg='Light Green')
        self.hostel_details_frame.pack(pady=10)

        self.hostel_details_label = Label(self.hostel_details_frame, text="", font=('Calibri', 14), bg='Light Green')
        self.hostel_details_label.pack(pady=10)

    def filter_hostel_list(self, event):
        search_term = self.search_var.get().lower()
        self.hostel_listbox.delete(0, 'end')
        filtered_hostels =[hostel for hostel in ["Sarada", "Medha", "Vaishnavi", "Yashoda", "Manasa", "Padmavathi", "Nirmala", "Sita", "Bhargavi"] if search_term in hostel.lower()]
        for hostel in filtered_hostels:
            self.hostel_listbox.insert('end', hostel)

    def display_hostel_details(self, event):
        selected_index = self.hostel_listbox.curselection()
        if selected_index:
            selected_hostel = self.hostel_listbox.get(selected_index)
            cursor.execute("SELECT room_no, beds FROM hostel WHERE hostel_name = %s", (selected_hostel,))
            hostel_details = cursor.fetchall()
            details_text = "Hostel Details:\n"
            for detail in hostel_details:
                details_text += f"Room No: {detail[0]}, Beds: {detail[1]}\n"
            self.hostel_details_label.config(text=details_text)
        else:
            self.hostel_details_label.config(text="")

    def check_admin_login(self):
        name = self.admin_user_name_entry.get()
        password = self.admin_user_pass_entry.get()

        cursor.execute("SELECT * FROM admin1 WHERE name = %s", (name,))
        admin = cursor.fetchone()

        if admin:  
            if password == admin[1]: 
                messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
                self.login_frame.destroy()
                dashboard = Dashboard(self.root, admin=True)
            else:
                messagebox.showerror('WRONG PASSWORD', 'CHECK YOUR PASSWORD')
        else: 
            cursor.execute("INSERT INTO admin1 (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            messagebox.showinfo('WELCOME', 'WELCOME ADMIN')
            self.login_frame.destroy()
            dashboard = Dashboard(self.root, admin=True)

    def logout(self):
        self.root.destroy()
        new_root = Tk()
        new_root.title('LOGIN')
        new_root.geometry('1300x500+200+140')
        new_root.resizable(False, False)
        login = Login(new_root,cursor)
        new_root.mainloop()

class Dashboard:
    def __init__(self, root, admin=False):
        self.root = root
        self.admin = admin
        if admin:
            self.root.title('ADMIN DASHBOARD')
            bg_color = 'Light Blue'

            self.admin_dashboard()
        else:
            self.root.title('STUDENT DASHBOARD')
            bg_color = 'Light Green'
            self.student_dashboard()

    def admin_dashboard(self):
        admin_dashboard_frame = Frame(self.root, bg='Light Yellow')  # Change background color here
        admin_dashboard_frame.pack(fill='both', expand=True)

        admin_image = Image.open("admin.jpg")
        admin_image = admin_image.resize((400, 400), Image.LANCZOS)
        self.admin_photo = ImageTk.PhotoImage(admin_image)
        admin_photo_label = Label(admin_dashboard_frame, image=self.admin_photo, bg='Light Yellow')
        admin_photo_label.pack(side="left", padx=5, pady=5)
        admin_photo_label.pack(anchor="nw", padx=5, pady=5)

        buttons_data = [
            ("ADD", self.add_data),
            ("UPDATE", self.update_data),
            ("DELETE", self.delete_data),
        ]
        
        for button_text, command_func in buttons_data:
            if button_text == "LOGOUT":
                button = Button(admin_dashboard_frame, text=button_text, command=command_func,
                                bg='red', fg='white', font=('Calibri', 14, 'bold'), width=10, height=2,
                                bd=0, cursor='hand2')
            else:
                button = Button(admin_dashboard_frame, text=button_text, command=command_func,
                                bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=2,
                                activebackground='Dark Orange', bd=0, cursor='hand2')
            button.pack(pady=10)
        logout_btn = Button(admin_dashboard_frame, text="Logout", command=self.logout, bg='Red', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1, activebackground='Dark Orange', bd=0, cursor='hand2')
        logout_btn.pack(pady=10)

        cursor.execute("SELECT * FROM hostel")
        hostels = cursor.fetchall()

        # Create a Combobox widget to display hostel details
        self.hostel_combobox = ttk.Combobox(admin_dashboard_frame, font=('Calibri', 14), state="readonly")
        self.hostel_combobox.pack(pady=10)

        # Extract hostel names and details

        hostel_details = []
        for hostel in hostels:
            hostel_name = hostel[0]
            room_no = hostel[1]
            beds = hostel[2]
            hostel_details.append((hostel_name, room_no, beds))

        self.hostel_combobox['values'] = hostel_details

        self.hostel_combobox.bind("<<ComboboxSelected>>", self.display_hostel_details)

    def display_hostel_details(self, event):
        selected_hostel = self.hostel_combobox.get()
        print(f"Selected Hostel Details: {selected_hostel}")
    

    def add_data(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Data")
        add_window.geometry("400x240")

        self.center_window(add_window)

        hostel_label = Label(add_window, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        hostel_label.grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(add_window, font=('Calibri', 14), bg='white')
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        room_label = Label(add_window, text="Room No:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        room_label.grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(add_window, font=('Calibri', 14), bg='white')
        room_entry.grid(row=1, column=1, padx=10, pady=10)
        beds_label = Label(add_window, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        beds_label.grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(add_window, font=('Calibri', 14), bg='white')
        beds_entry.grid(row=2, column=1, pady=10)

        store_btn = Button(add_window, text="ADD", command=lambda: self.store_data(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                           bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1,
                           activebackground='Dark Orange', bd=0, cursor='hand2')
        store_btn.grid(row=3, column=0, columnspan=2, pady=10)

        

    def update_data(self):
        update_window = Toplevel(self.root)
        update_window.title("Update Data")
        update_window.geometry("400x200")

        self.center_window(update_window)

        hostel_label = Label(update_window, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        hostel_label.grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(update_window, font=('Calibri', 14), bg='white')
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        room_label = Label(update_window, text="Room No:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        room_label.grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(update_window, font=('Calibri', 14), bg='white')
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        beds_label = Label(update_window, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        beds_label.grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(update_window, font=('Calibri', 14), bg='white')
        beds_entry.grid(row=2, column=1, pady=10)

        store_btn = Button(update_window, text="UPDATE", command=lambda: self.update_data_in_db(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                        bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1,
                        activebackground='Dark Orange', bd=0, cursor='hand2')
        store_btn.grid(row=3, column=0, columnspan=2, pady=10)


    def delete_data(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Data")
        delete_window.geometry("400x200")

        self.center_window(delete_window)

        hostel_label = Label(delete_window, text="Hostel Name:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        hostel_label.grid(row=0, column=0, padx=10, pady=10)
        hostel_entry = Entry(delete_window, font=('Calibri', 14), bg='white')
        hostel_entry.grid(row=0, column=1, padx=10, pady=10)

        room_label = Label(delete_window, text="Room No:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        room_label.grid(row=1, column=0, padx=10, pady=10)
        room_entry = Entry(delete_window, font=('Calibri', 14), bg='white')
        room_entry.grid(row=1, column=1, padx=10, pady=10)

        beds_label = Label(delete_window, text="Number of Beds:", font=('Calibri', 14, 'bold'), bg='Light Yellow')
        beds_label.grid(row=2, column=0, padx=10, pady=10)
        beds_entry = Entry(delete_window, font=('Calibri', 14), bg='white')
        beds_entry.grid(row=2, column=1, pady=10)

        store_btn = Button(delete_window, text="DELETE", command=lambda: self.delete_data_from_db(hostel_entry.get(), room_entry.get(), beds_entry.get()),
                        bg='Dark Orange', fg='white', font=('Calibri', 14, 'bold'), width=10, height=1,
                        activebackground='Dark Orange', bd=0, cursor='hand2')
        store_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def display_history(self):
        history_window = Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("600x400")

        # Centering the window on the screen
        self.center_window(history_window)

        history_text = scrolledtext.ScrolledText(history_window, width=60, height=20)
        history_text.pack(expand=True, fill='both')

        # Read history from CSV file and display it in the text area
        with open("hostel_history.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                history_text.insert('end', ', '.join(row) + '\n')

     # store the data in the database
    def store_data(self, hostel_name, room_no, beds):
        with open("hostel_history.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([hostel_name, room_no, beds])
        print("Data stored successfully.")

    # Insert data into the database table
    def store_data(self, hostel_name, room_no, beds):
        try:
            cursor.execute("INSERT INTO hostel (hostel_name, room_no, beds) VALUES (%s, %s, %s)", (hostel_name, room_no, beds))
            conn.commit() 
            messagebox.showinfo("Success", "Data added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    # Update data in the database table
    def update_data_in_db(self, hostel_name, room_no, beds):
        try:
            cursor.execute("UPDATE hostel SET beds = %s WHERE hostel_name = %s AND room_no = %s", (beds, hostel_name, room_no))
            conn.commit() 
            messagebox.showinfo("Success", "Data updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    # Delete data from the database table
    def delete_data_from_db(self, hostel_name, room_no, beds):
        try:
            cursor.execute("DELETE FROM hostel WHERE hostel_name = %s AND room_no = %s AND beds = %s", (hostel_name, room_no, beds))
            conn.commit()  
            messagebox.showinfo("Success", "Data deleted successfully.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def logout(self):
        self.root.destroy()
        new_root = Tk()
        new_root.title('LOGIN')
        new_root.geometry('1300x500+200+140')
        new_root.resizable(False, False)
        login = Login(new_root,cursor)
        new_root.mainloop()

    # Centering the window on the screen
    def center_window(self, window):
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(window.winfo_screenheight() / 2 - window_height / 2)
        window.geometry("+{}+{}".format(position_right, position_down))


if __name__ == "__main__":
    root = Tk()
    root.title('LOGIN')
    root.geometry('1300x500+200+140')
    root.resizable(False, False)
    login = Login(root,cursor)
    root.mainloop()
