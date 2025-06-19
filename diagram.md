###**High level system overview **


+----------------+           +--------------------+           +-----------------------------+
|  Frontend PWA  | <-------> |   API Gateway /    | <-------> |      Backend FastAPI        |
| ReactJS/TS     |   REST    | WebSocket / FCM    |   gRPC    | Cloud Run, PostgreSQL, etc. |
+----------------+           +--------------------+           +-----------------------------+
      |                                                                 |
      |                                                                 v
      |                                                      +----------------------+
      |                                                      |     Agent Layer      |
      |                                                      | (Companion Agents)   |
      |                                                      +----------------------+
      |                                                                 |
      |                                                                 v
      |                                                      +----------------------+
      |                                                      |   Data Warehouse &   |
      |                                                      |     BigQuery         |
      |                                                      +----------------------+



#### ** Frontend Layer (PWA ReactJS + WebSocket + FCM)**

+------------------------+           +-------------------------+
|    User Device /       |<--------->|    PWA (ReactJS)        |
|  Browser (Mobile/Web)  |           +-----------+-------------+
+------------------------+                       |
        |                                        |
        | REST (HTTP/S)                          | Push Notifications
        v                                        v
+------------------------+              +------------------------+
|   API Gateway /        |              |   Firebase Cloud       |
| Cloud Endpoints (REST) |              |     Messaging (FCM)    |
+------------------------+              +------------------------+
        |
        | WebSocket
        v
+------------------------+
|   FastAPI WebSocket    |
+------------------------+



#### **Backend (FastAPI, Cloud SQL, Pub/Sub)**

+------------------------+
|     API Gateway        |
+------------------------+
           |
           v
+------------------------+           +----------------------------+
|  FastAPI Core Service  |<--------->| FastAPI WebSocket Service  |
|    (Cloud Run)         |           +----------------------------+
+-----------+------------+
            |
            |  Operational Data
            v
+------------------------+
|   PostgreSQL (CloudSQL)|
+------------------------+

            |
            | Pub/Sub Topics
            v
+----------------------------+         +----------------------------+
| Agent Comms (Pub/Sub)     |<------->| Real-time Data Ingestion   |
+----------------------------+         +----------------------------+


#### **Agent Layer (GCP ADK Agent Engine)**

+---------------------------+     +---------------------------+     +---------------------------+
|   1. Companion Agent      |     | 2. Adaptive Questionnaire |     | 3. Trend Monitoring Agent |
+-------------+-------------+     +-------------+-------------+     +-------------+-------------+
              |                                   |                                   |
              | Vertex AI LLMs / Tools           | Vertex AI LLMs                    | Custom ML / LLMs
              v                                   v                                   v
     +--------------------+           +--------------------+             +--------------------+
     | Vertex AI LLMs     |           | Vertex AI LLMs     |             | Vertex AI + Custom |
     +--------------------+           +--------------------+             +--------------------+

              ^                                   ^                                   ^
              |                                   |                                   |
              |          API Calls (Internal)     |      BigQuery Client             |
              +---------> Core FastAPI <----------+<---------------------------------+


#### **Data Warehousing & Analytics**


+-----------------------------+
| Pub/Sub (BQ Ingestion)      |
+-----------------------------+
            |
            v
+-----------------------------+
| Cloud Function (BQ Ingester)|
+-----------------------------+
            |
            v
+-----------------------------+
|        BigQuery             |
+-----------------------------+

+-----------------------------+
|  PostgreSQL (Cloud SQL)     |
+-----------------------------+
            |
            v
+-----------------------------+
| Cloud Storage (Staging)     |
+-----------------------------+
            |
            v
+-----------------------------+
|   Batch Load / Dataflow     |
+-----------------------------+
            |
            v
+-----------------------------+
|        BigQuery             |
+-----------------------------+


##### **GCP Supporting Services**
+------------------+    +--------------------+    +-----------------+
|   Cloud Logging  |    |   Cloud Monitoring |    | Secret Manager  |
+------------------+    +--------------------+    +-----------------+

+------------------+    +--------------------+    +-----------------+
|  Cloud Storage   |    |    Cloud Build     |    | Artifact Registry |
| (PWA Assets)     |    |    (CI/CD)         |    | (Docker Images)   |
+------------------+    +--------------------+    +------------------+

+------------------+    +--------------------+
|   Cloud Scheduler|    | IAM / Service Accts|
+------------------+    +--------------------+

