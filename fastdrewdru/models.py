import uuid

from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from fastdrewdru.db import get_db_service

db_service = get_db_service()
Base = declarative_base(bind=db_service.engine, metadata=db_service.metadata)


class UserModel(Base):
    __tablename__ = "user"

    # user personal info
    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    uid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(254), unique=True)
    password = Column(String(64))
    first_name = Column(String(50))
    patronymic = Column(String(50))
    last_name = Column(String(50))
    # user configs
    lang = Column(String(2), nullable=False, default="en")
    # permissions
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)

    @property
    def full_name(self):
        return " ".join(
            filter(lambda x: x, [self.first_name, self.patronymic, self.last_name])
        )

    def __repr__(self):
        return f"<UserModel({self.id}, {self.username}, {self.uid})>"

    def __str__(self):
        return self.full_name or self.username
