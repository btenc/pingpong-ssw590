import os
from app.database import create_tables
from app.server.main import app
import app.scheduler as scheduler

create_tables()
scheduler.start()
app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 5000)))
