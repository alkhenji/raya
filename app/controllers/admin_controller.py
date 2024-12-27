from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, Contact
from app.config.database import login_manager, db

admin_bp = Blueprint('admin_routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@admin_bp.route('/login', methods=['GET', 'POST'])
@admin_bp.route('/login/', methods=['GET', 'POST'])
def login():
    print("Admin login route accessed")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin_routes.models'))
        
        flash('Invalid credentials', 'error')
    return render_template('admin/login.html')

@admin_bp.route('/models')
@admin_bp.route('/models/')
@login_required
def models():
    if not current_user.is_admin:
        return redirect(url_for('admin_routes.login'))
    
    models = [
        {'name': 'Users', 'url': url_for('admin_routes.list_users')},
        {'name': 'Contacts', 'url': url_for('admin_routes.list_contacts')},
    ]
    return render_template('admin/models.html', models=models)

@admin_bp.route('/users')
@admin_bp.route('/users/')
@login_required
def list_users():
    if not current_user.is_admin:
        return redirect(url_for('admin_routes.login'))
    
    users = User.query.limit(100).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/contacts')
@admin_bp.route('/contacts/')
@login_required
def list_contacts():
    if not current_user.is_admin:
        return redirect(url_for('admin_routes.login'))
    
    contacts = Contact.query.limit(100).all()
    return render_template('admin/contacts.html', contacts=contacts)

@admin_bp.route('/logout')
@admin_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_routes.login'))

@admin_bp.route('/')
@admin_bp.route('/index/')
@login_required
def index():
    if not current_user.is_admin:
        return redirect(url_for('admin_routes.login'))
    
    recent_users = User.query.order_by(User.id.desc()).limit(10).all()
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(10).all()
    
    return render_template('admin/index.html', 
                         recent_users=recent_users,
                         recent_contacts=recent_contacts) 