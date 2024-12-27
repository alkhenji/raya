from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_routes.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Ensure anonymous users are handled properly
    login_manager.session_protection = None
    
    with app.app_context():
        db.create_all()
        
        # Print debug info
        print("Database initialized")
        from app.models.user import User
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            print(f"Admin user exists: {admin.email}")
        else:
            print("No admin user found") 