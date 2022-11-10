
from dataclasses import dataclass
from src.models.model import Model

from src.utils.id import generate_id

@dataclass
class Person(Model):
    main: bool
    first_name: str
    last_name: str
    email: str
    phone_number: str

    person_id: str = None
    lead_id: str = None

    def assign_id(self):
        self.person_id = generate_id()