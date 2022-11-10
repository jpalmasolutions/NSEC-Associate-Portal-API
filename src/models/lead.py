from dataclasses import dataclass, field

from jsons import List
from src.models.model import Model
from src.models import appointment, file, note, person
from src.utils.id import generate_id


@dataclass
class Lead(Model):
    street: str
    city: str
    state: str
    postalcode: str
    status: str
    associate_canvasser_email: str
    associate_salesrep_email: str
    
    people: list[person.Person] = field(default_factory=list)
    notes: list[note.Note] = field(default_factory=list)
    files: list[file.File] = field(default_factory=list)
    appointments: list[appointment.Appointment] = field(default_factory=list)

    lead_id: str = None

    def assign_id(self) -> None:
        self.lead_id = generate_id()

        for person in self.people:
            person.lead_id = self.lead_id
            person.assign_id()
        
        for note in self.notes:
            note.lead_id = self.lead_id
            note.assign_id()

        for file in self.files:
            file.lead_id = self.lead_id
            file.assign_id()

        for appointment in self.appointments:
            appointment.lead_id = self.lead_id
            appointment.assign_id()