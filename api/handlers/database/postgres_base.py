# Note: the module name is psycopg, not psycopg3
import psycopg
from postgres_collection import PostgresCollection 

class PostgresBase:
    def __init__(self) -> None:
        self.conn = psycopg.connect("dbname=mtg user=postgres")
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def upsert_collection(self, oracle_id, qty=1):
        collection = PostgresCollection()
        collection.add_card(self.cur, oracle_id=oracle_id, qty=qty)
        self.conn.commit()

    def delete_card_from_collect(self, oracle_id):
        collection = PostgresCollection()
        collection.delete_card(self.cur, oracle_id=oracle_id)
        self.conn.commit()

if __name__ == '__main__':
    postgres = PostgresBase()
    postgres.delete_card_from_collect('test')


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