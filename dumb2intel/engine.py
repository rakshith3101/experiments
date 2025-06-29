from langchain.prompts import PromptTemplate

import re
import ast
import os

def extract_directions(response_text):
    try:
        # Look for the 'Directions: [...]' pattern in the response
        match = re.search(r'Directions:\s*(\[[^\]]+\])', response_text)
        if match:
            direction_list = match.group(1)
            return ast.literal_eval(direction_list)  # Safely parse the list
    except Exception as e:
        print("❌ Failed to parse directions:", e)

    print("⚠️ No valid direction list found.")
    return []

# Your OpenRouter-based LLM call
def generate_text(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),  # Replace with your key
    ) #make this model dumb
    completion = client.chat.completions.create(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return completion.choices[0].message.content.strip()


# Use LangChain PromptTemplate for dynamic formatting
from langchain.prompts import PromptTemplate
from gridWorld import GridWorld
# Grid setup
obstacles = [(1, 0), (1, 1),]
env = GridWorld(width=3, height=3, start=(0, 0), end=(2, 2), obstacles=obstacles)

# Prompt preparation
template = PromptTemplate(
    input_variables=["start", "end", "grid_size","obstacles"],
    template="""You are a navigation assistant.
The car is on a {grid_size} grid. Each move is 1 unit.
Allowed directions: up, down, left, right.

Start: {start}
End: {end}

There are obstacles on the grid at these positions: {obstacles}

Provide the shortest path avoiding the obstacles as a Python list.
Example format: ["right", "right", "down"]

Always provide the answer in the following format: 

Directions: ["right", "right", "down"] # have the directions placeholder while returning.
""".strip()
)

# Format prompt with obstacles
formatted_prompt = template.format(
    start=env.start,
    end=env.end,
    grid_size=f"{env.width}x{env.height}",
    obstacles=obstacles
)

MAX_ATTEMPTS = 10
MIN_ACCEPTABLE_REWARD = 80

from rewardFunction import evaluate_path_with_reward
def improve_with_feedback(env, initial_prompt, obstacles):
    current_prompt = initial_prompt
    best_directions = []
    best_reward = float("-inf")
    reward_history = []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n🧠 Attempt {attempt}: Asking LLM for directions...")
        response = generate_text(current_prompt)
        print("🤖 LLM Response:\n", response)

        directions = extract_directions(response)
        print("✅ Parsed Directions:", directions)

        reward = evaluate_path_with_reward(env, directions)
        print(f"🏁 Reward Score: {reward}")

        reward_history.append(reward)
        if reward > best_reward:
            best_reward = reward
            best_directions = directions

        # Exit early if reward is acceptable
        if reward >= MIN_ACCEPTABLE_REWARD:
            print("🎯 Acceptable path found.")
            break

        # Generate feedback and update the prompt
        feedback = f"""
Your previous path was: {directions}
This path received a reward score of {reward} on a {env.width}x{env.height} grid with obstacles at: {obstacles}

Please revise the path to avoid obstacles and reach the goal more efficiently.
Format your answer as:
Directions: ["right", "right", ...]
"""
        current_prompt = initial_prompt + "\n\n" + feedback.strip()

    return best_directions, best_reward, reward_history

# Reward Function Method
#final_directions, final_reward, reward_history = improve_with_feedback(env, formatted_prompt, obstacles)
# print(f"\n✅ Final Path: {final_directions}")
# print(f"🎯 Final Reward: {final_reward}")
# env.render()





# LLM as Judge method
from llmJudge import judge_best_path_with_llm

NUM_ATTEMPTS = 5
candidate_paths = []

for i in range(NUM_ATTEMPTS):
    print(f"\n🧠 LLM Attempt {i+1}")
    response = generate_text(formatted_prompt)
    print("🤖 LLM Output:", response)

    directions = extract_directions(response)
    if directions:
        candidate_paths.append(directions)


# Let the LLM be the judge
final_path = judge_best_path_with_llm(
    candidates=candidate_paths,
    grid_size=f"{env.width}x{env.height}",
    obstacles=obstacles,
    start=env.start,
    end=env.end
)

env.reset()
for move in final_path:
    env.move(move)

env.render()
print(f"🏁 Final Chosen Path: {final_path}")
