from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = "todos" #This specifies the name of the database table that will be created for this model. In this case, the table will be named "todos".

    id = Column(Integer, primary_key=True, index=True) #This defines a column named "id" that will store integer values. It is set as the primary key for the table, which means it will uniquely identify each record in the table. The index=True argument creates an index on this column to improve query performance.
    title = Column(String) #This defines a column named "title" that will store string values. This column will be used to store the title of each todo item.
    description = Column(String) #This defines a column named "description" that will store string values. This column will be used to store a description of each todo item.
    priority=Column(Integer) #This defines a column named "priority" that will store integer values. This column will be used to indicate the priority level of each todo item, with higher numbers indicating higher priority.
    completed = Column(Boolean, default=False) #This defines a column named "completed" that will store boolean values (True or False). The default=False argument means that if no value is provided for this column when creating a new record, it will default to False, indicating that the todo item is not completed.