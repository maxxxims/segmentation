from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import Base
from uuid import uuid4, UUID
from datetime import datetime


class User2Task(Base):
    __tablename__ = "user2tasks"
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(ForeignKey('users.username', ondelete='CASCADE'))
    task_id: Mapped[str] = mapped_column(ForeignKey('tasks.id', ondelete='CASCADE'))
    attempt_number: Mapped[int] = mapped_column(default=1)
    finished: Mapped[bool] = mapped_column(default=False)
    is_choosen: Mapped[bool] = mapped_column(default=False)
    metric: Mapped[float] = mapped_column(default=None, nullable=True)
    save_folder: Mapped[str] = mapped_column(default=None, nullable=True)