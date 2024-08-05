from dotenv import load_dotenv
import psycopg2
import os

# .env Datei laden
load_dotenv()

# Lade Umgebungsvariablen
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# Verbindung zur Datenbank herstellen
def connect_to_db():
    try:
        # Verbindung herstellen
        connection = psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"]
        )
        print("Verbindung zur Datenbank erfolgreich!")
        return connection
    except Exception as e:
        print("Fehler beim Herstellen der Verbindung zur Datenbank:", e)
        return None

def get_worker(id):
    connection = connect_to_db()
    if connection is not None:
        cursor = connection.cursor()

        cursor.execute("Select * FROM worker where id = %s", (id,))
     
        results = cursor.fetchall()

        coulmn_names = [desc[0] for desc in cursor.description]

        return [dict(zip(coulmn_names, row)) for row in results]

# Funktion zum Eingeben von Daten in die Tabelle
def fetch_worker(count):
    connection = connect_to_db()
    if connection is not None:
        try:
            # Cursor erstellen
            cursor = connection.cursor()
            # Daten einfügen
            cursor.execute("SELECT name, min_payment FROM worker LIMIT  %s", (count,))

            print("Daten erfolgreich eingefügt!")

            results = cursor.fetchall()
            
            return [{"id": row[0], "price": row[1]} for row in results]
        except Exception as e:
            print("Fehler beim Einfügen der Daten:", e)
            connection.rollback()
        finally:
            # Cursor und Verbindung schließen
            cursor.close()
            connection.close()

def update_Worker(worker):
    connection = connect_to_db()
    
    worker2 = get_worker(worker["id"])

    for key, new_value in worker.items():
                if key not in worker2[0]:
                    return {"error": f"Data mismatch. Unknown field '{key}'."}, 400

                current_value = worker2[0][key]
                if new_value != current_value:
                    # Falls der neue Wert nicht None ist, aktualisiere den bestehenden Wert
                    if new_value is not None:
                        worker2[0][key] = new_value

    cursor = connection.cursor()


    set_clause = ", ".join([f"{key} = %s" for key in worker2[0].keys()])
    update_query = f"UPDATE worker SET {set_clause} WHERE id = %s"
    values = list(worker2[0].values()) + [worker2[0]["id"]]

    cursor.execute(update_query, values)    
    connection.commit()
    