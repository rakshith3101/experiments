import re
import ast
from typing import List, Dict
import os


def LLM_judge(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),  # Replace with your key
    ) #make this model dumb
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return completion.choices[0].message.content.strip()

def judge_best_path_with_llm(candidates: List[List[str]], grid_size: str, obstacles: List[tuple], start: tuple, end: tuple) -> List[str]:
    """
    Uses an LLM to act as a judge and select the best path from a list of candidate paths.
    """

    # Label and format all candidate paths
    formatted_paths = []
    for i, path in enumerate(candidates):
        label = chr(65 + i)  # A, B, C, ...
        formatted_paths.append(f"Path {label}: {path}")

    prompt = f"""
You are a navigation expert. A car needs to go from {start} to {end} on a {grid_size} grid.
It must avoid obstacles at: {obstacles}

Below are multiple candidate paths (lists of directions). Each move is 1 unit in: "up", "down", "left", "right".

Choose the best path based on efficiency and safety (avoid obstacles). Explain briefly why.

Before answering always produce, DFS method to find the more efficient path. You should always rely on the DFS method instead of random output.

IF there is no correct path from the candidate paths. You give the right one.
IMPORTANT: Your response MUST be in this exact format:
Best Path: ["direction1", "direction2", ...]

Candidate Paths:
{chr(10).join(formatted_paths)}

Return ONLY the best path in the exact format shown above, with no additional text or explanation.
""".strip()

    print("Sending judgment prompt to LLM...")
    response = LLM_judge(prompt)
    print("Judge Response:\n", response)

    # Extract the best path from LLM's response
    match = re.search(r'Best Path:\s*(\[[^\]]+\])', response)
    if match:
        try:
            return ast.literal_eval(match.group(1))
        except Exception as e:
            print("Failed to parse judged path:", e)

    return []
