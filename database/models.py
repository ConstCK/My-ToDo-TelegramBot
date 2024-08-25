import datetime

from sqlalchemy import BigInteger, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.config import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    tasks: Mapped[list['Task']] =relationship()


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    tasks: Mapped[list['Task']] = relationship(back_populates='category')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    expire_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'))
    status: Mapped[str] = mapped_column(String(16), default='Выполняется')
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped['Category'] = relationship(back_populates='tasks')



