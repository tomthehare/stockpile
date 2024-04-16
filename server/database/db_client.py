import sqlite3


class DatabaseClient:

    def __init__(self, database_name):
        self.database_name = database_name

    def create_tables_if_not_exist(self):
        sql = """
            SELECT name 
            FROM sqlite_master 
            WHERE type = \'table\'
        """

        connection = ConnectionWrapper(self.database_name)
        connection.execute_sql(sql)

        results = connection.get_results()

        tables = []
        for result in results:
            tables.append(result[0])

        if "tblInventoryItem" not in tables:
            temperature_table_sql = """
             CREATE TABLE tblInventoryItem (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Description TEXT,
                    Location TEXT,
                    CreatedTs INTEGER
                );
            """
            connection.execute_sql(temperature_table_sql)

        connection.wrap_it_up()

    def get_all_inventory_items(self):
        sql = f"""
        SELECT Description, Location, CreatedTs
        FROM tblInventoryItem
        ORDER BY CreatedTs DESC
        """

        connection = ConnectionWrapper(self.database_name)

        try:
            connection.execute_sql(sql)
            results = connection.get_results()
        finally:
            connection.wrap_it_up()

        return results

    def update_inventory_item(self, id, description ):


    def insert_inventory_item(
            self,
            description,
            location,
            created_timestamp
    ):
        sql = f"""
        INSERT INTO tblInventoryItem (Description, Location, CreatedTs)
        VALUES ('{description}', '{location}', {created_timestamp})
        """

        connection = ConnectionWrapper(self.database_name)

        try:
            connection.execute_sql(sql)
        finally:
            connection.wrap_it_up()

        sql2 = f"""
        SELECT MAX(ID) AS newID
        FROM tblInventoryItem
        """

        try:
            connection.execute_sql(sql)
            results = connection.get_results()
        finally:
            connection.wrap_it_up()

        return results[0]['newID']


class ConnectionWrapper:
    _cursor = None
    _connection = None
    _last_rows = None

    def __init__(self, database_name):
        self._connection = sqlite3.connect(database_name)
        self._cursor = self._connection.cursor()

    def execute_sql(self, sql: str):

        if self._cursor is not None:
            self._cursor.execute(sql)

        if self._connection is not None:
            self._connection.commit()

    def get_results(self):
        return self._cursor.fetchall()

    def wrap_it_up(self):
        self._cursor.close()
        self._connection.close()