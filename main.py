from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import models  # Ensure this points to your models file
from database import engine, get_db  # Ensure this points to your database file

# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitLife Tracker API")

# Pydantic Schemas for validation
class ExerciseCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    difficulty: Optional[str] = "Medium"

class WorkoutCreate(BaseModel):
    name: str
    exercises: List[int]
    duration: Optional[int] = 0

class GoalCreate(BaseModel):
    name: str
    description: Optional[str] = None
    target_date: str
    progress: Optional[float] = 0.0

# Exercise Endpoints
@app.post("/exercises/", response_model=ExerciseCreate)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = models.Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@app.get("/exercises/", response_model=List[ExerciseCreate])
def get_exercises(db: Session = Depends(get_db)):
    return db.query(models.Exercise).all()

@app.get("/exercises/{exercise_id}", response_model=ExerciseCreate)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@app.put("/exercises/{exercise_id}", response_model=ExerciseCreate)
def update_exercise(exercise_id: int, exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    for key, value in exercise.dict().items():
        setattr(db_exercise, key, value)

    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db.delete(db_exercise)
    db.commit()
    return {"detail": "Exercise deleted"}

# Workout Endpoints
@app.post("/workouts/", response_model=WorkoutCreate)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    exercises_str = ",".join(map(str, workout.exercises))
    db_workout = models.Workout(name=workout.name, exercises=exercises_str, duration=workout.duration)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.get("/workouts/", response_model=List[WorkoutCreate])
def get_workouts(db: Session = Depends(get_db)):
    return db.query(models.Workout).all()

@app.get("/workouts/{workout_id}", response_model=WorkoutCreate)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@app.put("/workouts/{workout_id}", response_model=WorkoutCreate)
def update_workout(workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db_workout.name = workout.name
    db_workout.exercises = ",".join(map(str, workout.exercises))
    db_workout.duration = workout.duration

    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    db_workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    db.delete(db_workout)
    db.commit()
    return {"detail": "Workout deleted"}

# Goal Endpoints
@app.post("/goals/", response_model=GoalCreate)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    db_goal = models.Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.get("/goals/", response_model=List[GoalCreate])
def get_goals(db: Session = Depends(get_db)):
    return db.query(models.Goal).all()

@app.get("/goals/{goal_id}", response_model=GoalCreate)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@app.put("/goals/{goal_id}", response_model=GoalCreate)
def update_goal(goal_id: int, goal: GoalCreate, db: Session = Depends(get_db)):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    for key, value in goal.dict().items():
        setattr(db_goal, key, value)

    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(db_goal)
    db.commit()
    return {"detail": "Goal deleted"}

# Additional Functions for Fitness App
@app.get("/exercises/category/{category}")
def get_exercises_by_category(category: str, db: Session = Depends(get_db)):
    exercises = db.query(models.Exercise).filter(models.Exercise.category == category).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found in this category")
    return exercises

@app.get("/workouts/duration/{duration}")
def get_workouts_by_duration(duration: int, db: Session = Depends(get_db)):
    workouts = db.query(models.Workout).filter(models.Workout.duration == duration).all()
    if not workouts:
        raise HTTPException(status_code=404, detail="No workouts found with this duration")
    return workouts

@app.get("/goals/progress/total")
def get_total_goal_progress(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).all()
    total_progress = sum(goal.progress for goal in goals)
    return {"total_progress": total_progress}

@app.get("/exercises/difficulty/{difficulty}")
def get_exercises_by_difficulty(difficulty: str, db: Session = Depends(get_db)):
    exercises = db.query(models.Exercise).filter(models.Exercise.difficulty == difficulty)