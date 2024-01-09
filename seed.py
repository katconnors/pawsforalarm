

import os
import model
import server

os.system("dropdb pawsforalarm")
os.system("createdb pawsforalarm")
model.database_connect(server.app,"pawsforalarm")
model.database.create_all()

