import requests, uuid, os, json
from dotenv import load_dotenv

load_dotenv()

url = f"https://{os.getenv('LANGFLOW_REGION')}.langflow.datastax.com/lf/{os.getenv('LANGFLOW_ID')}/api/v1/run/macros"

payload = {
    "input_type": "text",
    "output_type": "text",
    "session_id": str(uuid.uuid4()),
    "tweaks": {
        "TextInput-V0W1U": {
            "input_value": "Muscle Gain"
        },
        "TextInput-0c1eL": {
            "input_value": "age:22, weight:53, height:173, gender:female"
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

text = r.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
print(json.loads(text))
