from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def main():
    print("Hello from langchain-me!")
    print(os.getenv("OPENAI_API_KEY"))  # Print the OpenAI API key from environment variables


if __name__ == "__main__":
    main()
