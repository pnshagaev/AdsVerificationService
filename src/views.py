from functools import wraps
from flask_admin import AdminIndexView, expose
from flask_security import current_user
from flask import url_for, redirect
from src.roles import RolesTypes


def redirect_not_autentificated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('security.login'))
    return wrapper


class MyHomeView(AdminIndexView):
    @expose('/')
    @redirect_not_autentificated
    def index(self):
        if current_user.has_role(RolesTypes.SUPERUSER.value):
            return redirect(url_for('user.index_view'))
        return redirect(url_for('role.index_view'))

    def is_visible(self):
        return False

    @expose('/search')
    @redirect_not_autentificated
    def search(self):
        return redirect(url_for('role.index_view'))
