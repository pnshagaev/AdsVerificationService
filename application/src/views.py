from functools import wraps

from flask import url_for, redirect, request, abort, jsonify
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib import sqla
from flask_security import current_user

from application.src.roles import RolesTypes, at_least_one_of_roles_in_roles_list, admin_roles
from application.src.screen_save import search_words


def redirect_not_autentificated(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('security.login'))
    return wrapper


class BaseModelView(object):

    @staticmethod
    def is_accessible():
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

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


class MyHomeView(AdminIndexView, BaseModelView):

    @expose('/')
    @redirect_not_autentificated
    def index(self):
        if current_user.has_role(RolesTypes.superuser.value):
            return redirect(url_for('user.index_view'))
        return redirect(url_for('client.index'))

    def is_visible(self):
        return False


class UserModelView(BaseModelView, sqla.ModelView):
    column_sortable_list = []
    column_searchable_list = ('first_name', 'last_name', 'email', 'description')
    column_list = ('full_name', 'email', 'description', 'roles', 'can_find_in_google')
    form_columns = ('first_name', 'last_name', 'email', 'description', 'password', 'roles', 'google_api_token', 'active')
    column_filters = ('roles',)
    column_labels = {
        'full_name': 'ФИО',
        '_password': 'Пароль',
        'can_find_in_google': 'Поиск в Google',
        'roles': 'Роли',
        'description': 'Заметки'
    }
    list_template = 'admin/lists/user_list.html'


class RoleModelView(BaseModelView, sqla.ModelView):
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

