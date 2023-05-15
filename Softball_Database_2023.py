from flask import Flask, render_template, request
import psycopg2

# Set up a Flask app
app = Flask(__name__)
POSTGRESQL_URI = "postgres://msydzjhv:bRRyUHzKCCwgLoP_lhECiyT1AoXwPBJ6@drona.db.elephantsql.com/msydzjhv"

connection = psycopg2.connect(POSTGRESQL_URI)
try:
    with connection: 
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE statistics (name TEXT, date DATE, singles INT, doubles INT, triples INT, home_runs INT, walks INT, at_bats INT, runs INT, rbis INT);")
except psycopg2.errors.DuplicateTable:
    pass
    
        
# Define a route for your HTML form
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":    
            print(request.form)
            with connection:
                with connection.cursor() as cursor:
                     cursor.execute(
                        "INSERT INTO statistics VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                   (
                                       str(request.form.get("name")),
                                       request.form.get("date"),
                                       int(request.form.get("singles")),
                                       int(request.form.get("doubles")),
                                       int(request.form.get("triples")),
                                       int(request.form.get("home_runs")),
                                       int(request.form.get("walks")),
                                       int(request.form.get("at_bats")),
                                       int(request.form.get("runs")),
                                       int(request.form.get("rbis")),                                     
                                    ),
                    )
                
    return render_template("html_softball_tracker.html")
   
# Define a route for your HTML form page
@app.route("/statistics",methods=["GET","POST"])
def show_transactions():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM statistics;")
            transactions = cursor.fetchall()
        return render_template("transactions.jinja2", entries=transactions)
    
if __name__ == '__main__':
    app.run()
