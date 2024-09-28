from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = "wardrobe_secret_key"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

DATABASE = 'clothes.db'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            clothing_type TEXT NOT NULL,
            description TEXT,
            material TEXT NOT NULL,
            image_filename TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            conn.close()
            flash('Signup successful, please login!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please login or use a different email.')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    user_id = session.get('user_id')

    if request.method == 'POST':
        category = request.form['category']
        clothing_type = request.form['clothing_type']
        material = request.form['material']
        description = request.form.get('description', '')

        file = request.files['image']
        image_filename = None

        if file and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO clothes (user_id, category, clothing_type, description, material, image_filename) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, category, clothing_type, description, material, image_filename))
        conn.commit()
        conn.close()

        flash('Clothing item added successfully!')

    conn = get_db_connection()
    formal_clothes = conn.execute('''
        SELECT * FROM clothes WHERE user_id = ? AND clothing_type = "Formal"
    ''', (user_id,)).fetchall()
    
    informal_clothes = conn.execute('''
        SELECT * FROM clothes WHERE user_id = ? AND clothing_type = "Informal"
    ''', (user_id,)).fetchall()
    conn.close()

    formal_outfit = random.sample(formal_clothes, 3) if len(formal_clothes) >= 3 else None
    informal_outfit = random.sample(informal_clothes, 3) if len(informal_clothes) >= 3 else None

    return render_template('home.html', formal_outfit=formal_outfit, informal_outfit=informal_outfit)

@app.route('/analytics')
def analytics():
    user_id = session.get('user_id')

    conn = get_db_connection()

    most_frequent = conn.execute('''
        SELECT * FROM clothes WHERE user_id = ? ORDER BY wear_count DESC LIMIT 1
    ''', (user_id,)).fetchone()

    least_frequent = conn.execute('''
        SELECT * FROM clothes WHERE user_id = ? ORDER BY wear_count ASC LIMIT 1
    ''', (user_id,)).fetchone()

    def calculate_years(date_added):
        date_added = datetime.strptime(date_added, "%Y-%m-%d")
        return (datetime.now() - date_added).days // 365

    most_frequent_years = calculate_years(most_frequent['date_added']) if most_frequent else None
    least_frequent_years = calculate_years(least_frequent['date_added']) if least_frequent else None

    conn.close()

    return render_template('analytics.html', 
                           most_frequent=most_frequent, 
                           least_frequent=least_frequent, 
                           most_frequent_years=most_frequent_years,
                           least_frequent_years=least_frequent_years)
                           
@app.route('/add_clothing', methods=['GET', 'POST'])
def add_clothing():
    if request.method == 'POST':
        user_id = session.get('user_id')
        category = request.form['category']
        clothing_type = request.form['clothing_type']
        material = request.form['material']
        description = request.form.get('description', '')

        file = request.files['image']
        image_filename = None

        if file and allowed_file(file.filename):
            image_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO clothes (user_id, category, clothing_type, description, material, image_filename) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, category, clothing_type, description, material, image_filename))
        conn.commit()
        conn.close()

        flash('Clothing item added successfully!')
        return redirect(url_for('add_clothing'))

    conn = get_db_connection()
    all_clothing = conn.execute('SELECT * FROM clothes').fetchall()
    conn.close()

    return render_template('add_clothing.html', all_clothing=all_clothing)


@app.route('/ethical_threads')
def ethical_threads():
    return render_template('ethical_threads.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
