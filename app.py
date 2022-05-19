from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
# Configuration

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_hernanb2'
app.config['MYSQL_PASSWORD'] = '4437' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_hernanb2'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route("/players", methods=["POST", "GET"])
def players():
    if request.method == "GET":
        query = "SELECT * FROM players;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("players.j2", data=data)

    if request.method == "POST":
        if request.form.get("Add_Player"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form["age"]
            height = request.form["height"]
            year = request.form["year"]

        query = "INSERT INTO players (first_name, last_name, age, height, year) VALUES (%s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (first_name, last_name, age, height, year))
        mysql.connection.commit()

        return redirect("/players")

@app.route("/delete_players/<int:player_id>")
def delete_players(player_id):
    query = "DELETE FROM players WHERE player_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (player_id,))
    mysql.connection.commit()

    return redirect("/players")

@app.route("/edit_players/<int:player_id>", methods=["POST", "GET"])
def edit_players(player_id):
    if request.method == "GET":
        query = "SELECT * FROM players WHERE player_id = %s" % (player_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_players.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Players"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form["age"]
            height = request.form["height"]
            year = request.form["year"]

            query = "UPDATE players SET players.first_name = %s, players.last_name = %s, players.age = %s, players.height = %s, players.year = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, age, height, year))
            mysql.connection.commit()

        return redirect("/players")

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