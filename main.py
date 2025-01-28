import xlrd
import sqlite3, os
from flask import Flask, request, jsonify

DB_NAME = "production_data.db"

# PART 1 : Load data from excel sheet
workbook = xlrd.open_workbook("20210309_2020_1 - 4.xls")
data = []

for sheet in workbook.sheets():
    for row_idx in range(1, sheet.nrows):  
        row = sheet.row(row_idx)
        api_well_number = str(int(row[0].value))  # String to use as key of dict
        oil, gas , brine = row[8].value, row[9].value, row[10].value
        data.append((api_well_number, oil, gas, brine))


# PART 2:  Annual production calculation
annual_data = {}

for api_well_number, oil, gas, brine in data:
    if not annual_data.get(api_well_number, False):
        annual_data[api_well_number] = {"oil": 0, "gas": 0, "brine": 0}
    annual_data[api_well_number]["oil"] += oil
    annual_data[api_well_number]["gas"] += gas
    annual_data[api_well_number]["brine"] += brine

# PART 3 : Loading into the db, in case it doesnt exist
if not os.path.isfile(DB_NAME):
    data_grouped = [(api_well_number, values["oil"], values["gas"], values["brine"])  for api_well_number, values in annual_data.items()]

    db_connection = sqlite3.connect(DB_NAME)

    with db_connection:
        db_connection.execute("""CREATE TABLE IF NOT EXISTS annual_production (
                                api_well_number TEXT PRIMARY KEY,
                                oil REAL,
                                gas REAL,
                                brine REAL
                            )""")
        db_connection.executemany(
            """
            INSERT OR REPLACE INTO annual_production (api_well_number, oil, gas, brine)
            VALUES (?, ?, ?, ?)
            """,
            data_grouped
                        )

    db_connection.close()


# PART 4: FLASK API 
app = Flask(__name__)

@app.route("/data", methods=["GET"])
def get_data():
    well_api_number = request.args.get("well")
    if not well_api_number:
        return jsonify({"error": "Well number is required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT oil, gas, brine FROM annual_production WHERE api_well_number = ?"
    cursor.execute(query, (well_api_number,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return jsonify({"oil": result[0], "gas": result[1], "brine": result[2]})
    else:
        return jsonify({"error": f"Well data for {well_api_number} not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
