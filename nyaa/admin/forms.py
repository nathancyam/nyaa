from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from nyaa.models import User, UserLevelType, UserStatusType


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

    def level_text(self, level):
        levels = dict(self.levels.choices)
        return levels.get(level)

    def status_text(self, status):
        statuses = {
            UserStatusType.INACTIVE: 'Inactive',
            UserStatusType.BANNED: 'Banned',
            UserStatusType.ACTIVE: 'Active'
        }

        return statuses.get(status)


class MassUserAction(UserAction):

    selected_ids = StringField()

    def execute(self):
        ids = self.data['selected_ids'].split(',')
        ids = [s for s in ids if s.isdigit()]
        [super(MassUserAction, self).execute(user_id) for user_id in ids]
