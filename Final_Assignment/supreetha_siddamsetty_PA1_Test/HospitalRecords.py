import csv
import datetime
import pandas as pd
pd.__version__ 
import matplotlib.pyplot as plt
import Patient
import Utility
import os
import base64
import io 

class HospitalRecords:
    def __init__(self):
        self.records = []
           
    def load_records(self, filename):
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                patient = Patient.Patient(
                    row["Patient_ID"],
                    row["Visit_time"],
                    row["Visit_ID"],
                    row["Visit_department"],
                    row["Race"],
                    row["Ethnicity"],
                    row["Gender"],
                    int(row["Age"]),
                    row["Insurance"],
                    row["Zip_code"],
                    row["Chief_complaint"],
                )
                patient.add_visit(
                    row["Visit_time"],
                    row["Visit_department"],
                    row["Chief_complaint"],
                    row["Note_type"],
                )
                self.records.append(patient)

    def retrieve_patient(self, patient_id, info_type):
        patient_found = False
        patient_info = {}
        for patient in self.records:
            if patient_id == patient.patient_id:
                patient_found = True
                if info_type == "Age":
                    patient_info["Patient Age"] = patient.Age
                elif info_type == "Visits":
                    visits_info = []
                    for visit in patient.visits:
                        visits_info.append({"Visit Time": visit.visit_time, "Visit Department": visit.Visit_department})
                    patient_info["Visits"] = visits_info
                elif info_type == "All":
                    # Collect all the relevant patient attributes
                    patient_info["Age"] = patient.Age
                    patient_info["Race"] = patient.Race
                    patient_info["Ethnicity"] = patient.Ethnicity
                    patient_info["Gender"] = patient.Gender
                    patient_info["Insurance"] = patient.Insurance
                    patient_info["Zip Code"] = patient.Zip_code
                    patient_info["Visited Departments"] = patient.Visit_department
                    patient_info["Chief Complaint"] = patient.Chief_complaint
                    visits_info = []
                    for visit in patient.visits:
                        visits_info.append({"Visit Time": visit.visit_time, "Visit Department": visit.Visit_department})
                    patient_info["Visits"] = visits_info

        if not patient_found:
            patient_info["Error"] = "Patient ID not found."

        return patient_info


# Similarly, modify other methods like add_patient, remove_patient, count_visits, etc. to take input parameters from Flask and return results accordingly.

    def add_visit_to_existing_patient(self, patient_id,Visit_time):
        # visit_time = Utility.Utility.getValidDate(self,Visit_time)
        visit_id = Utility.Utility.generate_visit_id(self)
        new_visit = {
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Visit_time": Visit_time,
        }
        self.records.append(new_visit)
        return  new_visit

    def collect_and_add_new_patient(self, patient_id,Visit_time,Race,Ethnicity,Gender,Age, Insurance, Zip_code, Chief_complaint, Note_type):
        patient_data = {
            "Patient_ID": patient_id,
            "Visit_time": Visit_time,
            "Race": Race,
            "Ethnicity": Ethnicity,
            "Gender": Gender,
            "Age": Age,
            "Insurance": Insurance,
            "Zip_code": Zip_code,
            "Chief_complaint": Chief_complaint,
            "Note_type": Note_type,
        }
        visit_id = Utility.Utility.generate_visit_id(self)
        note_id = Utility.Utility.generate_visit_id(self)
        patient_data["Visit_ID"] = visit_id
        patient_data["Note_ID"] = note_id
        self.records.append(patient_data)
        return patient_data

    def check_patient_existence(self,patient_id):
        for record in self.records:
            if record.patient_id == patient_id:
                return True
        else:
            return False

    def remove_patient(self,patient_id):
        try:
            self.records.remove(
                next(
                    record for record in self.records if record.patient_id == patient_id
                )
            )
            
            return "Patient record with id: {} is removed successfully.".format(patient_id)
            
        except StopIteration:
            return "Patient record not found"

    def count_visits(self, date_str):
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            count = 0  # Initialize the count
            for record in self.records:
                if datetime.datetime.strptime(record.Visit_time, "%Y-%m-%d").date() == target_date:
                    count += 1
            if count >= 1:
                return {"Visits for the date - {}".format(date_str): "{}".format( count)}
            else:
                return {"No Visits found for this date:": " {}".format(target_date)}
        except ValueError:
            return {"error_message": "Invalid date format."}


    def authenticate_user(user_roles_path):
        try:
            with open(user_roles_path, "r") as file:
                reader = csv.DictReader(file)
                user_roles = {
                    row["username"]: {"password": row["password"], "role": row["role"]}
                    for row in reader
                }
        except FileNotFoundError:
            print("User roles file not found.")
            return None, None
        except csv.Error:
            print("Error reading user roles file.")
            return None, None
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in user_roles:
            if password == user_roles[username]["password"]:
                return username, user_roles[username]["role"]
        else:
            print("Invalid username or password. Please try again.")
            return None, None

    def load_hospital_data(data_path):
        try:
            data = pd.read_csv(data_path)
            return data
        except FileNotFoundError:
            print("Hospital data file not found.")
            return None
        except pd.errors.EmptyDataError:
            print("Hospital data file is empty.")
            return None
        except pd.errors.ParserError:
            print("Error reading hospital data file.")
            return None
        

    def temporal_trend_hospital_visits(data):
        try:
            data["Visit_time"] = pd.to_datetime(data["Visit_time"])
            data["MonthYear"] = data["Visit_time"].dt.to_period("M")
            visits_by_monthyear = data.groupby("MonthYear").size()
            plt.figure(figsize=(10, 6))
            visits_by_monthyear.plot(marker="o", linestyle="-")
            plt.title("Temporal Trend of Hospital Visits")
            plt.xlabel("Month-Year (Visit_time)")
            plt.ylabel("Number of Patients")
            plt.xticks(rotation=45)
            plt.grid(True)
            # Convert plot to base64-encoded image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return plot_data
        except KeyError:
            return "Visit_time column not found in hospital data."
        except Exception as e:
            return f"An error occurred: {str(e)}"


    def temporal_trend_insurance_types(data):
        try:
            insurance_counts = data["Insurance"].value_counts()
            plt.figure(figsize=(10, 6))
            insurance_counts.plot(kind="bar")
            plt.title("Insurance Types in Hospital Visits")
            plt.xlabel("Insurance Type")
            plt.ylabel("Number of Patients")
            plt.xticks(rotation=45)
            plt.grid(True)
            # Convert plot to base64-encoded image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return plot_data
        except KeyError:
            return "Insurance column not found in hospital data."
        except Exception as e:
            return f"An error occurred: {str(e)}"


    def temporal_trend_demographics(data, demographics):
        try:
            plt.figure(figsize=(10, 6))
            for demographic in demographics:
                demographic_counts = data[demographic].value_counts()
                demographic_counts.plot(kind="bar", label=demographic)
            plt.title("Hospital Visits by Demographics")
            plt.xlabel("Demographic")
            plt.ylabel("Number of Patients")
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True)
            # Convert plot to base64-encoded image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            return plot_data
        except KeyError:
            return "One or more demographic columns not found in hospital data."
        except Exception as e:
            return f"An error occurred: {str(e)}"
