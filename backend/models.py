from database import Base
from sqlalchemy import Column , Integer , String , DateTime , Boolean , ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

#id, username, email, password, created_at
class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    #User object has access to all related Task object
    tasks = relationship("Task", back_populates="owner")



#id, title, description, is_done, created_at, owner_id
class Task(Base):
    __tablename__ = "tasks"

    owner_id = Column(Integer , ForeignKey("users.id"))
    id = Column(Integer , primary_key=True)
    title = Column(String)
    description = Column(String)
    is_done = Column(Boolean)
    created_at = Column(DateTime , default=datetime.utcnow)
    #Task object can access its owner User object
    owner = relationship("User", back_populates="tasks")


#line 15 and line 30 establishes a bidirectional relationship like : User.tasks <--> Task.owner