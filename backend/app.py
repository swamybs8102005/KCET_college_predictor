from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import distinct

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7444@localhost:5432/kcet'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()

# Reflect the table after app context is available
with app.app_context():
    Base.prepare(db.engine, reflect=True)
    table = Base.classes.second_table 

# Routes
@app.route('/', methods=['GET'])
def home():
    return jsonify("hello world")

@app.route('/predict', methods=['GET', 'POST'])
def predict_college():
    return "predicted colleges are"

@app.route('/colleges', methods=['GET'])
def list_college():
    rows = db.session.query(distinct(table.College)).all() 
     #table is the actual table instance present in the database and College is the column name in that db

    colleges=db.session.query(table).all()

    all_data= jsonify([{
         col: getattr(row,col) for col in row.__table__.columns.keys()
     }
     for row in colleges
     ])
    
    all_collges = jsonify([
        {"college" : row[0] 
         }
        for row in rows
    ])  
    
    return all_data 

if __name__ == "__main__":
    app.run(debug=True)
