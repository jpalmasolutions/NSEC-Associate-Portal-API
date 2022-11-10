from src.utils.db import get_db_connection

class DTO():
    def __init__(self):
        self.db = get_db_connection()