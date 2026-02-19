from sqlalchemy import create_engine
import psycopg2
import pandas as pd

engine_remote = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
conn_remote = psycopg2.connect('postgres://postgres:postgres@localhost:5432/postgres')
df =pd.read_sql("select*from goods", conn_remote)

print(df)