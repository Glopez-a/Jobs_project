import pandas as pd

def connect():
    # Create the connection to the database and all the information in a single dataframe
    df = pd.read_csv('./data/companies_info.csv')
    df = df.replace(to_replace="%C3%A9", value='e', regex=True)
    df = df.replace(to_replace="%C3%B3", value='o', regex=True)
    df = df.replace(to_replace="%C3%A1", value='a', regex=True)
    return df

def create_companie(values, connection):
    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    # Execute the SQL statement to insert the values
    cursor.execute("INSERT INTO companies (Name,Description,Mission,Sizing,Revenue,Industry,Founded,Overall,Culture,Diversity,Conciliation,Managers,Salaries,Opportunitys,URL,FriendRecomendation,CEO,Outlook) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor (not the connection)
    cursor.close()
