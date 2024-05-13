import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import HospitalRecords

class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Records Management System")
        self.geometry("600x400")
        self.CREDENTIALS_CSV = "PA3_credentials.csv"
        self.PATIENT_DATA = "PA3_patients.csv"
        self.hospital = HospitalRecords.HospitalRecords()
        self.hospital.load_records(self.PATIENT_DATA)
        self.create_login_widgets()

    def create_login_widgets(self):
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(expand=True, fill="both")

        # Username Label and Entry
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password Label and Entry
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame, show="*")  # Hide password with asterisks
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login Button
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            credentials = pd.read_csv(self.CREDENTIALS_CSV)
        except FileNotFoundError:
            messagebox.showerror("Error", "Credentials file not found.")
            return
       
        matched_user = credentials[(credentials['username'] == username) & (credentials['password'] == password)]

        if not matched_user.empty:
            role = matched_user.iloc[0]['role']
            self.show_dashboard(role)
        else:
            messagebox.showerror("Error", "Invalid username or password.")
        
    def show_date_input(self):
        # Show date input widgets
        self.date_id_label.pack(pady=5)
        self.date_id_entry.pack(pady=5)

        # Show Submit button
        self.submit_button.pack(pady=5)
        
    def exit_app(self):
        # Destroy the dashboard frame
        self.dashboard_frame.destroy() 

        # Recreate the login widgets
        self.create_login_widgets() 

    def count_visits(self):
        date_str = self.date_id_entry.get()
        visits_count = self.hospital.count_visits(date_str)
        messagebox.showinfo("Visits Count", f"Number of visits on {date_str}: {visits_count}")

        # Clear and hide input widgets
        self.date_id_entry.delete(0, tk.END)
        self.date_id_label.pack_forget()
        self.date_id_entry.pack_forget()
        self.submit_button.pack_forget()
        
    def generate_visits_report(self):
        data = pd.read_csv("PA3_patients.csv")
        HospitalRecords.HospitalRecords.temporal_trend_hospital_visits(data)

    def generate_insurance_report(self):
        data = pd.read_csv("PA3_patients.csv")
        HospitalRecords.HospitalRecords.temporal_trend_insurance_types(data)

    def generate_demographic_report(self):
        data = pd.read_csv("PA3_patients.csv")
        HospitalRecords.HospitalRecords.temporal_trend_demographics(data, ["Gender", "Ethnicity"])
        
    def add_patient(self):
        # Create a new top-level window for patient ID input
        self.patient_input_window = tk.Toplevel(self)
        self.patient_input_window.title("Add Patient")

        # Patient ID Label and Entry
        ttk.Label(self.patient_input_window, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.patient_id_entry = ttk.Entry(self.patient_input_window)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = ttk.Button(self.patient_input_window, text="Submit", command=self.check_patient_existence)
        submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
    def check_patient_existence(self):
        patient_id = self.patient_id_entry.get()
        patient_found = self.hospital.check_patient_existence(patient_id)

        if patient_found:
            ttk.Label(self.patient_input_window, text="Visit Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.visit_date_entry = ttk.Entry(self.patient_input_window)
            self.visit_date_entry.grid(row=2, column=1, padx=5, pady=5)

            add_visit_button = ttk.Button(self.patient_input_window, text="Add Visit", command=self.add_visit_to_existing_patient)
            add_visit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        else:
            # Display input fields for new patient information
            ttk.Label(self.patient_input_window, text="Visit Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.visit_date_entry = ttk.Entry(self.patient_input_window)
            self.visit_date_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Race:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.race_entry = ttk.Entry(self.patient_input_window)
            self.race_entry.grid(row=3, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Ethnicity:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
            self.ethnicity_entry = ttk.Entry(self.patient_input_window)
            self.ethnicity_entry.grid(row=4, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Gender:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
            self.gender_entry = ttk.Entry(self.patient_input_window)
            self.gender_entry.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Age:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
            self.age_entry = ttk.Entry(self.patient_input_window)
            self.age_entry.grid(row=6, column=1, padx=5, pady=5)
            
            ttk.Label(self.patient_input_window, text="Insurance:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
            self.insurance_entry = ttk.Entry(self.patient_input_window)
            self.insurance_entry.grid(row=7, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Zip Code:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
            self.zip_code_entry = ttk.Entry(self.patient_input_window)
            self.zip_code_entry.grid(row=8, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Chief Complaint:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
            self.chief_complaint_entry = ttk.Entry(self.patient_input_window)
            self.chief_complaint_entry.grid(row=9, column=1, padx=5, pady=5)

            ttk.Label(self.patient_input_window, text="Note Type:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
            self.note_type_entry = ttk.Entry(self.patient_input_window)
            self.note_type_entry.grid(row=10, column=1, padx=5, pady=5)

            # Add Patient Button
            add_patient_button = ttk.Button(self.patient_input_window, text="Add Patient", command=self.collect_and_add_new_patient)
            add_patient_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)


    def remove_patient(self):
    # Create a new top-level window for patient ID input
        self.patient_input_window = tk.Toplevel(self)
        self.patient_input_window.title("Remove Patient")

        # Patient ID Label and Entry
        ttk.Label(self.patient_input_window, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.patient_id_entry = ttk.Entry(self.patient_input_window)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Submit Button
        submit_button = ttk.Button(self.patient_input_window, text="Submit", command=self.remove_patient_from_records)
        submit_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def remove_patient_from_records(self):
        patient_id = self.patient_id_entry.get()
        result = self.hospital.remove_patient(patient_id)
        messagebox.showinfo("Result", result)
        self.patient_id_entry.delete(0, tk.END)
        self.patient_input_window.destroy()
        
    def retrieve_patient(self):
        # Create a new top-level window for patient ID and retrieval options input
        self.retrieve_patient_window = tk.Toplevel(self)
        self.retrieve_patient_window.title("Retrieve Patient Information")

        # Patient ID Label and Entry
        ttk.Label(self.retrieve_patient_window, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.patient_id_entry = ttk.Entry(self.retrieve_patient_window)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Retrieve Options Radio Buttons
        self.retrieve_option = tk.StringVar(value="All")  # Default to "All"
        ttk.Label(self.retrieve_patient_window, text="Retrieve:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(self.retrieve_patient_window, text="Age", variable=self.retrieve_option, value="Age").grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(self.retrieve_patient_window, text="Visits", variable=self.retrieve_option, value="Visits").grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(self.retrieve_patient_window, text="All", variable=self.retrieve_option, value="All").grid(row=4, column=0, sticky="w")

        # Submit Button
        submit_button = ttk.Button(self.retrieve_patient_window, text="Submit", command=self.get_patient_information)
        submit_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def get_patient_information(self):
        patient_id = self.patient_id_entry.get()
        info_type = self.retrieve_option.get()
        result = self.hospital.retrieve_patient(patient_id, info_type)
        if result:
            messagebox.showinfo("Patient Information", result)
        else:
            messagebox.showinfo("Patient Not Found", f"Patient with ID {patient_id} not found.")
        self.retrieve_patient_window.destroy()
        
    def add_visit_to_existing_patient(self):
        patient_id = self.patient_id_entry.get()
        visit_date = self.visit_date_entry.get()
        result = self.hospital.add_visit_to_existing_patient(patient_id, visit_date)
        messagebox.showinfo("Visit Added", result)
        
    def collect_and_add_new_patient(self):
            patient_id = self.patient_id_entry.get()
            visit_date = self.visit_date_entry.get()
            race = self.race_entry.get()
            ethnicity = self.ethnicity_entry.get()
            gender = self.gender_entry.get()
            age = self.age_entry.get()
            insurance = self.insurance_entry.get()
            zip_code = self.zip_code_entry.get()
            chief_complaint = self.chief_complaint_entry.get()
            note_type = self.note_type_entry.get()
            result = self.hospital.collect_and_add_new_patient(patient_id, visit_date, race, ethnicity, gender, age, insurance, zip_code, chief_complaint, note_type)
            messagebox.showinfo("Result", result)
            self.patient_input_window.destroy()
        
            
    def show_dashboard(self, role):
        self.login_frame.destroy()
        self.dashboard_frame = ttk.Frame(self)
        self.dashboard_frame.pack(expand=True, fill="both")

        if role == "admin":
            ttk.Label(self.dashboard_frame, text="Admin Dashboard").pack(pady=20)

            # Count Visits Button
            count_visits_button = ttk.Button(self.dashboard_frame, text="Count Visits", command=self.show_date_input)
            count_visits_button.pack(pady=10)

            # Date Input Widgets (initially hidden)
            self.date_id_entry = ttk.Entry(self.dashboard_frame)
            self.date_id_label = ttk.Label(self.dashboard_frame, text="Enter Visit Date (YYYY-MM-DD):")
            submit_button = ttk.Button(self.dashboard_frame, text="Submit", command=self.count_visits)
            submit_button.pack(pady=5)

                 # Exit Button
            exit_button = ttk.Button(self.dashboard_frame, text="Exit", command=self.exit_app)
            exit_button.pack(pady=10)

        elif role == "management":
            
            ttk.Label(self.dashboard_frame, text="Management Dashboard").pack(pady=20)

            # Visits Report Button
            visits_report_button = ttk.Button(self.dashboard_frame, text="Visits Report", command=self.generate_visits_report)
            visits_report_button.pack(pady=10)

            # Insurance Report Button
            insurance_report_button = ttk.Button(self.dashboard_frame, text="Insurance Report", command=self.generate_insurance_report)
            insurance_report_button.pack(pady=10)

            # Demographic Report Button
            demographic_report_button = ttk.Button(self.dashboard_frame, text="Demographic Report", command=self.generate_demographic_report)
            demographic_report_button.pack(pady=10)
            
            # Exit Button
            exit_button = ttk.Button(self.dashboard_frame, text="Exit", command=self.exit_app)
            exit_button.pack(pady=10)

        elif role == "clinician" or role == "nurse":
            ttk.Label(self.dashboard_frame, text="Clinician/Nurse Dashboard").pack(pady=20)

            # Add Patient Button
            add_patient_button = ttk.Button(self.dashboard_frame, text="Add Patient", command=self.add_patient)
            add_patient_button.pack(pady=10)

            # Remove Patient Button
            remove_patient_button = ttk.Button(self.dashboard_frame, text="Remove Patient", command=self.remove_patient)
            remove_patient_button.pack(pady=10)

            # Retrieve Patient Button
            retrieve_patient_button = ttk.Button(self.dashboard_frame, text="Retrieve Patient", command=self.retrieve_patient)
            retrieve_patient_button.pack(pady=10)

            # Count Visits Button
            count_visits_button = ttk.Button(self.dashboard_frame, text="Count Visits", command=self.show_date_input) 
            count_visits_button.pack(pady=10)
            
            # Date Input Widgets (initially hidden)
            self.date_id_entry = ttk.Entry(self.dashboard_frame)
            self.date_id_label = ttk.Label(self.dashboard_frame, text="Enter Visit Date (YYYY-MM-DD):")

            # Submit Button (initially hidden)
            self.submit_button = ttk.Button(self.dashboard_frame, text="Submit", command=self.count_visits)
            
            # Exit Button
            exit_button = ttk.Button(self.dashboard_frame, text="Exit", command=self.exit_app)
            exit_button.pack(pady=10)
        

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
