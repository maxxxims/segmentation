from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    image_name: Mapped[str] = mapped_column(unique=True)
    path_to_json: Mapped[str] = mapped_column()
    path_to_image: Mapped[str] = mapped_column()
    path_to_annotated_image: Mapped[str] = mapped_column()