from flask import Flask, jsonify, Response
import matplotlib.pyplot as plt
import database
import pandas as pd
import io

app = Flask(__name__)

#returns a diagram of given i workers and their price. 
@app.route("/worker/<int:count>", methods={"GET"})
def get_worker(count):
    produkt = database.fetch_worker(count)
    price = []
    ids = []

    if produkt is not None:
            # Daten verarbeiten
            for worker in produkt:
                # Überprüfe, ob die Schlüssel in worker existieren
                if "id" in worker:
                    ids.append(worker["id"])
                if "price" in worker:
                    price.append(worker["price"])

    df = pd.DataFrame({'Price': price, 'ID': ids})
    df["Price"] = pd.to_numeric(df["Price"])
    df.sort_values('ID', inplace=True)


    plt.figure(figsize=(10, 5))
    plt.bar(df['ID'], df['Price'],color='black')
    plt.title('Product Price History')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(False)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plt.close()

    return Response(img.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    # Flask-Anwendung starten
    app.run(debug=True)