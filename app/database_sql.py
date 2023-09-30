from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///database.db"
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

