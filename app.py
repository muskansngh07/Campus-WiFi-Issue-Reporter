from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import folium
from folium.plugins import HeatMap

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'database')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, 'reports.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hi'  

db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    issue_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_report = Report(
            location=request.form['location'],
            issue_type=request.form['issue_type'],  
            description=request.form['description'],
            name=request.form['name'],
            latitude=request.form.get('latitude', type=float),
            longitude=request.form.get('longitude', type=float)
        )
        db.session.add(new_report)
        db.session.commit()
        flash("Your report has been submitted. Thank you!")
        return redirect('/')
    reports = Report.query.order_by(Report.timestamp.desc()).all()  # fixed .all() position
    return render_template('index.html', reports=reports)

@app.route('/map')
def show_map():
    reports = Report.query.all()
    campus_map = folium.Map(location=[17.783005, 83.361459], zoom_start=17)
    heat_data = [[r.latitude, r.longitude] for r in reports if r.latitude and r.longitude]
    if heat_data:
        HeatMap(heat_data).add_to(campus_map)
    campus_map.save('templates/map.html')
    return render_template('map.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
