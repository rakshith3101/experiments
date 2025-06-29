# dumb2intel: From Dumb to Intelligent Pathfinding

## Overview
dumb2intel is an experimental project that demonstrates how to improve a simple pathfinding system using Large Language Models (LLMs) and reinforcement learning techniques. The project showcases the transformation from a basic grid navigation system to an intelligent pathfinding solution using LLMs as both generators and judges of potential solutions.

## Core Concept
The project implements a grid world navigation problem where an agent must find the shortest path from a start point to an end point while avoiding obstacles. The system evolves through three main approaches:

1. **Basic Path Generation**: Simple path generation using LLM
2. **Reward-Based Learning**: Using a reward function to evaluate and improve paths
3. **LLM as Judge**: Using an LLM to evaluate and select the best paths from multiple candidates
4. **Group Relative Policy Optimization (GRPO)**: An advanced approach that iteratively refines paths using relative comparisons within groups of candidates

## Components

### 1. Grid World (`gridWorld.py`)
- Implements a simple grid-based environment
- Handles agent movement and obstacle avoidance
- Provides visualization of the grid and agent's path

### 2. Reward Function (`rewardFunction.py`)
- Evaluates the quality of a given path
- Provides positive rewards for valid moves and reaching the goal
- Applies penalties for invalid moves and obstacles

### 3. LLM Integration (`llmJudge.py`)
- Implements an LLM-based judge to evaluate path quality
- Uses OpenRouter API to access various LLM models
- Implements a structured prompt for consistent path evaluation

### 4. Engine (`engine.py`)
- Contains the main logic for path generation and improvement
- Implements the reward-based learning loop
- Integrates with the LLM judge for path evaluation

### 5. GRPO Implementation (`grpo.py`)
- Implements Group Relative Policy Optimization
- Iteratively refines paths using relative comparisons within candidate groups
- Maintains and updates groups of solutions based on their relative performance

## How It Works

### Basic Flow
1. The system starts with a grid world containing a start point, end point, and obstacles
2. The LLM generates potential paths from start to end
3. Paths are evaluated using either:
   - A reward function (scoring based on valid moves and goal achievement)
   - An LLM judge (evaluating path quality based on instructions)
4. The best path is selected and visualized

### Advanced Features
- **Iterative Improvement**: The system can generate multiple paths and iteratively improve them
- **Multi-Model Support**: Can use different LLMs for generation and judging
- **Flexible Configuration**: Grid size, obstacles, and LLM parameters can be easily modified

## Getting Started

### Prerequisites
- Python 3.8+
- Required Python packages (install via `pip install -r requirements.txt`):
  ```
  openai
  langchain
  python-dotenv
  ```

### Configuration
1. Set up your OpenRouter API key in the environment variables or directly in the code
2. Configure the grid world parameters (size, obstacles) in the respective files
3. Adjust LLM parameters (model, temperature) as needed

### Running the Project

#### Basic Path Generation
```python
python engine.py
```

#### Using GRPO (Group Relative Policy Optimization)
```python
python grpo.py
```

## Example Output
```
🚀 GRPO Iteration 1
🧠 LLM Candidate 1
🤖 LLM Response: Directions: ["right", "right", "down", "down"]
...
🏁 GRPO Complete. Final Best Path:
✅ Directions: ['right', 'right', 'down']

🗺️ Current Grid:
S o o 
X X . 
. . E 
```

## Customization

### Modifying the Grid
Edit the `obstacles` list in `grpo.py` or `engine.py` to change the grid layout:

```python
obstacles = [(1, 0), (1, 1)]  # Add/remove obstacle positions as needed
```

### Adjusting LLM Parameters
Modify the `generate_text` function in `engine.py` to change the LLM model or parameters:

```python
completion = client.chat.completions.create(
    model="mistralai/mistral-small-3.2-24b-instruct:free",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.6,  # Adjust for more/less randomness
)
```
## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
