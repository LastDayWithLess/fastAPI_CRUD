from database import Base, async_engine
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Union, List
from datetime import datetime

class WorkerModel(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    resumes: Mapped[List["ResumeModel"]] = relationship(back_populates="worker")

class ResumeModel(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    compensation: Mapped[Union[int, None]]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    create_at: Mapped[datetime] = mapped_column(server_default=func.now())
    worker: Mapped[WorkerModel] = relationship(back_populates="resumes")


async def async_create():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
