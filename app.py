from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import difflib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PeeEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(20))

class PoopEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(20))

class SumEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, default=datetime.utcnow)
    vr = db.Column(db.Boolean, default=False)
    name1 = db.Column(db.String(50))
    name2 = db.Column(db.String(50))
    name3 = db.Column(db.String(50))

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def avg_interval(events):
    if len(events) < 2:
        return None
    intervals = [
        (events[i].ts - events[i-1].ts).total_seconds()
        for i in range(1, len(events))
    ]
    avg_sec = sum(intervals) / len(intervals)
    return str(timedelta(seconds=avg_sec))

def daily_avg(events):
    if not events:
        return 0
    days = (max(e.ts for e in events) - min(e.ts for e in events)).days + 1
    return round(len(events) / days, 2)

def group_names(all_names):
    groups = []
    for name in all_names:
        name = name.strip().lower()
        if not name:
            continue
        placed = False
        for grp in groups:
            # compare to the group's representative
            if difflib.SequenceMatcher(None, name, grp[0]).ratio() > 0.8:
                grp.append(name)
                placed = True
                break
        if not placed:
            groups.append([name])
    # build counts
    stats = {}
    for grp in groups:
        key = grp[0].capitalize()
        stats[key] = stats.get(key, 0) + len(grp)
    total = sum(stats.values())
    # percentages
    return [
        {'name': n, 'count': c, 'pct': round(c / total * 100, 1)}
        for n, c in stats.items()
    ]

@app.route('/api/pee', methods=['POST'])
def api_pee():
    data = request.json
    ev = PeeEvent(ts=datetime.fromisoformat(data['ts']), location=data['location'])
    db.session.add(ev); db.session.commit()
    return jsonify(success=True)

@app.route('/api/poop', methods=['POST'])
def api_poop():
    data = request.json
    ev = PoopEvent(ts=datetime.fromisoformat(data['ts']), location=data['location'])
    db.session.add(ev); db.session.commit()
    return jsonify(success=True)

@app.route('/api/sum', methods=['POST'])
def api_sum():
    data = request.json
    ev = SumEvent(
        ts=datetime.fromisoformat(data['ts']),
        vr=data.get('vr', False),
        name1=data.get('name1',''),
        name2=data.get('name2',''),
        name3=data.get('name3','')
    )
    db.session.add(ev); db.session.commit()
    return jsonify(success=True)

@app.route('/api/stats')
def api_stats():
    pees = PeeEvent.query.order_by(PeeEvent.ts).all()
    poops = PoopEvent.query.order_by(PoopEvent.ts).all()
    sums = SumEvent.query.order_by(SumEvent.ts).all()

    name_entries = []
    for s in sums:
        name_entries += [s.name1, s.name2, s.name3]
    name_stats = group_names(name_entries)

    return jsonify({
        'pee': {
            'events': [{'ts': e.ts.isoformat(), 'loc': e.location} for e in pees],
            'avg_interval': avg_interval(pees),
            'daily_avg': daily_avg(pees)
        },
        'poop': {
            'events': [{'ts': e.ts.isoformat(), 'loc': e.location} for e in poops],
            'avg_interval': avg_interval(poops),
            'daily_avg': daily_avg(poops)
        },
        'sum': {
            'count': len(sums),
            'names': name_stats
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
