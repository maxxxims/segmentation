from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey('users.username', ondelete='cascade'), unique=True)
    loaded_image: Mapped[bool] = mapped_column(default=False)

    start_annotation: Mapped[bool] = mapped_column(default=False)
    selected_class:   Mapped[int] = mapped_column(default=1)
    save_path:        Mapped[str] = mapped_column(default=None, nullable=True)