'''
Настройки сервиса
'''

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 2000

DB_KEY = 'Postgres'

WHITE_LIST = ('/login', '/register')
