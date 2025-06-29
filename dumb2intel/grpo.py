from gridWorld import GridWorld
from rewardFunction import evaluate_path_with_reward
from engine import generate_text
from engine import extract_directions
from langchain.prompts import PromptTemplate

# Grid setup
obstacles = [(1, 0), (1, 1)]
env = GridWorld(width=3, height=3, start=(0, 0), end=(2, 2), obstacles=obstacles)

# Prompt template
template = PromptTemplate(
    input_variables=["start", "end", "grid_size", "obstacles", "examples"],
    template="""
You are a navigation assistant.
The car is on a {grid_size} grid. Each move is 1 unit.
Allowed directions: up, down, left, right.

Start: {start}
End: {end}

There are obstacles at: {obstacles}

{examples}

Provide the shortest path avoiding the obstacles as a Python list.

Format:
Directions: ["right", "right", "down"]
""".strip()
)

# Format high-performing paths
def format_examples(paths):
    if not paths:
        return ""
    section = "Here are some relatively better paths from earlier attempts:\n"
    for p in paths:
        section += f"- {p}\n"
    return section.strip()

# GRPO Loop (Relative Policy Optimization)
MAX_ITER = 5
CANDIDATES_PER_ITER = 5
TOP_K = 2

best_group_paths = []

for iteration in range(1, MAX_ITER + 1):
    print(f"\n📦 GRPO Iteration {iteration}")

    examples = format_examples(best_group_paths)
    prompt = template.format(
        start=env.start,
        end=env.end,
        grid_size=f"{env.width}x{env.height}",
        obstacles=obstacles,
        examples=examples
    )

    batch = []

    for i in range(CANDIDATES_PER_ITER):
        print(f"\n🧠 Candidate {i + 1}")
        response = generate_text(prompt)
        print("🤖 LLM Response:", response)

        directions = extract_directions(response)
        if directions:
            reward = evaluate_path_with_reward(env, directions)
            print(f"📈 Reward: {reward}")
            batch.append((directions, reward))

    # 🧮 Rank relatively
    if not batch:
        print("⚠️ No valid paths parsed.")
        continue

    batch.sort(key=lambda x: x[1], reverse=True)
    top_relative = [x[0] for x in batch[:TOP_K]]

    # Add only unique top-K to guidance pool
    for path in top_relative:
        if path not in best_group_paths:
            best_group_paths.append(path)

    # Limit size of prompt memory
    best_group_paths = best_group_paths[-TOP_K:]

# Final Result
final_path = best_group_paths[-1] if best_group_paths else []
print("\n🏁 Final GRPO Path:", final_path)

# Replay path
env.reset()
for move in final_path:
    env.move(move)
env.render()
