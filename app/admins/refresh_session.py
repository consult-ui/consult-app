from sqladmin import ModelView

from app.models.refresh_session import RefreshSession


class RefreshSessionAdmin(ModelView, model=RefreshSession):
    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-key"

    column_list = "__all__"

    column_searchable_list = ["user_id", "refresh_token"]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    page_size = 25
    page_size_options = [25, 50, 100, 200]
