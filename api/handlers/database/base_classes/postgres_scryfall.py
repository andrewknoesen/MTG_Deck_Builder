import psycopg


class PostgresScryfall():
    def __init__(self) -> None:
        self.table_name = 'cards'

    def get_card_from_oracle(self, cursor: psycopg.Cursor, oracle_id):
        cursor.execute(
            f"SELECT name FROM {self.table_name} WHERE oracle_id = '{oracle_id}';"
        )

        return cursor.fetchone()[0]
    
    def get_oracle_from_card(self, cursor: psycopg.Cursor, card):
        print(f'Received {card}')
        cursor.execute(
            f"SELECT oracle_id FROM {self.table_name} WHERE name = '{card}';"
        )
        
        return cursor.fetchone()[0]
