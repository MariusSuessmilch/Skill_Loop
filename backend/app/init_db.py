from app.db.session import engine
from app.db import models
from app.db.user import User

models.Base.metadata.create_all(bind=engine)
print("Database tables created.")
