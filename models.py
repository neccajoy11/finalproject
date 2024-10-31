from sqlalchemy import Column, Integer, String, Float
from personalapi.database import Base


# Exercise Model
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, nullable=True)
    difficulty = Column(String, default="Medium")

# Workout Model
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    duration = Column(Integer)
    exercises = Column(String)  # Comma-separated exercise IDs

# Goal Model
class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    target_date = Column(String)
    progress = Column(Float, default=0.0)
