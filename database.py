"""Script defining a Database class for a better handling of the SQL functions."""

from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Database:
    """Class defining a SQLite Database."""

    def __init__(self, name):
        """Constructor."""

        # Creating database object
        self.__db = QSqlDatabase.addDatabase('QSQLITE')
        self.__db.setDatabaseName(name)

        # Checking the correct opening of the database
        if not self.__db.open():
            raise DatabaseNotOpenedError(name)

    def close(self):
        """Method closing the connection to the database."""
        self.__db.close()

    def execute(self, sql_query):
        """Method used to execute a SQL statement without returning data."""
        QSqlQuery().exec_(sql_query)
        self.__db.commit()

    def import_(self, file_name):
        """Method importing a SQL file."""
        with open(file_name, 'r') as f:
            for l in f.readlines():
                print(l)
                self.execute(l)

    def select(self, sql_query):
        """Method used to select data from the database."""
        query = QSqlQuery()
        query.exec_(sql_query)
        resp = []
        while query.next():
            row = []
            i = 0
            while query.value(i) is not None:
                row.append(query.value(i))
                i += 1
            resp.append(row)
        return resp


class DatabaseNotOpenedError(Exception):
    """Exception raised when the database failed to load."""

    def __init__(self, database_name):
        Exception.__init__(self, "Connection could not be made with database '{}'.".format(database_name))


if __name__ == '__main__':
    db = Database('fignos.db')
    db.import_('base_don_v2.sql')
    db.close()
