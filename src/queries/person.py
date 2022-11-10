from pypika import CustomFunction, FormatParameter, MySQLQuery, Order, Table, Criterion
from pypika.queries import QueryBuilder

class PersonQueries():
    people_table = Table('people')
    people_from_qb : QueryBuilder = MySQLQuery.from_(people_table)
    people_into_qb : QueryBuilder = MySQLQuery.into(people_table)

    JsonObject = CustomFunction(
        'JSON_OBJECT',
        [
            'person_id_key',
            'person_id_val',
            'lead_id_key',
            'lead_id_val',
            'main_id_key',
            'main_id_val',
            'first_name_key',
            'first_name_val',
            'last_name_key',
            'last_name_val',
            'email_key',
            'email_val',
            'phone_number_key',
            'phone_number_val'
        ]
    )

    GET_ALL_QUERY = people_from_qb.select(
        JsonObject(
            'person_id',
            people_table.person_id,
            'lead_id',
            people_table.lead_id,
            'main',
            people_table.main,
            'first_name',
            people_table.first_name,
            'last_name',
            people_table.last_name,
            'email',
            people_table.email,
            'phone_number',
            people_table.phone_number
        )
    ).orderby(
        people_table.main,
        order=Order.desc
    ).where(
        Criterion.eq(
            people_table.lead_id,
            FormatParameter()
        )
    ).get_sql(quote_char = '')

    INSERT_PERSON_QUERY = people_into_qb.columns(
            'person_id',
            'lead_id',
            'main',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        ).insert(
            FormatParameter(), # person_id
            FormatParameter(), # lead_id
            FormatParameter(), # main
            FormatParameter(), # first_name
            FormatParameter(), # last_name
            FormatParameter(), # email
            FormatParameter()  # phone_number
        ).get_sql(quote_char = '')

    DELETE_PERSON_QUERY = people_from_qb.delete().where(
        Criterion.eq(
            people_table.lead_id,
            FormatParameter()
        )
    ).get_sql(quote_char = '')