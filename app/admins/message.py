from sqladmin import ModelView

from app.models.message import Message


class MessageAdmin(ModelView, model=Message):
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-comment"

    column_searchable_list = [Message.chat_id]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [Message.created_at]

    form_excluded_columns = [Message.id, Message.created_at]

    page_size = 10
    page_size_options = [25, 50]
