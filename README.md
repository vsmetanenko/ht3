# ДЗ: 


```bash
docker run --name hw3 -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
npm i sqlalchemy
npm i alembic
npm i psycopg2-binary
npm i faker
npm i asyncpg
alembic upgrade head  
python seed.py
python my_select.py
```
