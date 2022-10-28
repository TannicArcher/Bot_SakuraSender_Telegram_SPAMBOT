from environs import Env

env = Env()
env.read_env()

ADMINS = env.list("ADMINS")
TOKEN = env.str("TOKEN")
api_id = env.str("api_id")
api_hash = env.str("api_hash")