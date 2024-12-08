from sqlalchemy import create_engine
import psycopg2


db_user = "postgres"
db_password = "password"
db_host = "localhost"
db_port = 5433

try:
    # Usa psycopg2 come driver
    engine = create_engine(
        f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres')
    with engine.connect() as connection:
        print("Connessione al database riuscita!")
except Exception as e:
    print(f"Errore di connessione: {e}")
