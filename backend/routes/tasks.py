from fastapi import APIRouter , Depends, HTTPException , status
from sqlalchemy.orm import Session
from models import Task 
from dependencies import get_current_user
from database import get_db 
from schemas import TaskOut , TaskCreate , TaskUpdate

router = APIRouter()

@router.get("/tasks" , response_model=list[TaskOut])
def get_tasks(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    id = current_user.id
    tasks = db.query(Task).filter(Task.owner_id == id).all()

    return tasks

    

@router.post("/tasks" , response_model=TaskOut)
def post_tasks(task: TaskCreate , current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    new_task = Task(owner_id= current_user.id ,
            title= task.title ,
            description = task.description ,
            is_done= False            
        )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task




#this id is task id
@router.put("/tasks/{id}" , response_model=TaskOut)
def update_task(id: int , task_info: TaskUpdate , current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    #check if task belongs to that user or not
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )


    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="task doesn't belong to current user"
        )

    #update database
    for field, value in task_info.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task
    


@router.delete("/tasks/{id}" , response_model=None)
def delete_task(id: int , current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )


    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="task doesn't belong to current user"
        )
    
    db.delete(task)
    db.commit()

    return "task deleted successfully"


