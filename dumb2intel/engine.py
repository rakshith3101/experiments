# from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
# from langchain.llms import HuggingFacePipeline
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # Load model and tokenizer locally (flan-t5 is good at instruction-following)
# model_name = "google/flan-t5-base"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# pipe = pipeline(
#     "text2text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=64,
#     temperature=0.2
# )

# llm = HuggingFacePipeline(pipeline=pipe)

# # Define prompt template
# template = """
# You are a navigation assistant.
# The car is on a {grid_size} grid. Each move is 1 unit.
# Allowed directions: up, down, left, right.

# Start: {start}
# End: {end}

# Give the shortest path from start to end as a Python list of directions.
# Example format: ["right", "right", "down"]
# Directions:
# """

# prompt = PromptTemplate(
#     input_variables=["start", "end", "grid_size"],
#     template=template.strip()
# )

# # LLM chain
# llm_chain = LLMChain(prompt=prompt, llm=llm)

# # Helper function
# def get_llm_directions(start, end, grid_size="5x5"):
#     response = llm_chain.run({"start": start, "end": end, "grid_size": grid_size})
#     try:
#         directions_start = response.find("[")
#         directions = response[directions_start:].split("]")[0] + "]"
#         moves = eval(directions)
#         if isinstance(moves, list):
#             return moves
#     except Exception as e:
#         print("Failed to parse directions:", e)
#     return []

# # Example usage
# start = (0, 0)
# end = (3, 2)
# directions = get_llm_directions(start, end)
# print("LLM Directions:", directions)


# from openai import OpenAI

# def query_hf_api(payload):
#     """Send a query to the OpenRouter API using the OpenAI client."""
#     try:
#         client = OpenAI(
#             base_url="https://openrouter.ai/api/v1",
#             api_key="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",
#         )
        
#         # Extract the prompt from the payload (assuming it's in the 'inputs' field for compatibility)
#         prompt = payload.get('inputs', '') if isinstance(payload, dict) else str(payload)
        
#         completion = client.chat.completions.create(
#             model="meta-llama/llama-4-maverick:free",
#             messages=[{
#                 "role": "user",
#                 "content": prompt
#             }]
#         )
        
#         # Return the response in a similar format to the HF API for compatibility
#         return [{"generated_text": completion.choices[0].message.content.strip()}]
        
#     except Exception as e:
#         print(f"Error calling OpenRouter API: {str(e)}")
#         # Return empty response in case of error
#         return [{"generated_text": "Error: Failed to generate response"}]

# # Define the text generation function using the query function
# def generate_text(prompt):
#     response = query_hf_api({"inputs": prompt})
    
#     # Print the raw response to inspect its structure
#     print(response)
    
#     # Safely access the response, handling errors
#     if isinstance(response, list) and len(response) > 0:
#         return response[0].get('generated_text', "No text generated.")
#     else:
#         return "Error: Unable to generate text."

# # Example usage
# generated_text = generate_text("Hello, how are you?")
# print("Generated Text:", generated_text)



# langchain implementation

from langchain.prompts import PromptTemplate

# Your OpenRouter-based LLM call
def generate_text(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  # Replace with your key
    )
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick:free",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content.strip()


# Use LangChain PromptTemplate for dynamic formatting
template = PromptTemplate(
    input_variables=["start", "end", "grid_size"],
    template="""
You are a navigation assistant.
The car is on a {grid_size} grid. Each move is 1 unit.
Allowed directions: up, down, left, right.

Start: {start}
End: {end}

Give the shortest path from start to end as a Python list of directions.
Example format: ["right", "right", "down"]
Directions:
""".strip()
)

# Format the prompt using LangChain, then send it manually
formatted_prompt = template.format(start=(0, 0), end=(2, 3), grid_size="5x5")
response = generate_text(formatted_prompt)

print("Generated Directions:", response)
