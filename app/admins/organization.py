from sqladmin import ModelView

from app.models.organization import Organization


class OrganizationAdmin(ModelView, model=Organization):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    icon = "fa-solid fa-briefcase"

    column_searchable_list = [Organization.name, Organization.tax_number, Organization.head_name]
    column_sortable_list = [
        "id",
        "created_at",
    ]

    column_exclude_list = [Organization.updated_at]

    form_excluded_columns = [Organization.id, Organization.created_at, Organization.updated_at]

    page_size = 50
    page_size_options = [25, 50, 100, 200]
