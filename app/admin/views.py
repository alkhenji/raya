from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from app.models.user import User, Contact
from app.config.database import db

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin_routes.login', next=request.url))
        return redirect(url_for('index'))

class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('admin_routes.login'))
        return super(AdminView, self).index()

    def is_visible(self):
        # Only show in navigation if user is authenticated and admin
        return current_user.is_authenticated and current_user.is_admin

def init_admin(app):
    admin = Admin(
        app, 
        name='Raya Admin', 
        template_mode='bootstrap4', 
        index_view=AdminView(url='/admin', endpoint='admin')
    )
    admin.add_view(SecureModelView(User, db.session, name='Users'))
    admin.add_view(SecureModelView(Contact, db.session, name='Contacts')) 