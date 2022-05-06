from flask import Flask, render_template
import os
import database.db_connector as db
import json

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/visiting_teams')
def visiting_teams():
    # Write the query and save it to a variable
    query = "SELECT * FROM visiting_teams;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    return render_template("database_template.j2", visiting_teams=results)
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)