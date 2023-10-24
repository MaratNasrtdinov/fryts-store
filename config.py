import environ
environ.Env.read_env()

env = environ.Env(
    TOKEN=(str),
    admins=(str),
    manager_id=(str)
)

TOKEN = env('TOKEN')

# Id for manager and administrator
ADMINS = env('ADMINS')
MANAGER = env('MANAGER')
