import jsons
from mysql.connector import IntegrityError
from src.dto.dto import DTO
from src.dto.person import PersonDTO
from src.dto.note import NoteDTO
from src.models.lead import Lead
from src.queries.lead import LeadQueries as queries
from werkzeug.exceptions import InternalServerError


class LeadDTO(DTO):
    
    person_dto = PersonDTO()
    note_dto = NoteDTO()

    def find_lead(self, lead = Lead):
        row = None

        query_params = (
            lead.street,
            lead.city,
            lead.state,
            lead.postalcode
        )

        with self.db.cursor() as cursor:
            cursor.execute(queries.FIND_LEAD_QUERY,query_params)
            row = cursor.fetchone()

        return row

    def insert_lead(self, lead = Lead):

        query_params = (
            lead.lead_id,
            lead.street,
            lead.city,
            lead.state,
            lead.postalcode,
            lead.status,
            lead.associate_canvasser_email,
            lead.associate_salesrep_email
        )

        with self.db.cursor() as cursor:
            try:
                cursor.execute(queries.INSERT_LEAD_QUERY,query_params)

                for person in lead.people:
                    self.person_dto.insert_person(person,cursor)

                for note in lead.notes:
                    self.note_dto.insert_note(note,cursor)

                self.db.commit()

            except IntegrityError as ie:
                raise InternalServerError('Inserting to database resulted in an integrity error.')

    def get_all_leads(self, limit : str, offset : str) -> list[Lead]:
        
        # Setting query parameters
        query_params = (limit,offset)

        with self.db.cursor() as cursor:
            cursor.execute(queries.GET_ALL_LEADS_QUERY,query_params)
            rows = cursor.fetchall()

        lead_list = list()

        for lead in rows:
            lead = jsons.loads(lead[0], Lead)
            lead.people = self.person_dto.get_all(lead_id = lead.lead_id)
            lead.notes = self.note_dto.get_all(lead_id = lead.lead_id)
            lead_list.append(lead)

        return lead_list

    def get_lead(self, lead_id : str) -> Lead:
        query_params =[lead_id]

        lead = None

        with self.db.cursor() as cursor:
            cursor.execute(queries.GET_LEAD_QUERY,query_params)
            lead_row = cursor.fetchone()

        if lead_row != None:
            lead = jsons.loads(lead_row[0],Lead)
            lead.people = self.person_dto.get_all(lead_id = lead.lead_id)
            lead.notes = self.note_dto.get_all(lead_id = lead.lead_id)
        
        return lead



    def delete_lead(self,lead_id : str):

        query_parameters = [lead_id]

        with self.db.cursor() as cursor:
            self.person_dto.delete_people(lead_id=lead_id,cursor=cursor)
            self.note_dto.delete_notes(lead_id=lead_id,cursor=cursor)
            cursor.execute(queries.DELETE_LEAD_QUERY,query_parameters)
            self.db.commit()
