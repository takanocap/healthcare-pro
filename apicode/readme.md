
Step 1:
create .env file

add below line there --> (SQLServer Database)
DATABASE_URL=mssql+pyodbc://<UserId>:<Password>@<database server instance>/<database name>?driver=ODBC+Driver+17+for+SQL+Server

- just make sure ODBC+Driver+17 is present in your local machine
- for postgresql connction string -> "postgresql://username:password@localhost:5432/mydatabase"

Step 2:
run command:
uvicorn main:app --reload


if needed -- run below command lines:
pip install fastapi uvicorn sqlalchemy pyodbc
pip install python-dotenv
