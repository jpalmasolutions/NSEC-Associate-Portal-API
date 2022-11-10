from pypika import CustomFunction, FormatParameter, MySQLQuery, Order, Table, Criterion
from pypika.queries import QueryBuilder

class NoteQueries():
    note_table = Table('notes')
    note_from_qb : QueryBuilder = MySQLQuery.from_(note_table)
    note_into_qb : QueryBuilder = MySQLQuery.into(note_table)

    JsonObject = CustomFunction(
        'JSON_OBJECT',
        [
            'note_id_key',
            'note_id_val',
            'lead_id_key',
            'lead_id_val',
            'content_key',
            'content_val',
            'created_at_key',
            'created_at_val'
        ]
    )

    INSERT_NOTE_QUERY = note_into_qb.columns(
        'note_id',
        'lead_id',
        'content',
        'created_at'
    ).insert(
        FormatParameter(), # note_id
        FormatParameter(), # lead_id
        FormatParameter(), # content
        FormatParameter()  # created_at
    ).get_sql(quote_char = '')


    GET_ALL_QUERY = note_from_qb.select(
        JsonObject(
            'note_id',
            note_table.note_id,
            'lead_id',
            note_table.lead_id,
            'content',
            note_table.content,
            'created_at',
            note_table.created_at
        )
    ).orderby(
        note_table.created_at,
        order=Order.desc
    ).where(
        Criterion.eq(
            note_table.lead_id,
            FormatParameter()
        )
    ).get_sql(quote_char = '')

    DELETE_NOTE_QUERY = note_from_qb.delete().where(
        Criterion.eq(
            note_table.lead_id,
            FormatParameter()
        )
    ).get_sql(quote_char = '')