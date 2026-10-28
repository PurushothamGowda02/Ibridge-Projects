from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default='user')
    email_alerts_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return self.is_active
        
    @property
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return str(self.id)
        
    cards = db.relationship('MetroCard', backref='owner', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('CardTransaction', backref='user', lazy=True, cascade='all, delete-orphan')
    journeys = db.relationship('Journey', backref='user', lazy=True, cascade='all, delete-orphan')

class MetroCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_number = db.Column(db.String(20), unique=True, nullable=False)
    card_type = db.Column(db.String(10), nullable=False) # NCMC or CMC
    balance = db.Column(db.Float, default=0.0)
    kyc_status = db.Column(db.String(20), default='Pending') # Pending, Verified, Rejected
    kyc_document = db.Column(db.String(256), nullable=True)
    linked_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class CardTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('metro_card.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False) # Recharge, Journey, Refund
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(256), nullable=True)

class MetroLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Operational') # Operational, Delayed, Closed
    stations = db.relationship('Station', backref='line', lazy=True, cascade='all, delete-orphan')

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    line_id = db.Column(db.Integer, db.ForeignKey('metro_line.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    distance_from_first = db.Column(db.Float, default=0.0) # km
    order_on_line = db.Column(db.Integer, nullable=False)

class Fare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    fare_amount = db.Column(db.Float, nullable=False)

class Journey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    from_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    journey_date = db.Column(db.DateTime, default=datetime.utcnow)
    fare_paid = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    # Relationships to Station for template access
    from_station = db.relationship('Station', foreign_keys=[from_station_id], lazy=True)
    to_station   = db.relationship('Station', foreign_keys=[to_station_id],   lazy=True)

class DemandForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    forecast_date = db.Column(db.DateTime, nullable=False)
    predicted_passengers = db.Column(db.Integer, nullable=False)
    prediction_time = db.Column(db.DateTime, default=datetime.utcnow)

class PassengerData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    entries = db.Column(db.Integer, nullable=False)
    exits = db.Column(db.Integer, nullable=False)

class TrainSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Integer, db.ForeignKey('metro_line.id'), nullable=False)
    from_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    train_capacity = db.Column(db.Integer, nullable=False)
    current_passengers = db.Column(db.Integer, default=0)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_type = db.Column(db.String(20), nullable=False) # user, bot
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # ── Seed real Namma Metro data only on first run ──────────────────────
        if MetroLine.query.first() is None:

            # ── Real Bangalore Namma Metro Lines ─────────────────────────────
            lines_seed = [
                {'name': 'Purple Line', 'color': '#9333ea'},   # East-West operational
                {'name': 'Green Line',  'color': '#16a34a'},   # North-South operational
            ]
            for ld in lines_seed:
                db.session.add(MetroLine(name=ld['name'], color=ld['color'], status='Operational'))
            db.session.commit()

            purple = MetroLine.query.filter_by(name='Purple Line').first()
            green  = MetroLine.query.filter_by(name='Green Line').first()

            # ── Purple Line: Whitefield (Kadugodi) ↔ Challaghatta ──────────────────
            # 37 stations, East-West corridor
            purple_stations = [
                ('Kadugodi',                  12.9988, 77.7489),
                ('Pattandur Agrahara',        12.9977, 77.7373),
                ('Whitefield (Kadugodi)',      12.9969, 77.7265),
                ('Hopefarm Channasandra',     12.9963, 77.7157),
                ('Garudacharpalya',           12.9913, 77.6985),
                ('Mahadevapura',              12.9892, 77.6872),
                ('Doddanekundi',              12.9868, 77.6742),
                ('Krishnarajapuram',          12.9843, 77.6624),
                ('Benniganahalli',            12.9869, 77.6527),
                ('Singayyanapalya',           12.9872, 77.6443),
                ('Hoodi',                     12.9850, 77.6321),
                ('Garudachar Palya',          12.9835, 77.6198),
                ('Baiyappanahalli',           12.9985, 77.6413),
                ('Swami Vivekananda Road',    12.9937, 77.6326),
                ('Indiranagar',               12.9784, 77.6408),
                ('Halasuru',                  12.9727, 77.6288),
                ('Trinity',                   12.9724, 77.6196),
                ('MG Road',                   12.9757, 77.6099),
                ('Cubbon Park',               12.9752, 77.5970),
                ('Vidhana Soudha',            12.9796, 77.5904),
                ('Sir M Visvesvaraya',        12.9772, 77.5814),
                ('Nadaprabhu Kempegowda',     12.9773, 77.5701),  # Majestic - interchange
                ('City Railway Station',      12.9770, 77.5653),
                ('Magadi Road',               12.9724, 77.5554),
                ('Hosahalli',                 12.9662, 77.5449),
                ('Vijayanagar',               12.9656, 77.5353),
                ('Attiguppe',                 12.9616, 77.5272),
                ('Deepanjali Nagar',          12.9561, 77.5196),
                ('Mysuru Road',               12.9513, 77.5126),
                ('Pantharapalya',             12.9456, 77.5063),
                ('Anjanapura Township',       12.9389, 77.4998),
                ('Jnanabharathi',             12.9353, 77.4946),
                ('Rajarajeshwari Nagar',      12.9283, 77.4989),
                ('Nayandahalli',              12.9337, 77.5060),
                ('Kengeri Bus Terminal',      12.9205, 77.4825),
                ('Kengeri',                   12.9167, 77.4839),
                ('Challaghatta',              12.9099, 77.4851),
            ]

            # ── Green Line: Nagasandra ↔ Silk Institute (Yelachenahalli) ─────
            # 24 stations, North-South corridor
            green_stations = [
                ('Nagasandra',                13.0515, 77.5244),
                ('Dasarahalli',               13.0427, 77.5261),
                ('Jalahalli',                 13.0347, 77.5281),
                ('Peenya Industry',           13.0159, 77.5123),
                ('Peenya',                    13.0069, 77.5140),
                ('Goraguntepalya',            12.9972, 77.5561),
                ('Yeshwanthpur',              13.0232, 77.5485),
                ('Sandal Soap Factory',       13.0163, 77.5537),
                ('Mahalakshmi',               13.0064, 77.5591),
                ('Rajajinagar',               12.9972, 77.5561),
                ('Kuvempu Road',              12.9909, 77.5638),
                ('Srirampura',                12.9864, 77.5683),
                ('Sampige Road',              12.9843, 77.5746),
                ('Nadaprabhu Kempegowda',     12.9773, 77.5701),  # Majestic - interchange
                ('Chickpete',                 12.9664, 77.5743),
                ('Krishna Rajendra Market',   12.9602, 77.5754),
                ('National College',          12.9536, 77.5769),
                ('Lalbagh',                   12.9497, 77.5839),
                ('South End Circle',          12.9406, 77.5891),
                ('Jayanagar',                 12.9315, 77.5831),
                ('RV Road',                   12.9274, 77.5839),
                ('Banashankari',              12.9213, 77.5773),
                ('JP Nagar',                  12.9086, 77.5762),
                ('Yelachenahalli (Silk Inst)',12.8965, 77.5758),
            ]

            def add_stations(line_obj, station_list):
                distance = 0.0
                for order, (name, lat, lng) in enumerate(station_list, start=1):
                    db.session.add(Station(
                        name=name, line_id=line_obj.id,
                        latitude=lat, longitude=lng,
                        distance_from_first=round(distance, 2),
                        order_on_line=order
                    ))
                    distance += 1.5   # avg ~1.5 km between Namma Metro stations
            
            add_stations(purple, purple_stations)
            add_stations(green,  green_stations)
            db.session.commit()

            # ── Fare table (station-count slabs, no raw distance formula) ────
            def slab_fare(stop_count):
                if stop_count <= 2:  return 10
                if stop_count <= 4:  return 20
                if stop_count <= 6:  return 30
                if stop_count <= 9:  return 40
                return 50

            all_stations = Station.query.all()
            for i, s1 in enumerate(all_stations):
                for s2 in all_stations[i+1:]:
                    if s1.line_id == s2.line_id:
                        stops = abs(s1.order_on_line - s2.order_on_line)
                        dist  = round(abs(s2.distance_from_first - s1.distance_from_first), 2)
                        db.session.add(Fare(
                            from_station_id=s1.id,
                            to_station_id=s2.id,
                            distance_km=dist,
                            fare_amount=slab_fare(stops)
                        ))
            db.session.commit()
