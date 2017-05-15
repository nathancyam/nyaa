from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, ValidationError
from wtforms.validators import InputRequired
from wtforms.widgets import HiddenInput
from nyaa import db
from nyaa.models import User, UserLevelType, UserStatusType


def existing_level(form, field):
    levels = [
        UserLevelType.REGULAR,
        UserLevelType.TRUSTED,
        UserLevelType.ADMIN,
        UserLevelType.SUPERADMIN
    ]

    if field.data in levels is False:
        raise ValidationError('Specified level does not exist')


class UserRowAction(FlaskForm):

    banned = IntegerField(widget=HiddenInput())

    levels = IntegerField('levels', [InputRequired(), existing_level], widget=HiddenInput())

    def execute(self, user_id):
        if self.validate() is False:
            return

        user = User.by_id(user_id)

        self.update_ban_status(user, self.data['banned'])
        self.update_level(user, self.data['levels'])

        db.session.commit()

    def update_ban_status(self, user, form_value):
        if form_value == UserStatusType.BANNED.value:
            user.status = UserStatusType.BANNED
        else:
            user.status = UserStatusType.ACTIVE

    def update_level(self, user, level):
        user.level = level

    def level_text(self, level):
        levels = {
            UserLevelType.REGULAR: 'Regular',
            UserLevelType.TRUSTED: 'Trusted',
            UserLevelType.ADMIN: 'Admin',
            UserLevelType.SUPERADMIN: 'Super Admin'
        }

        return levels.get(level)

    def status_text(self, status):
        statuses = {
            UserStatusType.INACTIVE: 'Inactive',
            UserStatusType.BANNED: 'Banned',
            UserStatusType.ACTIVE: 'Active'
        }

        return statuses.get(status)


class UserMassAction(UserRowAction):
    pass
