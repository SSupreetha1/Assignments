import sys
import HospitalRecords


class Main:

    input_path = sys.argv[2]
    user_roles_path = sys.argv[1]

    # creating object for Hospitalrecords class

    hospital = HospitalRecords.HospitalRecords()
    hospital.load_records(input_path)
    hospital_data = HospitalRecords.HospitalRecords.load_hospital_data(input_path)

    # Authenticate User and get the role  of the authenticated user
    username, role = HospitalRecords.HospitalRecords.authenticate_user(user_roles_path)

    if role is None:
        print("Authentication Failed. Exiting.")

    elif role == "clinician" or role == "nurse":
        print(f"Welcome, {username}! Your role is {role}.")
        while True:

            # User Actions menu for roles  'Clinician' & 'Nurse'

            user_input = input(
                "Enter action (Add_patient, Remove_patient, Retrieve_patient, Count_visits, Stop): "
            )
            if user_input == "Stop":
                break
            elif user_input == "Add_patient":
                HospitalRecords.HospitalRecords.add_patient(hospital)
            elif user_input == "Remove_patient":
                HospitalRecords.HospitalRecords.remove_patient(hospital)
            elif user_input == "Retrieve_patient":
                HospitalRecords.HospitalRecords.retrieve_patient(hospital)
            elif user_input == "Count_visits":
                HospitalRecords.HospitalRecords.count_visits(hospital)
            else:
                print("Invalid action or insufficient permissions. Please try again.")
    elif role == "admin":

        print(f"Welcome, {username}! Your role is {role}.")

        # Admin is restricted to only one action, i.e Count visits

        HospitalRecords.HospitalRecords.count_visits(hospital)
    elif role == "management":
        print(f"Welcome, {username}! Your role is {role}.")
        while True:

            # User Actions menu for role  'Management'.

            user_input = input(
                "Enter action (visits_report,insurances_report,demographic_report, Stop): "
            )
            if user_input == "Stop":
                break
            elif user_input == "visits_report":
                HospitalRecords.HospitalRecords.temporal_trend_hospital_visits(
                    hospital_data
                )
            elif user_input == "insurances_report":
                HospitalRecords.HospitalRecords.temporal_trend_insurance_types(
                    hospital_data
                )
            elif user_input == "demographic_report":
                HospitalRecords.HospitalRecords.temporal_trend_demographics(
                    hospital_data, ["Gender", "Ethnicity"]
                )
