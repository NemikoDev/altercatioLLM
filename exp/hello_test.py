import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from models import AnthropicClient, OpenAIClient

def main():
    prompt = "Hello, how are you?"
    
    # Claude
    try:
        claude = AnthropicClient()
        response = claude.generate(prompt)
        print(response.text)
        print(f"(tokens in={response.input_tokens}, out={response.output_tokens})\n")
    except Exception as e:
        print(e)
        
    # Openai
    
    try:
        gpt = OpenAIClient()
        response = gpt.generate(prompt)
        print(response.text)
        print(f"(tokens in={response.input_tokens}, out={response.output_tokens})\n")
    except Exception as e:
        print(e)




if __name__ == "__main__":
    main()
