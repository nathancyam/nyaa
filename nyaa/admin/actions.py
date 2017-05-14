from .forms import UserAction


class UpdateUserAction(object):

    def execute(self, form):
        if form.validate():

