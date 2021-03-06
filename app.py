from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import datetime
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

        query = "UPDATE players SET players.first_name = %s, players.last_name = %s, players.age = %s, players.height = %s, players.year = %s WHERE players.player_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (first_name, last_name, age, height, year, player_id))
        mysql.connection.commit()

        return redirect("/players")

@app.route('/player_stats', methods=["POST", "GET"])
def player_stats():
    if request.method == "GET":
        query = "SELECT player_stats.player_stats_id, players.first_name AS First, players.last_name AS Last, player_stats.points AS Points, \
        player_stats.rebounds AS Rebounds, player_stats.assists AS Assists FROM player_stats INNER JOIN players ON player_stats.player_id = players.player_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, first_name, last_name FROM players"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        return render_template("player_stats.j2", data=data, player_data=player_data)

    if request.method == "POST":
        if request.form.get("Add_Stats"):
            player_id = request.form["player_id"]
            points = request.form["points"]
            rebounds = request.form["rebounds"]
            assists = request.form["assists"]
            
        query = "INSERT INTO player_stats (player_id, points, rebounds, assists) VALUES (%s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (player_id, points, rebounds, assists))
        mysql.connection.commit()

        return redirect("/player_stats")

@app.route("/delete_player_stats/<int:player_stats_id>")
def delete_player_stats(player_stats_id):
    query = "DELETE FROM player_stats WHERE player_stats_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (player_stats_id,))
    mysql.connection.commit()

    return redirect("/player_stats")

@app.route("/edit_player_stats/<int:player_stats_id>", methods=["POST", "GET"])
def edit_player_stats(player_stats_id):
    if request.method == "GET":
        query = "SELECT player_stats.player_stats_id, players.first_name AS First, players.last_name AS Last, player_stats.points AS Points, \
        player_stats.rebounds AS Rebounds, player_stats.assists AS Assists FROM player_stats INNER JOIN players ON player_stats.player_id = players.player_id \
        WHERE player_stats_id = %s" % (player_stats_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, first_name, last_name FROM players"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        return render_template("edit_player_stats.j2", data=data, player_data=player_data)

    if request.method == "POST":
        if request.form.get("Edit_Player_Stats"):
            player_id = request.form["player_id"]
            points = request.form["points"]
            rebounds = request.form["rebounds"]
            assists = request.form["assists"]
            
        query = "UPDATE player_stats SET player_stats.player_id = %s, player_stats.points = %s, player_stats.rebounds = %s, player_stats.assists = %s WHERE player_stats.player_stats_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (player_id, points, rebounds, assists, player_stats_id))
        mysql.connection.commit()

        return redirect("/player_stats")

@app.route('/home_game_sales', methods=["POST", "GET"])
def home_game_sales():
    if request.method == "GET":
        query = "SELECT home_game_id, home_game_sales.home_game_date AS Date, home_game_sales.tickets_sold AS Tickets, \
        home_game_sales.merchandise_revenue AS Merchandise, home_game_sales.concession_revenue AS Concessions, visiting_teams.name as Visitor \
        FROM home_game_sales INNER JOIN visiting_teams ON visiting_teams.visiting_team_id = home_game_sales.visiting_team_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT visiting_team_id, name FROM visiting_teams"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        visiting_team_data = cur.fetchall()

        return render_template("home_game_sales.j2", data=data, visiting_team_data=visiting_team_data)

    if request.method == "POST":
        if request.form.get("Add_Game"):
            home_game_date = request.form["home_game_date"]
            visiting_team_id = request.form["visiting_team_id"]
            tickets_sold = request.form["tickets_sold"]
            merchandise_revenue = request.form["merchandise_revenue"]
            concession_revenue = request.form["concession_revenue"]

            if visiting_team_id == "":
                query = "INSERT INTO home_game_sales (home_game_date, tickets_sold, merchandise_revenue, concession_revenue) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (home_game_date, tickets_sold, merchandise_revenue, concession_revenue))
                mysql.connection.commit()

            else:
                query = "INSERT INTO home_game_sales (home_game_date, visiting_team_id, tickets_sold, merchandise_revenue, concession_revenue) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (home_game_date, visiting_team_id, tickets_sold, merchandise_revenue, concession_revenue))
                mysql.connection.commit()
    
        return redirect("/home_game_sales")



@app.route("/delete_home_game_sales/<int:home_game_id>")
def delete_home_game_sales(home_game_id):
    query = "DELETE FROM home_game_sales WHERE home_game_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (home_game_id,))
    mysql.connection.commit()

    return redirect("/home_game_sales")


@app.route("/edit_home_game_sales/<int:home_game_id>", methods=["POST", "GET"])
def edit_home_game_sales(home_game_id):
    if request.method == "GET":
            query = "SELECT home_game_id, home_game_sales.home_game_date AS Date, home_game_sales.tickets_sold AS Tickets, \
            home_game_sales.merchandise_revenue AS Merchandise, home_game_sales.concession_revenue AS Concessions, visiting_teams.name as Visitor \
            FROM home_game_sales INNER JOIN visiting_teams ON visiting_teams.visiting_team_id = home_game_sales.visiting_team_id WHERE home_game_id = %s" % (home_game_id)
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            query2 = "SELECT visiting_team_id, name FROM visiting_teams"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            visiting_team_data = cur.fetchall()

            return render_template("edit_home_game_sales.j2", data=data, visiting_team_data=visiting_team_data)

    if request.method == "POST":
        if request.form.get("Edit_Home_Game_Sales"):
            home_game_date = request.form["home_game_date"]
            visiting_team_id = request.form["visiting_team_id"]
            tickets_sold = request.form["tickets_sold"]
            merchandise_revenue = request.form["merchandise_revenue"]
            concession_revenue = request.form["concession_revenue"]

        if visiting_team_id == "":
            query = "UPDATE home_game_sales SET home_game_sales.home_game_date = %s, home_game_sales.tickets_sold = %s, home_game_sales.merchandise_revenue = %s, \
            home_game_sales.concession_revenue = %s WHERE home_game_sales.home_game_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (home_game_date, tickets_sold, merchandise_revenue, concession_revenue, home_game_id))
            mysql.connection.commit()

            return redirect("/home_game_sales")

        else:
            query = "UPDATE home_game_sales SET home_game_sales.home_game_date = %s, home_game_sales.visiting_team_id = %s, home_game_sales.tickets_sold = %s, \
            home_game_sales.merchandise_revenue = %s, home_game_sales.concession_revenue = %s WHERE home_game_sales.home_game_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (home_game_date, visiting_team_id, tickets_sold, merchandise_revenue, concession_revenue, home_game_id))
            mysql.connection.commit()
    
            return redirect("/home_game_sales")



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)