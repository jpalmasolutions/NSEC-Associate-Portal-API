import jsons

from src.dto.dto import DTO
from src.models.person import Person
from src.queries.person import PersonQueries as queries
from mysql.connector.connection import CursorBase

class PersonDTO(DTO):

    def insert_person(self, person : Person, cursor : CursorBase = None):
        query_params = (
            person.person_id,
            person.lead_id,
            person.main,
            person.first_name,
            person.last_name,
            person.email,
            person.phone_number
        )

        if cursor == None:
            cursor = self.db.cursor()

        cursor.execute(queries.INSERT_PERSON_QUERY,query_params)

    def get_all(self, lead_id : str) -> list[Person]:
        
        person_list = list()
        
        query_params = [lead_id]

        with self.db.cursor() as cursor:
            cursor.execute(queries.GET_ALL_QUERY,query_params)
            rows = cursor.fetchall()
        
        for person in rows:
            person = jsons.loads(person[0], Person)
            person_list.append(person)

        return person_list


    def delete_people(self, lead_id : str, cursor : CursorBase = None):
        query_params = [lead_id]
        if cursor == None:
            cursor = self.db.cursor()

        cursor.execute(queries.DELETE_PERSON_QUERY,query_params)