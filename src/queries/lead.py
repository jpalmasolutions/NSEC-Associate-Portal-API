from pypika import CustomFunction, FormatParameter, MySQLQuery, Order, Table, Criterion

class LeadQueries():
    lead_table = Table('leads')
    lead_from_qb = MySQLQuery.from_(lead_table)
    lead_into_qb = MySQLQuery.into(lead_table)

    JsonObject = CustomFunction(
        'JSON_OBJECT',
        [
            'lead_id_key',
            'lead_id_val',
            'street_key',
            'street_val',
            'city_key',
            'city_val',
            'state_key',
            'state_val',
            'postalcode_key',
            'postalcode_val',
            'associate_canvasser_email_key',
            'associate_canvasser_email_val',
            'associate_salesrep_email_key',
            'associate_salesrep_email_val',
            'status_key',
            'status_val'
        ]
    )

    GET_LEAD_QUERY = lead_from_qb.select(
        JsonObject(
            'lead_id',
            lead_table.lead_id,
            'street',
            lead_table.street,
            'city',
            lead_table.city,
            'state',
            lead_table.state,
            'postalcode',
            lead_table.postalcode,
            'associate_canvasser_email',
            lead_table.associate_canvasser_email,
            'associate_salesrep_email',
            lead_table.associate_salesrep_email,
            'status',
            lead_table.status
        )
    ).where(
        Criterion.eq(
            lead_table.lead_id,
            FormatParameter()
        )
    ).get_sql(quote_char = '')

    GET_ALL_LEADS_QUERY = lead_from_qb.select(
        JsonObject(
            'lead_id',
            lead_table.lead_id,
            'street',
            lead_table.street,
            'city',
            lead_table.city,
            'state',
            lead_table.state,
            'postalcode',
            lead_table.postalcode,
            'associate_canvasser_email',
            lead_table.associate_canvasser_email,
            'associate_salesrep_email',
            lead_table.associate_salesrep_email,
            'status',
            lead_table.status
        )
    ).orderby(
        'street',Order.desc
    ).orderby(
        'city', Order.desc
    ).orderby(
        'state',Order.desc
    ).limit(
        FormatParameter()
    ).offset(
        FormatParameter()
    ).get_sql(quote_char = '')

    FIND_LEAD_QUERY = lead_from_qb.select(lead_table.lead_id).where(
        Criterion.all(
            [
                lead_table.street == FormatParameter(),
                lead_table.city == FormatParameter(),
                lead_table.state == FormatParameter(),
                lead_table.postalcode == FormatParameter()
            ]
        )
    ).get_sql(quote_char = '')

    INSERT_LEAD_QUERY = lead_into_qb.columns(
            'lead_id',
            'street',
            'city',
            'state',
            'postalcode',
            'status',
            'associate_canvasser_email',
            'associate_salesrep_email'
        ).insert(
            FormatParameter(), # lead_id
            FormatParameter(), # street
            FormatParameter(), # city
            FormatParameter(), # state
            FormatParameter(), # postalcode
            FormatParameter(), # status
            FormatParameter(), # associate_canvasser_email
            FormatParameter()  # associate_salesrep_email
        ).get_sql(quote_char = '')

    DELETE_LEAD_QUERY = lead_from_qb.delete().where(
        Criterion.eq(
            lead_table.lead_id,
            FormatParameter()
        )
    ).get_sql(quote_char = '')