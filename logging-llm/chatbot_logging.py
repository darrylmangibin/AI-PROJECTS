import logging
from openai import OpenAI
import json
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

def setup_logging():
    """Configure logging to save logs in JSON format"""
    logger = logging.getLogger("chatbot")
    logger.setLevel(logging.INFO)

    # Create a file handler for JSON logs
    file_handler = logging.FileHandler("chatbot_logs.json")
    formatter = logging.Formatter("%(message)s")
    file_handler.setFormatter(formatter)

    # Create a console handler for pretty-printed logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
      logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      )
    )

    logger.addHandler(file_handler)

    return logger

def initialize_client(use_ollama: bool = True) -> OpenAI:
  """Initialize OpenAI client for either OpenAI or Ollama"""
  if use_ollama:
    return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
  else:
    return OpenAI()

class ChatBot:
  def __init__(self, use_ollama: bool = False):
    self.logger = setup_logging()
    self.session_id = str(uuid.uuid4())
    self.start_time = datetime.now()
    self.client = initialize_client(use_ollama)
    self.use_ollama = use_ollama
    self.model_name = "gpt-oss:120b-cloud" if use_ollama else "gpt-4o-mini"
    self.conversation_hist = []
   
    #  Initialize conversation with a system message
    self.messages = [{
      "role": "system",
      "content": "You are a helpful assistant."
    }]

  def chat(self, user_input: str) -> str:
    try:
      # log user input
      log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "user_input": user_input,
        "meta_data": {
          "session_id": self.session_id,
          "model": self.model_name
        }
      }
      self.logger.info(json.dumps(log_entry))

      # append user message to conversation
      self.messages.append({"role": "user", "content": user_input})

      start_time = datetime.now()
      response = self.client.chat.completions.create(
        model=self.model_name,
        messages=self.messages,
      )
      end_time = datetime.now()

      # calculate response time
      response_time = (end_time - start_time).total_seconds()

      # extract assistant's respomse
      assistant_response = response.choices[0].message.content

      # log assistant's respomse
      log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "INFO",
        "assistant_response": assistant_response,
        "meta_data": {
          "session_id": self.session_id,
          "model": self.model_name,
          "response_time_seconds": response_time,
          "tokens_used": (
            response.usage.total_tokens
            if hasattr(response, "usage") else None
          ),
        }
      }

    except Exception as e:
      log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": "ERROR",
        "error": str(e),
        "meta_data": {
          "session_id": self.session_id,
          "model": self.model_name,
        }
      }
      self.logger.error(json.dumps(log_entry))
      return f"Error: {str(e)}"

def main():
  print("\nSelect Model type:\n")
  print("1. Use OpenAI API (gpt-4o-mini)")
  print("2. Use Ollama API (kimi-k2.6:cloud)")
  
  while True:
    choice = input("Enter choice (1 or 2): ").strip()
    if choice in ["1", "2"]:
      break
    print("Invalid choice. Please try again.")
  
  
  use_ollama = choice == "2"

  # initialize chatbot
  chatbot = ChatBot(use_ollama)

  print("\n=== Chat Session Started ===")
  print(f"Using {'Ollama' if use_ollama else 'OpenAI'} model")
  print("Type 'quit' or 'exit' to end the session.")
  print(f"Session ID: {chatbot.session_id}\n")

  while True:
    user_input = input("You: ").strip()
  
    if user_input.lower() == "exit":
       print("\n Goodbye")
       break

    if not user_input:
      continue

    response = chatbot.chat(user_input)
    print(f"Chatbot: {response}\n")

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("\nChat session ended.")
    
