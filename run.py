from app.database import create_tables
from app.server.main import app
import app.scheduler as scheduler

create_tables()
scheduler.start()
app.run()
