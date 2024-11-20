from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Function to parse content using OpenAI GPT-4 API with streaming
def parse_with_gpt4_stream(dom_chunks, parse_description):
    system_prompt = "You are an AI assistant tasked with extracting specific information from the following text content. Remove HTML and CSS, and write it as if you were an advertiser for a Iols."
    
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            # Make the streaming API call to OpenAI's GPT-4
            stream = client.chat.completions.create(
                model="gpt-4o-mini",  # Use "gpt-4o-mini" or another appropriate model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Extract information matching this description: {parse_description} from the following content:\n\n{chunk}"}
                ],
                stream=True,  # Enable streaming
            )

            response_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content

            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            print(f"Response for batch {i}: {response_text}")  # Debug log

            if response_text:
                parsed_results.append(response_text)
            else:
                parsed_results.append("")  # Handle empty response if necessary
        except Exception as e:
            print(f"Error parsing batch {i}: {e}")
            parsed_results.append("")

    return "\n".join(parsed_results)