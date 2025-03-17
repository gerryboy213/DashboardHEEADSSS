from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import uuid
import mysql.connector
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

def get_questions():
    return Questions.query.filter_by(category='HOME').all()

with open("static/ph-json/province.json", "r", encoding="utf-8") as file:
    province_data = json.load(file)
    
# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    user_id = db.Column(db.Integer, nullable=False)  # Link to the user
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
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    job = db.Column(db.String(100), nullable=True)
    
@app.route('/get_yes_no_distribution', methods=['GET'])
def get_yes_no_distribution():
    # Query only responses from users that exist in the database
    response_counts = (
        db.session.query(
            UserResponse.question_number,
            UserResponse.response,
            db.func.count(UserResponse.response)
        )
        .join(User, UserResponse.user_id == User.id)  # Ensures only existing users are counted
        .group_by(UserResponse.question_number, UserResponse.response)
        .all()
    )

    # Structure the data into a dictionary
    yes_no_data = {}

    for question_number, response, count in response_counts:
        if question_number not in yes_no_data:
            yes_no_data[question_number] = {"Yes": 0, "No": 0}
        
        if response.lower() == "yes":
            yes_no_data[question_number]["Yes"] = count
        elif response.lower() == "no":
            yes_no_data[question_number]["No"] = count

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


@app.route('/admin/signup', methods=['POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_admin = Admin(username=username, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        
        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin_login'))

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

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    questions = Questions.query.all()
    users = User.query.all()
    
    # Get unread user responses
    unread_responses = UserResponse.query.filter_by(is_read=False).count()

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        questions=questions,
        users=users,
        unread_responses=unread_responses
    )
    
@app.route('/admin/list')
def admin_list():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users_pagination = User.query.paginate(page=page, per_page=per_page)
    users = users_pagination.items

    total_questions = db.session.query(Assessment).count()  # ✅ Get total assessment questions

    user_progress = {}
    for user in users:
        answered_questions = (
            db.session.query(AssessmentResponse)
            .filter_by(user_id=user.id)
            .count()
        )
        # ✅ If answered questions match total, mark as 'Done'
        user_progress[user.id] = answered_questions >= total_questions  

    unread_responses = UserResponse.query.filter_by(is_read=False).count()

    return render_template(
        'admin_list.html',
        admin=admin,
        users=users,  
        user_progress=user_progress,  # ✅ Pass progress data to template
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

    # Ensure file paths are correctly set inside the request context
    region_json_path = os.path.join(current_app.root_path, 'static', 'ph-json', 'region.json')
    province_json_path = os.path.join(current_app.root_path, 'static', 'ph-json', 'province.json')
    city_json_path = os.path.join(current_app.root_path, 'static', 'ph-json', 'city.json')
    brgy_json_path = os.path.join(current_app.root_path, 'static', 'ph-json', 'barangay.json')

    # Load JSON data safely
    try:
        with open(region_json_path, 'r', encoding='utf-8') as f:
            regions_data = json.load(f)

        with open(province_json_path, 'r', encoding='utf-8') as f:
            provinces_data = json.load(f)
            
        with open(city_json_path, 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
            
        with open(brgy_json_path, 'r', encoding='utf-8') as f:
            brgys_data = json.load(f)
            
    except FileNotFoundError:
        return "Error: JSON file not found", 500
    except json.JSONDecodeError:
        return "Error: Invalid JSON format", 500

    # Convert lists to dictionaries for easy lookup
    region_map = {reg["region_code"]: reg["region_name"] for reg in regions_data} if isinstance(regions_data, list) else {}
    province_map = {prov["province_code"]: prov["province_name"] for prov in provinces_data} if isinstance(provinces_data, list) else {}
    city_map = {city["city_code"]: city["city_name"] for city in cities_data} if isinstance(cities_data, list) else {}
    brgy_map = {brgy["brgy_code"]: brgy["brgy_name"] for brgy in brgys_data} if isinstance(brgys_data, list) else {}

    # Function to check if input is a code or a name
    def get_location_name(input_value, mapping):
        return mapping.get(input_value, input_value)  # If not in mapping, assume it's already a name

    # Convert codes to names or keep them if they are already names
    region_name = get_location_name(user.region, region_map)
    province_name = get_location_name(user.province, province_map)
    city_name = get_location_name(user.city, city_map)
    brgy_name = get_location_name(user.barangay, brgy_map)
    
    admin_username = None
    if 'admin' in session:
        admin = Admin.query.filter_by(username=session['admin']).first()
        admin_username = admin.username if admin else None


    return render_template(
        'view_client.html', 
        user=user, questions_with_answers=questions_with_answers,
        region_name=region_name, 
        province_name=province_name,
        city_name=city_name,
        brgy_name=brgy_name,
        admin_username=admin_username
    )

    
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
    
    if not query:
        return jsonify([])  # Return empty if no query

    results = User.query.filter(User.control_num.ilike(f"%{query}%")).all()
    
    return jsonify([
        {"id": user.id, "control_num": user.control_num} 
        for user in results
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
    key_question_numbers = [1, 4, 10]

    # Fetch users who answered "Yes" to key questions
    user_responses = (
        db.session.query(UserResponse.user_id, User.control_num, UserResponse.question_number, UserResponse.submitted_at)
        .join(User, UserResponse.user_id == User.id)
        .filter(UserResponse.question_number.in_(key_question_numbers))
        .filter(UserResponse.response == "Yes")
        .all()
    )

    user_data = {}
    for user_id, control_num, question, submitted_at in user_responses:
        if user_id not in user_data:
            user_data[user_id] = {
                "control_num": control_num,
                "answered": set(),
                "submitted_at": submitted_at  # Store the timestamp
            }
        user_data[user_id]["answered"].add(question)

    notifications = []
    for user_id, data in user_data.items():
        notifications.append({
            "id": user_id,  # Unique ID for frontend use
            "user_id": user_id,  # Corrected from n.user_id to user_id
            "sender": f"User {data['control_num']}",  # Name of the user
            "content": f"User {data['control_num']} requires immediate evaluation.",
            "time": data["submitted_at"].strftime("%Y-%m-%d %H:%M:%S"),  # Use actual submission time
            "unread": True  # Mark all as unread initially
        })

    return jsonify(notifications)

# @app.route('/get_assessment_summary', methods=['GET'])
# def get_assessment_summary():
#     user_id = request.args.get('user_id')
#     # Fetch data from your database based on user_id
#     summary_data = {
#         "summary": [
#             {"question": "Did you complete the test?", "answer": "Yes"},
#             {"question": "Was it helpful?", "answer": "No"},
#         ]
#     }
#     return jsonify(summary_data)


@app.route('/admin/settings')
def admin_settings():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    questions = Questions.query.all()
    users = User.query.all()

    return render_template('admin_settings.html', admin=admin, questions=questions, users=users)

@app.route('/admin/profile')
def admin_profile():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()
    questions = Questions.query.all()
    users = User.query.all()

    return render_template('admin_profile.html', admin=admin, questions=questions, users=users)

@app.route('/admin/edit_profile', methods=['GET', 'POST'])
def edit_admin_profile():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    if request.method == 'POST':
        # Update admin details
        admin.username = request.form.get('username', admin.username)  # Default to current username if not provided
        admin.email = request.form.get('email', admin.email)          # Default to current email if not provided
        admin.job = request.form.get('job', admin.job)                # Default to current job if not provided
        admin.phone = request.form.get('phone', admin.phone)          # Default to current phone if not provided
        admin.address = request.form.get('address', admin.address)    # Default to current address if not provided

        # Update password if provided
        if request.form.get('password'):
            admin.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        db.session.commit()

        # Update the session with the new username
        session['admin'] = admin.username

        return redirect(url_for('admin_profile'))

    return render_template('edit_admin_profile.html', admin=admin)

@app.route('/admin/messages')
def admin_messages():
    if 'admin' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('admin'))

    admin = Admin.query.filter_by(username=session['admin']).first()

    page = request.args.get('page', 1, type=int)
    per_page = 10  # Show 10 messages per page
    questions = Questions.query.paginate(page=page, per_page=per_page, error_out=False)
    
    users = User.query.all()

    return render_template('admin_messages.html', admin=admin, questions=questions, users=users)

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
    users = User.query.with_entities(User.age, User.sex).all()

    if not users:
        return jsonify({"error": "No user data available"}), 404

    # Define new age groups
    age_groups = {
        "1-10": {"Male": 0, "Female": 0},
        "11-20": {"Male": 0, "Female": 0},
        "21-30": {"Male": 0, "Female": 0},
        "31-40": {"Male": 0, "Female": 0},
        "41-50": {"Male": 0, "Female": 0},
        "51-60": {"Male": 0, "Female": 0}
    }

    # Categorize users into the correct age groups
    for age, sex in users:
        if age is None or sex is None:
            continue

        if 1 <= age <= 10:
            age_groups["1-10"][sex] += 1
        elif 11 <= age <= 20:
            age_groups["11-20"][sex] += 1
        elif 21 <= age <= 30:
            age_groups["21-30"][sex] += 1
        elif 31 <= age <= 40:
            age_groups["31-40"][sex] += 1
        elif 41 <= age <= 50:
            age_groups["41-50"][sex] += 1
        elif 51 <= age <= 60:
            age_groups["51-60"][sex] += 1

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


# @app.route('/questions', methods=['GET', 'POST'])
# def questions():
#     # Get the user_id from the session
#     user_id = session.get('user_id')

#     # If no user_id is found in the session, redirect to the assessment page to create a new user
#     if not user_id:
#         return redirect(url_for('assessment'))

#     # Get the current question number from the session, default to 1
#     current_question_number = session.get('current_question_number', 1)
#     print(f"Current question number: {current_question_number}")  # Debugging line
    
#     if current_question_number > 12:
#         session['current_question_number'] = 1
#         current_question_number = 1

#     # Retrieve the current question from the database based on the question number
#     question = db.session.query(Questions).filter_by(id=current_question_number).first()
    
#     if question is None:
#         print("❌ No question found for this ID.")  # Debugging line
#     else:
#         print(f"Retrieved question: {question.question_text}")
        

#     # Get the total number of questions in the database
#     total_questions = db.session.query(Questions).count()
#     print(f"Total questions: {total_questions}")

#     # Check if the current question is the last one
#     is_last_question = current_question_number == total_questions

#     if request.method == 'POST':
#         if 'back' in request.form:
#             current_question_number -= 1  # Decrement the question number when the "Back" button is clicked
#             session['current_question_number'] = current_question_number
#             return redirect(url_for('questions'))

#         # Get the response for the current question
#         response = request.form.get(f'q{current_question_number}')
        
#         if response:
#             # Save the response to the database
#             new_response = UserResponse(user_id=user_id, question_number=current_question_number, response=response)
#             db.session.add(new_response)
#             db.session.commit()

#         # Move to the next question by updating session, unless it's the last question
#         if not is_last_question:
#             session['current_question_number'] = current_question_number + 1
#             return redirect(url_for('questions'))
#         else:
#             # Handle submission when the last question is reached
#             return redirect(url_for('thank_you'))  # Redirect to a submission page (could be a 'Thank You' page or similar)

#     # Render the current question in the template, passing whether it's the last question or not
#     return render_template('questionnaire.html', question=question, is_last_question=is_last_question)

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0', port=5000, debug=True)

