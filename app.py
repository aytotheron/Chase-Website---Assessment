from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

#initialise app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetcha11()
    cur.close()
    return (rv[0] if rv else None) if one else rv

   
@app.route('/')
def home():
    #home page - just the ID, Nickname, Speciality and ImageURL
    sql = """
    SELECT Names.NameID,ChasersID.Name,Names.Speciality,Names.ImageURL
    FROM Names
    JOIN ChasersID ON ChasersID.ChaserID=Names.ChasersID;"""
    results = query_db(sql)
    return str(results)

@app.route("/names/<int:id>")
def names(id):
    #just one chaser based on id
    sql = """SELECT * FROM Names 
    JOIN ChasersID ON ChasersID.ChaserID=Names.ChasersID
    WHERE Names.NameID = ?;"""
    result = query_db(sql,(id,),True)
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)