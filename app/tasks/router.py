from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from loguru import logger

from app.dao.session_maker import SessionDep, TransactionSessionDep
from app.services.auth_dep import get_current_user
from app.tasks.dao import TasksDAO
from app.tasks.schemas import STaskCreate, STaskBase, STaskID, STaskUpdate, STaskStatus, TaskFilter

# uvicorn app.main:app --port 8000

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get('/all_tasks/', summary='Получение списка всех задач')
async def get_all_tasks(status: Optional[STaskStatus] = Query(default=None), user: dict = Depends(get_current_user),
                        session: AsyncSession = SessionDep):
    filters = TaskFilter(status=status)
    return await TasksDAO.find_all(session=session, filters=filters)


@router.post("/create_tasks/", summary='Добавление задачи')
async def create_tasks(task_data: STaskCreate, user: dict = Depends(get_current_user),
                       session: AsyncSession = TransactionSessionDep):
    try:
        task_data_dict = task_data.model_dump()
        new_task = await TasksDAO.add(session=session, values=STaskBase(**task_data_dict))
        if new_task:
            return {'message': f'Книга успешно создана!', 'id': new_task.id}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось создать запись')
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при работе с базой данных: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных.")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка: {str(e)}")


@router.put('/update_task/', summary='Обновление книги по ID')
async def update_task(task_id: STaskID, update_data: STaskUpdate, session: AsyncSession = TransactionSessionDep):
    try:
        rez = await TasksDAO.update(session=session, filters=task_id, values=update_data)
        if rez:
            return {'message': f'Запись успешно обновлена!'}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось обновить запись')
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при работе с базой данных: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных.")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка: {str(e)}")


@router.delete('/delete_task_by_id/', summary='Удаление книги по ID')
async def delete_task(task_id: STaskID, session: AsyncSession = TransactionSessionDep):
    try:
        rez = await TasksDAO.delete(session=session, filters=task_id)
        if rez:
            return {'message': f'Задача удалена!'}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось обновить запись')
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при работе с базой данных: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных.")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка: {str(e)}")
