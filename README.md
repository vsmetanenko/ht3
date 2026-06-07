# ДЗ: 


```bash
docker run --name hw3 -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
pip install sqlalchemy
pip install alembic
pip install psycopg2-binary
pip install faker
pip install asyncpg
alembic upgrade head  
python seed.py
python my_select.py
```
