import re
import uuid
import datetime

# Helper/Utility functions (getValidDate, getValidAge, getValidZipCode, generate_visit_id)

class Utility:

    def getValidDate(self):
        while True:
            try:

                Visit_time = input("Enter date (YYYY-MM-DD): ")
                datetime.datetime.strptime(Visit_time, "%Y-%m-%d")
                return Visit_time
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def getValidAge(self):
        while True:
            try:
                age = int(input("Enter Patient Age: "))
                if age > 0 and age <= 120:
                    return age
                else:
                    print("Invalid input. Please enter valid age.")
            except ValueError:
                print("Invalid input. Please enter valid age.")

    def getValidZipCode(self):
        while True:
            zipcode = input("Enter Patient Zip-Code: ")
            if re.match(r"^\d{5}$", zipcode):
                return zipcode
            else:
                print("Invalid ZIP code. Please enter a 5-digit number.")

    def generate_visit_id(self):
        return str(uuid.uuid4())


