from flask import Flask, render_template, flash, redirect, url_for
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.config.database import init_db, db
from app.controllers.admin_controller import admin_bp
from app.models.user import Contact
from app.forms.contact_form import ContactForm
from app.commands.create_admin import init_commands
from app.admin.views import init_admin

print("Starting application initialization...")

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# Get the absolute path to the template directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

print(f"Template directory: {template_dir}")
print(f"Static directory: {static_dir}")

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

print("Flask app created")

# Set the secret key from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
print(f"Secret key set: {'Yes' if app.config['SECRET_KEY'] else 'No'}")

# Initialize the database
print("Initializing database...")
init_db(app)
print("Database initialized")

# Initialize Flask-Migrate
print("Setting up migrations...")
migrate = Migrate(app, db)
print("Migrations setup complete")

# Initialize CLI commands
print("Initializing CLI commands...")
init_commands(app)
print("CLI commands initialized")

# Register blueprints
print("Registering blueprints...")
app.register_blueprint(admin_bp, url_prefix='/admin')
print("Blueprints registered")

# Initialize admin
init_admin(app)

@app.route('/')
def index():
    print("Index route accessed")
    context = {
        **get_common_context(),
    }
    print("Rendering index template")
    return render_template('index.html', **context)

def get_common_context():
    return {
        'year': datetime.now().year,
        'server_status': True
    }

# Add a simple test route
@app.route('/test/')
def test():
    return "Test route working!"

@app.route('/about/')
def about():
    context = {
        **get_common_context(),
    }
    return render_template('about.html', **context)

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Save to database
            contact = Contact(
                name=form.name.data,
                phone=form.phone.data,
                message=form.message.data
            )
            db.session.add(contact)
            db.session.commit()
            
            # Send email (existing email code...)
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while sending your message. Please try again later.', 'error')
            print(f"Error: {e}")
    
    return render_template('contact.html', form=form, **get_common_context())

print("Application setup complete")

if __name__ == '__main__':
    print("Starting development server...")
    app.run(debug=True) 