import os
from dotenv import load_dotenv
load_dotenv()
import random
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import joblib
import pandas as pd
from database import (
    db, init_db, PassengerData, TrainSchedule, User, MetroCard, Station,
    MetroLine, Fare, Journey, CardTransaction, ChatMessage, DemandForecast
)
from chatbot import MetroChatbot
from email_service import EmailService
from route_recommender import RouteRecommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-for-metro-optimized'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'metro_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize services
chatbot = MetroChatbot()
email_service = EmailService()

# Load ML Model
MODEL_PATH = os.path.join(basedir, 'models', 'demand_model.pkl')
demand_model = None
try:
    demand_model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print("Warning: ML model not found.")

# Global settings
GLOBAL_SETTINGS = {'base_trains': 4, 'max_capacity': 200}

@app.context_processor
def inject_global_stats():
    """Inject live stats for the sidebar across all pages"""
    if current_user.is_authenticated:
        try:
            user_cards = MetroCard.query.filter_by(user_id=current_user.id).all()
            total_balance = sum([card.balance for card in user_cards])
            
            # Count journeys started today
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_j_count = Journey.query.filter(
                Journey.user_id == current_user.id,
                Journey.journey_date >= today_start
            ).count()
            
            return {
                'sidebar_card_count': len(user_cards),
                'sidebar_total_balance': total_balance,
                'sidebar_today_journeys': today_j_count
            }
        except Exception:
            pass
            
    return {
        'sidebar_card_count': 0,
        'sidebar_total_balance': 0,
        'sidebar_today_journeys': 0
    }

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name', '')
            last_name = request.form.get('last_name', '')
            role = request.form.get('role', 'user')
            
            print(f"Registration attempt for email: {email}")  # Debug log
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'warning')
                return redirect(url_for('register'))
            
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            db.session.add(new_user)
            db.session.flush()  # Get the ID before committing
            
            print(f"User created with ID: {new_user.id}")  # Debug log
            
            # Create demo card for new user
            demo_card = MetroCard(
                user_id=new_user.id,
                card_number=f'DEMO{new_user.id:010d}',  # Unique card number based on user ID
                card_type='CMC',
                balance=100.0,
                kyc_status='Pending'
            )
            db.session.add(demo_card)
            db.session.flush()
            
            # Add sample journeys for demo data
            stations = Station.query.all()
            if len(stations) >= 2:
                for i in range(3):
                    from_idx = i % len(stations)
                    to_idx = (i + 2) % len(stations)
                    journey = Journey(
                        user_id=new_user.id,
                        from_station_id=stations[from_idx].id,
                        to_station_id=stations[to_idx].id,
                        fare_paid=random.randint(20, 50),
                        duration_minutes=random.randint(15, 45),
                        journey_date=datetime.now() - timedelta(days=random.randint(0, 7))
                    )
                    db.session.add(journey)
            
            db.session.commit()
            
            print(f"Registration successful for: {email}")  # Debug log
            login_user(new_user)
            flash('Account created successfully! Demo data loaded.', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Debug log
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# ==================== MAIN PAGES ====================

@app.route('/')
@login_required
def index():
    total_journeys = Journey.query.filter_by(user_id=current_user.id).count()
    cards = MetroCard.query.filter_by(user_id=current_user.id).all()
    total_balance = sum([card.balance for card in cards])
    
    # Get recent journeys
    recent_journeys = Journey.query.filter_by(user_id=current_user.id).order_by(
        Journey.journey_date.desc()
    ).limit(5).all()
    
    return render_template('index.html',
                         active_page='dashboard',
                         total_journeys=total_journeys,
                         total_balance=total_balance,
                         cards=cards,
                         recent_journeys=recent_journeys)

@app.route('/chatbot')
@login_required
def chatbot_page():
    chat_history = chatbot.get_chat_history(current_user.id)
    return render_template('chatbot.html', active_page='chatbot', chat_history=chat_history)

@app.route('/api/chat', methods=['POST'])
@login_required
def send_message():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Save user message
    chatbot.save_message(current_user.id, 'user', user_message)
    
    # Get bot response
    bot_response = chatbot.get_response(user_message, current_user.id)
    
    # Save bot message
    chatbot.save_message(current_user.id, 'bot', bot_response)
    
    return jsonify({'response': bot_response})

# ==================== CARD MANAGEMENT & RECHARGE ====================

@app.route('/cards')
@login_required
def cards_page():
    user_cards = MetroCard.query.filter_by(user_id=current_user.id).all()
    transactions = CardTransaction.query.filter_by(user_id=current_user.id).order_by(
        CardTransaction.transaction_date.desc()
    ).limit(10).all()
    
    return render_template('cards.html',
                         active_page='cards',
                         cards=user_cards,
                         transactions=transactions)

@app.route('/api/card/link', methods=['POST'])
@login_required
def link_card():
    data = request.json
    card_number = data.get('card_number')
    card_type = data.get('card_type')  # NCMC or CMC
    
    if not card_number or not card_type:
        return jsonify({'error': 'Missing data'}), 400
    
    if MetroCard.query.filter_by(card_number=card_number).first():
        return jsonify({'error': 'Card already linked'}), 400
    
    try:
        new_card = MetroCard(
            user_id=current_user.id,
            card_number=card_number,
            card_type=card_type,
            balance=0.0,
            kyc_status='Pending'
        )
        db.session.add(new_card)
        db.session.commit()
        
        flash(f'{card_type} Card linked successfully!', 'success')
        return jsonify({'success': True, 'card': {
            'id': new_card.id,
            'card_number': card_number,
            'card_type': card_type,
            'balance': 0.0,
            'kyc_status': 'Pending'
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/card/recharge', methods=['POST'])
@login_required
def recharge_card():
    data = request.json
    card_id = data.get('card_id')
    amount = float(data.get('amount', 0))
    
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    card = MetroCard.query.get(card_id)
    if not card or card.user_id != current_user.id:
        return jsonify({'error': 'Card not found'}), 404
    
    try:
        # Update card balance
        card.balance += amount
        
        # Create transaction record
        transaction = CardTransaction(
            user_id=current_user.id,
            card_id=card_id,
            transaction_type='Recharge',
            amount=amount,
            description=f'Recharge of ₹{amount}'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        # Send confirmation email
        if current_user.email_alerts_enabled:
            email_service.send_recharge_confirmation(
                current_user.email,
                {
                    'card_last_4': card.card_number[-4:],
                    'amount': amount,
                    'transaction_id': transaction.id,
                    'new_balance': card.balance
                }
            )
        
        flash(f'Recharged ₹{amount} successfully!', 'success')
        return jsonify({'success': True, 'new_balance': card.balance})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== KYC ROUTES ====================

@app.route('/kyc')
@login_required
def kyc_verification():
    user_cards = MetroCard.query.filter_by(user_id=current_user.id).all()
    return render_template('kyc.html', active_page='kyc', cards=user_cards)

@app.route('/api/kyc/upload', methods=['POST'])
@login_required
def upload_kyc():
    data = request.json
    card_id = data.get('card_id')
    doc_type = data.get('doc_type')  # Aadhar, PAN, Passport, etc.
    doc_number = data.get('doc_number')
    
    card = MetroCard.query.get(card_id)
    if not card or card.user_id != current_user.id:
        return jsonify({'error': 'Card not found'}), 404
    
    try:
        # In production, validate and store document
        card.kyc_status = 'Verified'  # Auto-approve for demo
        card.kyc_document = f"{doc_type}:{doc_number}"
        db.session.commit()
        
        flash('KYC verified successfully!', 'success')
        return jsonify({'success': True, 'kyc_status': 'Verified'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== ROUTE & TIMETABLE ====================

@app.route('/routes')
@login_required
def routes_page():
    stations = Station.query.all()
    return render_template('routes.html', active_page='routes', stations=stations)

@app.route('/api/route/find', methods=['POST'])
@login_required
def find_route():
    data = request.json
    from_station_id = int(data.get('from_station'))
    to_station_id = int(data.get('to_station'))
    
    route = RouteRecommender.find_shortest_route(from_station_id, to_station_id)
    
    if not route:
        return jsonify({'error': 'Route not found'}), 404
    
    schedules = RouteRecommender.get_available_schedules(from_station_id, to_station_id)
    
    return jsonify({
        'route': route,
        'schedules': schedules
    })

@app.route('/api/timetable/<int:line_id>')
@login_required
def get_timetable(line_id):
    """Get timetable for a specific metro line"""
    line = MetroLine.query.get(line_id)
    if not line:
        return jsonify({'error': 'Line not found'}), 404
    
    schedules = TrainSchedule.query.filter_by(line_id=line_id).order_by(
        TrainSchedule.departure_time
    ).all()
    
    return jsonify({
        'line': {
            'id': line.id,
            'name': line.name,
            'color': line.color,
            'status': line.status
        },
        'schedules': [{
            'id': s.id,
            'departure': s.departure_time.isoformat(),
            'arrival': s.arrival_time.isoformat(),
            'capacity': s.train_capacity,
            'current_passengers': s.current_passengers
        } for s in schedules]
    })

# ==================== METRO LINES & STATUS ====================

@app.route('/lines')
@login_required
def lines_page():
    """View all metro lines and their status"""
    lines = MetroLine.query.all()
    return render_template('lines.html', active_page='lines', lines=lines)

@app.route('/api/lines')
def get_lines():
    """API endpoint for metro lines data"""
    lines = MetroLine.query.all()
    return jsonify([{
        'id': line.id,
        'name': line.name,
        'color': line.color,
        'status': line.status,
        'stations': [{
            'id': s.id,
            'name': s.name,
            'latitude': float(s.latitude) if s.latitude else 0.0,
            'longitude': float(s.longitude) if s.longitude else 0.0
        } for s in line.stations if s.latitude and s.longitude]
    } for line in lines])

@app.route('/api/line/<int:line_id>/status')
def line_status(line_id):
    """Get detailed status of a metro line"""
    line = MetroLine.query.get(line_id)
    if not line:
        return jsonify({'error': 'Line not found'}), 404
    
    # Get all stations on this line
    stations = Station.query.filter_by(line_id=line_id).all()
    
    # Get passenger data for each station
    station_data = []
    for station in stations:
        passenger_data = PassengerData.query.filter_by(station_id=station.id).order_by(
            PassengerData.timestamp.desc()
        ).first()
        
        current_passengers = 0
        if passenger_data:
            current_passengers = passenger_data.entries - passenger_data.exits
        
        if station.latitude and station.longitude:  # Only add if we have coordinates
            station_data.append({
                'id': station.id,
                'name': station.name,
                'current_passengers': max(0, current_passengers),
                'latitude': float(station.latitude),
                'longitude': float(station.longitude)
            })
    
    return jsonify({
        'line': {
            'id': line.id,
            'name': line.name,
            'color': line.color,
            'status': line.status
        },
        'stations': station_data
    })

# ==================== PRICING & FARES ====================

@app.route('/pricing')
@login_required
def pricing_page():
    """View pricing information"""
    stations = Station.query.all()
    return render_template('pricing.html', active_page='pricing', stations=stations)

@app.route('/api/fare/calculate', methods=['POST'])
@login_required
def calculate_fare():
    """Calculate station-count-based fare between two stations"""
    data = request.json
    from_station_id = int(data.get('from_station'))
    to_station_id = int(data.get('to_station'))

    from_station = Station.query.get(from_station_id)
    to_station = Station.query.get(to_station_id)

    if not from_station or not to_station:
        return jsonify({'error': 'Station not found'}), 404

    # ---- Station-count based fare (Bangalore Metro slab) ----
    if from_station.line_id == to_station.line_id:
        # Same line — count stations between them
        min_order = min(from_station.order_on_line, to_station.order_on_line)
        max_order = max(from_station.order_on_line, to_station.order_on_line)
        station_count = max_order - min_order  # number of stops
    else:
        # Cross-line — approximate via sum of orders as worst case
        station_count = from_station.order_on_line + to_station.order_on_line

    fare_amount = _fare_by_stations(station_count)
    distance = round(abs(to_station.distance_from_first - from_station.distance_from_first), 1)

    return jsonify({
        'from': from_station.name,
        'to': to_station.name,
        'stations_count': station_count,
        'distance_km': distance,
        'fare_amount': fare_amount,
        'fare_formatted': f'₹{fare_amount}'
    })

def _fare_by_stations(station_count):
    """Bangalore Metro standard station-count fare slabs"""
    if station_count <= 0:
        return 10
    elif station_count <= 2:
        return 10
    elif station_count <= 4:
        return 20
    elif station_count <= 6:
        return 30
    elif station_count <= 9:
        return 40
    else:
        return 50

# ==================== METRO MAP ====================

@app.route('/map')
@login_required
def metro_map():
    """Interactive metro map visualization"""
    lines = MetroLine.query.all()
    return render_template('map.html', active_page='map', lines=lines)

@app.route('/api/map/data')
def map_data():
    """Get metro map data for visualization"""
    lines = MetroLine.query.all()
    
    lines_data = []
    for line in lines:
        stations_list = Station.query.filter_by(line_id=line.id).order_by(
            Station.order_on_line
        ).all()
        
        if stations_list:  # Only add line if it has stations
            lines_data.append({
                'id': line.id,
                'name': line.name,
                'color': line.color,
                'stations': [{
                    'id': s.id,
                    'name': s.name,
                    'lat': float(s.latitude) if s.latitude else 0.0,
                    'lng': float(s.longitude) if s.longitude else 0.0,
                    'distance': float(s.distance_from_first) if s.distance_from_first else 0.0
                } for s in stations_list if s.latitude and s.longitude]
            })
    
    return jsonify({'lines': lines_data})

# ==================== AI BASED DEMAND FORECAST ====================

@app.route('/forecast')
@login_required
def demand_forecast():
    """AI-based demand forecast page"""
    lines = MetroLine.query.all()
    return render_template('forecast.html', active_page='forecast', lines=lines)

@app.route('/api/forecast/demand', methods=['GET', 'POST'])
def predict_demand_api():
    """Predict passenger demand using ML model"""
    data = request.json or {}
    station_id = int(data.get('station_id', 1))
    
    predictions = []
    for i in range(1, 25):  # 24-hour forecast
        future_time = datetime.now() + timedelta(hours=i)
        is_weekend = int(future_time.weekday() >= 5)
        hour = future_time.hour
        
        if demand_model is not None:
            # Use ML model if available
            input_data = pd.DataFrame(
                [[station_id, is_weekend, hour]],
                columns=['station_id', 'is_weekend', 'hour']
            )
            prediction = demand_model.predict(input_data)[0]
        else:
            # Demo data: realistic passenger patterns
            base_demand = 150
            if 6 <= hour <= 9:  # Morning peak
                base_demand = 400
            elif 12 <= hour <= 14:  # Lunch time
                base_demand = 250
            elif 17 <= hour <= 20:  # Evening peak
                base_demand = 380
            elif 0 <= hour <= 6:  # Night time
                base_demand = 50
            
            prediction = base_demand + random.randint(-50, 50)
        
        predictions.append({
            'time': future_time.strftime("%H:00"),
            'predicted_demand': int(prediction),
            'trains_needed': max(4, int(prediction / 200) + 1)
        })
    
    return jsonify({'predictions': predictions})

# ==================== ROUTE RECOMMENDATIONS ====================

@app.route('/recommendations')
@login_required
def route_recommendations():
    """Get smart route recommendations for user"""
    frequent_routes = RouteRecommender.get_personalized_routes(current_user.id)
    return render_template('recommendations.html',
                         active_page='recommendations',
                         frequent_routes=frequent_routes)

@app.route('/api/recommendations/frequent')
@login_required
def get_frequent_routes():
    """API for frequently used routes"""
    routes = RouteRecommender.get_personalized_routes(current_user.id)
    return jsonify({'routes': routes})

# ==================== EMAIL ALERTS ====================

@app.route('/alerts')
@login_required
def alerts_page():
    """Manage email alerts and notifications"""
    return render_template('alerts.html',
                         active_page='alerts',
                         alerts_enabled=current_user.email_alerts_enabled)

@app.route('/api/alerts/toggle', methods=['POST'])
@login_required
def toggle_alerts():
    """Toggle email alerts for user"""
    current_user.email_alerts_enabled = not current_user.email_alerts_enabled
    db.session.commit()
    
    return jsonify({
        'success': True,
        'alerts_enabled': current_user.email_alerts_enabled
    })

@app.route('/api/alert/send-line-status', methods=['POST'])
@login_required
def send_line_alert():
    """Send line status alert email"""
    if not current_user.email_alerts_enabled:
        return jsonify({'error': 'Alerts disabled'}), 400
    
    data = request.json
    line_id = int(data.get('line_id'))
    line = MetroLine.query.get(line_id)
    
    if not line:
        return jsonify({'error': 'Line not found'}), 404
    
    alert_data = {
        'line_name': line.name,
        'status': line.status,
        'color': line.color,
        'message': data.get('message', f'{line.name} is currently {line.status}'),
        'resolution_time': data.get('resolution_time', 'To be updated soon')
    }
    
    email_service.send_line_alert(current_user.email, alert_data)
    
    return jsonify({'success': True})

# ==================== USER ACCOUNTS & SETTINGS ====================

@app.route('/account')
@login_required
def account_settings():
    """User account settings page"""
    return render_template('account.html',
                         active_page='account',
                         user=current_user)

@app.route('/api/account/update', methods=['POST'])
@login_required
def update_account():
    """Update user account information"""
    data = request.json
    
    if 'first_name' in data:
        current_user.first_name = data['first_name']
    if 'last_name' in data:
        current_user.last_name = data['last_name']
    if 'phone' in data:
        current_user.phone = data['phone']
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    
    return jsonify({'success': True})

# ==================== STATISTICS & ANALYTICS ====================

@app.route('/api/stats/user')
@login_required
def user_stats():
    """Get user journey statistics"""
    journeys = Journey.query.filter_by(user_id=current_user.id).all()
    
    total_journeys = len(journeys)
    total_distance = sum([j.duration_minutes or 0 for j in journeys])
    total_fare = sum([j.fare_paid for j in journeys])
    
    # Most used stations
    from_counts = {}
    for journey in journeys:
        from_station = Station.query.get(journey.from_station_id)
        if from_station:
            from_counts[from_station.name] = from_counts.get(from_station.name, 0) + 1
    
    most_used = sorted(from_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return jsonify({
        'total_journeys': total_journeys,
        'total_distance_km': total_distance,
        'total_fare_paid': total_fare,
        'most_used_stations': most_used
    })

@app.route('/api/stats/realtime')
def realtime_stats():
    """Get real-time system statistics"""
    lines = MetroLine.query.all()
    
    line_data = []
    total_passengers = 0
    
    for line in lines:
        line_stations = Station.query.filter_by(line_id=line.id).all()
        passengers = 0
        
        for station in line_stations:
            passenger_data = PassengerData.query.filter_by(station_id=station.id).order_by(
                PassengerData.timestamp.desc()
            ).first()
            if passenger_data:
                passengers += max(0, passenger_data.entries - passenger_data.exits)
        
        total_passengers += passengers
        line_data.append({
            'name': line.name,
            'color': line.color,
            'status': line.status,
            'passengers': passengers
        })
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'total_passengers': total_passengers,
        'lines': line_data,
        'system_status': 'Operational',
        'active_trains': GLOBAL_SETTINGS['base_trains']
    })

# ==================== SETTINGS API ====================

@app.route('/api/settings', methods=['GET'])
@login_required
def get_settings():
    """Return current global optimization settings"""
    return jsonify(GLOBAL_SETTINGS)

@app.route('/api/settings', methods=['POST'])
@login_required
@admin_required
def save_settings():
    """Update global optimization settings"""
    data = request.json
    try:
        GLOBAL_SETTINGS['base_trains'] = int(data.get('base_trains', GLOBAL_SETTINGS['base_trains']))
        GLOBAL_SETTINGS['max_capacity'] = int(data.get('max_capacity', GLOBAL_SETTINGS['max_capacity']))
        return jsonify({'success': True, 'settings': GLOBAL_SETTINGS})
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid value: {e}'}), 400

# ==================== MISSING PAGE ROUTES ====================

@app.route('/schedules')
@login_required
def schedules_page():
    """Train schedules view"""
    lines = MetroLine.query.all()
    return render_template('schedules.html', active_page='schedules', lines=lines)

@app.route('/passenger-flow')
@login_required
def passenger_flow_page():
    """Passenger flow analysis"""
    return render_template('passenger_flow.html', active_page='passenger_flow')

@app.route('/settings')
@login_required
@admin_required
def settings_page():
    """System settings page"""
    return render_template('settings.html', active_page='settings')

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Administrative command center"""
    users = User.query.all()
    stations_count = Station.query.count()
    lines_count = MetroLine.query.count()
    journeys_count = Journey.query.count()
    
    return render_template('admin.html', 
                         active_page='admin', 
                         users=users,
                         stations_count=stations_count,
                         lines_count=lines_count,
                         journeys_count=journeys_count)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
