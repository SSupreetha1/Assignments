import re
import uuid
import datetime

# Helper/Utility functions (getValidDate, getValidAge, getValidZipCode, generate_visit_id)

class Utility:

    def getValidDate(self,Visit_time):
        while True:
            try:
                datetime.datetime.strptime(Visit_time, "%Y-%m-%d")
                return Visit_time
            except ValueError:
                return("Invalid date format. Please use YYYY-MM-DD.")

    def getValidAge(self,Age):
        while True:
            try:
                if Age > 0 and Age <= 120:
                    return Age
                else:
                    return("Invalid input. Please enter valid age.")
            except ValueError:
                return("Invalid input. Please enter valid age.")

    def getValidZipCode(self,zip_code):
        while True:
            
            if re.match(r"^\d{5}$", zip_code):
                return zip_code
            else:
                return("Invalid ZIP code. Please enter a 5-digit number.")

    def generate_visit_id(self):
        return str(uuid.uuid4())


