import mysql.connector
from mysql.connector import Error

class Manage_DB:
    def __init__(self):
        # Dictionary to map keys to data types
        self.data_type_mapping = {
            'Sender': 'VARCHAR(255)',
            'PAO_Code': 'VARCHAR(255)',
            'Entity_Name': 'VARCHAR(255)',
            'Ministry_Department': 'VARCHAR(255)',
            'Sender_Name': 'VARCHAR(255)',
            'Central_Govt_State_Govt': 'VARCHAR(255)',
            'Focal_point_with_official_designation': 'VARCHAR(255)',
            'Full_office_Address_wih_pin_code': 'VARCHAR(255)',
            'Full_address_of_Focal_point': 'VARCHAR(255)',
            'Phone_number_of_Focal_point': 'VARCHAR(255)',
            'Official_Email_Address': 'VARCHAR(255)',
            'Official_Website': 'VARCHAR(255)',
            'GSTIN': 'VARCHAR(255)',
            'Name_Designation': 'VARCHAR(255)',
            'Dept_Ministry': 'VARCHAR(255)',
            'E_mail': 'VARCHAR(255)',
            'Phone_No': 'VARCHAR(255)',
            'Date_': 'DATE',
            'Pdf_Data': 'LONGBLOB',
            'Pdf_Name': 'VARCHAR(255)',
            'Approval': 'VARCHAR(5)',
            'Domain_Name': 'VARCHAR(255)',  # Add data type for Domain_Name
            'Timestamp': 'DATETIME',       # Add data type for Timestamp
            'Usage_Flag': 'BOOLEAN'         # Assuming BOOLEAN; adjust if necessary
            # Add more mappings as needed
        }


        self.create_connection("localhost", "root", "abc@123456789", "pdf_database")
        self.create_table("pdf_records", pattern_dict_keys, "pdf_database")


    def create_connection(self, host_name, user_name, user_password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password,
                database=database
            )
            self.cursor = self.connection.cursor()

        except Error as e:
            print(f"Error: {str(e)}")
            # If the database doesn't exist, create it
            if "1049" in str(e):  # MySQL error code for "unknown database"
                print("Creating Database..")
                self.connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    password=user_password,
                )
                self.cursor = self.connection.cursor()
                self.create_database(database)

    def create_database(self, db_name):
        query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        
        try:
            self.execute_query(query)
            print(f"Database '{db_name}' created successfully!!")

        except (Exception, Error) as err:
            print(f"Error: '{err}'")

    def create_table(self, table_name, keys, database):
        self.execute_query(f"USE {database}")  # Switch to the specified database

        # Create a list of columns with appropriate data types based on the mapping
        columns = [f"{key.lower()} {self.data_type_mapping[key].lower()}" for key in keys]
        columns.extend(["pdf_data LONGBLOB", "pdf_name VARCHAR(255)", "timestamp DATETIME",
                        "usage_flag BOOLEAN" ])  # Add fields for storing PDF files and PDF names

        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {', '.join(columns)}
            )
        '''
        try:
            self.execute_query(query)
            print(f"Table '{table_name}' created successfully!!")

        except (Exception, Error) as err:
            print(f"Error: '{err}'")

    # def create_record(self, table_name, record_dict):
        
    #     # columns = ', '.join([f"{key.lower()}" for key in record_dict.keys()])
    #     # placeholders = ', '.join(['%s'] * len(record_dict))
    #     # query = f"INSERT INTO {table_name} ({columns}) \nVALUES ({placeholders})"
    #     # dict_type = [type(z) for z in record_dict.values()]
    #     # try:
    #     #     record_values = list(record_dict.values())
    #     #     self.execute_query(query, tuple(record_values))
            
    #     #     print("Record created successfully!")

    #     # except (Exception, Error) as err:
    #     #     print(f"Error: '{err}'")

    def create_record(self, table_name, record_dict):
        domain_name = record_dict['Domain_Name']
        # usage_flag = record_dict.get('usage_flag', False)
        record_dict['usage_flag'] = True
        # Check if there is an existing record with the same domain name and usage_flag = true
        existing_record_query = f"SELECT * FROM {table_name} WHERE domain_name = %s AND usage_flag = TRUE"
        existing_record_values = (domain_name,)

        try:
            self.cursor.execute(existing_record_query, existing_record_values)
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Update existing record's usage_flag to false
                update_query = f"UPDATE {table_name} SET usage_flag = FALSE WHERE id = %s"
                self.execute_query(update_query, (existing_record[0],))

        except (Exception, Error) as err:
            print(f"Error checking existing record: {err}")

        # Include current timestamp in the record_dict
        # record_dict['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert the new record
        columns = ', '.join(record_dict.keys())
        placeholders = ', '.join(['%s'] * len(record_dict))
        insert_query = f"INSERT INTO {table_name} ({columns}) \nVALUES ({placeholders})"

        try:
            self.execute_query(insert_query, tuple(record_dict.values()))
            print("Record created successfully!")

        except (Exception, Error) as err:
            print(f"Error inserting record: {err}")

    def update_record(self, table_name, update_dict, condition_dict):
        set_clause = ', '.join([f"{key} = %s" for key in update_dict.keys()])
        condition_clause = ' AND '.join([f"{key} = %s" for key in condition_dict.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"

        try:
            values = list(update_dict.values()) + list(condition_dict.values())
            self.execute_query(query, tuple(values))
            print("Record updated successfully!")

        except (Exception, Error) as err:
            print(f"Error: '{err}'")

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Query was successful")

        except (Exception, Error) as err:
            print(f"Error: '{err}'")

# Usage example:
pattern_dict_keys = [
    'Sender', 'PAO_Code', 'Entity_Name', 'Ministry_Department',
    'Sender_Name', 'Central_Govt_State_Govt', 'Focal_point_with_official_designation',
    'Full_office_Address_wih_pin_code', 'Full_address_of_Focal_point',
    'Phone_number_of_Focal_point', 'Official_Email_Address', 'Official_Website',
    'GSTIN', 'Name_Designation', 'Dept_Ministry', 'E_mail', 'Phone_No', 'Date_','Approval', 'Domain_Name'
]

# if __name__ == '__main__':

#     db_manager = Manage_DB()
#     db_manager.create_connection("localhost", "root", "root", "")
#     db_manager.create_table("documents", pattern_dict_keys, "your_database_name")

