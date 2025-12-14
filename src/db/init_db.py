from sqlalchemy.orm import Session
from ..core import security
from ..db import models
from ..schemas.schemas import UserRole

def init_db(db: Session) -> None:
    # Check for Super Admin
    user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if not user:
        user = models.User(
            email="admin@example.com",
            hashed_password=security.get_password_hash("admin_password"),
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Super Admin created: admin@example.com")
    else:
        print("Super Admin already exists")
