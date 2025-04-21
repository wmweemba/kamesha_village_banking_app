import mysql.connector

class UserHandler:
    """
    A class to handle user-related operations in the database.
    """

    def __init__(self, host, user, password, database):
        """
        Initialize the database connection.

        Args:
            host (str): Database host.
            user (str): Database user.
            password (str): Database password.
            database (str): Database name.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        Establish a connection to the database.
        """
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_user(self, name, email, phone):
        """
        Create a new user in the database.

        Args:
            name (str): Full name of the user.
            email (str): Email address of the user.
            phone (str): Phone number of the user.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = """
            INSERT INTO Users (name, email, phone)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, email, phone))
            connection.commit()

            print("User has been successfully created.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_user(self, user_id):
        """
        Delete an existing user from the database.

        Args:
            user_id (int): The ID of the user to delete.
        """
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = "DELETE FROM Users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()

            if cursor.rowcount > 0:
                print("User has been successfully deleted.")
            else:
                print("No user found with the given ID.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()