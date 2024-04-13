import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import Patient
import Utility


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

    def retrieve_patient(self):
        patient_id1 = input("Enter the patient_id: ")
        patient_found = False
        for patient in self.records:
            if patient_id1 == patient.patient_id:
                while True:  # Loop for getting multiple pieces of information
                    info_type = input(
                        "Enter the type of information needed (e.g., Age, Visits, All, Stop): "
                    )

                    if info_type == "Age":
                        print(f"Patient Age: {patient.Age}")
                    elif info_type == "Visits":
                        for visit in patient.visits:
                            print(
                                f"  - Visit Time: {visit.visit_time} & Visit_department: {visit.Visit_department}"
                            )
                    elif info_type == "All":
                        # Print all the relevant patient attributes
                        print(f"Age: {patient.Age}")
                        print(f"Race: {patient.Race}")
                        print(f"Ethnicity: {patient.Ethnicity}")
                        print(f"Gender: {patient.Gender}")
                        print(f"Insurance: {patient.Insurance}")
                        print(f"Zip_code: {patient.Zip_code}")
                        print(f"Visted departments: {patient.Visit_department}")
                        print(f"Chief_complaint: {patient.Chief_complaint}")
                        print("Visits:")
                        for visit in patient.visits:
                            print(
                                f"  - Visit Time: {visit.visit_time} & Visit_department: {visit.Visit_department}"
                            )
                    elif info_type == "Stop":
                        break

        if not patient_found:  # Check the flag after the loop
            print("Patient ID not found.")

    def add_visit_to_existing_patient(self, patient_id):
        visit_time = Utility.getValidDate(self)
        visit_id = Utility.generate_visit_id(self)
        new_visit = {
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Visit_time": visit_time,
        }
        self.records.append(new_visit)
        print("Patient visit added successfully.", new_visit)

    def collect_and_add_new_patient(self, patient_id):
        Visit_time = Utility.getValidDate()
        Race = input("Enter Patient Race: ")
        Ethnicity = input("Enter Patient Ethnicity: ")
        Gender = input("Enter Patient Gender: ")
        Age = Utility.getValidAge()
        Insurance = input("Enter Patient Insurance: ")
        Zip_code = Utility.getValidZipCode()
        Chief_complaint = input("Enter Patient Chief Complaint: ")
        Note_type = input("Enter Patient Note Type: ")
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
        visit_id = Utility.generate_visit_id()
        note_id = Utility.generate_visit_id()
        patient_data["Visit_ID"] = visit_id
        patient_data["Note_ID"] = note_id
        self.records.append(patient_data)
        print("New patient added successfully.", patient_data)

    def add_patient(self):
        patient_id = input("Enter Patient ID: ")
        patient_found = False
        for record in self.records:
            if record.patient_id == patient_id:
                patient_found = True
                break
        print("Patient Found Status:", patient_found)

        if patient_found:
            print("Updating existing patient record!")
            self.add_visit_to_existing_patient(patient_id)
        else:
            print("Creating a new patient record!")
            self.collect_and_add_new_patient(patient_id)

    def remove_patient(self):
        patient_id = input("Enter Patient_ID: ")
        try:
            self.records.remove(
                next(
                    record for record in self.records if record.patient_id == patient_id
                )
            )
            print(
                "Patient record with id: {} is removed successfully.".format(patient_id)
            )
        except StopIteration:
            print("Patient record not found")

    def count_visits(self):
        date_str = input("Enter date (yyyy-mm-dd): ")
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            print("target date is: ", target_date)
            count = 0  # Initialize the count
            for record in self.records:
                if (
                    datetime.datetime.strptime(record.Visit_time, "%Y-%m-%d").date()
                    == target_date
                ):
                    count += 1
            if count >= 1:
                print(f"Visits on this date : {date_str} are : {count}")
            else:
                print(f"No Visitis found for this date: ", target_date)
        except ValueError:
            print("Invalid date format.")

    def authenticate_user(user_roles_path, max_attempts=3):
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
            plt.show()
        except KeyError:
            print("Visit_time column not found in hospital data.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def temporal_trend_insurance_types(data):
        try:
            # Count occurrences of each insurance type
            insurance_counts = data["Insurance"].value_counts()
            plt.figure(figsize=(10, 6))
            insurance_counts.plot(kind="bar")
            plt.title("Insurance Types in Hospital Visits")
            plt.xlabel("Insurance Type")
            plt.ylabel("Number of Patients")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        except KeyError:
            print("Insurance column not found in hospital data.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def temporal_trend_demographics(data, demographic):
        try:
            # for demographic in demographics:
            demographic_counts = data[demographic].value_counts()
            plt.figure(figsize=(10, 6))
            demographic_counts.plot(kind="bar")
            plt.title(f"Hospital Visits by {demographic}")
            plt.xlabel(demographic)
            plt.ylabel("Number of Patients")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.show()
        except KeyError:
            print("One or more demographic columns not found in hospital data.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
