import jsons
from datetime import datetime
from src.dto.dto import DTO
from src.models.note import Note
from mysql.connector.connection import CursorBase
from src.queries.note import NoteQueries as queries

class NoteDTO(DTO):

    def insert_note(self, note : Note, cursor : CursorBase = None):

        note.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query_params = (
            note.note_id,
            note.lead_id,
            note.content,
            note.created_at
        )

        if cursor == None:
            cursor = self.db.cursor()

        cursor.execute(queries.INSERT_NOTE_QUERY,query_params)

    def get_all(self, lead_id : str) -> list[Note]:

        note_list = list()
        query_params = [lead_id]

        with self.db.cursor() as cursor:
            cursor.execute(queries.GET_ALL_QUERY,query_params)
            rows = cursor.fetchall()

        for note in rows:
            note = jsons.loads(note[0],Note)
            note_list.append(note)

        return note_list

    def delete_notes(self, lead_id : str, cursor : CursorBase = None):
        query_params = [lead_id]
        if cursor == None:
            cursor = self.db.cursor()

        cursor.execute(queries.DELETE_NOTE_QUERY,query_params)