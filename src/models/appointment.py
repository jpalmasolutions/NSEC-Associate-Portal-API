from dataclasses import dataclass
from src.models.model import Model
from mysql.connector import DATETIME

from src.utils.id import generate_id

@dataclass
class Appointment(Model):
    start_time: DATETIME
    end_time: DATETIME

    appointment_id: str = None
    note_id: str = None
    lead_id: str = None

    def assign_id(self):
        self.appointment_id = generate_id()