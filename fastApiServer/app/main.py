from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .model import ClickCount, SessionDep, create_db_and_tables


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://react-client:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _get_user_agent_ip(request: Request) -> str:
    user_agent = request.headers.get("user-agent", "unknown")
    client_ip = request.client.host if request.client else "unknown"
    return f"{client_ip}:{user_agent}"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/clickcount")
def get_click_count(request: Request, session: SessionDep):
    key = _get_user_agent_ip(request)
    click_count = session.get(ClickCount, key)
    if click_count is None:
        click_count = ClickCount(user_agent_ip=key, click_count=0)
        session.add(click_count)
        session.commit()
        session.refresh(click_count)
    return {"user_agent_ip": key, "click_count": click_count.click_count}


@app.get("/clickcount/increment")
def increment_click_count(request: Request, session: SessionDep):
    key = _get_user_agent_ip(request)

    click_count = session.get(ClickCount, key)
    if click_count is None:
        click_count = ClickCount(user_agent_ip=key, click_count=1)
        session.add(click_count)
    else:
        click_count.click_count += 1

    session.commit()
    session.refresh(click_count)

    return {"user_agent_ip": key, "click_count": click_count.click_count}