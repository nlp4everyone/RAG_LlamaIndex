from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider,ServiceChatModel
from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService,_QDRANT_COLLECTION
from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenEmbeddingProvider
from ai_modules.embedding_modules.service_embedding import ServiceEmbedding
from llama_index.core.ingestion import IngestionPipeline
from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
from system_component.system_logging import Logger
from ai_modules.query_modules.custom_query_engine import BaseQueryEngine

# Init embedding
# open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
# embedding_model = open_embedding.get_embedding_model()
service_embedding = ServiceEmbedding(service_name="COHERE",model_name="embed-english-light-v3.0")
embedding_model = service_embedding.get_embedding_model()

# Init vector stor service
qdrant_service = QdrantService(mode="local")
# es_service = ElasticSearchService()
# mongo_service = MongoService()

# Define large language model
service_provider = ServiceChatModel()
llm = service_provider.get_chat_model()

# Web url for crawling
web_url = "https://en.wikipedia.org/wiki/Neymar"



def insert_data(url=web_url):
    # Load data
    web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
    docs = web_loader.load_data(url)

    # Ingestion
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=1000, chunk_overlap=200),
        ],
    )
    nodes = pipeline.run(documents=docs)

    # Convert nodes to docs
    docs = utils.convert_nodes_to_docs(nodes)

    # Build index
    # index = mongo_service.build_index_from_nodes(nodes=nodes,embedding_model=embedding_model)
    index = qdrant_service.build_index_from_docs(documents=docs, embedding_model=embedding_model)
    # es_service.build_index_from_docs(documents=docs,embedding_model=embedding_model)
    return index

def main():
    # When collection is not existed, create new collection
    if not qdrant_service.collection_exists(collection_name=_QDRANT_COLLECTION):
        insert_data()

    # storage_context = StorageContext.from_defaults(index_store=index_store)
    # index = load_index_from_storage(storage_context,embed_model=embedding_model)
    # Query Data
    index = qdrant_service.load_index(embedding_model=embedding_model)
    # index = es_service.load_index(embedding_model=embedding_model)
    # index = mongo_service.load_index(embedding_model=embedding_model)
    # query_engine = index.as_query_engine(llm=llm,verbose=True)
    # response = query_engine.query("Who is Neymar?")
    # print("Response")
    # print(response)

    # Define query engine
    query_engine = BaseQueryEngine(index=index,chat_model=llm)
    # Print response
    response = query_engine.query("Who is Neymar?")
    print("Response")
    print(response)
    # Logger.info(f"Response: {response}")

    # Print retrieval
    retrieval_docs,_ = query_engine.retrieve(query="Who is Neymar?")
    # Logger.info(f" ")
    # Logger.info(retrieval_docs)
    print("Retrival doc:")
    print(_)


if __name__ == "__main__":
    main()