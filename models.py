from __future__ import annotations

from app import db, Base
from sqlalchemy import func, ForeignKey, Column, Table, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy_utils import EmailType
from flask_login import UserMixin
from datetime import datetime, timezone


class TimestampMixin:
    created: Mapped[datetime] = mapped_column(default=func.now())
    updated: Mapped[datetime] =  mapped_column(
        default=func.now(),
        onupdate=datetime.now(timezone.utc))


class RoomParticipants(db.Model):
    __tablename__ = 'room_participants'
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True)
    

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] 
    email: Mapped[str]
    bio: Mapped[str] = mapped_column(nullable=True)
    
    user_messages: Mapped[list["Message"]] = relationship(back_populates="user")
    
    rooms: Mapped[list["Room"]] = relationship(back_populates="participants", secondary="room_participants")
    
    
class Room(TimestampMixin, db.Model):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    host_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    topic: Mapped[str]
    name: Mapped[str]
    description: Mapped[str]
    
    participants: Mapped[list["User"]] = relationship(back_populates="rooms", secondary="room_participants")
    
    room_messages: Mapped[list["Message"]] = relationship(back_populates="room", cascade="all, delete")
           
    
class Message(TimestampMixin, db.Model):
    __tablename__ = 'messages'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    body: Mapped[str]
    
    user: Mapped["User"] = relationship(back_populates="user_messages")
    
    room: Mapped["Room"] = relationship(back_populates="room_messages")
   

    
    
    