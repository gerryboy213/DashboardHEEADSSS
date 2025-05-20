from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import distinct, and_, desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from sqlalchemy import or_, func
from sqlalchemy import extract
import json
import os
import uuid
import mysql.connector
import re
from datetime import datetime
from collections import defaultdict


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'form_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Add this to fetch results as dictionaries

# Database Configuration (Update your MySQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/form_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Folder to save uploaded signatures
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions (optional but recommended)
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
    age = db.Column(db.String, nullable=False)  # Calculated automatically
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
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    responses = db.relationship(
        'UserResponse',
        backref='user',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
       
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
    response = db.Column(db.String(10), nullable=False)  # 'Yes' or 'No'
    is_read = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class AssessmentResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Link to the user
    assessment_number = db.Column(db.Integer, nullable=False)
    response = db.Column(db.String(10), nullable=False)  # 'Yes' or 'No'
    
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
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)  # New field for profile image
    
class Services(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    services_saved = db.Column(db.Boolean, default=False)
    service_detail = db.Column(db.String(255), nullable=False, default='')
    user_id = db.Column(db.Integer, nullable=False)  # Link to the user

class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recommendation_text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=False)
    recommendation_saved = db.Column(db.Boolean, default=False)  # ✅ Add this


class Signature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    
@app.route('/get_yes_no_distribution', methods=['GET'])
def get_yes_no_distribution():
    if 'admin' not in session:
        return jsonify({"error": "Not authorized"}), 403

    admin = Admin.query.filter_by(username=session['admin']).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    # Define center codes mapping
    center_codes = {
        "BHS Union AFHF": ("0837", "01"),
        "RHU Mayorga": ("0837", "02"),
        "Gandara AFHF": ("0860", "02"),
        "RHU Gandara": ("0860", "03"),
        "RHU Pagsanghan": ("0860", "04"),
        "Abuyog District Hospital AFHF": ("0837", "04"),
        "Gandara District Hospital AFHF": ("0860", "05")
    }

    center_name = admin.center_name
    center_info = center_codes.get(center_name)

    if not center_info:
        return jsonify({"error": "Center not found"}), 404

    province_code, city_code = center_info

    # Load region, province, city JSON for mapping (same approach as before)
    json_files = {
        "region": "region.json",
        "province": "province.json",
        "city": "city.json"
    }

    json_data = {}
    try:
        for key, filename in json_files.items():
            path = os.path.join(current_app.root_path, 'static', 'ph-json', filename)
            with open(path, 'r', encoding='utf-8') as f:
                json_data[key] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": f"Error loading JSON data: {str(e)}"}), 500

    region_map = {item["region_code"]: item["region_name"] for item in json_data.get("region", [])}
    province_map = {item["province_code"]: item["province_name"] for item in json_data.get("province", [])}
    city_map = {item["city_code"]: item["city_name"] for item in json_data.get("city", [])}

    admin_region = admin.region
    admin_province = admin.province
    admin_city = admin.city

    year = request.args.get('year')
    month = request.args.get('month')

    # Subquery to get the latest UserResponse per user per question
    latest_responses_subquery = db.session.query(
        UserResponse.user_id,
        UserResponse.question_number,
        func.max(UserResponse.id).label('max_id')
    ).group_by(
        UserResponse.user_id,
        UserResponse.question_number
    ).subquery()

    # Main query with center code-based filtering (based on control_num prefix)
    query = db.session.query(
        UserResponse.question_number,
        UserResponse.response,
        func.count(UserResponse.response)
    ).join(
        latest_responses_subquery,
        UserResponse.id == latest_responses_subquery.c.max_id
    ).join(
        User, User.id == UserResponse.user_id
    ).filter(
        User.control_num.isnot(None),
        User.control_num != '',
        User.control_num.like(f"{province_code}-{city_code}-%"),  # Filter by control number prefix
    )

    # Optional filters by year and month
    if year and year != 'all':
        query = query.filter(extract('year', UserResponse.submitted_at) == int(year))
    if month and month != 'all':
        query = query.filter(extract('month', UserResponse.submitted_at) == int(month))

    latest_responses = query.group_by(
        UserResponse.question_number,
        UserResponse.response
    ).all()

    expected_question_numbers = range(1, 12)
    yes_no_data = {q_num: {"Yes": 0, "No": 0} for q_num in expected_question_numbers}

    # Accumulate "Yes" and "No" responses per question number
    for question_number, response, count in latest_responses:
        if question_number not in yes_no_data:
            yes_no_data[question_number] = {"Yes": 0, "No": 0}

        normalized_response = response.strip().lower()
        if normalized_response == "yes":
            yes_no_data[question_number]["Yes"] += count
        elif normalized_response == "no":
            yes_no_data[question_number]["No"] += count

    return jsonify(yes_no_data)


    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/login')
def admin():
    return render_template('admin_login.html')

@app.route('/admin/signup')
def admin_signup_page():
    return render_template('admin_signup.html')


@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
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

    return render_template('admin_signup.html')

# Admin Login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin_data = Admin.query.filter_by(username=username).first()

        if admin_data and check_password_hash(admin_data.password, password):

            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Try again.', 'danger')
            return redirect(url_for('admin_login'))
        
def get_grouped_counts_by_question(question_number, start_date, end_date, admin):
    # Initialize the grouped counts dictionary
    grouped_counts = {
        "10-14": {"Male": 0, "Female": 0},
        "15-19": {"Male": 0, "Female": 0}
    }

    # Define the center codes mapping
    center_codes = {
        "BHS Union AFHF": ("0837", "01"),
        "RHU Mayorga": ("0837", "02"),
        "Gandara AFHF": ("0860", "02"),
        "RHU Gandara": ("0860", "03"),
        "RHU Pagsanghan": ("0860", "04"),
        "Abuyog District Hospital AFHF": ("0837", "04"),
        "Gandara District Hospital AFHF": ("0860", "05")
    }

    # Get the province and city codes from the admin's center
    center_name = admin.center_name
    center_info = center_codes.get(center_name)

    if not center_info:
        return {"error": "Center not found"}

    province_code, city_code = center_info

    # Query to get the grouped counts by question number, filtering by center code
    query = db.session.query(User.age, User.sex).join(
        UserResponse, User.id == UserResponse.user_id
    ).filter(
        UserResponse.question_number == question_number,
        func.lower(func.trim(UserResponse.response)) == 'yes',  # Only 'Yes' responses
        User.control_num.isnot(None),
        func.trim(User.control_num) != '',
        UserResponse.submitted_at.between(start_date, end_date),
        User.control_num.like(f"{province_code}-{city_code}-%")  # Center code filter
    ).all()

    # Process the query results
    for age, sex in query:
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




@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    services = Services.query.all()
    questions = Questions.query.all()
    users = User.query.all()

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

    # Get unread user responses
    unread_responses = UserResponse.query.filter_by(is_read=False).count()
    
    
    # Attempted suicide (Q4)
    grouped_attempted_suicide = get_grouped_counts_by_question(4, start_date, end_date, admin)
    male_attempted_10_14 = grouped_attempted_suicide["10-14"]["Male"]
    female_attempted_10_14 = grouped_attempted_suicide["10-14"]["Female"]
    male_attempted_15_19 = grouped_attempted_suicide["15-19"]["Male"]
    female_attempted_15_19 = grouped_attempted_suicide["15-19"]["Female"]
    
    total_attempted_suicide_10_14 = male_attempted_10_14 + female_attempted_10_14
    total_attempted_suicide_15_19 = male_attempted_15_19 + female_attempted_15_19
    total_attempted_suicide_overall = total_attempted_suicide_10_14 + total_attempted_suicide_15_19

    # Sexual violence (Q10)
    grouped_sexual_violence = get_grouped_counts_by_question(10, start_date, end_date, admin)
    male_sv_10_14 = grouped_sexual_violence["10-14"]["Male"]
    female_sv_10_14 = grouped_sexual_violence["10-14"]["Female"]
    male_sv_15_19 = grouped_sexual_violence["15-19"]["Male"]
    female_sv_15_19 = grouped_sexual_violence["15-19"]["Female"]
    
    total_sv_10_14 = male_sv_10_14 + female_sv_10_14
    total_sv_15_19 = male_sv_15_19 + female_sv_15_19
    total_sv_overall = total_sv_10_14 + total_sv_15_19

    # Binge drinking (Q6)
    grouped_binge = get_grouped_counts_by_question(6, start_date, end_date, admin)
    male_binge_10_14 = grouped_binge["10-14"]["Male"]
    female_binge_10_14 = grouped_binge["10-14"]["Female"]
    male_binge_15_19 = grouped_binge["15-19"]["Male"]
    female_binge_15_19 = grouped_binge["15-19"]["Female"]
    
    total_binge_10_14 = male_binge_10_14 + female_binge_10_14
    total_binge_15_19 = male_binge_15_19 + female_binge_15_19
    total_binge_overall = total_binge_10_14 + total_binge_15_19

    # Tobacco use (Q5)
    grouped_tobacco = get_grouped_counts_by_question(5, start_date, end_date, admin)
    male_tobacco_10_14 = grouped_tobacco["10-14"]["Male"]
    female_tobacco_10_14 = grouped_tobacco["10-14"]["Female"]
    male_tobacco_15_19 = grouped_tobacco["15-19"]["Male"]
    female_tobacco_15_19 = grouped_tobacco["15-19"]["Female"]
    
    total_tobacco_10_14 = male_tobacco_10_14 + female_tobacco_10_14
    total_tobacco_15_19 = male_tobacco_15_19 + female_tobacco_15_19
    total_tobacco_overall = total_tobacco_10_14 + total_tobacco_15_19

    # Drug use (Q7)
    grouped_drugs = get_grouped_counts_by_question(7, start_date, end_date, admin)
    male_drugs_10_14 = grouped_drugs["10-14"]["Male"]
    female_drugs_10_14 = grouped_drugs["10-14"]["Female"]
    male_drugs_15_19 = grouped_drugs["15-19"]["Male"]
    female_drugs_15_19 = grouped_drugs["15-19"]["Female"]
    
    total_drugs_10_14 = male_drugs_10_14 + female_drugs_10_14
    total_drugs_15_19 = male_drugs_15_19 + female_drugs_15_19
    total_drugs_overall = total_drugs_10_14 + total_drugs_15_19

    # Domestic Violence (Q1)
    grouped_domestic = get_grouped_counts_by_question(1, start_date, end_date, admin)
    male_domestic_10_14 = grouped_domestic["10-14"]["Male"]
    female_domestic_10_14 = grouped_domestic["10-14"]["Female"]
    male_domestic_15_19 = grouped_domestic["15-19"]["Male"]
    female_domestic_15_19 = grouped_domestic["15-19"]["Female"]
    
    total_domestic_10_14 = male_domestic_10_14 + female_domestic_10_14
    total_domestic_15_19 = male_domestic_15_19 + female_domestic_15_19
    total_domestic_overall = total_domestic_10_14 + total_domestic_15_19
    
    # Bullying (Q3)
    grouped_bullying = get_grouped_counts_by_question(3, start_date, end_date, admin)
    male_bullying_10_14 = grouped_bullying ["10-14"]["Male"]
    female_bullying_10_14 = grouped_bullying["10-14"]["Female"]
    male_bullying_15_19 = grouped_bullying["15-19"]["Male"]
    female_bullying_15_19 = grouped_bullying["15-19"]["Female"]
    
    total_bullying_10_14 = male_bullying_10_14 + female_bullying_10_14
    total_bullying_15_19 = male_bullying_15_19 + female_bullying_15_19
    total_bullying_overall = total_bullying_10_14 + total_bullying_15_19
    
    # Users who submitted responses in the admin’s area
    responded_users_subquery = db.session.query(UserResponse.user_id).select_from(UserResponse).join(
        User, UserResponse.user_id == User.id
        
    ).filter(
        func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name)),
    ).distinct().subquery()

    # Assessed users from your services table
    assessed_users_subquery = db.session.query(Services.user_id).distinct().subquery()

    # Pending = those who responded but haven't been assessed yet
    pending_review_count = db.session.query(User).filter(
        User.control_num.isnot(None),
        User.control_num != '',
        User.id.in_(responded_users_subquery),
        ~User.id.in_(assessed_users_subquery)
    ).count()

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
        return f"Error: {str(e)}", 500  # Provide the actual error message for debugging

    # Initialize the region_map, province_map, and city_map from JSON data
    region_map = {item["region_code"]: item["region_name"] for item in json_data.get("region", [])}
    province_map = {item["province_code"]: item["province_name"] for item in json_data.get("province", [])}
    city_map = {item["city_code"]: item["city_name"] for item in json_data.get("city", [])}

    # Get the region, province, and city of the admin
    admin_region = admin.region
    admin_province = admin.province
    admin_city = admin.city

    def get_gender_age_counts(service_name, start_date, end_date, admin_region, admin_province, admin_city):
        counts = {
            'male_10_14': 0,
            'male_15_19': 0,
            'female_10_14': 0,
            'female_15_19': 0,
        }

        # Base filters
        filters = [
            Services.timestamp.between(start_date, end_date),
            User.age.isnot(None),
            or_(
                func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name)),
               
            ),
            User.age.between(10, 19),
            Services.service_name.isnot(None),  # Ensure accessed service
            Services.service_name != ''
        ]

        # Only add service_name filter if not counting 'Any Service Accessed'
        if service_name != 'Any Service Accessed':
            filters.append(Services.service_name == service_name)

        # Choose what to COUNT
        if service_name == 'Any Service Accessed':
            count_expression = func.count(func.distinct(User.id))  # <-- COUNT DISTINCT USERS
        else:
            count_expression = func.count(Services.id)  # Normal count per service

        query_results = (
            db.session.query(User.sex, User.age, count_expression)
            .select_from(Services)
            .join(User, Services.user_id == User.id)
            .filter(*filters)
            .group_by(User.sex, User.age)
            .all()
        )

        for sex, age, count in query_results:
            key = None
            if sex == 'Male':
                if 10 <= age <= 14:
                    key = 'male_10_14'
                elif 15 <= age <= 19:
                    key = 'male_15_19'
            elif sex == 'Female':
                if 10 <= age <= 14:
                    key = 'female_10_14'
                elif 15 <= age <= 19:
                    key = 'female_15_19'

            if key:
                counts[key] += count

        return counts



    # Get counts for adolescents assessed using HEEADSSS
    heeadsss_counts = get_gender_age_counts('Assessed using HEEADSSS', start_date, end_date, admin_region, admin_province, admin_city)
    heeadsss_total = sum(heeadsss_counts.values())

    # Assign counts individually (optional, if needed somewhere)
    male_heeadsss_10_14 = heeadsss_counts['male_10_14']
    female_heeadsss_10_14 = heeadsss_counts['female_10_14']
    male_heeadsss_15_19 = heeadsss_counts['male_15_19']
    female_heeadsss_15_19 = heeadsss_counts['female_15_19']

    # Get counts for adolescents reached by HYO
    hyo_counts = get_gender_age_counts('Reached by HYO', start_date, end_date, admin_region, admin_province, admin_city)
    hyo_total = sum(hyo_counts.values())

    # Assign counts individually (optional, if needed somewhere)
    male_hyo_10_14 = hyo_counts['male_10_14']
    female_hyo_10_14 = hyo_counts['female_10_14']
    male_hyo_15_19 = hyo_counts['male_15_19']
    female_hyo_15_19 = hyo_counts['female_15_19']

    # Get counts for adolescents referred using HEEADSSS and accessed services
    adolescents_with_services = get_gender_age_counts(
        'Any Service Accessed',  
        start_date,
        end_date,
        admin_region,
        admin_province,
        admin_city
    )

    referred_using_heeadsss_total = sum(adolescents_with_services.values())

    # Assign counts individually
    male_referred_10_14 = adolescents_with_services['male_10_14']
    female_referred_10_14 = adolescents_with_services['female_10_14']
    male_referred_15_19 = adolescents_with_services['male_15_19']
    female_referred_15_19 = adolescents_with_services['female_15_19']

    matched_users = db.session.query(User.id).filter(
        Services.timestamp.between(start_date, end_date),
        or_(
            func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name)),
        ),
    ).subquery()
    
    hyo_yes_user_ids = db.session.query(Services.user_id).join(User, Services.user_id == User.id).filter(
        Services.service_name == 'Reached by HYO',
        Services.timestamp.between(start_date, end_date),
        or_(
            func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name)),
        ),
    ).subquery()
    
        # Count users who matched the admin's location but are not in the list above
    hyo_no_count = db.session.query(User).filter(
        User.id.in_(matched_users),
        ~User.id.in_(hyo_yes_user_ids)
    ).count()

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        questions=questions,
        users=users,
        province_map=province_map,
        city_map=city_map,
        unread_responses=unread_responses,
        services=services,
        heeadsss_total=heeadsss_total,
        available_years=available_years,
        selected_year=int(selected_year),
        selected_month=selected_month,
        
        pending_review_count=pending_review_count,
        
        adolescents_with_services=adolescents_with_services,
        referred_using_heeadsss_total=referred_using_heeadsss_total,
        male_referred_10_14=male_referred_10_14,
        female_referred_10_14=female_referred_10_14,
        male_referred_15_19=male_referred_15_19,
        female_referred_15_19=female_referred_15_19,
        
        # hyo count
        hyo_no_count=hyo_no_count,
        male_hyo_10_14=male_hyo_10_14,            # added
        female_hyo_10_14=female_hyo_10_14,        # added
        male_hyo_15_19=male_hyo_15_19,            
        female_hyo_15_19=female_hyo_15_19,
        hyo_total=hyo_total,
        
        # assessed using heeadsss
        male_heeadsss_10_14=male_heeadsss_10_14,
        female_heeadsss_10_14=female_heeadsss_10_14,
        male_heeadsss_15_19=male_heeadsss_15_19,
        female_heeadsss_15_19=female_heeadsss_15_19,
        
        grouped_attempted_suicide=grouped_attempted_suicide,
        male_attempted_10_14=male_attempted_10_14,
        female_attempted_10_14=female_attempted_10_14,
        male_attempted_15_19=male_attempted_15_19,
        female_attempted_15_19=female_attempted_15_19,
        total_attempted_suicide_overall=total_attempted_suicide_overall,
        
        grouped_sexual_violence=grouped_sexual_violence,
        male_sv_10_14=male_sv_10_14,
        female_sv_10_14=female_sv_10_14,
        male_sv_15_19=male_sv_15_19,
        female_sv_15_19=female_sv_15_19,
        total_sv_10_14=total_sv_10_14,
        total_sv_15_19=total_sv_15_19,
        total_sv_overall=total_sv_overall,

        grouped_binge=grouped_binge,
        male_binge_10_14=male_binge_10_14,
        female_binge_10_14=female_binge_10_14,
        male_binge_15_19=male_binge_15_19,
        female_binge_15_19=female_binge_15_19,
        total_binge_10_14=total_binge_10_14,
        total_binge_15_19=total_binge_15_19,
        total_binge_overall=total_binge_overall,

        grouped_tobacco=grouped_tobacco,
        male_tobacco_10_14=male_tobacco_10_14,
        female_tobacco_10_14=female_tobacco_10_14,
        male_tobacco_15_19=male_tobacco_15_19,
        female_tobacco_15_19=female_tobacco_15_19,
        total_tobacco_10_14=total_tobacco_10_14,
        total_tobacco_15_19=total_tobacco_15_19,
        total_tobacco_overall=total_tobacco_overall,

        grouped_drugs=grouped_drugs,
        male_drugs_10_14=male_drugs_10_14,
        female_drugs_10_14=female_drugs_10_14,
        male_drugs_15_19=male_drugs_15_19,
        female_drugs_15_19=female_drugs_15_19,
        total_drugs_10_14=total_drugs_10_14,
        total_drugs_15_19=total_drugs_15_19,
        total_drugs_overall=total_drugs_overall,
        
        grouped_domestic=grouped_domestic,
        male_domestic_10_14=male_domestic_10_14,
        female_domestic_10_14=female_domestic_10_14,
        male_domestic_15_19=male_domestic_15_19,
        female_domestic_15_19=female_domestic_15_19,
        total_domestic_10_14=total_domestic_10_14,
        total_domestic_15_19=total_domestic_15_19,
        total_domestic_overall=total_domestic_overall,
        
        grouped_bullying=grouped_bullying,
        male_bullying_10_14=male_bullying_10_14,
        female_bullying_10_14=female_bullying_10_14,
        male_bullying_15_19=male_bullying_15_19,
        female_bullying_15_19=female_bullying_15_19,
        total_bullying_10_14=total_bullying_10_14,
        total_bullying_15_19=total_domestic_15_19,
        total_bullying_overall=total_bullying_overall,

    )   



@app.route('/admin/list')
def admin_list():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Load JSON files (optional, used for location display maybe)
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

    # Center code mapping
    center_codes = {
        "BHS Union AFHF": ("0837", "01"),
        "RHU Mayorga": ("0837", "02"),
        "Gandara AFHF": ("0860", "02"),
        "RHU Gandara": ("0860", "03"),
        "RHU Pagsanghan": ("0860", "04"),
        "Abuyog District Hospital AFHF": ("0837", "04"),
        "Gandara District Hospital AFHF": ("0860", "05")
    }

    # Get province and city codes for center
    center_info = center_codes.get(admin.center_name)
    if not center_info:
        flash('Center not found in center codes.', 'danger')
        return redirect(url_for('admin'))

    province_code, city_code = center_info

    # Filter users by control number matching center code
    users_query = User.query.filter(
        User.control_num.isnot(None),
        User.control_num != '',
        User.control_num.like(f"{province_code}-{city_code}-%")
    )

    # Pagination
    users_pagination = users_query.paginate(page=page, per_page=per_page)
    users = users_pagination.items

    total_questions = db.session.query(Assessment).count()
    user_progress = {}
    highlighted_users = {}
    highlighted_users_yellow = {}

    for user in users:
        has_services = db.session.query(Services).filter_by(user_id=user.id, services_saved=True).first() is not None
        has_recommendations = db.session.query(Recommendations).filter_by(user_id=user.id, recommendation_saved=True).first() is not None
        user_progress[user.id] = has_services and has_recommendations

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



@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    try:
        return datetime.strptime(value, format)
    except (ValueError, TypeError):
        return None
    
@app.route('/view-client/<int:user_id>')
def view_client(user_id):
    
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    user = User.query.get_or_404(user_id)  # Fetch user once
    
    signature = Signature.query.filter_by(user_id=user.id).order_by(Signature.id.desc()).first()

    
    
    user_services = Services.query.filter_by(user_id=user_id).all()

    saved_services = [service.service_name for service in user_services]

    user_recommendations = Recommendations.query.filter_by(user_id=user_id).all()
    
    saved_recommendations = [rec.recommendation_text for rec in user_recommendations]
    
    other_service = Services.query.filter_by(user_id=user_id, service_name='Other').first()
    
    other_service_detail = other_service.service_detail if other_service else ''
    
    other_recommendation = Recommendations.query.filter_by(user_id=user_id, recommendation_text='Other').first()
    other_recommendation_detail = other_recommendation.recommendation_text if other_recommendation and other_recommendation.recommendation_text else ''
    
    # For input value in HTML (datetime-local format)
    follow_up_datetime_input = ''
    follow_up_datetime_display = ''
    for service in saved_services:
        if service.startswith('Follow-up at '):
            raw_dt = service.replace('Follow-up at ', '')
            try:
                dt_obj = datetime.fromisoformat(raw_dt)
                follow_up_datetime_input = dt_obj.strftime('%Y-%m-%dT%H:%M')  # for input
                follow_up_datetime_display = dt_obj.strftime('%m/%d/%y')      # for showing to user
            except ValueError:
                pass
            break
        
    recommended_follow_up_datetime_input = ''
    for rec in saved_recommendations:
        if rec.startswith('Follow-up at '):
            raw_rec_dt = rec.replace('Follow-up at ', '')
            try:
                dt_obj = datetime.fromisoformat(raw_rec_dt)
                recommended_follow_up_datetime_input = dt_obj.strftime('%Y-%m-%dT%H:%M')  # Correct format for input field
            except ValueError:
                recommended_follow_up_datetime_input = ''
            break
        
    # Fetch user responses
    questions_with_answers = get_questions_and_answers(user_id)  # Get questions and answers
    
    # Define key questions
    question_messages = {
    1: 'The client has disclosed experiencing domestic violence or threats at home, requiring immediate attention',

    2: 'The client has expressed thoughts of running away or leaving home, which may indicate distress, family conflicts, or insecurity',

    3: 'The client reported experiencing physical or cyberbullying at school or work, which can severely impact mental and emotional well-being',

    4: 'The client has expressed serious thoughts of self-harm or suicide, indicating an urgent need for psychological support and crisis intervention',

    10: 'The client reported experiencing forced sexual activity, a serious concern requiring urgent intervention. '
        'Take appropriate action, including notifying legal authorities, arranging medical care, and providing trauma-informed psychological support',

    12: 'The client has requested counseling or consultation, presenting an opportunity to provide professional support tailored to their needs',

    "relationships_sexual_health": 'The client has shared concerns regarding romantic relationships, sexual activity, or pregnancy. '
                                   'Encourage discussions on safe practices, consent, and emotional well-being, while offering referrals to counseling or medical professionals for further support'
}

    import re
    def highlight_keywords(text, keywords):
        for kw in keywords:
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            text = pattern.sub(lambda m: f'<span style="color:red;">{m.group(0)}</span>', text)
        return text

    keywords_to_highlight = [
        "domestic violence or threats at home",
        "self-harm or suicide",
        "forced sexual activity"    
    ]

    formatted_messages = {}
    for key, message in question_messages.items():
        formatted_messages[key] = highlight_keywords(message, keywords_to_highlight)

   
    # Check if user answered 'Yes' to any special question
    yes_answers = {int(q_id) for q_id, data in questions_with_answers.items() if data["answer"].strip().lower() == "yes"}
    
    displayed_messages = {}
    
    for q in [1, 4, 10]:
        if q in yes_answers:
            displayed_messages[q] = formatted_messages[q] 

    # Display messages for questions 2, 3, 5, 6, 7, 8, 9, 11, 12 if answered "Yes"
    for q in [2, 3]:
        if q in yes_answers:
            displayed_messages[q] = question_messages[q]

    # Check if the user answered "Yes" to any of the substance use questions (5, 6, 7)
    substance_message = format_substance_use_message(questions_with_answers)
    if substance_message:
        displayed_messages[5] = substance_message

        
    if any(q in yes_answers for q in [8, 9, 11]):
        displayed_messages[8] = question_messages["relationships_sexual_health"]
        
    if 12 in yes_answers:
        displayed_messages[12] = question_messages[12]
        
    formatted_messages = format_messages(displayed_messages)
        
    # Load JSON files in one try-except block for efficiency
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
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error: JSON file missing or invalid format", 500

    # Convert lists to dictionaries for quick lookups
    mappings = {
    "region": {item["region_code"]: item["region_name"] for item in json_data["region"]} if isinstance(json_data["region"], list) else {},
    "province": {item["province_code"]: item["province_name"] for item in json_data["province"]} if isinstance(json_data["province"], list) else {},
    "city": {item["city_code"]: item["city_name"] for item in json_data["city"]} if isinstance(json_data["city"], list) else {},
    "barangay": {item.get("brgy_code", item.get("brgy_code")): item["brgy_name"] for item in json_data["barangay"] if "brgy_name" in item} if isinstance(json_data["barangay"], list) else {}
}

    # Function to safely get location name from code
    def get_location_name(value, mapping):
        return mapping.get(value, value)  # Return name if found, else return input

    # Convert user location codes to names
    region_name = get_location_name(user.region, mappings["region"])
    province_name = get_location_name(user.province, mappings["province"])
    city_name = get_location_name(user.city, mappings["city"])
    brgy_name = get_location_name(user.barangay, mappings["barangay"])

    # Fetch admin username if logged in
    admin_username = session.get('admin')
    if admin_username:
        admin = Admin.query.filter_by(username=admin_username).first()
        admin_username = admin.username if admin else None

    show_message = True
    

    return render_template(
        'view_client.html', 
        admin=admin,
        signature=signature,
        user=user, 
        questions_with_answers=questions_with_answers,
        displayed_messages=displayed_messages,
        region_name=region_name, 
        province_name=province_name,
        city_name=city_name,
        brgy_name=brgy_name,
        admin_username=admin_username,
        show_message=show_message,
        formatted_messages=formatted_messages,
        saved_services=saved_services,
        saved_recommendations=saved_recommendations,
        follow_up_datetime=follow_up_datetime_input,
        follow_up_display=follow_up_datetime_display,
         recommended_follow_up_datetime=recommended_follow_up_datetime_input,
         other_service_detail=other_service_detail,
         other_recommendation_detail=other_recommendation_detail,

    )
    
def format_messages(messages):
    formatted_paragraphs = []
    current_paragraph = []

    for message in messages.values():
        sentences = message.split('. ')
        for sentence in sentences:
            formatted_sentence = sentence + "."  
            if not current_paragraph:  
                formatted_sentence = " " + formatted_sentence  # Adds an indent (em space)
            current_paragraph.append(formatted_sentence)

            if len(current_paragraph) == 5:  # Limit each paragraph to 5 sentences
                formatted_paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []

    if current_paragraph:  # Add any remaining sentences
        formatted_paragraphs.append(" ".join(current_paragraph))

    return formatted_paragraphs

def format_substance_use_message(answers):
    substances = []

    if answers.get(5, {}).get("answer", "").strip().lower() == "yes":
        substances.append("smoking")
    if answers.get(6, {}).get("answer", "").strip().lower() == "yes":
        substances.append("alcohol consumption")
    if answers.get(7, {}).get("answer", "").strip().lower() == "yes":
        substances.append("exposure to illegal drugs")

    if substances:
        if len(substances) == 2:
            substance_list = " and ".join(substances)
        else:
            substance_list = ", ".join(substances[:-1]) + ", and " + substances[-1] if len(substances) > 2 else substances[0]

        return (f"The client disclosed {substance_list}. This may indicate potential dependence or exposure to harmful environments")
    
    return None  # No message if no "Yes" answers

@app.route('/save_services', methods=['POST'])
def save_services():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        services = data.get('services', [])
        recommendations = data.get('recommendations', [])
        follow_up_datetime = data.get('follow_up_datetime')
        recommended_follow_up_datetime = data.get('recommended_follow_up_datetime')
        
        # Custom "Other" inputs
        other_service_detail = data.get('other_service_detail', '').strip()
        other_recommendation_detail = data.get('other_recommendation_detail', '').strip()

        if not user_id:
            return 'User ID is required', 400

        print("Received services:", services)
        print("Received recommendations:", recommendations)
        print("Other service detail:", other_service_detail)
        print("Other recommendation detail:", other_recommendation_detail)
        print("Follow-up datetime (service):", follow_up_datetime)
        print("Follow-up datetime (recommendation):", recommended_follow_up_datetime)

        # Clear existing entries
        Services.query.filter_by(user_id=user_id).delete()
        Recommendations.query.filter_by(user_id=user_id).delete()

        # Save services
        for service in services:
            if service == "Other":
                new_service = Services(
                    service_name="Other",
                    service_detail=other_service_detail,  # ✅ Save custom input
                    user_id=user_id,
                    services_saved=True
                )
            else:
                new_service = Services(
                    service_name=service,
                    service_detail="",  # Optional: blank for non-Other
                    user_id=user_id,
                    services_saved=True
                )
            db.session.add(new_service)

        # Save recommendations
        for recommendation in recommendations:
            if recommendation == "Other":
                new_recommendation = Recommendations(
                    recommendation_text=other_recommendation_detail,  # ✅ Save custom input
                    user_id=user_id,
                    recommendation_saved=True
                )
            else:
                new_recommendation = Recommendations(
                    recommendation_text=recommendation,
                    user_id=user_id,
                    recommendation_saved=True
                )
            db.session.add(new_recommendation)

        # Update user follow-up datetimes
        user = User.query.get(user_id)
        if user:
            user.services_saved = True
            if follow_up_datetime:
                user.follow_up_datetime = follow_up_datetime
            if recommended_follow_up_datetime:
                user.recommended_follow_up_datetime = recommended_follow_up_datetime
        else:
            return 'User not found', 404

        db.session.commit()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return str(e), 500


@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.contact_number = request.form['contact_number']
        user.status = request.form['status']
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_list'))
    return render_template('edit_user.html', user=user)

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True})

    
@app.route('/admin/summary/<int:user_id>')
def admin_summary(user_id):
    user = User.query.get_or_404(user_id)

    # Fetch responses of the specific user from UserResponse
    responses = UserResponse.query.filter_by(user_id=user_id).all()

    # Get all question numbers that the user answered
    question_ids = [resp.question_number for resp in responses]

    # Fetch all corresponding questions
    questions = Questions.query.filter(Questions.id.in_(question_ids)).all()

    # Match questions with the user's responses
    questions_with_answers = {
        q.id: {
            "question": q.question_text, 
            "answer": next((r.response for r in responses if r.question_number == q.id), None)
        }
        for q in questions
    }

    return render_template('summary.html', user=user, questions_with_answers=questions_with_answers)


@app.route("/search_control_num", methods=["GET"])
def search_control_num():
    query = request.args.get("q", "").strip().lower()
    admin = Admin.query.filter_by(username=session.get('admin')).first()

    if not query or not admin:
        return jsonify([])

    # Load location JSON files
    json_files = {
        "region": "region.json",
        "province": "province.json",
        "city": "city.json"
    }

    json_data = {}
    try:
        for key, filename in json_files.items():
            path = os.path.join(current_app.root_path, 'static', 'ph-json', filename)
            with open(path, 'r', encoding='utf-8') as f:
                json_data[key] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500

    # Main search filtered by location
    results = User.query.filter(
        or_(
            User.control_num.ilike(f"%{query}%"),
            User.first_name.ilike(f"%{query}%"),
            User.last_name.ilike(f"%{query}%")
        ),
        User.control_num.isnot(None),
        User.control_num != '',
        or_(
            func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name)),
            
        )
    ).all()

    return jsonify([
        {
            "id": user.id,
            "control_num": user.control_num,
            "first_name": user.first_name,
            "last_name": user.last_name
        } for user in results
    ])


@app.route('/admin/unread_notifications')
def get_unread_notifications():
    unread_responses = UserResponse.query.filter_by(is_read=False, question_number=0).all()

    notifications = [
        {
            "sender": "User " + str(resp.user_id),
            "time": "Just now",
            "content": "User has completed the assessment!",
            "unread": True
        } 
        for resp in unread_responses
    ]

    return jsonify({
        "unread_count": len(notifications),
        "notifications": notifications
    })

@app.route('/admin/mark_notification_read', methods=['POST'])
def mark_notification_read():
    data = request.get_json()
    message_id = data.get('message_id')

    notification = UserResponse.query.get(message_id)
    if notification:
        notification.is_read = True
        db.session.commit()

    return jsonify({'message': 'Notification marked as read'})

@app.route('/get_notifications')
def get_notifications():
    if 'admin' not in session:
        return jsonify({"error": "Not authorized"}), 403

    admin = Admin.query.filter_by(username=session['admin']).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    # Load region, province, city JSON
    json_files = {
        "region": "region.json",
        "province": "province.json",
        "city": "city.json"
    }

    json_data = {}
    try:
        for key, filename in json_files.items():
            path = os.path.join(current_app.root_path, 'static', 'ph-json', filename)
            with open(path, 'r', encoding='utf-8') as f:
                json_data[key] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500

    all_question_numbers = list(range(1, 13))
    key_question_numbers = [1, 4, 10]

    # Get users who already received any service
    served_user_ids = set(
        db.session.query(Services.user_id)
        .join(User, Services.user_id == User.id)
        .filter(
            Services.service_name.isnot(None),
            Services.service_name != '',
            func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name))
        )
        .distinct()
        .all()
    )
    # Unpack tuples into plain IDs
    served_user_ids = set(uid for (uid,) in served_user_ids)

    # Fetch all relevant responses for all 12 questions
    all_answers = (
        db.session.query(UserResponse.user_id, User.control_num, UserResponse.question_number,
                         UserResponse.response, UserResponse.submitted_at)
        .join(User, UserResponse.user_id == User.id)
        .filter(UserResponse.question_number.in_(all_question_numbers))
        .filter(User.control_num.isnot(None), User.control_num != '')
        .filter(
            or_(
                func.lower(func.trim(User.location)) == func.lower(func.trim(admin.center_name)),
            ),
        )
        .all()
    )

    # Group responses by user
    from collections import defaultdict

    responses_by_user = defaultdict(dict)
    latest_by_user = {}

    for user_id, control_num, qnum, resp, submitted_at in all_answers:
        if user_id in served_user_ids:
            continue  # Skip users who already received a service

        responses_by_user[user_id][qnum] = resp
        if user_id not in latest_by_user or submitted_at > latest_by_user[user_id]["submitted_at"]:
            latest_by_user[user_id] = {
                "control_num": control_num,
                "submitted_at": submitted_at
            }

    notifications = []

    for user_id, answers in responses_by_user.items():
        responses = [answers.get(qn, "") for qn in all_question_numbers]
        control_num = latest_by_user[user_id]["control_num"]
        submitted_at = latest_by_user[user_id]["submitted_at"]

        # Determine urgency
        key_yes = any(answers.get(qn) == "Yes" for qn in key_question_numbers)
        all_no = all(answers.get(qn) == "No" for qn in all_question_numbers)
        yellow_criteria = (
            all(answers.get(qn) == "No" for qn in key_question_numbers) and
            any(answers.get(qn) == "Yes" for qn in all_question_numbers if qn not in key_question_numbers)
        )

        if all_no:
            continue  # Green - skip notification

        if key_yes:
            urgency = "high"
        elif yellow_criteria:
            urgency = "medium"
        else:
            urgency = "medium"  # Fallback

        notifications.append({
            "id": user_id,
            "user_id": user_id,
            "sender": f"{control_num}",
            "content": f"Client {control_num} requires immediate evaluation.",
            "submitted_at": submitted_at,
            "urgency": urgency,
            "unread": True
        })

    # Sort by submission time
    notifications.sort(key=lambda x: x["submitted_at"], reverse=True)

    for notif in notifications:
        notif["time"] = notif["submitted_at"].strftime("%Y-%m-%d %H:%M:%S")
        del notif["submitted_at"]

    return jsonify(notifications)


@app.route('/admin/profile')
def admin_settings():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    questions = Questions.query.all()
    users = User.query.all()

    return render_template('admin_settings.html', admin=admin, questions=questions, users=users)

# @app.route('/admin/profile')
# def admin_profile():
#     if 'admin' not in session:
#         flash('Please log in first.', 'danger')
#         return redirect(url_for('admin'))

#     admin = Admin.query.filter_by(username=session['admin']).first()
#     print(f"Admin fetched: username={admin.username}, full_name={admin.full_name}")  # Debug

#     questions = Questions.query.all()
#     users = User.query.all()

#     return render_template('admin_profile.html', admin=admin, questions=questions, users=users)


@app.route('/admin/edit_profile', methods=['GET', 'POST'])
def edit_admin_profile():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    if request.method == 'POST':
        # Only update if provided
        if request.form.get('username'):
            admin.username = request.form['username']
        if request.form.get('email'):
            admin.email = request.form['email']
        if request.form.get('centerName'):
            admin.center_name = request.form['centerName']
        if request.form.get('job'):
            admin.job = request.form['job']
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

        return redirect(url_for('admin_settings'))

    return render_template('edit_admin_profile.html', admin=admin)


@app.route('/admin/messages')
def admin_messages():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    # Fetch questions and user responses
    questions = (
        db.session.query(Questions, UserResponse.response, UserResponse.submitted_at, User.control_num)
        .join(UserResponse, Questions.id == UserResponse.question_number)
        .join(User, User.id == UserResponse.user_id)
        .order_by(User.control_num.desc())
    )

    # Filter "Yes" answers for critical questions (1, 4, 10)
    critical_yes_answers = (
        db.session.query(User.control_num, Questions.id)
        .join(UserResponse, Questions.id == UserResponse.question_number)
        .filter(UserResponse.response == 'Yes', Questions.id.in_([1, 4, 10]))
        .all()
    )

    # Group critical "Yes" answers by control number
    critical_responses = {}
    for control_num, question_id in critical_yes_answers:
        if control_num not in critical_responses:
            critical_responses[control_num] = []
        critical_responses[control_num].append(question_id)

    users = User.query.all()

    return render_template(
        'admin_messages.html',
        admin=admin,
        questions=questions,
        users=users,
        critical_responses=critical_responses
    )

@app.route('/get_summary/<control_num>')
def get_summary(control_num):
    # Fetch the user and their critical responses
    user = User.query.filter_by(control_num=control_num).first_or_404()
    critical_responses = (
        db.session.query(Questions.id, Questions.question_text)
        .join(UserResponse, Questions.id == UserResponse.question_number)
        .filter(UserResponse.user_id == user.id, UserResponse.response == 'Yes', Questions.id.in_([1, 4, 10]))
        .all()
    )

    if not critical_responses:
        return "No critical responses found for this user.", 404

    # Generate the summary content
    summary = f"<h3>Critical Questions Summary for User {control_num}</h3><ul>"
    for question_id, question_text in critical_responses:
        summary += f"<li>Question {question_id}: {question_text}</li>"
    summary += "</ul>"

    return summary
  
@app.route('/admin/files')
def admin_files():
    if 'admin' not in session:
        flash('Please log in first.' 'danger')
        return redirect(url_for('admin'))
    
    admin = Admin.query.filter_by(username=session['admin']).first()
    questions = Questions.query.all()
    users = User.query.all()
    
    return render_template('admin_files.html', admin=admin, questions=questions, users=users)

@app.route('/admin/results')
def admin_results():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))
    
    admin = Admin.query.filter_by(username=session['admin']).first()
    questions = Questions.query.all()
    users = User.query.all()
    
    return render_template('admin_results.html', admin=admin, questions=questions, users=users)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin'))

@app.route('/instructions')
def instructions(): 
    return render_template("instructions.html")

# Route for Form Submission
@app.route('/personal/information', methods=['GET', 'POST'])
def personal_info():
    user_data = None  # Default value

    if request.method == 'POST':
        try:
            control_num = request.form.get('control_num')  # Retrieve control number
            
            if control_num:
                # Fetch user with the given control number
                user_data = User.query.filter_by(control_num=control_num).first()
                
                if user_data:
                    # ✅ Allow proceeding if 'reason' is NULL or empty
                    if user_data.reason not in [None, ""]:
                        flash("This control number has already been used.", "warning")
                        return redirect(url_for('assessment'))  # Prevent reuse
                    
                    # ✅ Save user ID in session
                    session['user_id'] = user_data.id

                    # ✅ If not used, check if a reason was provided
                    reason = request.form.get('reason')
                    
                    if reason:
                        user_data.reason = reason  # Update reason only
                        db.session.commit()
                    

                    print("✅ Redirecting to headsss...")  # Debugging output
                    return redirect(url_for('headsss'))  # ✅ Proceed to next page
  
        except Exception as e:
            print(f"❌ Error processing form: {e}")  # Debugging output
            flash("An error occurred. Please try again.", "danger")

    return render_template("personal_info.html", user=user_data)

@app.route('/headsss-assessment', methods=['GET', 'POST'])
def headsss():
    # Get the user_id from the session
    user_id = session.get('user_id')

    # If no user_id is found in the session, redirect to the assessment page to create a new user
    if not user_id:
        return redirect(url_for('assessment'))

    # Check if the user has existing responses
    existing_responses = db.session.query(AssessmentResponse).filter_by(user_id=user_id).count()

    # Reset session if it's a new user or their session is outdated
    if existing_responses == 0:
        session['current_assessment_number'] = 1  # Start from the first question
    elif 'current_assessment_number' not in session:
        session['current_assessment_number'] = 1  # Ensure session starts correctly
    
    current_assessment_number = session['current_assessment_number']
    print(f"Current assessment number: {current_assessment_number}")  # Debugging line

    # Fetch total number of questions
    total_assessment = db.session.query(Assessment).count()
    print(f"Total questions: {total_assessment}")

    # Ensure current question is within bounds
    if current_assessment_number > total_assessment:
        session['current_assessment_number'] = 1
        current_assessment_number = 1

    # Retrieve current question from database
    assessment = db.session.query(Assessment).filter_by(id=current_assessment_number).first()

    if not assessment:
        print("❌ No question found for this ID.")  # Debugging line
        return redirect(url_for('thank_you'))  # Redirect if no question found

    is_last_question = current_assessment_number == total_assessment

    if request.method == 'POST':
        if 'back' in request.form:
            # Move to previous question, ensuring it doesn’t go below 1
            session['current_assessment_number'] = max(1, current_assessment_number - 1)
            return redirect(url_for('headsss'))

        # Get user's response for the current question
        response = request.form.get(f'q{current_assessment_number}')

        if response:
            # Check if response already exists (update instead of adding new)
            existing_response = db.session.query(AssessmentResponse).filter_by(
                user_id=user_id, assessment_number=current_assessment_number
            ).first()

            if existing_response:
                existing_response.response = response  # Update response
            else:
                # Insert new response if not previously answered
                new_response = AssessmentResponse(user_id=user_id, assessment_number=current_assessment_number, response=response)
                db.session.add(new_response)

            db.session.commit()

        # Move to next question unless it's the last one
        if not is_last_question:
            session['current_assessment_number'] += 1
            return redirect(url_for('headsss'))
        else:
            return redirect(url_for('thank_you'))  # Redirect to thank-you page

    return render_template('questionnaire.html', assessment=assessment, is_last_question=is_last_question)


@app.route('/thank-you', methods=['GET', 'POST'])
def thank_you():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('headsss'))
    
    if request.method == 'POST' and 'confirm_submit' in request.form:
        return redirect(url_for('submission_complete'))

    # Fetch all responses from the database for this user
    responses = db.session.query(AssessmentResponse).filter_by(user_id=user_id).all()

    if not responses:
        return render_template('thankyou.html', assessment=[], page=1, total_pages=1)

    # Fetch corresponding questions from the Assessment table
    assessment_data = db.session.query(Assessment).filter(Assessment.id.in_([r.assessment_number for r in responses])).all()

    # Map responses by assessment_number for quick lookup
    response_dict = {str(r.assessment_number): r.response for r in responses}

    # Organize assessments by category
    grouped_assessments = defaultdict(list)
    for assessment in assessment_data:
        grouped_assessments[assessment.category].append({
            "assessment": assessment.assessment_text,
            "answer": response_dict.get(str(assessment.id), "No Answer"),
            "is_category": False  # Ensures it’s not misidentified as a category row
        })

    # Flatten grouped data while keeping category headers
    all_assessments = []
    for category, items in grouped_assessments.items():
        all_assessments.append({"category": category, "is_category": True})  # Category header
        all_assessments.extend(items)  # Append actual questions under the category

    # Pagination settings
    page = request.args.get('page', 1, type=int)
    assessments_per_page = 22  # Adjust this number based on your UI needs

    total_assessments = len(all_assessments)
    total_pages = max((total_assessments + assessments_per_page - 1) // assessments_per_page, 1)

    start_index = (page - 1) * assessments_per_page
    end_index = min(start_index + assessments_per_page, total_assessments)

    paginated_assessments = all_assessments[start_index:end_index]

    return render_template('thankyou.html', 
                           assessment=paginated_assessments, 
                           page=page, 
                           total_pages=total_pages)


@app.route('/submision_complete')
def submission_complete():
    return render_template('submission_complete.html')


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    control_num = request.args.get('control_num')

    if not control_num:
        return jsonify({"error": "Control number is required"}), 400

    user = User.query.filter_by(control_num=control_num).first()

    if user:
        return jsonify({
            "first_name": user.first_name,
            "middle_initial": user.middle_initial or "",
            "last_name": user.last_name,
            "dob": user.dob.strftime('%Y-%m-%d') if user.dob else "",
            "age": user.age,
            "contact": user.contact,
            "sex": user.sex,
            "location": user.location or "",  # Keeping location if needed
            "date": user.date.strftime('%Y-%m-%d') if user.date else "",
            "reason": user.reason
        })
    
    return jsonify({"error": "User not found"}), 404

@app.route('/get_age_distribution', methods=['GET'])
def get_age_distribution():
    if 'admin' not in session:
        return jsonify({"error": "Not authorized"}), 403

    admin = Admin.query.filter_by(username=session['admin']).first()
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    # Define center codes mapping
    center_codes = {
        "BHS Union AFHF": ("0837", "01"),
        "RHU Mayorga": ("0837", "02"),
        "Gandara AFHF": ("0860", "02"),
        "RHU Gandara": ("0860", "03"),
        "RHU Pagsanghan": ("0860", "04"),
        "Abuyog District Hospital AFHF": ("0837", "04"),
        "Gandara District Hospital AFHF": ("0860", "05")
    }

    center_name = admin.center_name  # Assuming `location` is the center name for the admin

    # Fetch center information based on the center name
    center_info = center_codes.get(center_name)
    if not center_info:
        return jsonify({"error": "Center not found"}), 404

    province_code, city_code = center_info

    # Load region, province, city JSON for mapping (we can use the same approach)
    json_files = {
        "region": "region.json",
        "province": "province.json",
        "city": "city.json"
    }

    json_data = {}
    try:
        for key, filename in json_files.items():
            path = os.path.join(current_app.root_path, 'static', 'ph-json', filename)
            with open(path, 'r', encoding='utf-8') as f:
                json_data[key] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return jsonify({"error": str(e)}), 500

    # Get the year and month parameters from the request
    year = request.args.get('year')
    month = request.args.get('month')

    # Start query with users who have a control number matching the center's province and city
    query = db.session.query(User.age, User.sex, User.control_num).filter(
        User.control_num.isnot(None),
        User.control_num != '',
        User.control_num.like(f"{province_code}-{city_code}-%")  # Filter by control number prefix
    )

    # Apply optional filters for year and month
    if year:
        query = query.filter(extract('year', User.date) == int(year))
    if month and month.lower() != 'all':
        query = query.filter(extract('month', User.date) == int(month))

    # Fetch the users based on the query
    users = query.all()

    # Initialize age groups with zero counts
    age_groups = {
        "10-14": {"Male": 0, "Female": 0},
        "15-19": {"Male": 0, "Female": 0}
    }

    # Count users by age and sex
    for age, sex, _ in users:
        if age is None or sex is None:
            continue
        sex = sex.capitalize()
        if sex not in ["Male", "Female"]:
            continue
        if 10 <= age <= 14:
            age_groups["10-14"][sex] += 1
        elif 15 <= age <= 19:
            age_groups["15-19"][sex] += 1

    return jsonify(age_groups)

@app.route('/get_user_details', methods=['GET'])
def get_user_details():
    control_num = request.args.get('control_num')
    print(f"Received Control Number: {control_num}")  # Debugging log

    if not control_num:
        return jsonify({"valid": False, "message": "No control number provided"})

    user = User.query.filter_by(control_num=control_num).first()

    if user:
        print("User found in database.")  # Debugging log
        return jsonify({
            "valid": True,
            "first_name": user.first_name,
            "middle_initial": user.middle_initial,
            "last_name": user.last_name,
            "contact": user.contact,
            "dob": user.dob,
            "age": user.age,
            "sex": user.sex,
            "region": user.region,
            "province": user.province,
            "city": user.city,
            "barangay": user.barangay,
            "street": user.street,
            "date": user.date,
            "location": user.location
        })
    else:
        print("User NOT found in database.")  # Debugging log
        return jsonify({"valid": False, "message": "Invalid control number"})

    

@app.route('/update_reason', methods=['POST'])
def update_reason():
    data = request.json
    control_num = data.get("control_num")
    reason = data.get("reason")

    if not control_num or not reason:
        return jsonify({"success": False, "message": "Missing control number or reason"}), 400

    user = User.query.filter_by(control_num=control_num).first()
   
    if user:
        user.reason = reason
        db.session.commit()
        return jsonify({"success": True, "message": "Reason updated successfully"})
    else:
        return jsonify({"success": False, "message": "Invalid control number"}), 404
    

@app.route('/get_questions', methods=['GET'])
def get_questions():
    try:
        result = db.session.execute(text("SELECT id, assessment_text, translation_text FROM assessment"))
        assessment = [{"id": row[0], "assessment_text": row[1], "translation_text": row[2]} for row in result.fetchall()]
        return jsonify(assessment)
    except Exception as e:
        return jsonify([{"id": q[0], "assessment_text": q[1], "translation_text": q[2]} for q in assessment])


@app.route('/save_answer', methods=['POST'])
def save_answer():
    try:
        data = request.json  # Get JSON data from request
        print(f"📥 Received Data: {data}")  # Debugging

        control_num = data.get('control_num')
        assessment_number = data.get('question_number')
        response = data.get('response')

        # Check if any field is missing
        if not all([control_num, assessment_number, response]):  
            print("❌ Missing required fields!")  # Debugging
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Connect to MySQL
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        cursor = connection.cursor()

        # Fetch user_id using control_num
        cursor.execute("SELECT id FROM user WHERE control_num = %s", (control_num,))
        user = cursor.fetchone()
       
        if not user:
            print("❌ Invalid control number!")  # Debugging
            return jsonify({"success": False, "error": "Invalid control number"}), 400

        user_id = user[0]  # Get user_id from tuple

        # Insert the answer into the database
        sql = """
        INSERT INTO assessment_response (user_id, assessment_number, response)
        VALUES (%s, %s, %s)
        """
        values = (user_id, assessment_number, response)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"success": True, "message": "Answer saved successfully"}), 201

    except Exception as e:
        print(f"❌ Error saving answer: {e}")  # Debugging
        return jsonify({"success": False, "error": str(e)}), 500
    
    
@app.route('/get_summary1', methods=['GET'])
def get_summary1():
    try:
        control_num = request.args.get('control_num')

        # Debugging
        print(f"Received control_num: {control_num}")

        if not control_num:
            return jsonify({"success": False, "error": "Missing control number"}), 400

        # Get user_id from control_num
        result = db.session.execute(text("SELECT id FROM user WHERE control_num = :control_num"), {"control_num": control_num})
        user = result.fetchone()

        if not user:
            return jsonify({"success": False, "error": "Invalid control number"}), 400

        user_id = user[0]
        print(f"Found user_id: {user_id}")  # Debugging

        # Fetch data from assessment and assessment_response tables
        result = db.session.execute(text("""
            SELECT a.assessment_text, a.translation_text, ar.response
            FROM assessment_response ar
            JOIN assessment a ON ar.assessment_number = a.id
            WHERE ar.user_id = :user_id
        """), {"user_id": user_id})

        summary_data = [{"assessment_text": row[0], "translation_text": row[1], "response": row[2]} for row in result.fetchall()]

        print(f"Summary Data: {summary_data}")  # Debugging

        return jsonify(summary_data), 200

    except Exception as e:
        print(f"❌ Error fetching summary: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/upload_signature', methods=['POST'])
def upload_signature():
    if 'signature' not in request.files:
        return jsonify({"error": "No signature file part"}), 400

    file = request.files['signature']
    user_id = request.form.get('user_id')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Secure filename and add timestamp for uniqueness
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    filename = secure_filename(f"{timestamp}_{file.filename}")

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Save record to database
    signature = Signature(
        user_id=int(user_id),
        filename=filename
    )
    db.session.add(signature)
    db.session.commit()

    return jsonify({"message": "Signature uploaded successfully", "filename": filename}), 200

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5005, debug=True)

