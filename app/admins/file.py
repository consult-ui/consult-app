from sqladmin import ModelView

from app.models.file import File


class FileAdmin(ModelView, model=File):
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True

    icon = "fa-solid fa-file"

    column_searchable_list = [File.name, File.chat_id]
    column_sortable_list = [
        File.created_at
    ]

    column_exclude_list = [File.updated_at]

    form_excluded_columns = [File.id, File.created_at, File.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]
