from flask import g, render_template, abort, request, redirect
from flask.views import View, MethodView
from nyaa.models import User
from .forms import UserRowAction, UserMassAction


def admin_required(f):
    def decorator(*args, **kwargs):
        if not g.user or not g.user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorator


class AdminUserView(MethodView):

    decorators = [admin_required]

    template = 'admin/users.html'

    mass_action_form = UserMassAction

    def get(self):
        users = User.query.all()
        form = self.mass_action_form(request.form)
        return render_template(self.template, users=users, form=form)

    def post(self):
        form = self.mass_action_form(request.form)
        return redirect('/admin/users')


class UpdateUserRowView(View):

    decorators = [admin_required]

    methods = ['POST']

    row_form = UserRowAction

    def dispatch_request(self, user_id):
        form = self.row_form(request.form)
        form.execute(user_id)
        return redirect('/admin/users')
