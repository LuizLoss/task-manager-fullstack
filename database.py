from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. URL de conexão
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# 2. Cria o motor de conexão (engine)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 3. Cria a fábrica de sessões do banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Classe base para criarmos os modelos das tabelas
Base = declarative_base()

# 5. Função geradora (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()