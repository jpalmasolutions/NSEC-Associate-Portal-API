from dataclasses import dataclass
from src.models.model import Model
from mysql.connector import DATETIME
from src.utils.id import generate_id

@dataclass
class File(Model):
    name: str
    aws_location: str
    dbx_location: str

    file_id: str = None
    lead_id: str = None

    def assign_id(self):
        self.file_id = generate_id()