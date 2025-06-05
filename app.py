from flask import FLASK,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database/reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
class Report(db.Model):
    id=db.column(db.Integer,primary_key=True)
    location=db.column(db.String(100))
    issue_type=db.Column(db.String(50))
    description=db.Column(db.Text)
    name=db.Column(db.String(50))
    timestamp=db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        new_report=Report(location=request.form['location'],issue_type=request.form['isuue_type'],description=request.form['description'],name=request.form['name'])
        db.session.add(new_report)
        db.session.commit()
        return redirect('/')
    reports=Report.query.order_by(Report.timestamp.desc().all())
    return render_template('index.html',reports=reports)

if __name__=='__main__':
    if not os.path.exists('database'):
        os.makedirs('database')
    db.create_all()
    app.run(debug=True)