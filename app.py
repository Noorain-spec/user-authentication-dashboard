from flask import Flask, request, redirect, render_template, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from flask_session import Session
from datetime import timedelta
import os


app = Flask(__name__)
app.secret_key = 'my-secret-key'

# Server side setup config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)

Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.before_request
def check_session_expiry():
    allowed_paths = ['login', 'register', 'static']
    print("user session:", session.get('username'))
    if 'username' not in session and request.endpoint not in allowed_paths:
        flash('Session expired, Please login again', 'error')
        return redirect(url_for('login'))

@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user  = User.query.filter_by(username=username).first()
        if existing_user:
            flash(f'{username} already exist. Please try other username', 'error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username= username, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'{username} user created','success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found. Please register Now!','error')
            return redirect(url_for('register'))
        
        if not check_password_hash(user.password, password):
            flash('Wrong Credentials. Pleaase try again', 'error')
            return redirect(url_for('login'))
    
        session['username']= user.username
        session['role']= user.role
        session.permanent = True
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin')
def admin_panel():
    if 'username' not in session:
        flash('Session expired, Please login again', 'error')
        return redirect(url_for('login'))
    if session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))

    users = User.query.all()
    return render_template('admin_panel.html', users=users)

@app.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('role') !='admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user =User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"User '{user.username}' deleted.", 'success')
    else:
        flash('Error during deletion', 'error')
    return redirect(url_for('admin_panel'))

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if session.get('role') != 'admin':
        return "Access denied"

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin_panel'))

    # Block editing if target user is the 'admin'
    if user.username.lower() == 'admin':
        flash('Editing the Admin user is not allowed.', 'error')
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        new_username = request.form.get('username')
        if new_username:
            user.username = new_username

        new_role = request.form.get('role')
        if new_role:
            user.role = new_role

        new_password = request.form.get('new_password')
        if new_password:
            user.password = generate_password_hash(new_password)

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('edit_user.html', user=user)

@app.route('/admin/create', methods=['GET', 'POST'])
def create_user():
    if session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect(url_for('create_user'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('User created.', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('create_user.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged Out', 'success')
    return redirect(url_for('login'))

@app.route('/test')
def test_flash():
    #error = None
    flash('testing flash','error')
    flash('success flash','success')
    print(dict(session))
    #error ='this is error'
    #return render_template('register.html', error=error)
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)
