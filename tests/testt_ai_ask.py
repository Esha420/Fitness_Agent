import requests, uuid, os
from dotenv import load_dotenv

load_dotenv()

url = f"https://{os.getenv('LANGFLOW_REGION')}.langflow.datastax.com/lf/{os.getenv('LANGFLOW_ID')}/api/v1/run/runflow"

payload = {
    "input_type": "text",
    "output_type": "text",
    "session_id": str(uuid.uuid4()),
    "tweaks": {
        "TextInput-osEzK": {
            "input_value": "How many calories should I eat?"
        },
        "TextInput-rDUdT": {
            "input_value": "age:22, gender:female, height:173, weight:53"
        }
    }
}

headers = {
    "Authorization": f"Bearer {os.getenv('LANGFLOW_TOKEN')}",
    "X-DataStax-Current-Org": os.getenv("ASTRA_ORG_ID"),
    "Content-Type": "application/json",
}

r = requests.post(url, json=payload, headers=headers)
r.raise_for_status()

print(r.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
