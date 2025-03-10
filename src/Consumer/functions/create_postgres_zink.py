from constants.constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from quixstreams.sinks.community.postgresql import PostgreSQLSink

def create_postgres_sink(table):
    sink = PostgreSQLSink(
        host = POSTGRES_HOST,
        port = POSTGRES_PORT,
        dbname = POSTGRES_DBNAME,
        user = POSTGRES_USER,
        password = POSTGRES_PASSWORD,
        table_name = table,
        schema_auto_update = True
    )

    return sink