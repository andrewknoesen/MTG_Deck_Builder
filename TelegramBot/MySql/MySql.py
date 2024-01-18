import logging
import os
from sqlalchemy import create_engine, text, exc
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | MySql | %(levelname)s | %(message)s',
    force=True
)

class MySql:
    def __init__(self, user: str | None = None, password: str | None = None, database: str | None = None, host: str | None = None):
        if user is None:
            user = os.environ['MYSQL_USER']

        if password is None:
            password = os.environ['MYSQL_PASSWORD']

        if database is None:
            database = os.environ['MYSQL_DATABASE']

        if host is None:
            host = os.environ['LOCAL_IP']
        

        connection_config = f'mysql+mysqlconnector://{user}:{password}@{host}:3307/{database}?&autocommit=true'
        engine = create_engine(connection_config)
        self.connection = engine.connect()

    def list_all(self):
        sql = f"SELECT * FROM cards"
        logging.info(f'SQL query="{sql}"')

        return pd.read_sql(sql, self.connection)

    def get_user_cards(self, username: str, list_output = False):
        sql = f"SELECT card_name FROM cards WHERE username = '{username}'"
        logging.info(f'SQL query="{sql}"')
        df = pd.read_sql(sql, self.connection)
        if list_output:
            return df['card_name'].to_list()
        return df['card_name'].to_string(index=False)

    def remove_user(self, username: str):
        sql = f"DELETE FROM cards WHERE username = '{username}'"
        logging.info(f'SQL query="{sql}"')

        self.connection.execute(text(sql))

    def check_user_exits(self, username: str):
        sql = f"SELECT * FROM cards WHERE username = '{username}'"
        logging.info(f'SQL query="{sql}"')
        user = self.connection.execute(text(sql))

        if len(user.fetchall()) == 0 :
            return False
        else:
            return True

    def add_card(self, username: str, card: str):
        sql = f"INSERT INTO cards (username, card_name) VALUES ('{username}', '{card}')"
        logging.info(f'SQL query="{sql}"')

        try:
            self.connection.execute(text(sql))
            logging.info('Card added successfully!')
        except exc.IntegrityError as e:
            if "Duplicate entry" in str(e):
                logging.warn('Card already exists.')
            else:
                logging.error(f'Error: {e}')
        except Exception as e:
            self.connection.rollback()
            logging.error(f'Error: {e}')

    def remove_card(self, username: str, card: str):
        sql = f"DELETE FROM cards WHERE username = '{username}' AND card_name = '{card}'"
        logging.info(f'SQL query="{sql}"')

        try:
            self.connection.execute(text(sql))
            logging.info('Card removed successfully!')
        except Exception as err:
            self.connection.rollback()
            logging.error(f'Error: {err}')

    def get_users_for_card(self, card: str):
        sql = f"SELECT DISTINCT username FROM cards where card_name = '{card}'"
        logging.info(f'SQL query="{sql}"')

        df = pd.read_sql(sql, self.connection)
        return df['username'].to_list()

if __name__ == "__main__":
    my_sql = MySql('root', 'my_root_password', 'card_database')
    logging.info(f'SQL query="{sql}"')
    username = 'andrew'
    card = 'Fireball'
    # my_sql.add_card(username, card)
    # my_sql.remove_user('andrew')
    my_sql.remove_card(username, card)
    # my_sql.remove_card(username, card)
    logging.info(my_sql.list_all())
