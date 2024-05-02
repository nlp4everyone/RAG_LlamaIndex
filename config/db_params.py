from dotenv import load_dotenv
import os
load_dotenv()

# Elastic Search
ES_NAME = os.getenv("ES_NAME")
ES_CLOUD_ID = os.getenv("ES_CLOUD_ID")
ES_API_KEY = os.getenv("ES_API_KEY")

# Upstash
UPSTASH_URL = os.getenv("UPSTASH_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_TOKEN")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_TOKEN = os.getenv("QDRANT_TOKEN")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")