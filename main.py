
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from routers.students import routers as students_router


app = FastAPI(title="Student Management API")

app.include_router(students_router)

app.mount(
     "/ui",
     StaticFiles(directory="frontend", html=True),
     name="frontend"
                    )


@app.get("/")

def home():
    return {"message": "Student Management API is running!"}

app.include_router(students_router)
