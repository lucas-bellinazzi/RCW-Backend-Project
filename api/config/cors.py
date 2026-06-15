import os
from flask_cors import CORS
from src.utils.constants import ENVIRONMENTS

frontend_url = os.getenv("FRONT_END_URL")

def configure_cors(app):
    origins_map = {
        ENVIRONMENTS.LOCAL.value: ["*"],
        ENVIRONMENTS.PRODUCTION.value: [frontend_url]
    }    
    
    environment = os.getenv("ENVIRONMENT")
    
    allowed_origin = origins_map.get(environment, origins_map[ENVIRONMENTS.PRODUCTION.value])     

    CORS(app, origins = allowed_origin)