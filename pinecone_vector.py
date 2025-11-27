import os
import time
import re
import concurrent.futures
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import ServerlessSpec
from tqdm import tqdm
from dotenv import load_dotenv

def split_docs(documents, chunk_size=1500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# Load environment variables
load_dotenv()

# Initialize embeddings
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize Pinecone client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = 'endometriosis'

# Check if index exists; if not, create it
existing_indexes = pc.list_indexes()
existing_index_names = [index.name for index in existing_indexes.indexes]
if index_name not in existing_index_names:
    pc.create_index(
        name=index_name,
        dimension=768,  # Dimension for Google's embedding-001
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    print(f"Created Pinecone index: {index_name}")
    time.sleep(60)  # Wait for index to be ready
pinecone_index = pc.Index(index_name)

# Helper to parse retry wait time from error messages
def parse_retry_wait_time(error):
    if hasattr(error, 'response') and error.response is not None:
        retry_after = error.response.headers.get('Retry-After')
        if retry_after:
            return int(retry_after)
    error_message = str(error)
    match = re.search(r'(\d+)s', error_message)
    return int(match.group(1)) if match else 20

# Helper function to embed a single batch with retry logic
def embed_batch_with_retry(embed_model, batch_contents, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return embed_model.embed_documents(batch_contents)
        except Exception as e:
            print(f"Error while embedding batch on attempt {attempt+1}: {e}")
            wait_time = parse_retry_wait_time(e)
            print(f"Waiting {wait_time}s before retrying...")
            time.sleep(wait_time)
            if attempt == max_attempts - 1:
                raise

# Parallelize embedding calls using a ThreadPoolExecutor
def concurrent_embed_documents(embed_model, documents, batch_size=100, max_workers=4):
    all_embeddings = []
    all_contents = []
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_contents = [doc.page_content for doc in batch]
            futures.append((executor.submit(embed_batch_with_retry, embed_model, batch_contents), batch_contents))
        
        for future, contents in tqdm(futures, total=len(futures), desc="Embedding batches"):
            try:
                batch_embeddings = future.result()
                all_embeddings.extend(batch_embeddings)
                all_contents.extend(contents)
            except Exception as e:
                print(f"Error in embedding batch: {e}")
    return all_embeddings, all_contents

# Load documents from PDF
pdf_file_path = 'Endometriosis Health Guidance Chatbot.pdf'
pdf_loader = PyPDFLoader(pdf_file_path)
documents = pdf_loader.load()

# Split documents
docs = split_docs(documents, chunk_size=1500, chunk_overlap=100)

# Generate embeddings concurrently
all_embeddings, all_batch_content = concurrent_embed_documents(embed_model, docs, batch_size=50, max_workers=4)

# Batch upsert vectors to Pinecone
BATCH_SIZE = 100
vectors_to_upsert = [
    (str(idx), embedding, {"text": content})
    for idx, (embedding, content) in enumerate(zip(all_embeddings, all_batch_content))
]

def batch_upsert(index, vectors, batch_size=BATCH_SIZE):
    batches = [vectors[i:i+batch_size] for i in range(0, len(vectors), batch_size)]
    for batch_number, batch in enumerate(tqdm(batches, desc="Upserting batches", total=len(batches))):
        for attempt in range(3):
            try:
                index.upsert(vectors=batch)
                break
            except Exception as e:
                print(f"Upsert error on batch {batch_number+1}, attempt {attempt+1}: {e}")
                if attempt < 2:
                    wait_time = 10 * (attempt + 1)
                    print(f"Waiting {wait_time}s before retrying...")
                    time.sleep(wait_time)
                else:
                    print(f"Batch {batch_number+1} failed after 3 attempts.")
                    raise e

print("\nStarting Pinecone batched upserts...\n")
batch_upsert(pinecone_index, vectors_to_upsert)
print("\nPinecone vector storage complete!\n")