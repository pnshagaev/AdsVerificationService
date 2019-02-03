from flask_admin import AdminIndexView, expose
from flask_security import current_user
from flask import url_for, redirect


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return redirect('admin/user')
        else:
            return redirect(url_for('security.login'))

    def is_visible(self):
        return False