from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import Base
from uuid import uuid4, UUID
from datetime import datetime as dt
import datetime


def get_current_time() -> str:
    offset = datetime.timedelta(hours=3)
    tz = datetime.timezone(offset=offset, name='МСК')
    now = dt.now(tz=tz)
    return now


class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(ForeignKey('users.username', ondelete='cascade'), unique=True)
    loaded_image: Mapped[bool] = mapped_column(default=False)

    start_annotation: Mapped[bool] = mapped_column(default=False)
    selected_class:   Mapped[int] = mapped_column(default=1)
    show_polygons:    Mapped[bool] = mapped_column(default=True)
    save_path:        Mapped[str] = mapped_column(default=None, nullable=True)
    
    line_width:       Mapped[int] = mapped_column(default=2.15)
    fill_opacity:     Mapped[float] = mapped_column(default=0.85)
    line_opacity:     Mapped[float] = mapped_column(default=0.4)
    zoom_value:       Mapped[float] = mapped_column(default=0.9)
    wheel_zoom:       Mapped[bool]  = mapped_column(default=False)
    opened_settings:  Mapped[bool]  = mapped_column(default=True)
    
    last_activity:    Mapped[datetime.datetime] = mapped_column(onupdate=get_current_time,
                                                                default=get_current_time)