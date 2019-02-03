
from flask import url_for, redirect, request, abort
from flask_admin.contrib import sqla
from flask_security import current_user


class BaseModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
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


class UserModelView(BaseModelView):
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


class RoleModelView(BaseModelView):
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