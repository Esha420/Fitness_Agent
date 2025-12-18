from astrapy import DataAPIClient
import os
from dotenv import load_dotenv

load_dotenv()

client = DataAPIClient(os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
db = client.get_database_by_api_endpoint(os.getenv("ASTRA_ENDPOINT"))

print(db.list_collection_names())
