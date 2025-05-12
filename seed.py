import os
from model import database, database_connect
import server

# will drop the db


def reset_pfa():
    os.system("dropdb pawsforalarm")
    os.system("createdb pawsforalarm")

    database_connect(server.app, "pawsforalarm")
    database.create_all()


if __name__ == "__main__":
    reset_pfa()
