  
from dataclasses import dataclass
from src.models.model import Model
from datetime import datetime

from src.utils.id import generate_id

@dataclass
class Note(Model):
    content: str
    created_at: str = None

    note_id: str = None
    lead_id: str = None

    def assign_id(self):
        self.note_id = generate_id()