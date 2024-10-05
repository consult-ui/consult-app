from sqladmin import ModelView
from wtforms import fields
from wtforms.validators import DataRequired

from app.models.user import User
from app.utils.auth import ph


class PasswordField(fields.PasswordField):
    def _value(self):
        if self.data:
            return ph.hash(self.data)
        return ""

    def process_formdata(self, valuelist):
        if not valuelist:
            raise ValueError("Invalid password")
        try:
            self.data = ph.hash(valuelist[0])
        except ValueError:
            raise ValueError("Invalid password")


class UserAdmin(ModelView, model=User):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-user"

    column_searchable_list = ["phone_number", "email", "first_name", "last_name"]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [User.password, User.updated_at]

    page_size = 25
    page_size_options = [25, 50, 100, 200]

    form_columns = [
        User.phone_number,
        User.email,
        User.password,
        User.first_name,
        User.last_name,
        User.expiration_date,
        User.whatsapp_url,
        User.telegram_url,
    ]

    form_overrides = dict(password=PasswordField)

    form_args = dict(
        password=dict(
            label="Password",
            validators=[DataRequired()],
        )
    )
