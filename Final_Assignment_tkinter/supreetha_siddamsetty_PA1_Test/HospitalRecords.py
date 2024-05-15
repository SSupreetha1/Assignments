import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from Patient import Patient
from Utility import Utility


class HospitalRecords:
    def __init__(self):
        self.records = {}

    def load_records(self, filename):
        try:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.records[row["Patient_ID"]] = row
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred while loading records: {str(e)}")

    def remove_patient(self, patient_id):
        if patient_id in self.records:
            del self.records[patient_id]
            return f"Patient record with id: {patient_id} is removed successfully."
        else:
            return "Patient record not found"

    def retrieve_patient(self, patient_id, info_type):
        info_retrievers = {
            "Age": lambda patient: {"Patient Age": patient["Age"]},
            "Visits": lambda patient: {
                "Visits": {
                    "Visit Time": patient["Visit_time"],
                    "Visit Department": patient["Visit_department"],
                }
            },
            "All": lambda patient: patient,
        }
        patient = self.records.get(patient_id)
        if patient is None:
            return {"Error": "Patient ID not found."}
        try:
            return info_retrievers[info_type](patient)
        except KeyError:
            return {"Error": f"Info type {info_type} not found."}

    def count_visits(self, date_str):
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"error_message": "Invalid date format."}
        count = sum(
            1
            for record in self.records.values()
            if datetime.datetime.strptime(record["Visit_time"], "%Y-%m-%d").date()
            == target_date
        )
        return (
            {"Visits for the date - {}".format(date_str): "{}".format(count)}
            if count
            else {"No Visits found for this date:": " {}".format(target_date)}
        )

    def get_patient(self, patient_id):
        return self.records.get(patient_id)

    def check_patient_existence(self, patient_id):
        return patient_id in self.records

    def add_visit_to_existing_patient(self, patient_id, visit_time):
        visit_id = Utility.generate_visit_id(self)
        new_visit = {
            "Patient_ID": patient_id,
            "Visit_ID": visit_id,
            "Visit_time": visit_time,
        }
        if patient_id in self.records:
            try:
                self.records[patient_id]["visits"].append(new_visit)
            except KeyError:
                self.records[patient_id]["visits"] = [new_visit]
        return new_visit

    def collect_and_add_new_patient(
        self,
        patient_id,
        visit_time,
        race,
        ethnicity,
        gender,
        age,
        insurance,
        zip_code,
        chief_complaint,
        note_type,
    ):
        visit_id = Utility.generate_visit_id(self)
        note_id = Utility.generate_visit_id(self)
        patient_data = {
            "Patient_ID": patient_id,
            "Visit_time": visit_time,
            "Race": race,
            "Ethnicity": ethnicity,
            "Gender": gender,
            "Age": age,
            "Insurance": insurance,
            "Zip_code": zip_code,
            "Chief_complaint": chief_complaint,
            "Note_type": note_type,
            "Visit_ID": visit_id,
            "Note_ID": note_id,
            "visits": [],
        }
        self.records[patient_id] = patient_data
        return patient_data

    @staticmethod
    def load_hospital_data(data_path):
        try:
            data = pd.read_csv(data_path, error_bad_lines=False)
            return data
        except FileNotFoundError:
            print("Hospital data file not found.")
            return None
        except pd.errors.EmptyDataError:
            print("Hospital data file is empty.")
            return None

    @staticmethod
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

    @staticmethod
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
            plt.show()
        except KeyError:
            print("Insurance column not found in hospital data.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @staticmethod
    def temporal_trend_demographics(data, demographic):
        try:
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
            print(f"{demographic} column not found in hospital data.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
