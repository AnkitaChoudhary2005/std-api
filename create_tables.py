
from db import engine, Base

from models import Student



Base.metadata.create_all(bind=engine)



print("Tables created successfully!")
