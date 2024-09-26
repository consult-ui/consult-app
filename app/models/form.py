from sqlalchemy import Text, TIMESTAMP, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.sql import func

from app.db import Base


class ContactRequest(Base):
    __tablename__ = "contact_request"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"