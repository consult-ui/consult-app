from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.chat import get_user_organization_chats
from app.exceptions import NotFoundError
from app.models.assistant import Assistant
from app.models.chat import Chat
from app.models.user import User
from app.prompts.default import default_chat
from app.service.openai import openai_client


async def add_org_context_to_user_chats(db_session: AsyncSession, user: User, org_id: int) -> None:
    chats = await get_user_organization_chats(db_session, user.id, org_id=None)
    for chat in chats:
        chat.system_prompt = make_system_prompt(user, org_id, chat.system_prompt)


async def create_default_chat(db_session: AsyncSession, user: User, org_id: Optional[int]) -> Chat:
    chat = Chat(
        user_id=user.id,
        organization_id=org_id,
        name="Бизнес ассистент",
        desc="Стандартный чат для общих вопросов",
        system_prompt=make_system_prompt(user, org_id, default_chat),
    )

    await obtain_openai_entities(chat)

    db_session.add(chat)

    await db_session.commit()

    await db_session.refresh(chat)

    return chat


async def create_chat(db_session: AsyncSession, user: User, org_id: Optional[int], assistant_id: int) -> Chat:
    assistant = await db_session.get(Assistant, assistant_id)
    if not assistant:
        raise NotFoundError("Ассистент не найден")

    chat = Chat(
        user_id=user.id,
        organization_id=org_id,
        name=assistant.name,
        desc=assistant.desc,
        color=assistant.color,
        icon_url=assistant.icon_url,
        system_prompt=make_system_prompt(user, org_id, assistant.instruction),
    )

    await obtain_openai_entities(chat)

    db_session.add(chat)

    await db_session.commit()

    await db_session.refresh(chat)

    return chat


async def obtain_openai_entities(chat: Chat) -> None:
    assistant = await openai_client.beta.assistants.create(
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        name=chat.name,
        description=chat.desc,
        instructions=chat.system_prompt,
    )

    chat.openai_assistant_id = assistant.id

    thread = await openai_client.beta.threads.create()

    chat.openai_thread_id = thread.id


def make_system_prompt(user: User, organization_id: Optional[int], assistant_prompt: str) -> str:
    if not organization_id:
        return assistant_prompt

    organization = None
    for organization in user.organizations:
        if organization.id == organization_id:
            break

    if not organization:
        return assistant_prompt

    context_parts = []
    if organization.name:
        context_parts.append(f"Organization Name: {organization.name}")
    if organization.activity_type:
        context_parts.append(f"Activity Type: {organization.activity_type}")
    if organization.tax_number:
        context_parts.append(f"Tax Number: {organization.tax_number}")
    if organization.head_name:
        context_parts.append(f"Head of Organization: {organization.head_name}")
    if organization.address:
        context_parts.append(f"Address: {organization.address}")
    if organization.quarterly_income is not None:
        context_parts.append(f"Quarterly Income: {organization.quarterly_income}")
    if organization.quarterly_expenses is not None:
        context_parts.append(f"Quarterly Expenses: {organization.quarterly_expenses}")
    if organization.number_employees is not None:
        context_parts.append(f"Number of Employees: {organization.number_employees}")
    if organization.average_receipt is not None:
        context_parts.append(f"Average Receipt: {organization.average_receipt}")
    if organization.context:
        context_parts.append(f"Additional Context: {organization.context}")

    organization_context = '\n'.join(context_parts)

    system_prompt = f"{assistant_prompt}\n\nOrganization Context:\n{organization_context}"

    return system_prompt
