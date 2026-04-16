import os
import logging
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialResearcher:
    """
    Researcher Agent using Pinecone Assistant SDK.
    """
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.assistant_host = os.getenv("PINECONE_ASSISTANT_HOST")

        if not self.api_key:
            logger.error("PINECONE_API_KEY not found in environment variables.")
            raise ValueError("PINECONE_API_KEY is required.")
        
        if not self.assistant_host:
            logger.error("PINECONE_ASSISTANT_HOST not found in environment variables.")
            raise ValueError("PINECONE_ASSISTANT_HOST is required.")

        try:
            # Initialize Pinecone
            self.pc = Pinecone(api_key=self.api_key)
            
            # Initialize Assistant - using the name 'ledgerai' which we found exists
            # The SDK will resolve the host automatically, but we can also pass it if we find the right param
            self.assistant = self.pc.assistant.Assistant(assistant_name="ledgerai")
            
            logger.info("FinancialResearcher: Pinecone Assistant connection established.")
        except Exception as e:
            logger.error(f"FinancialResearcher: Pinecone Assistant connection failed: {e}")
            self.assistant = None

    def query(self, query_str: str):
        """
        Performs a query using Pinecone Assistant.
        """
        if not self.assistant:
            return "Researcher error: Pinecone Assistant unavailable."
            
        try:
            # Using the chat interface of Pinecone Assistant
            response = self.assistant.chat(messages=[{"role": "user", "content": query_str}])
            # The response object has a 'message' attribute which contains the 'content'
            return response.message.content
        except Exception as e:
            logger.error(f"FinancialResearcher Query Error: {e}")
            return f"Error during research: {e}"
