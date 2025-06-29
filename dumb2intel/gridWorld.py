class GridWorld:
    def __init__(self, width, height, start, end, obstacles):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.obstacles = set(obstacles)
        self.reset()

    def reset(self):
        self.position = self.start
        self.path = [self.start]
        return self.position

    def is_valid(self, pos):
        x, y = pos
        return (
            0 <= x < self.width and
            0 <= y < self.height and
            pos not in self.obstacles
        )
    
    def move(self, direction):
        x, y = self.position
        new_pos = {
            "up": (x, y - 1),
            "down": (x, y + 1),
            "left": (x - 1, y),
            "right": (x + 1, y),
        }.get(direction, self.position)

        if self.is_valid(new_pos):
            self.position = new_pos
            self.path.append(new_pos)
            return True
        return False

    def render(self):
        print("\n🗺️ Current Grid:")
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                pos = (x, y)
                if pos == self.start:
                    row += "S "
                elif pos == self.end:
                    row += "E "
                elif pos in self.obstacles:
                    row += "X "
                elif pos in self.path:
                    row += "o "
                else:
                    row += ". "
            print(row)
        print()