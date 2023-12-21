import os
from sqlalchemy import create_engine, text, exc
import pandas as pd


class MySql:
    def __init__(self, user: str | None = None, password: str | None = None, database: str | None = None):
        if user is None:
            user = os.environ['MYSQL_USER']

        if password is None:
            password = os.environ['MYSQL_PASSWORD']

        if database is None:
            database = os.environ['MYSQL_DATABASE']

        connection_config = f'mysql+mysqlconnector://{user}:{password}@localhost:3307/{database}?&autocommit=true'
        engine = create_engine(connection_config)
        self.connection = engine.connect()

    def list_all(self):
        sql = f"SELECT * FROM cards"

        return pd.read_sql(sql, self.connection)

    def get_user_cards(self, username: str):
        sql = f"SELECT card_name FROM cards WHERE username = '{username}'"
        # df = pd.read_sql(sql, self.connection)
        return pd.read_sql(sql, self.connection)['card_name'].to_string(index=False)

    def remove_user(self, username: str):
        sql = f"DELETE FROM cards WHERE username = '{username}'"

        self.connection.execute(text(sql))

    def check_user_exits(self, username: str):
        sql = f"SELECT * FROM cards WHERE username = '{username}'"
        user = self.connection.execute(text(sql))

        if len(user.fetchall()) == 0 :
            return False
        else:
            return True

    def add_card(self, username: str, card: str):
        sql = f"INSERT INTO cards (username, card_name) VALUES ('{username}', '{card}')"

        try:
            self.connection.execute(text(sql))
            print('Card added successfully!')
        except exc.IntegrityError as e:
            if "Duplicate entry" in str(e):
                print('Card already exists.')
            else:
                print(f'Error: {e}')
        except Exception as e:
            print(f'Error: {e}')

    def remove_card(self, username: str, card: str):
        sql = f"DELETE FROM cards WHERE username = '{username}' AND card_name = '{card}'"

        try:
            self.connection.execute(text(sql))
            print('Card removed successfully!')
        except Exception as err:
            print(f'Error: {err}')

if __name__ == "__main__":
    my_sql = MySql('root', 'my_root_password', 'card_database')
    username = 'andrew'
    card = 'Fireball'
    # my_sql.add_card(username, card)
    # my_sql.remove_user('andrew')
    my_sql.remove_card(username, card)
    # my_sql.remove_card(username, card)
    print(my_sql.list_all())
