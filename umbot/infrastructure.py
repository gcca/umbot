import psycopg


async def StateSchema(pg_conn: str) -> None:
    async with await psycopg.AsyncConnection.connect(pg_conn) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS umbot_record (
                    id SERIAL PRIMARY KEY,
                    msg_data JSONB NOT NULL,
                    req_data JSONB DEFAULT NULL,
                    res_status INTEGER DEFAULT 0,
                    res_text TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


async def StoreRecord(
    pg_conn: str, msg_data: str, req_data: str, res_status: int, res_text: str
) -> None:
    async with await psycopg.AsyncConnection.connect(pg_conn) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO umbot_record (msg_data, req_data, res_status, res_text) VALUES (%s, %s, %s, %s)",
                (msg_data, req_data, res_status, res_text),
            )
