from flask import Flask, render_template, request, jsonify, redirect, url_for # type: ignore
import pandas as pd
import HospitalRecords
import csv 
import base64
from matplotlib import pyplot as plt

app = Flask(__name__)

# Define the path to the CSV file containing credentials and patient data
CREDENTIALS_CSV = "PA3_credentials.csv"
PATIENT_DATA = "PA3_patients.csv"

# Load credentials from the CSV file
def load_credentials():
    credentials = {}
    with open(CREDENTIALS_CSV, "r") as file:
        reader = csv.DictReader(file)
        credentials = {
            row["username"]: {"password": row["password"], "role": row["role"]}
            for row in reader
        }
    return credentials

# Load patient data
hospital = HospitalRecords.HospitalRecords()
hospital.load_records(PATIENT_DATA)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    credentials = load_credentials()

    if username in credentials and credentials[username]["password"] == password:
        role = credentials[username]["role"]
        return redirect(url_for("dashboard", username=username, role=role))
    else:
        return "Authentication Failed. Please check your username and password."

@app.route("/dashboard/<username>/<role>")
def dashboard(username, role):
    template = "admin.html" if role == "admin" else "management.html" if role == "management" else "dashboard.html"
    return render_template(template, username=username, role=role)

@app.route("/action", methods=["GET", "POST"])
def user_action():
    if request.method == "POST":
        actions = request.form.getlist("action")
        role = request.form.get("role")
        if "Exit" in actions:
            return render_template("login.html")
        else:
            results = {}
            if role == "management":
                results = management_action(actions)
                return render_template("results1.html", results=results)
            else:
                results = clinician_nurse_action(actions)
                if results:
                    return render_template("results.html", results=results)
                else:
                    return render_template("results.html", results={})
    else:
        action = request.args.get("action")
        return render_template("results.html", results={action: "Action received."})
   


@app.route('/check_patient_exists', methods=['POST'])
def check_patient_exists():
    patient_id = request.json.get('patient_id')
    print(patient_id)
    patient_exists = HospitalRecords.HospitalRecords.check_patient_existence(hospital,patient_id)
    print(patient_exists)  
    return jsonify(patient_exists)

    
def clinician_nurse_action(actions):
    results = {}
    for action in actions:
        if action == 'Add_patient':
            patient_id = request.form.get('patient_id')
            patient_found = HospitalRecords.HospitalRecords.check_patient_existence(hospital,patient_id)
            if patient_found:
                Visit_time = request.form.get('date_id')
                result =  HospitalRecords.HospitalRecords.add_visit_to_existing_patient(hospital,patient_id,Visit_time)
            else: 
                visit_time = request.form.get('date_id')
                race = request.form.get("Race")
                ethnicity = request.form.get("Ethnicity")
                gender = request.form.get("Gender")
                age = request.form.get("Age")
                insurance = request.form.get("Insurance")
                zip_code = request.form.get("Zip_code")
                chief_complaint = request.form.get("Chief_complaint")
                note_type = request.form.get("Note_type")
                result =  HospitalRecords.HospitalRecords.collect_and_add_new_patient(hospital,patient_id,visit_time,race,ethnicity,gender,age, insurance, zip_code, chief_complaint, note_type)   
            results[action] = result
        elif action == 'Remove_patient':
            patient_id = request.form.get('patient_id')
            result = HospitalRecords.HospitalRecords.remove_patient(hospital, patient_id)
            results[action] = result
        elif action == 'Retrieve_patient':
            patient_id = request.form.get('patient_id')
            info_type = request.form.get('retrieve_option')
            result = HospitalRecords.HospitalRecords.retrieve_patient(hospital, patient_id, info_type)
            results[action] = result
        elif action == 'Count_visits':
            date_str = request.form.get('date_id')
            result = HospitalRecords.HospitalRecords.count_visits(hospital, date_str)
            results[action] = result
        elif action == 'Exit':
            return render_template('login.html')
        else:
            results[action] = "Unknown action"
    return results

def management_action(actions):
    results = {}
    for action in actions:
        # Fetch data (replace with your actual data loading)
        data = pd.read_csv(PATIENT_DATA)  

        if action == 'visits_report':
            plot_data = HospitalRecords.HospitalRecords.temporal_trend_hospital_visits(data)
        elif action == 'insurances_report':
            plot_data = HospitalRecords.HospitalRecords.temporal_trend_insurance_types(data)
        elif action == 'demographic_report':
            plot_data = HospitalRecords.HospitalRecords.temporal_trend_demographics(data, ["Gender", "Ethnicity"])
        elif action == 'Exit':
            return render_template("login.html")
        else:
            results[action] = "Unknown action"

        # Convert Matplotlib figure to base64 image
        if plot_data is not None:  # Check if plot_data is a valid figure
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            results[action] = plot_url  
        else:
            results[action] = None  # or set to a default message

    return results
   
if __name__ == "__main__":
    app.run(debug=True)
