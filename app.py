from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Inicialice app Flask
app = Flask(__name__)
CORS(app)


#Config database
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://suuuwuumxxwjzu:808f9ccfb822232d940c25941e1ffb90f9a7cee72bd96e99089897098af23c52@ec2-23-20-140-229.compute-1.amazonaws.com:5432/dc7fgda0la5dde'
db.init_app(app)

# Create our database model
class Benefit(db.Model):
    __tablename__ = "benefits"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1200), unique=True)
    service_plan_id = db.Column(db.Integer, db.ForeignKey('service_plans.id'),
        nullable=False)

    def __init__(self, desription):
        self.desription = desription

    def serialize(self):
        return {"id": self.id,
                "description": self.description,
                "service_plan_id": self.service_plan_id}


class ServicePlan(db.Model):
    __tablename__ = "service_plans"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(1200))
    price = db.Column(db.Float)
    benefits = db.relationship('Benefit', backref='benefits', lazy=True)


    def __init__(self, name, desription, price):
        self.name = name
        self.desription = desription
        self.price = price

    def serialize(self):
        return {"id": self.id,
                "description": self.description,
                "name": self.name,
                "price": self.price,
                "benefits": [b.serialize() for b in self.benefits]}

class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    url = db.Column(db.String(200))
    description = db.Column(db.String(1200))

    def __init__(self, name, desription, url):
        self.name = name
        self.desription = desription
        self.url = url
    
    def serialize(self):
        return {"id": self.id,
                "description": self.description,
                "name": self.name,
                "url": self.url}

migrate = Migrate(app,db)

@app.route("/service_plans")
def get_service_plans():   
    try:
        data = ServicePlan.query.all() 
    except Exception as e:
        print(e) 

    return jsonify([s.serialize() for s in data])

@app.route("/clients")
def get_clients():
    try:
        data = Client.query.all()
    except Exception as e:
        print(e)

    return jsonify([c.serialize() for c in data])


if __name__ == "__main__":
    app.run(debug = True)