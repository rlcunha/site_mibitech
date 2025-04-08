from sqlalchemy import create_engine, inspect
import os

DATABASE_URL = "postgresql://postgres:Mfcd62!!Mfcd62!!@server.mibitech.com.br:5432/mibitech"

def check_tables():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print("Tabelas existentes no banco de dados:")
            for table in tables:
                print(f"- {table}")
                
            if 'social_media' in tables:
                print("\nConteúdo da tabela social_media:")
                result = conn.execute("SELECT * FROM social_media")
                for row in result:
                    print(row)
            else:
                print("\nTabela social_media não encontrada")
                
            if 'mensagem' in tables:
                print("\nTabela mensagem existe no banco de dados")
            else:
                print("\nTabela mensagem não encontrada")
                
    except Exception as e:
        print(f"Erro ao verificar tabelas: {str(e)}")

if __name__ == "__main__":
    check_tables()