from sqladmin import ModelView

from app.models.assistant import Assistant


class AssistantAdmin(ModelView, model=Assistant):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-robot"

    column_list = "__all__"
    column_searchable_list = [Assistant.name, Assistant.desc, Assistant.instruction]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    form_excluded_columns = [Assistant.id, Assistant.created_at, Assistant.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]
