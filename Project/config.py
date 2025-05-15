from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    bot_token: str

def load_config() -> Config:
    env = Env()
    env.read_env()
    
    return Config(
        bot_token=env.str("BOT_TOKEN")
    ) 