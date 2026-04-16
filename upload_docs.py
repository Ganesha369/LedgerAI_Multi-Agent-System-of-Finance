import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

def upload_to_assistant():
    api_key = os.getenv("PINECONE_API_KEY")
    assistant_name = "ledgerai"
    file_path = "data/mock_ledger.txt"

    if not api_key:
        print("Error: PINECONE_API_KEY not found.")
        return

    pc = Pinecone(api_key=api_key)
    
    try:
        assistant = pc.assistant.Assistant(assistant_name=assistant_name)
        print(f"Connected to assistant: {assistant_name}")
        
        print(f"Uploading {file_path}...")
        response = assistant.upload_file(file_path=file_path)
        print(f"Upload successful: {response}")
        
    except Exception as e:
        print(f"Error during upload: {e}")

if __name__ == "__main__":
    upload_to_assistant()
