from flask import Flask, render_template, flash, redirect, url_for
from datetime import datetime
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.forms.contact_form import ContactForm

# Load environment variables
load_dotenv()

# Get the absolute path to the template directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

# Set the secret key from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def get_common_context():
    """Get common context variables for all templates"""
    return {
        'year': datetime.now().year,
        'server_status': True  # You can make this dynamic
    }

@app.route('/')
def index():
    context = {
        **get_common_context(),
    }
    return render_template('index.html', **context)

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
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = os.getenv('MAIL_USERNAME')
            msg['To'] = 'info@sanid.qa'
            msg['Subject'] = f"New Contact Form Submission from {form.name.data}"
            
            body = f"""
            New contact form submission:
            
            Name: {form.name.data}
            Phone: {form.phone.data}
            Message: {form.message.data}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT'))) as server:
                server.starttls()
                server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
                server.send_message(msg)
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'error')
            print(f"Error sending email: {e}")
    
    return render_template('contact.html', form=form, **get_common_context())

# Make sure this is at the bottom of the file if you're running directly
if __name__ == '__main__':
    print(f"Template directory: {template_dir}")  # Debug print
    print("Available routes:")
    print([rule.rule for rule in app.url_map.iter_rules()])  # This will print all registered routes
    app.run(debug=True) 