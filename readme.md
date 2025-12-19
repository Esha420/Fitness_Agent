# AI-Powered Personal Fitness Tool

A modern, full-stack fitness application that leverages **Generative AI** for personalized nutrition coaching, **Cerbos** for attribute-based access control (ABAC), and **DataStax Astra DB** for scalable, vector-enabled data storage.

---

## Overview

This system is designed to provide users with a secure, AI-driven fitness experience. It doesn't just store data; it interprets it through specialized AI agents while ensuring that every piece of personal information is strictly protected by fine-grained authorization policies.



## Key Features

- **AI Macro Calculation**: Personalized nutrition targets generated via Langflow based on activity level, weight, and fitness goals.
- **Fitness QA Agent**: An interactive AI assistant that uses MCP (Model Context Protocol) patterns to provide context-aware fitness advice.
- **Attribute-Based Access Control (ABAC)**: Powered by Cerbos, ensuring users can only view, edit, or delete their own profiles and notes.
- **Vector-Ready Storage**: Built on Astra DB, allowing for future semantic search capabilities over user notes and workout history.
- **Agent Metrics**: Real-time logging of AI latency and success rates for performance monitoring.

## Tech Stack

| Component          | Technology                         |
|-------------------|------------------------------------|
| **Frontend** | Streamlit                          |
| **Database** | DataStax Astra DB (Serverless)     |
| **AI Orchestration**| Langflow (DataStax)              |
| **Authorization** | Cerbos (PDP via Docker)            |
| **Data Layer** | Astrapy (Data API)                 |

---

## System Architecture

The application follows a modular architecture:

1.  **Identity Layer**: Assigns unique identifiers and roles (User/Agent).
2.  **Authorization Layer**: Before any DB write/delete, the system queries the **Cerbos PDP** to validate permissions based on resource ownership.
3.  **Intelligence Layer**: Connects to **Langflow** DAGs to process user queries and nutrition logic.
4.  **Persistence Layer**: Stores profiles, notes (with vector embeddings), and performance metrics in **Astra DB**.



---

## Setup & Installation

### 1. Environment Variables
Create a `.env` file in the root directory:
```env
# Astra DB
ASTRA_ENDPOINT="your_astra_endpoint"
ASTRA_DB_APPLICATION_TOKEN="your_astra_token"
ASTRA_ORG_ID="your_org_id"

# Langflow
LANGFLOW_ID="your_flow_id"
LANGFLOW_TOKEN="your_langflow_token"
LANGFLOW_REGION="your_region"
```

### 2. Run Cerbos (Authorization Engine)

Cerbos runs as a sidecar container. Ensure your policies are in the /policies folder:
```
docker run -d \
  --name cerbos \
  -p 3592:3592 \
  -v $(pwd)/policies:/policies \
  ghcr.io/cerbos/cerbos:latest
  ```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Launch the App
```
export PYTHONPATH=$PYTHONPATH:.
streamlit run app/main.py
```

---
## Security Policy (Cerbos)

The system implements the following logic:

* Profiles: Only the owner can read or update.

* Notes: Users can write notes. They can only delete a note if the user_id on the note matches their own ID.

* Agents: Specialized roles can access the call action for specific internal metrics.

## Monitoring

All AI interactions are logged to the mcp_metrics collection in Astra DB, tracking:

* Latency: Time taken for Langflow to respond.
* Status: Success/Failure rates.
* Agent Type: Categorization of queries (QA vs. Macros).