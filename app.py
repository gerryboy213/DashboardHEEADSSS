import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, distinct, and_, desc, or_, func, extract
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import or_  # Make sure this import exists
import json
import os
import uuid
import mysql.connector
import re
from datetime import datetime, date  # <-- ADD 'date' HERE
from collections import defaultdict

app = Flask(__name__)
app.run(debug=True)
app.secret_key = 'your_secret_key'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/form_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ... all your other routes and code ...


# Session management
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# Debug routes
@app.route('/test_db')
def test_db():
    try:
        # Test SQLAlchemy connection
        result = db.session.execute(text('SELECT 1'))
        db.session.commit()
        print("✅ SQLAlchemy connection works")
        return "Database connection is working"
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return f"Database error: {e}", 500

@app.route('/check_tables')
def check_tables():
    try:
        # For SQLAlchemy 1.4+
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("Available tables:", tables)
        
        # Check if specific tables exist
        required_tables = ['user', 'questions', 'user_response', 'services', 'recommendations']
        for table in required_tables:
            if table in tables:
                print(f"✅ {table} table exists")
            else:
                print(f"❌ {table} table missing")
                
        return f"Tables: {tables}"
    except Exception as e:
        return f"Error checking tables: {e}", 500

@app.route('/debug_user/<int:user_id>')
def debug_user(user_id):
    try:
        # Method 1: Direct query
        user1 = User.query.get(user_id)
        print(f"Direct query: {user1.control_num if user1 else 'Not found'}")
        
        # Method 2: Session refresh
        if user1:
            db.session.refresh(user1)
            print(f"After refresh: {user1.control_num}")
        
        # Method 3: New query
        user2 = db.session.query(User).filter(User.id == user_id).first()
        print(f"New query: {user2.control_num if user2 else 'Not found'}")
        
        return jsonify({
            "direct_query": user1.control_num if user1 else None,
            "after_refresh": user1.control_num if user1 else None,
            "new_query": user2.control_num if user2 else None
        })
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/debug_services/<int:user_id>')
def debug_services(user_id):
    try:
        services = Services.query.filter_by(user_id=user_id).all()
        print(f"Found {len(services)} services for user {user_id}")
        
        service_data = []
        for service in services:
            service_data.append({
                'id': service.id,
                'service_name': service.service_name,
                'service_detail': service.service_detail,
                'timestamp': service.timestamp.isoformat() if service.timestamp else None,
                'source': service.source
            })
            print(f"Service: {service.service_name}, Detail: {service.service_detail}")
        
        return jsonify(service_data)
    except Exception as e:
        return f"Error: {e}", 500

# Folder to save uploaded signatures
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_questions():
    return Questions.query.filter_by(category='HOME').all()

def get_questions_and_answers(user_id):
    """Fetches the user's responses along with the corresponding questions."""
    responses = (
        db.session.query(Questions.id, Questions.question_text, UserResponse.response)
        .join(UserResponse, Questions.id == UserResponse.question_number)
        .filter(UserResponse.user_id == user_id)
        .all()
    )

    return {
        question_id: {"question": question_text, "answer": response}
        for question_id, question_text, response in responses
    }

# ========== FIXED SECTION: Moved functions outside the route ==========

def get_gender_age_counts(service_name, start_date, end_date):
    try:
        counts = {
            'male_10_14': 0,
            'male_15_19': 0,
            'female_10_14': 0,
            'female_15_19': 0,
        }

        # Build query
        query = db.session.query(User.sex, User.age)
        
        if service_name != 'Any Service Accessed':
            query = query.join(Services, User.id == Services.user_id)
            query = query.filter(
                Services.service_name == service_name,
                Services.timestamp.between(start_date, end_date)
            )
        else:
            query = query.join(Services, User.id == Services.user_id)
            query = query.filter(Services.timestamp.between(start_date, end_date))

        # Add user filters
        query = query.filter(
            User.age.between(10, 19),
            User.sex.in_(['Male', 'Female'])
        )

        results = query.all()
        
        print(f"🔍 {service_name}: Found {len(results)} records")
        
        for sex, age in results:
            if sex == 'Male':
                if 10 <= age <= 14:
                    counts['male_10_14'] += 1
                elif 15 <= age <= 19:
                    counts['male_15_19'] += 1
            elif sex == 'Female':
                if 10 <= age <= 14:
                    counts['female_10_14'] += 1
                elif 15 <= age <= 19:
                    counts['female_15_19'] += 1

        return counts
    except Exception as e:
        print(f"❌ Error in get_gender_age_counts: {e}")
        return {'male_10_14': 0, 'male_15_19': 0, 'female_10_14': 0, 'female_15_19': 0}

def get_grouped_counts_by_question(question_number, start_date, end_date, admin):
    try:
        grouped_counts = {
            "10-14": {"Male": 0, "Female": 0},
            "15-19": {"Male": 0, "Female": 0}
        }

        # More flexible query
        query = db.session.query(User.age, User.sex)\
            .join(UserResponse, User.id == UserResponse.user_id)\
            .filter(
                UserResponse.question_number == question_number,
                func.lower(func.trim(UserResponse.response)) == 'yes'
            )

        # Add date filter if dates are provided
        if start_date and end_date:
            query = query.filter(UserResponse.submitted_at.between(start_date, end_date))

        results = query.all()
        
        print(f"🔍 Question {question_number}: Found {len(results)} 'yes' responses")

        for age, sex in results:
            if age is None or sex is None:
                continue
                
            sex = sex.capitalize()
            if sex not in ["Male", "Female"]:
                continue
                
            if 10 <= age <= 14:
                grouped_counts["10-14"][sex] += 1
            elif 15 <= age <= 19:
                grouped_counts["15-19"][sex] += 1

        return grouped_counts
    except Exception as e:
        print(f"❌ Error in get_grouped_counts_by_question: {e}")
        return {"10-14": {"Male": 0, "Female": 0}, "15-19": {"Male": 0, "Female": 0}}

with open("static/ph-json/province.json", "r", encoding="utf-8") as file:
    province_data = json.load(file)
    
# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    control_num = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_initial = db.Column(db.String(5), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    barangay = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    location = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    assigned_center = db.Column(db.String(100))
    referral_history = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    visible_to_rhu = db.Column(db.Boolean, default=True)
    visible_to_brgy = db.Column(db.Boolean, default=True)
    visible_to_hospital = db.Column(db.Boolean, default=True)
    last_forwarded_by = db.Column(db.String(150))
    last_forwarded_by_position = db.Column(db.String(100))
    
    responses = db.relationship(
        'UserResponse',
        backref='user',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
class ReferralHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    from_center = db.Column(db.String(100), nullable=False)
    to_center = db.Column(db.String(100), nullable=False)
    forwarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='referrals')
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    center_name = db.Column(db.String(100))
    message = db.Column(db.Text)
    urgency = db.Column(db.String(10))
    unread = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_text = db.Column(db.Text, nullable=False)
    translation_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    
class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )    
    question_number = db.Column(db.Integer, nullable=False)
    response = db.Column(db.String(10), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class AssessmentResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    assessment_number = db.Column(db.Integer, nullable=False)
    response = db.Column(db.String(10), nullable=False)
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    center_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    
class Services(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    services_saved = db.Column(db.Boolean, default=False)
    service_detail = db.Column(db.String(255), nullable=False, default='')
    user_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(50), nullable=False, default='brgy')

class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recommendation_text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False)
    recommendation_saved = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(50), nullable=False, default='brgy')

class Signature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ========== ROUTES ==========

@app.route('/')
def home():
    return render_template('index.html')

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin_data = Admin.query.filter_by(username=username).first()

        if admin_data and check_password_hash(admin_data.password, password):
            session['admin'] = username
            print(session['admin'])

            # Determine source from center_name
            center_source_map = {
                "BHS Union AFHF": "brgy",
                "RHU Mayorga": "rhu",
                "Gandara AFHF": "hospital",
                "RHU Gandara": "rhu",
                "RHU Pagsanghan": "rhu",
                "Abuyog DH AFHF": "hospital",
                "Gandara DH AFHF": "hospital"
            }

            session['source'] = center_source_map.get(admin_data.center_name, 'unknown')

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return "OK"

            return redirect(url_for('admin_dashboard'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return "Invalid"

            flash('Invalid credentials. Try again.', 'danger')
            return redirect(url_for('admin_login'))

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'GET':
        return render_template('admin_signup.html')
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('new_username')
        password = request.form.get('new_password')
        position = request.form.get('position')
        region = request.form.get('region')
        province = request.form.get('province')
        city = request.form.get('city')
        center_name = request.form.get('centerName')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')

        # Validate required fields
        if not full_name or not username or not password or not region or not province or not city or not center_name:
            return "Please fill in all required fields", 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        new_admin = Admin(
            full_name=full_name,
            username=username,
            password=hashed_password,
            position=position,
            region=region,
            province=province,
            city=city,
            center_name=center_name,
            phone=contact_number,
            email=email,
        )

        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    # Refresh admin data
    db.session.refresh(admin)

    # Load region, province, and city data from JSON files
    json_files = {
        "region": "region.json",
        "province": "province.json",
        "city": "city.json",
        "barangay": "barangay.json"
    }

    json_data = {}
    try:
        for key, filename in json_files.items():
            path = os.path.join(current_app.root_path, 'static', 'ph-json', filename)
            with open(path, 'r', encoding='utf-8') as f:
                json_data[key] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return f"Error: {str(e)}", 500

    # Initialize the region_map, province_map, and city_map from JSON data
    region_map = {item["region_code"]: item["region_name"] for item in json_data.get("region", [])}
    province_map = {item["province_code"]: item["province_name"] for item in json_data.get("province", [])}
    city_map = {item["city_code"]: item["city_name"] for item in json_data.get("city", [])}

    # Get basic counts for the dashboard
    services = Services.query.all()
    questions = Questions.query.all()
    users = User.query.all()
    unread_responses = UserResponse.query.filter_by(is_read=False).count()

    # Get current year and month for filters
    selected_year = request.args.get('year', str(datetime.now().year))
    selected_month = request.args.get('month', 'all')
    
    if selected_month != 'all':
        start_date = f"{selected_year}-{selected_month}-01"
        # get last day of the month
        next_month = int(selected_month) % 12 + 1
        next_year = int(selected_year) + 1 if next_month == 1 else int(selected_year)
        end_date = f"{next_year}-{str(next_month).zfill(2)}-01"
    else:
        start_date = f"{selected_year}-01-01"
        end_date = f"{selected_year}-12-31"
    
    current_year = datetime.now().year
    available_years = list(range(2025, current_year + 6))  # 2025 to 5 years ahead

    # Get basic service counts using the improved functions
    heeadsss_counts = get_gender_age_counts('Assessed using HEEADSSS', start_date, end_date)
    heeadsss_total = sum(heeadsss_counts.values())

    hyo_counts = get_gender_age_counts('Reached by HYO', start_date, end_date)
    hyo_total = sum(hyo_counts.values())

    adolescents_with_services = get_gender_age_counts('Any Service Accessed', start_date, end_date)
    referred_using_heeadsss_total = sum(adolescents_with_services.values())

    # Get counts for key questions
    grouped_attempted_suicide = get_grouped_counts_by_question(4, start_date, end_date, admin)
    grouped_sexual_violence = get_grouped_counts_by_question(10, start_date, end_date, admin)
    grouped_binge = get_grouped_counts_by_question(6, start_date, end_date, admin)
    grouped_tobacco = get_grouped_counts_by_question(5, start_date, end_date, admin)
    grouped_drugs = get_grouped_counts_by_question(7, start_date, end_date, admin)
    grouped_domestic = get_grouped_counts_by_question(1, start_date, end_date, admin)
    grouped_bullying = get_grouped_counts_by_question(3, start_date, end_date, admin)

    # ========== ADD MISSING CHART DATA CALCULATIONS ==========
    
    # 1. Age Group Distribution by Gender
    def get_age_group_distribution(start_date, end_date):
        """Get age group distribution for male and female"""
        try:
            # Query to get all users with their age and sex
            users = db.session.query(User.age, User.sex).filter(
                User.age.between(10, 19),
                User.sex.in_(['Male', 'Female'])
            ).all()
            
            age_groups = {
                '10-14': {'Male': 0, 'Female': 0},
                '15-19': {'Male': 0, 'Female': 0}
            }
            
            for age, sex in users:
                if 10 <= age <= 14:
                    age_groups['10-14'][sex] += 1
                elif 15 <= age <= 19:
                    age_groups['15-19'][sex] += 1
            
            return age_groups
        except Exception as e:
            print(f"❌ Error in get_age_group_distribution: {e}")
            return {'10-14': {'Male': 0, 'Female': 0}, '15-19': {'Male': 0, 'Female': 0}}
    
    age_group_distribution = get_age_group_distribution(start_date, end_date)
    
    # 2. Rapid HEEADSSS Result Distribution
    def get_heeadsss_risk_distribution(start_date, end_date):
        """Get distribution of HEEADSSS risk levels"""
        try:
            # This is a simplified version - you might need to adjust based on your actual risk calculation logic
            low_risk = 0
            moderate_risk = 0
            high_risk = 0
            
            # Get all users who completed HEEADSSS assessment
            users_with_assessment = db.session.query(User.id).join(
                AssessmentResponse, User.id == AssessmentResponse.user_id
            ).distinct().all()
            
            user_ids = [user.id for user in users_with_assessment]
            
            # For each user, calculate risk based on their responses
            for user_id in user_ids:
                # Get all "yes" responses for this user
                yes_responses = db.session.query(UserResponse).filter(
                    UserResponse.user_id == user_id,
                    func.lower(UserResponse.response) == 'yes'
                ).count()
                
                # Simple risk calculation (adjust based on your criteria)
                if yes_responses == 0:
                    low_risk += 1
                elif yes_responses <= 2:
                    moderate_risk += 1
                else:
                    high_risk += 1
            
            return {
                'low_risk': low_risk,
                'moderate_risk': moderate_risk,
                'high_risk': high_risk
            }
        except Exception as e:
            print(f"❌ Error in get_heeadsss_risk_distribution: {e}")
            return {'low_risk': 0, 'moderate_risk': 0, 'high_risk': 0}
    
    heeadsss_risk_distribution = get_heeadsss_risk_distribution(start_date, end_date)
    
    # 3. Service Utilization by Type (for other charts that might be missing)
    def get_service_utilization(start_date, end_date):
        """Get count of each service type"""
        try:
            service_counts = {}
            
            # Get all distinct service names
            services = db.session.query(Services.service_name).filter(
                Services.timestamp.between(start_date, end_date)
            ).distinct().all()
            
            for service in services:
                service_name = service.service_name
                if service_name:
                    count = db.session.query(Services).filter(
                        Services.service_name == service_name,
                        Services.timestamp.between(start_date, end_date)
                    ).count()
                    service_counts[service_name] = count
            
            return service_counts
        except Exception as e:
            print(f"❌ Error in get_service_utilization: {e}")
            return {}
    
    service_utilization = get_service_utilization(start_date, end_date)

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        questions=questions,
        users=users,
        province_map=province_map,
        city_map=city_map,
        region_map=region_map,
        unread_responses=unread_responses,
        services=services,
        heeadsss_total=heeadsss_total,
        available_years=available_years,
        selected_year=int(selected_year),
        selected_month=selected_month,
        
        # Service counts
        adolescents_with_services=adolescents_with_services,
        referred_using_heeadsss_total=referred_using_heeadsss_total,
        male_referred_10_14=adolescents_with_services['male_10_14'],
        female_referred_10_14=adolescents_with_services['female_10_14'],
        male_referred_15_19=adolescents_with_services['male_15_19'],
        female_referred_15_19=adolescents_with_services['female_15_19'],
        
        # HYO counts
        hyo_total=hyo_total,
        male_hyo_10_14=hyo_counts['male_10_14'],
        female_hyo_10_14=hyo_counts['female_10_14'],
        male_hyo_15_19=hyo_counts['male_15_19'],
        female_hyo_15_19=hyo_counts['female_15_19'],
        
        # HEEADSSS counts
        male_heeadsss_10_14=heeadsss_counts['male_10_14'],
        female_heeadsss_10_14=heeadsss_counts['female_10_14'],
        male_heeadsss_15_19=heeadsss_counts['male_15_19'],
        female_heeadsss_15_19=heeadsss_counts['female_15_19'],
        
        # Question counts
        grouped_attempted_suicide=grouped_attempted_suicide,
        male_attempted_10_14=grouped_attempted_suicide["10-14"]["Male"],
        female_attempted_10_14=grouped_attempted_suicide["10-14"]["Female"],
        male_attempted_15_19=grouped_attempted_suicide["15-19"]["Male"],
        female_attempted_15_19=grouped_attempted_suicide["15-19"]["Female"],
        total_attempted_suicide_overall=grouped_attempted_suicide["10-14"]["Male"] + grouped_attempted_suicide["10-14"]["Female"] + grouped_attempted_suicide["15-19"]["Male"] + grouped_attempted_suicide["15-19"]["Female"],
        
        grouped_sexual_violence=grouped_sexual_violence,
        male_sv_10_14=grouped_sexual_violence["10-14"]["Male"],
        female_sv_10_14=grouped_sexual_violence["10-14"]["Female"],
        male_sv_15_19=grouped_sexual_violence["15-19"]["Male"],
        female_sv_15_19=grouped_sexual_violence["15-19"]["Female"],
        total_sv_overall=grouped_sexual_violence["10-14"]["Male"] + grouped_sexual_violence["10-14"]["Female"] + grouped_sexual_violence["15-19"]["Male"] + grouped_sexual_violence["15-19"]["Female"],

        grouped_binge=grouped_binge,
        male_binge_10_14=grouped_binge["10-14"]["Male"],
        female_binge_10_14=grouped_binge["10-14"]["Female"],
        male_binge_15_19=grouped_binge["15-19"]["Male"],
        female_binge_15_19=grouped_binge["15-19"]["Female"],
        total_binge_overall=grouped_binge["10-14"]["Male"] + grouped_binge["10-14"]["Female"] + grouped_binge["15-19"]["Male"] + grouped_binge["15-19"]["Female"],

        grouped_tobacco=grouped_tobacco,
        male_tobacco_10_14=grouped_tobacco["10-14"]["Male"],
        female_tobacco_10_14=grouped_tobacco["10-14"]["Female"],
        male_tobacco_15_19=grouped_tobacco["15-19"]["Male"],
        female_tobacco_15_19=grouped_tobacco["15-19"]["Female"],
        total_tobacco_overall=grouped_tobacco["10-14"]["Male"] + grouped_tobacco["10-14"]["Female"] + grouped_tobacco["15-19"]["Male"] + grouped_tobacco["15-19"]["Female"],

        grouped_drugs=grouped_drugs,
        male_drugs_10_14=grouped_drugs["10-14"]["Male"],
        female_drugs_10_14=grouped_drugs["10-14"]["Female"],
        male_drugs_15_19=grouped_drugs["15-19"]["Male"],
        female_drugs_15_19=grouped_drugs["15-19"]["Female"],
        total_drugs_overall=grouped_drugs["10-14"]["Male"] + grouped_drugs["10-14"]["Female"] + grouped_drugs["15-19"]["Male"] + grouped_drugs["15-19"]["Female"],
        
        grouped_domestic=grouped_domestic,
        male_domestic_10_14=grouped_domestic["10-14"]["Male"],
        female_domestic_10_14=grouped_domestic["10-14"]["Female"],
        male_domestic_15_19=grouped_domestic["15-19"]["Male"],
        female_domestic_15_19=grouped_domestic["15-19"]["Female"],
        total_domestic_overall=grouped_domestic["10-14"]["Male"] + grouped_domestic["10-14"]["Female"] + grouped_domestic["15-19"]["Male"] + grouped_domestic["15-19"]["Female"],
        
        grouped_bullying=grouped_bullying,
        male_bullying_10_14=grouped_bullying["10-14"]["Male"],
        female_bullying_10_14=grouped_bullying["10-14"]["Female"],
        male_bullying_15_19=grouped_bullying["15-19"]["Male"],
        female_bullying_15_19=grouped_bullying["15-19"]["Female"],
        total_bullying_overall=grouped_bullying["10-14"]["Male"] + grouped_bullying["10-14"]["Female"] + grouped_bullying["15-19"]["Male"] + grouped_bullying["15-19"]["Female"],
        
        # ========== ADD THE NEW CHART DATA ==========
        age_group_distribution=age_group_distribution,
        heeadsss_risk_distribution=heeadsss_risk_distribution,
        service_utilization=service_utilization,
        
        # Age group distribution specific values for easier access in template
        male_10_14_age=age_group_distribution['10-14']['Male'],
        female_10_14_age=age_group_distribution['10-14']['Female'],
        male_15_19_age=age_group_distribution['15-19']['Male'],
        female_15_19_age=age_group_distribution['15-19']['Female'],
        
        # Risk distribution specific values
        low_risk=heeadsss_risk_distribution['low_risk'],
        moderate_risk=heeadsss_risk_distribution['moderate_risk'],
        high_risk=heeadsss_risk_distribution['high_risk'],
    )
@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user and all associated data"""
    if 'admin' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    try:
        # Find the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        print(f"🗑️ Deleting user {user_id}: {user.first_name} {user.last_name}")
        
        # Start transaction
        db.session.begin_nested()
        
        # Delete associated records in the correct order to avoid foreign key constraints
        
        # 1. Delete services
        services_deleted = Services.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {services_deleted} services")
        
        # 2. Delete recommendations
        recommendations_deleted = Recommendations.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {recommendations_deleted} recommendations")
        
        # 3. Delete user responses
        responses_deleted = UserResponse.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {responses_deleted} user responses")
        
        # 4. Delete assessment responses
        assessment_responses_deleted = AssessmentResponse.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {assessment_responses_deleted} assessment responses")
        
        # 5. Delete referral history
        referrals_deleted = ReferralHistory.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {referrals_deleted} referral history records")
        
        # 6. Delete notifications
        notifications_deleted = Notification.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {notifications_deleted} notifications")
        
        # 7. Delete signatures
        signatures_deleted = Signature.query.filter_by(user_id=user_id).delete()
        print(f"✅ Deleted {signatures_deleted} signatures")
        
        # 8. Finally delete the user
        db.session.delete(user)
        
        # Commit all changes
        db.session.commit()
        
        print(f"✅ Successfully deleted user {user_id}")
        
        return jsonify({
            'success': True, 
            'message': f'User {user.first_name} {user.last_name} deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error deleting user {user_id}: {e}")
        return jsonify({
            'success': False, 
            'error': f'Failed to delete user: {str(e)}'
        }), 500
    
@app.route('/get_notifications')
def get_notifications():
    """Get unread notifications for the current admin"""
    if 'admin' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        admin = Admin.query.filter_by(username=session['admin']).first()
        if not admin:
            return jsonify({'error': 'Admin not found'}), 404
        
        # Get unread notifications
        notifications = Notification.query.filter_by(unread=True).order_by(Notification.timestamp.desc()).limit(10).all()
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'message': notification.message,
                'urgency': notification.urgency,
                'timestamp': notification.timestamp.isoformat() if notification.timestamp else None,
                'center_name': notification.center_name
            })
        
        # Get count of unread notifications
        unread_count = Notification.query.filter_by(unread=True).count()
        
        return jsonify({
            'success': True,
            'notifications': notifications_data,
            'unread_count': unread_count
        })
        
    except Exception as e:
        print(f"❌ Error fetching notifications: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'notifications': [],
            'unread_count': 0
        }), 500
@app.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    if 'admin' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        notification = Notification.query.get(notification_id)
        if notification:
            notification.unread = False
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error marking notification as read: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/mark_all_notifications_read', methods=['POST'])
def mark_all_notifications_read():
    """Mark all notifications as read"""
    if 'admin' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        notifications = Notification.query.filter_by(unread=True).all()
        for notification in notifications:
            notification.unread = False
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'Marked {len(notifications)} notifications as read'})
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error marking all notifications as read: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/debug_notifications')
def debug_notifications():
    """Debug route to check notifications data"""
    if 'admin' not in session:
        return "Not logged in"
    
    notifications_count = Notification.query.count()
    unread_count = Notification.query.filter_by(unread=True).count()
    
    return jsonify({
        'total_notifications': notifications_count,
        'unread_notifications': unread_count,
        'all_notifications': [{
            'id': n.id,
            'message': n.message,
            'unread': n.unread,
            'timestamp': n.timestamp.isoformat() if n.timestamp else None
        } for n in Notification.query.limit(5).all()]
    })
@app.route('/create_test_notification')
def create_test_notification():
    """Create a test notification (for testing purposes)"""
    if 'admin' not in session:
        return "Not logged in"
    
    try:
        test_notification = Notification(
            message="This is a test notification",
            urgency="info",
            center_name="Test Center",
            unread=True
        )
        db.session.add(test_notification)
        db.session.commit()
        return "Test notification created successfully"
    except Exception as e:
        return f"Error creating test notification: {e}"

@app.route('/debug_chart_data')
def debug_chart_data():
    """Debug endpoint to check chart data"""
    if 'admin' not in session:
        return jsonify({'error': 'Not logged in'})
    
    selected_year = request.args.get('year', str(datetime.now().year))
    start_date = f"{selected_year}-01-01"
    end_date = f"{selected_year}-12-31"
    
    age_group_data = get_age_group_distribution(start_date, end_date)
    risk_data = get_heeadsss_risk_distribution(start_date, end_date)
    
    return jsonify({
        'age_group_distribution': age_group_data,
        'risk_distribution': risk_data,
        'debug_info': {
            'age_group_keys': list(age_group_data.keys()),
            'risk_keys': list(risk_data.keys())
        }
    })

@app.route('/admin/list')
def admin_list():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    # Refresh admin data
    db.session.refresh(admin)

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # SIMPLIFIED: Show all users first to test
    users_query = User.query.filter(
        User.control_num.isnot(None),
        User.control_num != ''
    )

    # Debug: Print the query and count
    print(f"🔍 Users query count: {users_query.count()}")
    
    users_pagination = users_query.paginate(page=page, per_page=per_page)
    users = users_pagination.items

    # Debug: Print the users found
    print(f"🔍 Found {len(users)} users on page {page}")
    for user in users:
        print(f"  - User {user.id}: {user.control_num}, {user.first_name} {user.last_name}")

    # Refresh each user to ensure fresh data
    for user in users:
        db.session.refresh(user)

    # Initialize progress and highlighting dictionaries
    user_progress = {}
    highlighted_users = {}
    highlighted_users_yellow = {}

    for user in users:
        # Match source based on admin's center
        has_services = db.session.query(Services).filter_by(
            user_id=user.id,
            services_saved=True
            # Removed source filter for now
        ).first() is not None

        has_recommendations = db.session.query(Recommendations).filter_by(
            user_id=user.id,
            recommendation_saved=True
            # Removed source filter for now
        ).first() is not None

        user_progress[user.id] = has_services and has_recommendations

        # Highlighting logic
        questions_with_answers = get_questions_and_answers(user.id)
        yes_answers = {int(q_id) for q_id, data in questions_with_answers.items() if data["answer"].strip().lower() == "yes"}

        if 1 in yes_answers or 4 in yes_answers or 10 in yes_answers:
            highlighted_users[user.id] = True
        if any(q not in [1, 4, 10] and q in yes_answers for q in yes_answers):
            highlighted_users_yellow[user.id] = True

    unread_responses = UserResponse.query.filter_by(is_read=False).count()

    return render_template(
        'admin_list.html',
        admin=admin,
        users=users,
        user_progress=user_progress,
        highlighted_users=highlighted_users,
        highlighted_users_yellow=highlighted_users_yellow,
        unread_responses=unread_responses,
        pagination=users_pagination
    )

@app.route('/view-client/<int:user_id>')
def view_client(user_id):
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    # Use filter with refresh to ensure fresh data
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_list'))
    
    # Refresh user data
    db.session.refresh(user)
    
    # Get fresh services and recommendations
    user_services = db.session.query(Services).filter_by(user_id=user_id).all()
    user_recommendations = db.session.query(Recommendations).filter_by(user_id=user_id).all()
    
    # Refresh each service and recommendation
    for service in user_services:
        db.session.refresh(service)
    for recommendation in user_recommendations:
        db.session.refresh(recommendation)
    
    print(f"🔍 Debug - Found {len(user_services)} services and {len(user_recommendations)} recommendations")

    saved_services = [service.service_name for service in user_services]
    saved_recommendations = [rec.recommendation_text for rec in user_recommendations]

    # Get questions and answers
    questions_with_answers = get_questions_and_answers(user_id)

    return render_template(
        'view_client.html', 
        admin=admin,
        user=user, 
        questions_with_answers=questions_with_answers,
        saved_services=saved_services,
        saved_recommendations=saved_recommendations
    )

@app.route('/save_services', methods=['POST'])
def save_services():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        user_id = data.get('user_id')
        services = data.get('services', [])
        recommendations = data.get('recommendations', [])
        follow_up_datetime = data.get('follow_up_datetime')
        recommended_follow_up_datetime = data.get('recommended_follow_up_datetime')
        other_service_detail = data.get('other_service_detail', '').strip()
        other_recommendation_detail = data.get('other_recommendation_detail', '').strip()

        print(f"🔍 Debug - Received data: user_id={user_id}, services={services}, recommendations={recommendations}")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        source = session.get('source', 'unknown')

        # Start transaction
        db.session.begin_nested()

        # Clear existing entries for this source
        deleted_services = Services.query.filter_by(user_id=user_id, source=source).delete()
        deleted_recommendations = Recommendations.query.filter_by(user_id=user_id, source=source).delete()
        
        print(f"🗑️ Deleted {deleted_services} services and {deleted_recommendations} recommendations")

        # Save services
        saved_services = []
        for service in services:
            if service == "Other":
                new_service = Services(
                    service_name="Other",
                    service_detail=other_service_detail,
                    user_id=user_id,
                    services_saved=True,
                    source=source
                )
            else:
                new_service = Services(
                    service_name=service,
                    service_detail="",
                    user_id=user_id,
                    services_saved=True,
                    source=source
                )
            db.session.add(new_service)
            saved_services.append(new_service)
            print(f"✅ Added service: {service}")

        # Save recommendations
        saved_recommendations = []
        for recommendation in recommendations:
            if recommendation == "Other":
                new_recommendation = Recommendations(
                    recommendation_text=other_recommendation_detail,
                    user_id=user_id,
                    recommendation_saved=True,
                    source=source
                )
            else:
                new_recommendation = Recommendations(
                    recommendation_text=recommendation,
                    user_id=user_id,
                    recommendation_saved=True,
                    source=source
                )
            db.session.add(new_recommendation)
            saved_recommendations.append(new_recommendation)
            print(f"✅ Added recommendation: {recommendation}")

        # Commit all changes
        db.session.commit()
        print("✅ All changes committed successfully")
        
        # Refresh the entities to get their IDs
        for service in saved_services:
            db.session.refresh(service)
        for recommendation in saved_recommendations:
            db.session.refresh(recommendation)
        
        return jsonify({
            "status": "success", 
            "message": "Services and recommendations saved successfully",
            "services_count": len(saved_services),
            "recommendations_count": len(saved_recommendations)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error saving services: {e}")
        return jsonify({"error": f"Failed to save: {str(e)}"}), 500

# ========== ADD MISSING ROUTES ==========

@app.route('/admin/messages')
def admin_messages():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    return render_template('admin_messages.html', admin=admin)

@app.route('/admin/profile')
def admin_profile():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    return render_template('admin_profile.html', admin=admin)

@app.route('/admin/settings')
def admin_settings():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    return render_template('admin_settings.html', admin=admin)

@app.route('/admin/files')
def admin_files():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    return render_template('admin_files.html', admin=admin)

@app.route('/admin/results')
def admin_results():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    return render_template('admin_results.html', admin=admin)

@app.route('/admin/edit_profile', methods=['GET', 'POST'])
def edit_admin_profile():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    if request.method == 'POST':
        # Update profile logic here
        if request.form.get('username'):
            admin.username = request.form['username']
        if request.form.get('email'):
            admin.email = request.form['email']
        if request.form.get('centerName'):
            admin.center_name = request.form['centerName']
        if request.form.get('position'):
            admin.position = request.form['position']
        if request.form.get('phone'):
            admin.phone = request.form['phone']
        if request.form.get('address'):
            admin.address = request.form['address']
        
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                filename = f"{uuid.uuid4().hex}_{file.filename}"
                upload_path = os.path.join('static/uploads', filename)
                file.save(upload_path)
                admin.profile_image = f'/static/uploads/{filename}'

        if request.form.get('password'):
            admin.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        db.session.commit()

        # Update the session if username changed
        if request.form.get('username'):
            session['admin'] = admin.username

        return redirect(url_for('admin_profile'))

    return render_template('edit_admin_profile.html', admin=admin)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

# Public routes
@app.route('/instructions')
def instructions(): 
    return render_template("instructions.html")

@app.route('/personal/information', methods=['GET', 'POST'])
def personal_info():
    user_data = None

    if request.method == 'POST':
        try:
            control_num = request.form.get('control_num')
            
            if control_num:
                user_data = User.query.filter_by(control_num=control_num).first()
                
                if user_data:
                    if user_data.reason not in [None, ""]:
                        flash("This control number has already been used.", "warning")
                        return redirect(url_for('personal_info'))
                    
                    session['user_id'] = user_data.id

                    reason = request.form.get('reason')
                    
                    if reason:
                        user_data.reason = reason
                        db.session.commit()

                    return redirect(url_for('headsss'))
  
        except Exception as e:
            print(f"❌ Error processing form: {e}")
            flash("An error occurred. Please try again.", "danger")

    return render_template("personal_info.html", user=user_data)

@app.route('/headsss-assessment', methods=['GET', 'POST'])
def headsss():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('personal_info'))

    existing_responses = db.session.query(AssessmentResponse).filter_by(user_id=user_id).count()

    if existing_responses == 0:
        session['current_assessment_number'] = 1
    elif 'current_assessment_number' not in session:
        session['current_assessment_number'] = 1
    
    current_assessment_number = session['current_assessment_number']

    total_assessment = db.session.query(Assessment).count()

    if current_assessment_number > total_assessment:
        session['current_assessment_number'] = 1
        current_assessment_number = 1

    assessment = db.session.query(Assessment).filter_by(id=current_assessment_number).first()

    if not assessment:
        return redirect(url_for('thank_you'))

    is_last_question = current_assessment_number == total_assessment

    if request.method == 'POST':
        if 'back' in request.form:
            session['current_assessment_number'] = max(1, current_assessment_number - 1)
            return redirect(url_for('headsss'))

        response = request.form.get(f'q{current_assessment_number}')

        if response:
            existing_response = db.session.query(AssessmentResponse).filter_by(
                user_id=user_id, assessment_number=current_assessment_number
            ).first()

            if existing_response:
                existing_response.response = response
            else:
                new_response = AssessmentResponse(user_id=user_id, assessment_number=current_assessment_number, response=response)
                db.session.add(new_response)

            db.session.commit()

        if not is_last_question:
            session['current_assessment_number'] += 1
            return redirect(url_for('headsss'))
        else:
            return redirect(url_for('thank_you'))

    return render_template('questionnaire.html', assessment=assessment, is_last_question=is_last_question)

@app.route('/thank-you', methods=['GET', 'POST'])
def thank_you():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('headsss'))
    
    if request.method == 'POST' and 'confirm_submit' in request.form:
        return redirect(url_for('submission_complete'))

    responses = db.session.query(AssessmentResponse).filter_by(user_id=user_id).all()

    if not responses:
        return render_template('thankyou.html', assessment=[], page=1, total_pages=1)

    assessment_data = db.session.query(Assessment).filter(Assessment.id.in_([r.assessment_number for r in responses])).all()

    response_dict = {str(r.assessment_number): r.response for r in responses}

    grouped_assessments = defaultdict(list)
    for assessment in assessment_data:
        grouped_assessments[assessment.category].append({
            "assessment": assessment.assessment_text,
            "answer": response_dict.get(str(assessment.id), "No Answer"),
            "is_category": False
        })

    all_assessments = []
    for category, items in grouped_assessments.items():
        all_assessments.append({"category": category, "is_category": True})
        all_assessments.extend(items)

    page = request.args.get('page', 1, type=int)
    assessments_per_page = 22

    total_assessments = len(all_assessments)
    total_pages = max((total_assessments + assessments_per_page - 1) // assessments_per_page, 1)

    start_index = (page - 1) * assessments_per_page
    end_index = min(start_index + assessments_per_page, total_assessments)

    paginated_assessments = all_assessments[start_index:end_index]

    return render_template('thankyou.html', 
                           assessment=paginated_assessments, 
                           page=page, 
                           total_pages=total_pages)

@app.route('/submission_complete')
def submission_complete():
    return render_template('submission_complete.html')

# ... all your other routes and code ...
@app.route('/debug_dashboard_data')
def debug_dashboard_data():
    if 'admin' not in session:
        return "Not logged in"
    
    selected_year = request.args.get('year', str(datetime.now().year))
    selected_month = request.args.get('month', 'all')
    
    # Test the data functions
    test_counts = get_gender_age_counts('Assessed using HEEADSSS', f"{selected_year}-01-01", f"{selected_year}-12-31")
    test_questions = get_grouped_counts_by_question(4, f"{selected_year}-01-01", f"{selected_year}-12-31", None)
    
    return jsonify({
        'service_counts': test_counts,
        'question_counts': test_questions,
        'year': selected_year,
        'month': selected_month
    })

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    """Custom filter to format datetime objects and date strings"""
    if value is None:
        return "N/A"
    
    try:
        # If it's already a datetime object
        if isinstance(value, datetime):
            return value.strftime(format)
        
        # If it's a date object (but not datetime)
        if isinstance(value, date) and not isinstance(value, datetime):
            return value.strftime(format)
        
        # If it's a string, try to parse it
        if isinstance(value, str):
            # Try different date formats
            for date_format in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S.%f']:
                try:
                    # Try parsing as datetime first
                    date_obj = datetime.strptime(value, date_format)
                    return date_obj.strftime(format)
                except ValueError:
                    continue
            
            # If none of the formats work, return the original string
            return value
        
        # For any other type, convert to string
        return str(value)
        
    except (ValueError, TypeError, AttributeError) as e:
        print(f"Error formatting date: {e}, value: {value}, type: {type(value)}")
        return str(value) if value else "N/A"
# Add these debug routes after your existing routes

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5005, debug=True)