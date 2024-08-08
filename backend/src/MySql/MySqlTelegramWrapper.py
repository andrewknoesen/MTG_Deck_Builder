from MySql.MySql import MySql

class MySqlTelegramWrapper:
    def __init__(self, case: str):
        if case == 'test':
            self.my_sql = MySql('root', 'my_root_password', 'card_database')
        else:
            self.my_sql = MySql()