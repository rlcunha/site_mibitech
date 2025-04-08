from sqlalchemy import create_engine, text
import os

DATABASE_URL = "postgresql://postgres:Mfcd62!!Mfcd62!!@server.mibitech.com.br:5432/mibitech"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Conexão bem-sucedida! Resultado do teste:", result.scalar())
except Exception as e:
    print("Erro na conexão com o banco de dados:", str(e))