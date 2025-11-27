# 🌸 Endometriosis Health Guidance Chatbot

Welcome to the 🌸 Endometriosis Health Guidance Chatbot! 🎉 This practicum is designed to demonstrate how to build a helpful chatbot using Large Language Models (LLMs), vector databases, and Streamlit for the user interface.

This README will guide you step-by-step from setting up the project to understanding its core components. Whether you're new to Python, LLMs, or even coding, we aim to make this journey smooth and educational!

**GitHub Repository:** https://github.com/GRACENGARI/TAMBUA-WOMENINTECH-CHATBOT

---

## 📚 Table of Contents

* [About The Project](#about-the-project)
* [✨ Features](#-features)
* [🛠️ Tech Stack](#️-tech-stack)
* [🚀 Getting Started](#-getting-started)
    * [Prerequisites](#prerequisites)
    * [Cloning the Repository](#cloning-the-repository)
    * [Setting up in VS Code](#setting-up-in-vs-code)
    * [Installation](#installation)
    * [Environment Variables (.env file)](#environment-variables-env-file)
* [🏃‍♀️ Running the Project](#️-running-the-project)
    * [Step 1: Prepare Your Knowledge Base (PDF)](#step-1-prepare-your-knowledge-base-pdf)
    * [Step 2: Populate the Vector Database (`pinecone_vector.py`)](#step-2-populate-the-vector-database-pinecone_vectorpy)
    * [Step 3: Run the Chatbot Application (`main.py`)](#step-3-run-the-chatbot-application-mainpy)
* [Understanding the Code](#understanding-the-code)
    * [`pinecone_vector.py` - The Data Processor](#pinecone_vectorpy---the-data-processor)
    * [`main.py` - The Chatbot Application](#mainpy---the-chatbot-application)
* [📂 Project Structure](#-project-structure)
* [🤔 Troubleshooting](#-troubleshooting)
* [🤝 Contributing](#-contributing)
* [📄 License](#-license)
* [🙏 Acknowledgments](#-acknowledgments)

---

## This project is an Endometriosis Health Guidance Chatbot. Its main goal is to answer user questions about endometriosis accurately and briefly. It uses information from a medical document (in this case, ENDOMETRIOSIS_GUIDE.pdf) to provide context-aware responses.

Imagine you have a lot of information in a PDF document, and you want an easy way for people to ask questions and get answers directly from that document. This project shows you how to build such a system!

The chatbot:

Takes a user's question.

Searches a specialized database (Pinecone) for relevant information from the ENDOMETRIOSIS_GUIDE.pdf document.

Uses a powerful AI model (Google's Gemini 2.0 Flash) to understand the question and the retrieved information.

Generates a concise and helpful answer.
---

## ✨ Features

* **AI-Powered Responses:** Utilizes Google's Gemini 2.0 Flash model for intelligent answers.
* **Context-Aware:** Retrieves relevant information from a PDF document using Pinecone vector search.
* **Conversational Memory:** Remembers previous parts of the conversation to provide more relevant follow-up answers.
* **User-Friendly Interface:** Built with Streamlit for an easy-to-use web interface.
* **Beginner-Friendly Code:** Structured for easy understanding and learning.

---

## 🛠️ Tech Stack

This project uses several exciting technologies:

* **Python:** The primary programming language.
* **Streamlit:** For creating the web application interface.
* **Langchain:** A framework to simplify building applications with Large Language Models (LLMs).
* **Google Generative AI (Gemini 2.0 Flash):** The LLM used for understanding and generating text.
* **GoogleGenerativeAIEmbeddings:** For converting text into numerical representations (embeddings) that AI can understand.
* **Pinecone:** A vector database used to store and efficiently search through the embeddings of our knowledge base.
* **PyPDFLoader:** To load and read text from PDF files.
* **Dotenv:** To manage sensitive information like API keys.

---

## 🚀 Getting Started

Let's get your project up and running!

### Prerequisites

Before you begin, make sure you have the following installed on your computer:

1.  **Python (version 3.8 or newer):** You can download it from [python.org](https://www.python.org/downloads/).
    * To check if you have Python, open your terminal (Command Prompt on Windows, Terminal on macOS/Linux) and type: `python --version` or `python3 --version`.
2.  **Git:** For cloning the project from GitHub. You can download it from [git-scm.com](https://git-scm.com/downloads).
    * To check if you have Git, open your terminal and type: `git --version`.
3.  **Visual Studio Code (VS Code):** A popular code editor. You can download it from [code.visualstudio.com](https://code.visualstudio.com/).
    * Make sure to install the **Python extension** for VS Code. You can find it in the Extensions view (Ctrl+Shift+X or Cmd+Shift+X).

### Cloning the Repository

1.  **Open your terminal or command prompt.**
2.  **Navigate to the directory** where you want to store the project (e.g., `cd Documents/Projects`).
3.  **Clone the repository** using the following command:
    ```bash
    https://github.com/GRACENGARI/TAMBUA-WOMENINTECH-CHATBOT/
    
    ```
4.  **Navigate into the project directory:**
    ```bash
    cd  Endometriosis
    ```

### Setting up in VS Code

1.  **Open VS Code.**
2.  Go to **File > Open Folder...** (or `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`).
3.  Navigate to the `DSA_HIV` folder you just cloned and click **Open**.
4.  VS Code might ask if you trust the authors of the files in this folder. Click "Yes, I trust the authors."

### Installation

We need to install all the Python libraries listed in the `requirements.txt` file.

1.  **Open a new terminal in VS Code:** Go to **Terminal > New Terminal** (or `Ctrl+\`` / `Cmd+\``).
2.  **(Recommended) Create a Virtual Environment:** This helps keep your project's dependencies separate from other Python projects.
    ```bash
    python -m venv venv  # For Python 3
    # or
    # python3 -m venv venv
    ```
    * **Activate the virtual environment:**
        * **On Windows (Git Bash or PowerShell):**
            ```bash
            source venv/Scripts/activate
            ```
        * **On macOS/Linux:**
            ```bash
            source venv/bin/activate
            ```
        You should see `(venv)` at the beginning of your terminal prompt.
3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
    This command reads `requirements.txt` and installs all the listed libraries. This might take a few minutes.

### Environment Variables (.env file)

This project requires API keys for Google (Gemini AI) and Pinecone. These keys are like passwords for accessing their services. We'll store them securely in a `.env` file.

1.  **Locate the `.env.example` file** in the project folder. It looks like this:
    ```
    GOOGLE_API_KEY=
    PINECONE_API_KEY=
    ```
2.  **Create a new file named `.env`** in the same project folder (the root directory of `DSA_HIV`).
3.  **Copy the content** from `.env.example` into your new `.env` file.
4.  **Obtain your API keys:**
    * **Google API Key:**
        * Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
        * Sign in with your Google account.
        * Click on "Create API key" or use an existing one.
        * Copy the generated API key.
    * **Pinecone API Key:**
        * Go to [Pinecone](https://www.pinecone.io/).
        * Sign up for a free account or log in.
        * Navigate to the "API Keys" section in your Pinecone console.
        * Copy your API key (it usually starts with something like `pcsk_...`).
5.  **Paste your keys** into the `.env` file:
    ```env
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
    PINECONE_API_KEY=YOUR_PINECONE_API_KEY_HERE
    ```
    **Important:**
    * Replace `YOUR_GOOGLE_API_KEY_HERE` and `YOUR_PINECONE_API_KEY_HERE` with your actual keys.
    * The `.env` file is listed in `.gitignore` (if not, it should be!) to prevent you from accidentally sharing your secret keys on GitHub. **Never commit your `.env` file with actual keys to a public repository.**

---

## 🏃‍♀️ Running the Project

The project has two main Python scripts:
1.  `pinecone_vector.py`: This script processes your PDF document (`WHO_HIV.pdf`), converts its content into "embeddings" (numerical representations), and stores them in your Pinecone vector database. **You only need to run this once** (or whenever your PDF document changes).
2.  `main.py`: This script runs the Streamlit web application, allowing you to chat with the HIV Health Guidance Assistant.

### Step 1: Prepare Your Knowledge Base (PDF)

1.  **Download or place your PDF file** into the root directory of the project. The current script `pinecone_vector.py` is set to look for a file named `WHO_HIV.pdf`.
    * If your PDF has a different name, you'll need to update this line in `pinecone_vector.py`:
        ```python
        pdf_file_path = 'WHO_Endometriosis.pdf' # name of pdf
        ```
    * For this practicum, ensure you have a `WHO_endometriosis.pdf` file in the main `DSA_HIV` folder. You can find suitable WHO HIV documents online or use one provided for the practicum.

### Step 2: Populate the Vector Database (`pinecone_vector.py`)

This script will read your PDF, break it into smaller chunks, generate embeddings for each chunk, and then upload them to your Pinecone index.

1.  **Make sure your virtual environment is activated** (you should see `(venv)` in your terminal prompt).
2.  **Ensure your `.env` file is correctly set up** with your `PINECONE_API_KEY` and `GOOGLE_API_KEY`.
3.  **Run the script from your VS Code terminal:**
    ```bash
    python pinecone_vector.py
    ```
    * **What to Expect:**
        * The script will first check if a Pinecone index named `hiv` exists. If not, it will create one (this might take about 60 seconds).
        * You'll see progress bars as it loads the PDF, splits the documents, embeds the text chunks, and upserts (uploads) them to Pinecone.
        * This process can take some time, especially for large PDFs or if you have a slower internet connection, as it involves making many API calls.
        * You should see messages like "Embedding batches" and "Upserting batches" with progress bars.
        * Once finished, you'll see a message like "Pinecone vector storage complete!".

    * **Important Note on Pinecone Index:** The script is configured to create an index named `hiv` with a specific dimension (768, for `models/embedding-001`) and metric (`cosine`). If you run this script multiple times, it will use the existing index.

### Step 3: Run the Chatbot Application (`main.py`)

Once your Pinecone database is populated, you can start the chatbot!

1.  **Make sure your virtual environment is activated.**
2.  **Ensure your `.env` file is correctly set up.**
3.  **Run the Streamlit application from your VS Code terminal:**
    ```bash
    streamlit run main.py
    ```
4.  **What to Expect:**
    * This command will start a local web server.
    * Your web browser should automatically open to a new tab displaying the chatbot interface (usually at `http://localhost:8501`).
    * If it doesn't open automatically, your terminal will show you the URLs (e.g., "Local URL: http://localhost:8501"). Copy and paste this into your browser.
    * You'll see the "HIV Health Guidance Assistant" title and a chat interface.
    * You can now type your HIV-related health questions into the input box at the bottom and press Enter!

    * **Terminal Output (Debugging):** The `main.py` script is set up to print the documents it retrieves from Pinecone into the terminal where you ran `streamlit run main.py`. This is very helpful for debugging and understanding what information the chatbot is using to answer your questions.

---

## Understanding the Code

Let's break down what each Python script does.

### `pinecone_vector.py` - The Data Processor

This script is responsible for taking your raw data (the PDF file) and preparing it for the chatbot to use.

```python
# Import necessary libraries
import os                     # For interacting with the operating system (e.g., environment variables)
import time                   # For adding delays (e.g., waiting for Pinecone index to be ready)
import re                     # For regular expressions (used to parse error messages)
import concurrent.futures     # For running tasks in parallel (speeds up embedding)
from pinecone import Pinecone # Pinecone client library
from langchain_community.document_loaders import PyPDFLoader # To load text from PDF files
from langchain_google_genai import GoogleGenerativeAIEmbeddings # To create embeddings using Google's model
from langchain.text_splitter import RecursiveCharacterTextSplitter # To split large texts into smaller chunks
from pinecone import ServerlessSpec # For specifying Pinecone serverless index configuration
from tqdm import tqdm             # For showing progress bars
from dotenv import load_dotenv    # To load API keys from the .env file

# Function to split documents into smaller chunks
def split_docs(documents, chunk_size=1500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # chunk_size: max characters per chunk
    # chunk_overlap: how many characters chunks should overlap (helps maintain context)
    return text_splitter.split_documents(documents)

# Load environment variables from .env file (GOOGLE_API_KEY, PINECONE_API_KEY)
load_dotenv()

# Initialize the Google embedding model
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# "models/embedding-001" is a specific Google model that turns text into 768-dimensional vectors.

# Initialize Pinecone client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"]) # Get Pinecone API key from environment
index_name = 'hiv' # The name we'll use for our Pinecone index

# Check if the 'hiv' index already exists in Pinecone
existing_indexes = pc.list_indexes()
existing_index_names = [index.name for index in existing_indexes.indexes]
if index_name not in existing_index_names:
    # If it doesn't exist, create it
    pc.create_index(
        name=index_name,
        dimension=768,  # Must match the dimension of embeddings from "models/embedding-001"
        metric='cosine', # 'cosine' is a common way to measure similarity between vectors
        spec=ServerlessSpec(cloud='aws', region='us-east-1') # Specifies serverless deployment
    )
    print(f"Created Pinecone index: {index_name}")
    time.sleep(60)  # Wait for the index to become ready (important!)
pinecone_index = pc.Index(index_name) # Connect to our 'hiv' index

# Helper function to extract wait time from API error messages if we get rate limited
def parse_retry_wait_time(error):
    # ... (details omitted for brevity, it tries to find a suggested wait time) ...
    return int(match.group(1)) if match else 20 # Default to 20s if not found

# Function to embed a batch of text, with retries if it fails (e.g., due to API limits)
def embed_batch_with_retry(embed_model, batch_contents, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return embed_model.embed_documents(batch_contents) # Try to embed
        except Exception as e: # If an error occurs
            # ... (prints error, waits, then retries) ...
            if attempt == max_attempts - 1: raise # Give up after max_attempts

# Function to embed many documents concurrently (faster) using multiple threads
def concurrent_embed_documents(embed_model, documents, batch_size=100, max_workers=4):
    all_embeddings = [] # To store all generated embeddings
    all_contents = []   # To store the original text content for each embedding
    futures = []
    # Using ThreadPoolExecutor to manage multiple embedding tasks at once
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Process documents in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_contents = [doc.page_content for doc in batch] # Get text from document objects
            # Submit the embedding task to the executor
            futures.append((executor.submit(embed_batch_with_retry, embed_model, batch_contents), batch_contents))

        # Collect results as they complete, with a progress bar
        for future, contents in tqdm(futures, total=len(futures), desc="Embedding batches"):
            try:
                batch_embeddings = future.result() # Get the embeddings from the completed task
                all_embeddings.extend(batch_embeddings)
                all_contents.extend(contents)
            except Exception as e:
                print(f"Error in embedding batch: {e}")
    return all_embeddings, all_contents

# --- Main part of the script ---
# Define the path to your PDF file
pdf_file_path = 'WHO_HIV.pdf' # Make sure this file exists in your project folder!
pdf_loader = PyPDFLoader(pdf_file_path) # Initialize the PDF loader
documents = pdf_loader.load() # Load the PDF content (this can be slow for large PDFs)
print(f"Loaded {len(documents)} pages from {pdf_file_path}")

# Split the loaded documents into smaller, more manageable chunks
docs = split_docs(documents, chunk_size=1500, chunk_overlap=100)
print(f"Split into {len(docs)} document chunks.")

# Generate embeddings for all document chunks concurrently
print("Starting to generate embeddings for document chunks...")
all_embeddings, all_batch_content = concurrent_embed_documents(embed_model, docs, batch_size=50, max_workers=4)
print(f"Generated {len(all_embeddings)} embeddings.")

# Prepare vectors for upserting to Pinecone
# Each vector needs: an ID (we use index), the embedding itself, and metadata (the original text)
BATCH_SIZE = 100 # How many vectors to upload to Pinecone in one go
vectors_to_upsert = [
    (str(idx), embedding, {"text": content}) # (id, embedding_vector, metadata_dictionary)
    for idx, (embedding, content) in enumerate(zip(all_embeddings, all_batch_content))
]

# Function to upload vectors to Pinecone in batches, with retries
def batch_upsert(index, vectors, batch_size=BATCH_SIZE):
    # Split all vectors into smaller batches
    batches = [vectors[i:i+batch_size] for i in range(0, len(vectors), batch_size)]
    for batch_number, batch in enumerate(tqdm(batches, desc="Upserting batches", total=len(batches))):
        for attempt in range(3): # Try up to 3 times per batch
            try:
                index.upsert(vectors=batch) # Upload the batch to Pinecone
                break # Success, move to next batch
            except Exception as e:
                # ... (handles errors and retries) ...
                if attempt == 2: # Failed after 3 attempts
                    print(f"Batch {batch_number+1} failed after 3 attempts.")
                    raise e # Re-raise the error to stop the script

print("\nStarting Pinecone batched upserts...\n")
batch_upsert(pinecone_index, vectors_to_upsert) # Call the upsert function
print("\nPinecone vector storage complete!\n")
````

**Key Steps in `pinecone_vector.py`:**

1.  **Load Configuration:** Reads API keys from `.env`.
2.  **Initialize Models & Pinecone:** Sets up the Google embedding model and connects to your Pinecone account.
3.  **Create Pinecone Index:** If an index named `hiv` doesn't exist, it creates one. This index will store our document vectors.
4.  **Load PDF:** Uses `PyPDFLoader` to read the content from `WHO_HIV.pdf`.
5.  **Split Documents:** Breaks the loaded PDF content into smaller chunks using `RecursiveCharacterTextSplitter`. This is important because LLMs have limits on how much text they can process at once, and smaller chunks are better for precise information retrieval.
6.  **Generate Embeddings:** For each text chunk, it uses `GoogleGenerativeAIEmbeddings` to create a numerical vector (embedding). These embeddings capture the semantic meaning of the text. This step is done concurrently (in parallel) to speed it up.
7.  **Upsert to Pinecone:** The script uploads these embeddings (along with their original text as metadata) to the `hiv` Pinecone index in batches. Pinecone is optimized for fast similarity searches on these vectors.

### `main.py` - The Chatbot Application

This script creates the web interface using Streamlit and handles the chat logic.

```python
# Import necessary libraries
import os
import asyncio                 # For asynchronous operations (though nest_asyncio handles some complexities)
import nest_asyncio            # Allows asyncio event loops to be nested (useful in environments like Streamlit)
import streamlit as st         # The library for building the web app
from dotenv import load_dotenv # To load API keys from .env
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings # Google's LLM and embedding models
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate # For creating flexible prompts for the LLM
from langchain.chains import LLMChain # For creating a sequence of calls to an LLM
from langchain.memory import ChatMessageHistory, ConversationBufferMemory # To store and manage chat history
from pinecone import Pinecone       # Pinecone client

# Apply nest_asyncio patch. This is often needed when using asyncio in environments
# that might already have an event loop running (like Jupyter notebooks or Streamlit).
nest_asyncio.apply()

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if API keys are available. If not, show an error in the Streamlit app and stop.
if not PINECONE_API_KEY:
    st.error("Pinecone API key is missing. Please set it in your .env file.")
    st.stop() # Halts the Streamlit app
if not GOOGLE_API_KEY:
    st.error("Google API key is missing. Please set it in your .env file.")
    st.stop()

# Initialize Pinecone client and connect to the 'hiv' index
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index("hiv") # Assumes the 'hiv' index was created by pinecone_vector.py

# Initialize the Google embedding model (same one used in pinecone_vector.py)
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Define the system prompt template. This tells the AI how to behave.
system_prompt_template = """
Your name is HIV Health Guidance Chatbot. You are a health advisor specializing in HIV. Answer questions very very briefly and accurately. Use the following information to answer the user's question:

{doc_content}

Provide very brief accurate and helpful health response based on the provided information and your expertise.
"""
# {doc_content} is a placeholder where we'll insert relevant text from our PDF.

# This is the main function that generates a response to a user's question
def generate_response(question):
    """Generate a response using Pinecone retrieval and Gemini 2.0 Flash."""
    # Create a new asyncio event loop for the current thread.
    # This can be necessary when Langchain's async functions are called from a synchronous context.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 1. Embed the user's question: Convert the question text into a numerical vector.
    query_embed = embed_model.embed_query(question)
    query_embed = [float(val) for val in query_embed]  # Ensure standard floats for Pinecone

    # 2. Query Pinecone: Search the 'hiv' index for documents most similar to the user's question.
    results = pinecone_index.query(
        vector=query_embed,       # The embedding of the user's question
        top_k=3,                  # Retrieve the top 3 most relevant document chunks
        include_values=False,     # We don't need the embedding values themselves, just the metadata
        include_metadata=True     # We need the metadata, which contains the original text ('text')
    )

    # 3. Extract document contents from Pinecone results
    doc_contents = []
    print("\n" + "="*50) # Print to terminal for debugging
    print(f"RETRIEVED DOCUMENTS FOR: '{question}'")
    for i, match in enumerate(results.get('matches', [])):
        text = match['metadata'].get('text', '') # Get the 'text' field from metadata
        doc_contents.append(text)
        print(f"\nDOCUMENT {i+1}:\n{text}\n") # Print retrieved docs to terminal
    print("="*50 + "\n")

    # Join the retrieved document contents into a single string.
    # If no documents were found, use a default message.
    # .replace('{', '{{').replace('}', '}}') is to escape curly braces for the .format() method later.
    doc_content = "\n".join(doc_contents).replace('{', '{{').replace('}', '}}') if doc_contents else "No additional information found from my knowledge base."

    # 4. Format the system prompt with the retrieved content
    formatted_prompt = system_prompt_template.format(doc_content=doc_content)

    # 5. Rebuild chat history from Streamlit's session state
    # Streamlit's session_state helps remember things across user interactions.
    chat_history = ChatMessageHistory()
    for msg in st.session_state.chat_history: # st.session_state.chat_history stores our conversation
        if msg["role"] == "user":
            chat_history.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            chat_history.add_ai_message(msg["content"])

    # 6. Initialize conversation memory with the rebuilt chat history
    memory = ConversationBufferMemory(
        memory_key="chat_history", # Name for this part of the memory
        chat_memory=chat_history,  # The actual history object
        return_messages=True      # Ensure it returns message objects
    )

    # 7. Create the full conversation prompt template for the LLM
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(formatted_prompt), # The initial instructions + retrieved docs
            MessagesPlaceholder(variable_name="chat_history"), # Placeholder for past conversation messages
            HumanMessagePromptTemplate.from_template("{question}") # The user's current question
        ]
    )

    # 8. Initialize the Google Gemini 2.0 Flash LLM
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", # Specifies the smaller, faster "flash" version of Gemini 2.0
        temperature=0.1,          # Low temperature for more factual, less creative responses
        google_api_key=GOOGLE_API_KEY
    )

    # 9. Create the Langchain LLMChain. This chain combines the LLM, prompt, and memory.
    conversation = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=memory,
        verbose=True # Set to True to see more detailed output from Langchain in the terminal
    )

    # 10. Generate the response by running the conversation chain with the user's question
    res = conversation({"question": question}) # The input to the chain is a dictionary

    # 11. Return the AI's generated text response
    return res.get('text', '') # Extract the actual text from the response dictionary

# --- Streamlit App UI (User Interface) ---

st.title("HIV Health Guidance Assistant") # Set the title of the web page
st.write("Ask your HIV-related health questions and receive guidance based on our knowledge base.")

# Initialize chat history in Streamlit's session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I'm your HIV Health Guidance Assistant. How can I assist you today?"}
    ] # Start with a greeting from the assistant

# Display past chat messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): # Creates a chat bubble for 'user' or 'assistant'
        st.markdown(message["content"])    # Display the message content (supports Markdown)

# Get user input from a chat input box at the bottom of the screen
user_input = st.chat_input("Ask your health question:")
if user_input: # If the user typed something and pressed Enter
    # Display user's message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    # Add user's message to the chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Show a "Thinking..." spinner while generating the response
    with st.spinner("Thinking..."):
        response = generate_response(user_input) # Call our main function

    # Display AI's response
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add AI's response to the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
```

**Key Steps in `main.py`:**

1.  **Load Configuration & Initialize:** Loads API keys, initializes Pinecone and the Google embedding model.
2.  **`generate_response(question)` Function:** This is the heart of the chatbot logic.
      * **Embed Question:** The user's question is converted into an embedding.
      * **Query Pinecone:** This embedding is used to search Pinecone for the `top_k=3` most similar text chunks from the `WHO_HIV.pdf` data. These chunks provide context.
      * **Prepare Prompt:** The retrieved text chunks are inserted into a "system prompt" that instructs the AI (Gemini 2.0 Flash) on its role and how to use the provided information.
      * **Manage Memory:** It uses `ConversationBufferMemory` to keep track of the ongoing conversation. This allows the chatbot to understand follow-up questions.
      * **Call LLM:** It sends the formatted prompt (including context, chat history, and current question) to the Gemini 2.0 Flash model via `LLMChain`.
      * **Return Response:** The LLM's generated text is returned.
3.  **Streamlit UI:**
      * **Title & Welcome:** Sets up the page title and a brief description.
      * **Chat History:** Initializes and displays the chat history. Each message is shown in a chat bubble. `st.session_state` is crucial here; it's Streamlit's way of remembering data (like the chat history) between user interactions.
      * **User Input:** Provides a `st.chat_input` field for the user to type their questions.
      * **Process & Display:** When the user submits a question:
          * Their question is displayed and added to the history.
          * The `generate_response` function is called (showing a spinner).
          * The assistant's response is displayed and added to the history.

**How `main.py` and `pinecone_vector.py` work together:**

  * `pinecone_vector.py` is run **once** (or when the PDF updates) to process the PDF and store its knowledge in Pinecone.
  * `main.py` is run **every time you want to use the chatbot**. It uses the knowledge already stored in Pinecone to answer questions.

-----

## 📂 Project Structure

Here's a quick look at the important files and what they do:

```
DSA_HIV/
├── .env                   # (You create this) Stores your secret API keys
├── .env.example           # Example for creating your .env file
├── .gitignore             # Tells Git which files to ignore (like .env, venv/)
├── main.py                # Runs the Streamlit chatbot application
├── pinecone_vector.py     # Processes the PDF and uploads to Pinecone
├── requirements.txt       # Lists all Python libraries needed for the project
├── WHO_HIV.pdf            # (You add this) The knowledge base for the chatbot
├── venv/                  # (Optional, created by you) Virtual environment folder
└── README.md              # This file!
```

-----

## 🤔 Troubleshooting

  * **`ModuleNotFoundError: No module named '...'`**:
      * Make sure your virtual environment is activated (`source venv/bin/activate` or `venv\Scripts\activate`).
      * Ensure you've installed all requirements: `pip install -r requirements.txt`.
  * **API Key Errors (e.g., `AuthenticationError`, `PermissionDenied`)**:
      * Double-check that your `GOOGLE_API_KEY` and `PINECONE_API_KEY` in the `.env` file are correct and have no extra spaces.
      * Ensure the `.env` file is in the root directory of the `DSA_HIV` project.
      * Make sure the Google API key has the "Generative Language API" (or similar, like "Vertex AI API" if using Vertex models) enabled in your Google Cloud Console.
      * For Pinecone, ensure your API key is active and you're using the correct environment if prompted (though serverless usually simplifies this).
  * **`pinecone_vector.py` fails during embedding or upserting:**
      * Check your internet connection.
      * The script has retry logic, but very large PDFs or restrictive API rate limits might still cause issues. Try with a smaller PDF or a smaller `batch_size` in `concurrent_embed_documents` and `batch_upsert` functions.
      * The `parse_retry_wait_time` and `embed_batch_with_retry` functions are designed to handle common rate-limiting errors from the Google API by waiting and retrying.
  * **`pinecone_index.query` errors in `main.py`:**
      * Ensure `pinecone_vector.py` ran successfully and populated the `hiv` index.
      * Verify the `index_name` in `main.py` (`pinecone_index = pc.Index("hiv")`) matches the one used in `pinecone_vector.py`.
      * The dimension of the embeddings (768 for `models/embedding-001`) must match between the data loading script and the query script.
  * **Streamlit app doesn't load or shows errors:**
      * Check the terminal where you ran `streamlit run main.py` for specific error messages.
      * Ensure all libraries are installed correctly.
  * **"nest\_asyncio.apply() was called too late" or similar asyncio issues:**
      * The `nest_asyncio.apply()` at the beginning of `main.py` should help. If issues persist, it might be due to interactions with other asyncio-using libraries in your environment.
  * **Pinecone Free Tier Limits:**
      * The free tier of Pinecone has limitations (e.g., only one index, limits on the number of vectors or pods). If you are working with very large datasets, you might hit these limits. The `ServerlessSpec` is generally more flexible for starting.

-----

## 🤝 Contributing

If you have suggestions or improvements, please feel free to:

1.  Fork the Project 
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

We appreciate any contributions that make this learning experience better for everyone\!

-----

## 📄 License

This project is likely distributed under a license like MIT or Apache 2.0.

-----


  * The creators of Langchain, Streamlit, Pinecone, and Google Generative AI for their powerful tools.
  * The open-source community.

```
