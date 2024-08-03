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