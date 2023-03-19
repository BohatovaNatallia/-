from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import app, db

import os.path

with app.app_context():
	db.create_all()
# if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
# 	api.create(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# 	api.vesrion_controle(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# else:
# 	api.vesrion_controle(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))