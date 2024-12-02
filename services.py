from typing import TYPE_CHECKING

import database as _database
import models as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
async def create_contact(contact: _schemas.CreateContact, db: "Session") -> _schemas.Contact:
    # 1. pydantic 모델을 SQLAlchemy 모델로 변환
    contact = _models.Contact(**contact.model_dump())
    
    # 2. DB 세션에 추가
    db.add(contact)
    
    # 3. 커밋하여 데이터베이스에 반영
    db.commit()
    
    # 4. DB에서 업데이트된 객체 불러오기
    db.refresh(contact)
    
    # 5. Pydantic 모델로 변환하여 반환
    return _schemas.Contact.model_validate(contact)