import uuid

class Visit:
    def __init__(self, visit_time, Visit_department, chief_complaint, note_type):
        self.visit_id = str(uuid.uuid4())
        self.Visit_department = Visit_department
        self.visit_time = visit_time
        self.chief_complaint = chief_complaint
        self.note_type = note_type
        self.note_id = str(uuid.uuid4())

