# Note: the module name is psycopg, not psycopg3
import psycopg

# from api.handlers.database.base_classes.postgres_collection import PostgresCollection
# from api.handlers.database.base_classes.postgres_scryfall import PostgresScryfall
# from api.handlers.database.base_classes.postgress_bulk import PostgresBulk
from postgres_collection import PostgresCollection
from postgres_scryfall import PostgresScryfall
from postgress_bulk import PostgresBulk

class PostgresBase:
    def __init__(self) -> None:
        self.conn = psycopg.connect("dbname=mtg user=postgres")
        self.cur = self.conn.cursor()

        self.scryfall = PostgresScryfall()
        self.collection = PostgresCollection()
        self.bulk = PostgresBulk()

    def close(self):
        self.conn.close()

    def get_card_from_oracle(self, oracle_id):
        return self.scryfall.get_card_from_oracle(self.cur, oracle_id=oracle_id)
    
    def get_oracle_from_card(self, card):
        return self.scryfall.get_oracle_from_card(self.cur, card=card)
    
    def update_bulk_table(self):
        self.bulk.add_cards(self.conn)
        self.conn.commit()

    def upsert_collection(self, oracle_id, qty=1):
        self.collection.add_card(self.cur, oracle_id=oracle_id, qty=qty)
        self.conn.commit()

    def upsert_collection_from_name(self, name, qty=1):
        oracle_id = self.get_oracle_from_card(name)
        self.collection.add_card(self.cur, oracle_id=oracle_id, qty=qty)
        self.conn.commit()


    def delete_card_from_collection(self, oracle_id):
        self.collection.delete_card(self.cur, oracle_id=oracle_id)
        self.conn.commit()

if __name__ == '__main__':
    postgres = PostgresBase()
    postgres.update_bulk_table()
    # print(postgres.get_card_from_oracle('0004ebd0-dfd6-4276-b4a6-de0003e94237'))


# # Connect to an existing database
# with psycopg.connect("dbname=test user=postgres") as conn:

#     # Open a cursor to perform database operations
#     with conn.cursor() as cur:

#         # Execute a command: this creates a new table
#         cur.execute("""
#             CREATE TABLE test (
#                 id serial PRIMARY KEY,
#                 num integer,
#                 data text)
#             """)

#         # Pass data to fill a query placeholders and let Psycopg perform
#         # the correct conversion (no SQL injections!)
#         cur.execute(
#             "INSERT INTO test (num, data) VALUES (%s, %s)",
#             (100, "abc'def"))

#         # Query the database and obtain data as Python objects.
#         cur.execute("SELECT * FROM test")
#         cur.fetchone()
#         # will return (1, 100, "abc'def")

#         # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
#         # of several records, or even iterate on the cursor
#         for record in cur:
#             print(record)

#         # Make the changes to the database persistent
#         conn.commit()