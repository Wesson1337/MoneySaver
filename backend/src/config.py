import os

DATABASE_URL = f"{os.getenv('POSTGRES_USER')}:" \
               f"{os.getenv('POSTGRES_PASSWORD')}@" \
               f"{os.getenv('POSTGRES_HOST')}:" \
               f"{os.getenv('POSTGRES_PORT')}/" \
               f"{os.getenv('POSTGRES_DB')}"
