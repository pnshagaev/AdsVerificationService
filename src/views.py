from functools import wraps
from flask_admin import AdminIndexView, expose, BaseView
from flask_security import current_user
from flask import url_for, redirect
from src.roles import RolesTypes, at_least_one_of_roles_in_roles_list, admin_roles
from flask import jsonify
from flask import request
from src.screen_save import search_words


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
        return redirect(url_for('client.index'))

    def is_visible(self):
        return False


class ClientView(BaseView):
    @expose('/', methods=['GET'])
    @redirect_not_autentificated
    def index(self):
        return self.render('admin/client_index.html')

    @expose('/', methods=['POST'])
    def processing_search_queries(self):
        data = request.form.get('data')
        if data:
            data = data.split('\n')
            search_words(data)
            return jsonify(status=200)
        else:
            return jsonify(status=400)

    def is_visible(self):
        if current_user.is_authenticated and \
                at_least_one_of_roles_in_roles_list(admin_roles, current_user.roles):
            return True
        else:
            return False
