from tkinter import *
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Appointment
import bcrypt
from tkcalendar import DateEntry
from datetime import datetime
from PIL import ImageTk, Image

# Initializing the database connection
engine = create_engine('sqlite:///HairbyFrida.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class HairbyFridaApp:
    def __init__(self, root):
        self.time_var = None
        self.service_var = None
        self.date_entry = None
        self.root = root
        self.root.title("Hair By Frida")

        # Load background image
        self.bg_image = Image.open("C:\\Users\\Kachisicho\\PycharmProjects\\pythonProject\\hairbyfrida2.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Initialize StringVars for user inputs
        self.login_username_var = StringVar()
        self.login_password_var = StringVar()
        self.register_username_var = StringVar()
        self.register_password_var = StringVar()
        self.register_email_var = StringVar()
        self.register_phone_var = StringVar()
        self.register_gender_var = StringVar()
        self.register_role_var = StringVar()
        self.appointment_date_var = StringVar()
        self.appointment_time_var = StringVar()

        self.current_user_id = None  # Store the logged-in user's ID
        self.username_entry = None
        self.password_entry = None

        # Create login screen
        self.create_login_screen()

    def clear_screen(self):
        """Utility function to clear the current screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_background(self):
        """Create the background for the screen"""
        background_label = Label(self.root, image=self.bg_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_login_screen(self):
        """Create the login screen UI"""
        self.clear_screen()
        self.root.geometry("800x600")  # 400x300

        self.create_background()  # set background image

        title_label = Label(self.root, text="Welcome to Hair by Frida", font=("Baskerville Old Face", 20, "bold"),
                            bg="lightpink")
        title_label.grid(row=0, column=1, columnspan=2, pady=(10, 20))

        # Configure the grid layout to center the widgets
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Login screen widgets
        Label(self.root, text="Username", bg="brown").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        Entry(self.root, textvariable=self.login_username_var, bg="lightpink").grid(row=1, column=2, padx=10, pady=5,
                                                                                    sticky="w")

        Label(self.root, text="Password", bg="brown").grid(row=2, column=1, padx=10, pady=5, sticky="e")
        Entry(self.root, textvariable=self.login_password_var, show='*', bg="lightpink").grid(row=2, column=2, padx=10,
                                                                                              pady=5,
                                                                                              sticky="w")

        Button(self.root, text="Login", command=self.login, bg="brown").grid(row=3, column=1, columnspan=2, pady=10,
                                                                             sticky="ew")
        Button(self.root, text="Go to Register", command=self.create_register_screen, bg="brown").grid(row=4, column=1,
                                                                                                       columnspan=2,
                                                                                                       pady=5,
                                                                                                       sticky="ew")

    def create_register_screen(self):
        """Create the registration screen UI"""
        self.clear_screen()
        self.root.geometry("800x600")  # 400x500
        self.create_background()

        title_label = Label(self.root, text="Register With Us Now!", font=("Baskerville Old Face", 20, "bold"),
                            bg="lightpink")
        title_label.grid(row=0, column=1, columnspan=2, pady=(10, 20))

        # Set default values for role and gender
        self.register_role_var.set("Select Role")
        self.register_gender_var.set("Select Gender")

        # Configure the grid layout to center the widgets
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Registration screen widgets
        Label(self.root, text="Username", bg="brown").grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        Entry(self.root, textvariable=self.register_username_var, bg="lightpink").grid(row=1, column=2, padx=10, pady=5,
                                                                                       sticky="ew")

        Label(self.root, text="Password", bg="brown").grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        Entry(self.root, textvariable=self.register_password_var, show='*', bg="lightpink").grid(row=2, column=2,
                                                                                                 padx=10, pady=5,
                                                                                                 sticky="ew")

        Label(self.root, text="Email", bg="brown").grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        Entry(self.root, textvariable=self.register_email_var, bg="lightpink").grid(row=3, column=2, padx=10, pady=5,
                                                                                    sticky="ew")

        Label(self.root, text="Phone Number", bg="brown").grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        Entry(self.root, textvariable=self.register_phone_var, bg="lightpink").grid(row=4, column=2, padx=10, pady=5,
                                                                                    sticky="ew")

        Label(self.root, text="Role", bg="brown").grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        OptionMenu(self.root, self.register_role_var, "Customer", "Staff", "Admin").grid(row=5, column=2, padx=10,
                                                                                         pady=5, sticky="ew")

        Label(self.root, text="Gender", bg="brown").grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        OptionMenu(self.root, self.register_gender_var, "Male", "Female", "Other").grid(row=6, column=2, padx=10,
                                                                                        pady=5, sticky="ew")

        Button(self.root, text="Register", command=self.register, bg="brown").grid(row=7, column=2, pady=10,
                                                                                   sticky="ew")

    def login(self):
        """Handle user login"""
        username = self.login_username_var.get()
        password = self.login_password_var.get()

        # Query the database for the user
        user = session.query(User).filter_by(username=username).first()

        # Check if the user exists and if the password matches
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.current_user_id = user.id  # Store current user ID

            # Redirect to dashboard based on role
            if user.role == 'Customer':
                self.create_customer_dashboard()
            elif user.role == 'Staff':
                self.create_staff_dashboard()
            elif user.role == 'Admin':
                self.create_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def register(self):
        """Handle user registration"""
        username = self.register_username_var.get()
        password = self.register_password_var.get()
        email = self.register_email_var.get()
        phone = self.register_phone_var.get()
        role = self.register_role_var.get()
        gender = self.register_gender_var.get()

        # Validate input fields
        if not username or not password or not email or not phone or role == "Select Role" or gender == "Select Gender":
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check if the username or email already exists
        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            messagebox.showerror("Error", "Username or Email already exists!")
            return
        if existing_user:
            if existing_user.username == username:
                messagebox.showerror("Error", "Username already exists!")
            elif existing_user.email == email:
                messagebox.showerror("Error", "Email already exists!")
            elif existing_user.phone == phone:
                messagebox.showerror("Error", "Phone number already exists!")
            return

        # Hash the password and save the new user
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password.decode('utf8'), email=email, phone=phone,
                        role=role, gender=gender)
        session.add(new_user)
        session.commit()

        messagebox.showinfo("Registration Success", f'User "{username}" has been registered successfully')
        self.create_login_screen()

    def create_customer_dashboard(self):
        """Create the customer dashboard screen"""
        self.clear_screen()
        self.root.geometry("800x600")  # 400x300

        self.create_background()

        # Configure the grid layout to center the widgets
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Dashboard screen widgets
        Label(self.root, text="Customer Dashboard", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(
            row=1,
            column=1,
            columnspan=2,
            pady=10)

        Button(self.root, text="View Available Services", command=self.view_services, bg="brown").grid(row=2, column=1,
                                                                                                       columnspan=2,
                                                                                                       pady=5,
                                                                                                       sticky="ew")
        Button(self.root, text="Book Appointment", command=self.book_appointment, bg="brown").grid(row=3, column=1,
                                                                                                   columnspan=2,
                                                                                                   pady=5, sticky="ew")
        Button(self.root, text="View Appointment History", command=self.view_appointment_history, bg="brown").grid(
            row=4, column=1,
            columnspan=2,
            pady=5,
            sticky="ew")

        Button(self.root, text="Logout", command=self.create_login_screen, bg="brown").grid(row=5, column=1,
                                                                                            columnspan=2, pady=10,
                                                                                            sticky="ew")

    def view_services(self):
        """Display available services to the customer"""
        self.clear_screen()

        self.create_background()

        # Mock-up of available services
        services = [
            {"name": "Haircut", "price": "15,000"},
            {"name": "Hair Coloring", "price": "10,000"},
            {"name": "Hair Styling", "price": "15,000"},
            {"name": "Hair Braiding", "price": "30,000"},
            {"name": "Manicure", "price": "10,000"},
            {"name": "Pedicure", "price": "10,000"},
        ]

        Label(self.root, text="Available Services", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(
            row=0,
            column=1,
            padx=10,
            pady=10)
        for i, service in enumerate(services, start=1):
            Label(self.root, text=f"{service['name']} - {service['price']}", bg="lightpink").grid(row=i, column=1,
                                                                                                  padx=10, pady=5)

        Button(self.root, text="Back", command=self.create_customer_dashboard, bg="brown").grid(row=len(services) + 1,
                                                                                                column=1,
                                                                                                pady=10)

    def book_appointment(self):
        """Create the book appointment screen"""
        self.clear_screen()
        self.root.geometry("800x600")  # 400x400

        self.create_background()

        # Configure the grid layout to center the widgets
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # Title
        Label(self.root, text="Book an Appointment", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(
            row=1,
            column=1,
            columnspan=2,
            pady=(
                10,
                20),
            sticky="n")

        # Select Service
        Label(self.root, text="Select Service:", bg="brown").grid(row=2, column=1, sticky="e", pady=5)
        self.service_var = StringVar(self.root)
        self.service_var.set("Haircut")  # Default value
        OptionMenu(self.root, self.service_var, "Haircut", "Hair Coloring", "Hair Styling", "Hair Braiding", "Manicure",
                   "Pedicure").grid(row=2, column=2, sticky="w",
                                    pady=5)

        # Select Date using date picker
        Label(self.root, text="Select Date:", bg="brown").grid(row=3, column=1, sticky="e", pady=5)
        self.appointment_date_var = StringVar(self.root)
        self.date_entry = DateEntry(self.root, textvariable=self.appointment_date_var, date_pattern='yyyy-mm-dd',
                                    bg="lightpink")
        self.date_entry.grid(row=3, column=2, sticky="w", pady=5)

        # Select Time
        Label(self.root, text="Select Time:", bg="brown").grid(row=4, column=1, sticky="e", pady=5)
        self.time_var = StringVar(self.root)
        self.time_var.set("10:00 AM")  # Default time
        Entry(self.root, textvariable=self.time_var, bg="lightpink").grid(row=4, column=2, sticky="w", pady=5)

        # Confirm Button
        Button(self.root, text="Confirm Appointment", command=self.confirm_appointment, bg="brown").grid(row=5,
                                                                                                         column=1,
                                                                                                         columnspan=2,
                                                                                                         pady=(20, 10))

        # Back Button
        Button(self.root, text="Back", command=self.create_customer_dashboard, bg="brown").grid(row=6, column=1,
                                                                                                columnspan=2,
                                                                                                pady=(10, 20))

    def confirm_appointment(self):
        """Confirm and save the appointment to the database"""
        user_id = self.current_user_id
        service = self.service_var.get()
        date_str = self.appointment_date_var.get()
        time_str = self.appointment_time_var.get()

        # Convert date_str to a date object
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Ensure the date format is correct
        except ValueError as e:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format")
            return

        # Create new appointment
        new_appointment = Appointment(user_id=user_id, date=appointment_date, service=service, time=time_str,
                                      status="Pending")

        # Save to the database
        session.add(new_appointment)
        session.commit()

        messagebox.showinfo("Appointment Booked", "Your appointment has been booked successfully!")
        self.create_customer_dashboard()

    def view_appointment_history(self):
        """Display appointment history for the customer"""
        self.clear_screen()
        self.root.geometry("800x600")  # 500x400

        self.create_background()

        Label(self.root, text="Appointment History", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(
            row=0, column=1, padx=10, pady=10)

        # Fetch user's appointment history
        appointments = session.query(Appointment).filter_by(user_id=self.current_user_id).all()
        if appointments:
            for i, appointment in enumerate(appointments, start=1):
                Label(self.root, text=f"{appointment.date} - {appointment.service} at {appointment.time}",
                      bg="lightpink").grid(row=i,
                                           column=1,
                                           padx=10,
                                           pady=5)
        else:
            Label(self.root, text="No appointments found.").grid(row=1, column=1, padx=10, pady=5)

        Button(self.root, text="Back", command=self.create_customer_dashboard, bg="brown").grid(
            row=len(appointments) + 1, column=1,
            pady=10)

    def create_staff_dashboard(self):
        """Create the staff dashboard UI"""
        self.clear_screen()
        self.root.geometry("800x600")

        self.create_background()

        Label(self.root, text="Staff Dashboard", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=10,
                                                                                                                 pady=10)
        Button(self.root, text="View All Appointments", command=self.view_all_appointments, bg="brown").grid(row=1,
                                                                                                             column=1,
                                                                                                             padx=10,
                                                                                                             pady=10)
        Button(self.root, text="Logout", command=self.create_login_screen, bg="brown").grid(row=2, column=1, padx=10,
                                                                                            pady=10)

    def view_all_appointments(self):
        """View all appointments (for staff and admin)"""
        self.clear_screen()
        self.root.geometry("800x600")  # 500x400

        self.create_background()

        Label(self.root, text="All Appointments", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(row=0,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=10)

        appointments = session.query(Appointment).all()
        if appointments:
            for i, appointment in enumerate(appointments, start=1):
                Label(self.root,
                      text=f"{appointment.date} - {appointment.service} at {appointment.time} for user ID {appointment.user_id}",
                      bg="lightpink").grid(
                    row=i, column=1, padx=10, pady=5)

                # Add button to allow admin to revoke an appointment
                if session.query(User).filter_by(id=self.current_user_id).first().role == 'Admin':
                    Button(self.root, text="Revoke",
                           command=lambda appt_id=appointment.id: self.revoke_appointment(appt_id),
                           bg="brown").grid(row=i,
                                            column=2,
                                            padx=5, pady=5)

        else:
            Label(self.root, text="No appointments found.").grid(row=1, column=1, padx=10, pady=5)

        Button(self.root, text="Back", command=self.create_staff_dashboard, bg="brown" if session.query(User).filter_by(
            id=self.current_user_id).first().role == 'Staff' else self.create_admin_dashboard).grid(
            row=len(appointments) + 1, column=1, pady=10)

    def revoke_appointment(self, appointment_id):
        """Allow admin to revoke (delete) an appointment"""
        session.query(Appointment).filter_by(id=appointment_id).delete()
        session.commit()

        messagebox.showinfo("Appointment Revoked", "The appointment has been successfully revoked.")
        self.view_all_appointments()

    def create_admin_dashboard(self):
        """Create the admin dashboard UI"""
        self.clear_screen()
        self.root.geometry("800x600")  # 500x400

        self.create_background()

        Label(self.root, text="Admin Dashboard", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=10,
                                                                                                                 pady=10)
        Button(self.root, text="Manage Users", command=self.manage_users, bg="brown").grid(row=1, column=1, padx=10,
                                                                                           pady=10)
        Button(self.root, text="View All Appointments", command=self.view_all_appointments, bg="brown").grid(row=2,
                                                                                                             column=1,
                                                                                                             padx=10,
                                                                                                             pady=10)
        Button(self.root, text="Logout", command=self.create_login_screen, bg="brown").grid(row=3, column=1,
                                                                                            padx=10, pady=10)

    def manage_users(self):
        """Allow admin to manage users"""
        self.clear_screen()
        self.root.geometry("800x600")  # 500x400

        self.create_background()

        Label(self.root, text="Manage Users", font=("Baskerville Old Face", 20, "bold"), bg="lightpink").grid(row=0,
                                                                                                              column=1,
                                                                                                              padx=10,
                                                                                                              pady=10)

        users = session.query(User).all()
        if users:
            for i, user in enumerate(users, start=1):
                Label(self.root, text=f"ID: {user.id}, Username: {user.username}, Role: {user.role}",
                      bg="lightpink").grid(row=i,
                                           column=1,
                                           padx=10,
                                           pady=5)

                # Buttons to allow admin to delete a user
                Button(self.root, text="Delete", command=lambda user_id=user.id: self.delete_user(user_id),
                       bg="brown").grid(row=i,
                                        column=2,
                                        padx=5,
                                        pady=5)

                # Button to allow admin to add a new user (already in the registration functionality)

        else:
            Label(self.root, text="No users found.").grid(row=1, column=1, padx=10, pady=5)

        Button(self.root, text="Back", command=self.create_admin_dashboard, bg="brown").grid(row=len(users) + 1,
                                                                                             column=1, pady=10)

    def delete_user(self, user_id):
        """Allow admin to delete a user"""
        session.query(User).filter_by(id=user_id).delete()
        session.commit()

        messagebox.showinfo("User Deleted", "The user has been successfully deleted.")
        self.manage_users()


if __name__ == "__main__":
    root = Tk()
    app = HairbyFridaApp(root)
    root.mainloop()
