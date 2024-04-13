import Visit

class Patient:
    def __init__(
        self,
        Patient_ID,
        Visit_time,
        Visit_ID,
        Visit_department,
        Race,
        Ethnicity,
        Gender,
        Age,
        Insurance,
        Zip_code,
        Chief_complaint,
    ):
        self.patient_id = Patient_ID
        self.Visit_time = Visit_time
        self.Visit_ID = Visit_ID
        self.Visit_department = Visit_department
        self.Race = Race
        self.Ethnicity = Ethnicity
        self.Gender = Gender
        self.Age = Age
        self.Insurance = Insurance
        self.Zip_code = Zip_code
        self.Chief_complaint = Chief_complaint
        self.visits = []

    def add_visit(self, visit_time, Visit_department, chief_complaint, note_type):
        visit = Visit.Visit(visit_time, Visit_department, chief_complaint, note_type)
        self.visits.append(visit)

