from sqladmin import ModelView

from app.models.chat import Chat


class ChatAdmin(ModelView, model=Chat):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-headset"

    column_searchable_list = [Chat.name, Chat.desc, Chat.system_prompt]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [Chat.updated_at]

    form_excluded_columns = [Chat.id, Chat.created_at, Chat.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]
