from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Configure your AWS RDS database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:hamzahamza@hamzahamza.cjhcozhoozjh.eu-west-1.rds.amazonaws.com:3306/flaskaws'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy instance
db = SQLAlchemy(app)

API_KEY = 'DED6D825-C607-4DFB-9B77-A6A428996447'

class Earthquake(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    mag = db.Column(db.Float)
    place = db.Column(db.String(255))
    time = db.Column(db.BigInteger)
    url = db.Column(db.String(255))
    detail = db.Column(db.String(255))
    felt = db.Column(db.Integer)
    cdi = db.Column(db.Float)
    mmi = db.Column(db.Float)
    alert = db.Column(db.String(50))
    status = db.Column(db.String(50))
    tsunami = db.Column(db.Integer)
    sig = db.Column(db.Integer)
    net = db.Column(db.String(10))
    code = db.Column(db.String(50))
    ids = db.Column(db.String(255))
    sources = db.Column(db.String(255))
    types = db.Column(db.String(255))
    nst = db.Column(db.Integer)
    dmin = db.Column(db.Float)
    rms = db.Column(db.Float)
    gap = db.Column(db.Float)
    magType = db.Column(db.String(50))
    earthquakeType = db.Column(db.String(50))
    title = db.Column(db.String(255))
    coordinates = db.Column(db.String(255))

@app.route('/')
def index():
    EARTHQUAKE_API_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-03-01&endtime=2023-03-02&minmagnitude=5'
    response = requests.get(EARTHQUAKE_API_URL)

    if response.status_code == 200:
        data = response.json()

        selected_earthquakes = [
            {
                'id': item['id'],
                'mag': item['properties']['mag'],
                'place': item['properties']['place'],
                'time': item['properties']['time'],
                'url': item['properties']['url'],
                'detail': item['properties']['detail'],
                'felt': item['properties']['felt'],
                'cdi': item['properties']['cdi'],
                'mmi': item['properties']['mmi'],
                'alert': item['properties']['alert'],
                'status': item['properties']['status'],
                'tsunami': item['properties']['tsunami'],
                'sig': item['properties']['sig'],
                'net': item['properties']['net'],
                'code': item['properties']['code'],
                'ids': item['properties']['ids'],
                'sources': item['properties']['sources'],
                'types': item['properties']['types'],
                'nst': item['properties']['nst'],
                'dmin': item['properties']['dmin'],
                'rms': item['properties']['rms'],
                'gap': item['properties']['gap'],
                'magType': item['properties']['magType'],
                'earthquakeType': item['properties']['type'],
                'title': item['properties']['title'],
                'coordinates': ','.join(map(str, item['geometry']['coordinates'])),
            }
            for item in data['features']
        ]

        print("Selected Earthquakes:", selected_earthquakes)

        # Clear existing data in the Earthquake table
        Earthquake.query.delete()

        # Insert new data into the Earthquake table
        db.session.bulk_insert_mappings(Earthquake, selected_earthquakes)

        # Commit changes to the database
        db.session.commit()
    else:
        selected_earthquakes = [{'error': 'Failed to fetch data from API'}]

    # Fetch data from the database
    earthquakes_from_db = Earthquake.query.all()

    return render_template('index.html', result=earthquakes_from_db)


if __name__ == '__main__':
    with app.app_context():
        # Create tables before running the app
        db.create_all()

        # Run the Flask app
        app.run(debug=True)
