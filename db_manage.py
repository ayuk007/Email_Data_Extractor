import mysql.connector
from mysql.connector import Error

# Function to create a MySQL database and table

class Manage_DB:
    def __init__(self):
        pass

    def create_connection(self, host_name, user_name, user_password, database):
        try:
            self.connection = mysql.connector.connect(
                host = host_name,
                user = user_name,
                password = user_password,
                database = database
            )

            self.cursor = self.connection.cursor()

            # Create table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    from VARCHAR(255),
                        ,
                    pdf_data LONGBLOB,
                    description TEXT
                )
            ''')

            self.connection.commit()

        except Error as e:
            print(f"Error: {e}")

    def create_database(self, query):
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(query)
            print("Database created successfully!!")
        
        except Error as err:
            print(f"Error: '{err}'")

    def execute_query(self, query):

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query was successful")
        
        except Error as err:
            print(f"Error: '{err}'")

    
    def create_query(self):
        pass

def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='email_extraction_db'
        )

        cursor = connection.cursor()

        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                from VARCHAR(255),
                       ,
                pdf_data LONGBLOB,
                description TEXT
            )
        ''')

        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to insert a PDF document into the MySQL database
def insert_document(title, file_path, description):
    try:
        connection = mysql.connector.connect(
            host='your_mysql_host',
            user='your_mysql_user',
            password='your_mysql_password',
            database='your_database_name'
        )

        cursor = connection.cursor()

        # Read PDF file data
        with open(file_path, 'rb') as file:
            pdf_data = file.read()

        # Insert data into the table
        cursor.execute('''
            INSERT INTO documents (title, pdf_data, description)
            VALUES (%s, %s, %s)
        ''', (title, pdf_data, description))

        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to retrieve and display a document from the MySQL database
def retrieve_document(document_id):
    try:
        connection = mysql.connector.connect(
            host='your_mysql_host',
            user='your_mysql_user',
            password='your_mysql_password',
            database='your_database_name'
        )

        cursor = connection.cursor()

        # Retrieve data from the table
        cursor.execute('''
            SELECT id, title, description
            FROM documents
            WHERE id = %s
        ''', (document_id,))

        row = cursor.fetchone()

        if row:
            print(f"Document ID: {row[0]}")
            print(f"Title: {row[1]}")
            print(f"Description: {row[2]}")
        else:
            print("Document not found")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main program
if __name__ == "__main__":
    # Create MySQL database and table
    create_database()

    # Insert a sample document
    insert_document('Sample Document', 'path/to/pdf/sample.pdf', 'A sample PDF document')

    # Retrieve and display the document
    retrieve_document(1)
