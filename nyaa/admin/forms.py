from flask_wtf import FlaskForm
from wtforms import SelectField
from nyaa.models import User, UserLevelType


class UserAction(FlaskForm):
    action = SelectField(choices=[
        ('ban', 'Ban'),
        ('promote', 'Promote')
    ])

    levels = SelectField(choices=[
        (UserLevelType.REGULAR, 'Regular'),
        (UserLevelType.TRUSTED, 'Trusted'),
        (UserLevelType.ADMIN, 'Admin'),
        (UserLevelType.SUPERADMIN, 'Super Admin')
    ])

    def execute(self, user_id):
        if self.validate() is False:
            return

        user = User.by_id(user_id)
        if self.data['action'] == 'ban':
            self.ban(user)
        elif self.data['action'] == 'level-change':
            self.update_level(user, self.data['rank'])

    def ban(self, user):
        pass

    def update_level(self, user, rank):
        pass
