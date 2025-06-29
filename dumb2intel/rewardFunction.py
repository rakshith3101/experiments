from gridWorld import GridWorld
def evaluate_path_with_reward(env: GridWorld, directions: list[str]) -> int:
    reward = 0
    env.reset()

    for move in directions:
        moved = env.move(move)
        if moved:
            reward += 20     # Reward per valid step
        else:
            reward -= 10    # Penalty for invalid move

    if env.position == env.end:
        reward += 100    
        

    return reward