from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.sql import text
app = Flask(__name__)

@app.route("/")
def hello_cbna():
    return "<p>Hello, CBNA!</p>"


engine = create_engine("postgresql://cbna:akQU0nTmDVr2tOOQAdoIF2CD5A6LmSjn@dpg-cug94hqj1k6c738kjs00-a.frankfurt-postgres.render.com/cbna")


def appBD():
    with engine.connect() as conn:
        stmt = text("select * from cbna")
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    appBD()
    app.run()