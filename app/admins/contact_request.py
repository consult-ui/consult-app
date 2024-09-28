from sqladmin import ModelView, action

from app.models.form import ContactRequest


class ContactRequestAdmin(ModelView, model=ContactRequest):
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True

    icon = "fa-solid fa-poll-people"

    column_searchable_list = ["name", "email", "phone_number"]
    column_sortable_list = ["id", "created_at", "is_processed"]

    column_exclude_list = []

    page_size = 25
    page_size_options = [25, 50, 100, 200]

    contact_request_columns = [
        ContactRequest.name,
        ContactRequest.email,
        ContactRequest.phone_number,
        ContactRequest.created_at,
        ContactRequest.is_processed
    ]

    contact_request_args = dict(
        email=dict(
            label="Email",
        ),
        phone_number=dict(
            label="Телефон",
        )
    )

    column_default_sort = ("is_processed", False)


@action('mark_processed', 'Пометить как обработанную',
        'Вы уверены, что хотите пометить выбранные заявки как обработанные?')
def action_mark_processed(self, ids):
    try:
        for id in ids:
            contact_request_user = self.get_one(id)
            if contact_request_user:
                contact_request_user.is_processed = True
                self.session.commit()
        self.flash('Заявки успешно помечены как обработанные.')
    except Exception as e:
        self.flash('Ошибка при пометке заявок: {}'.format(str(e)), 'error')
