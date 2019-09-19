from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Association(Base):
    __tablename__ = "associations"

    id = Column(Integer, primary_key=True)
    code = Column(String(36), nullable=False)
    name = Column(String(128))
    slug = Column(String(128))

    members = relationship("Member")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128))
    phone = Column(String(128))
    active = Column(Boolean, default=False)

    association_id = Column(Integer, ForeignKey("associations.id"))
