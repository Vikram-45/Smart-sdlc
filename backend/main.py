from fastapi import FastAPI 
from routers import pdf
from routers import generate
from routers import chat
from routers import bug
from routers import test     
from routers import feedback                
app = FastAPI()

app.include_router(pdf.router)
app.include_router(generate.router)
app.include_router(bug.router)
app.include_router(test.router)
app.include_router(chat.router)
app.include_router(feedback.router)


