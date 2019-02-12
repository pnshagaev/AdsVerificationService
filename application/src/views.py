from functools import wraps

from flask import url_for, redirect, request, abort, jsonify
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib import sqla
from flask_security import current_user

from application.src.roles import RolesTypes, at_least_one_of_roles_in_roles_list, admin_roles
from application.src.scheduler import add_scheduled_job


def redirect_not_autentificated(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('security.login'))
    return wrapper


class BaseModelView(object):

    def _handle_view(self, *args, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class BaseAdminView(BaseModelView):
    @staticmethod
    def is_accessible():
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if at_least_one_of_roles_in_roles_list(admin_roles, current_user.roles):
            return True
        return False


class BaseClientView(BaseModelView):
    @staticmethod
    def is_accessible():
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role(RolesTypes.user.name):
            return True
        return False


class MyHomeView(AdminIndexView, BaseModelView):

    @expose('/')
    @redirect_not_autentificated
    def index(self):
        if at_least_one_of_roles_in_roles_list(admin_roles, current_user.roles):
            return redirect(url_for('user.index_view'))
        return redirect(url_for('client.index'))

    def is_visible(self):
        return False


class UserModelView(BaseAdminView, sqla.ModelView):
    column_sortable_list = []
    column_searchable_list = ('first_name', 'last_name', 'email', 'description')
    column_list = ('full_name', 'email', 'description', 'roles')
    form_columns = ('first_name', 'last_name', 'email', 'description', 'password', 'roles', 'active')
    column_labels = {
        'full_name': 'ФИО',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        '_password': 'Пароль',
        'roles': 'Роли',
        'description': 'Заметки'
    }
    list_template = 'admin/lists/user_list.html'
    action_disallowed_list = ['delete']


class RoleModelView(BaseAdminView, sqla.ModelView):
    column_sortable_list = []
    form_excluded_columns = ('users',)
    can_create = False
    can_delete = False
    can_edit = False

    column_labels = {
        'name': 'Роль',
        'description': 'Описание'
    }
    list_template = 'admin/lists/role_list.html'


class ClientView(BaseView, BaseClientView):

    @expose('/', methods=['GET'])
    @redirect_not_autentificated
    def index(self):
        return self.render('admin/client_index.html')

    @expose('/', methods=['POST'])
    def processing_search_queries(self):
        data = request.form.get('data')
        if data:
            data = data.split('\n')
            add_scheduled_job(current_user.email, data)
            return jsonify(status=200)
        else:
            return jsonify(status=400)

    def is_visible(self):
        return current_user.is_authenticated and at_least_one_of_roles_in_roles_list(admin_roles, current_user.roles)
