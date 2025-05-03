from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class EnterpriseAccount(Base):
    __tablename__ = "enterprise_accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)

class EnterpriseUser(Base):
    __tablename__ = "enterprise_users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    account_id = Column(String, ForeignKey("enterprise_accounts.id"))

    account = relationship("EnterpriseAccount", backref="members")
