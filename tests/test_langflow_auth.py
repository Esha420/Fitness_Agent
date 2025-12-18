import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

url = f"https://{os.getenv('LANGFLOW_REGION')}.langflow.datastax.com/lf/{os.getenv('LANGFLOW_ID')}/api/v1/run/runflow"

headers = {
    "Authorization": f"Bearer {os.getenv('LANGFLOW_TOKEN')}",
    "X-DataStax-Current-Org": os.getenv("ASTRA_ORG_ID"),
    "Content-Type": "application/json",
}

payload = {
    "input_type": "text",
    "output_type": "text",
    "session_id": str(uuid.uuid4()),
    "tweaks": {}
}

r = requests.post(url, json=payload, headers=headers)

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)
