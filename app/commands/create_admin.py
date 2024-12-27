import click
from flask.cli import with_appcontext
from app.models.user import User
from app.config.database import db

@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(email, password):
    """Create an admin user."""
    user = User(email=email, is_admin=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Created admin user: {email}')

def init_commands(app):
    app.cli.add_command(create_admin) 