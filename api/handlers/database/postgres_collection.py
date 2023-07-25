import psycopg


class PostgresCollection():
    def __init__(self) -> None:
        self.table_name = 'collection'

    def add_card(self, cursor, oracle_id, qty):
        cursor.execute(
            f"INSERT INTO {self.table_name} (oracle_id, qty) VALUES ('{oracle_id}', {qty}) ON CONFLICT (oracle_id) DO UPDATE SET qty = {qty};"
        )

    def delete_card(self, cursor, oracle_id):
        cursor.execute(
            f"DELETE FROM {self.table_name} where oracle_id = '{oracle_id}'"
        )
