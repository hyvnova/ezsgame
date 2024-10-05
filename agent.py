import random
from ezsgame import *

class Agent(Rect):
    def __init__(self, pos: Pos, goals: Group, obstacles: Group, agents: Group) -> None:
        self.goals = goals
        self.obstacles = obstacles
        self.agents = agents
        self.visited_goals = []
        self.speed = random.randint(1, 3)
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.safe_distance = 40  # Minimum distance to be considered safe to pass between obstacles

        super().__init__(pos, Size(20), color=random_color())

        @on_event("update")
        def on_update():
            self.update()

    def update(self) -> None:
        if not self.goals:
            return

        # if touching a goal, remove it from the list of goals
        for goal in self.goals:
            if is_colliding(self, goal, scale=1):
                self.goals.remove(goal)
                break

        # Choose the closest goal that is not closer to another agent considering obstacles
        closest_goal = self.get_closest_goal_with_obstacles()
        if closest_goal:
            # Move towards the closest goal while avoiding obstacles
            self.move_towards_with_obstacle_avoidance(closest_goal.pos)

    def get_closest_goal_with_obstacles(self):
        closest_goal = None
        min_distance = float('inf')

        for goal in self.goals:
            distance_to_goal = self.distance(self.pos, goal.pos)
            if distance_to_goal < min_distance:
                closest_goal = goal
                min_distance = distance_to_goal

        return closest_goal

    def move_towards_with_obstacle_avoidance(self, target_pos: Pos) -> None:
        dx = target_pos.x - self.pos.x
        dy = target_pos.y - self.pos.y
        distance_to_target = (dx ** 2 + dy ** 2) ** 0.5

        # Normalize the vector towards the target
        dx /= distance_to_target
        dy /= distance_to_target

        # Calculate the potential next position
        next_pos = Pos(self.pos.x + dx * self.speed, self.pos.y + dy * self.speed)

        # Check for collision with obstacles
        if self.is_colliding_with_obstacle(next_pos):
            # If colliding, adjust movement direction
            dx, dy = self.avoid_obstacle(next_pos)

        # Move the agent
        self.pos.x += dx * self.speed
        self.pos.y += dy * self.speed

    def is_colliding_with_obstacle(self, pos: Pos) -> bool:
        for obstacle in self.obstacles:
            if is_colliding(Rect(pos, self.size), obstacle):
                return True
        return False

    def avoid_obstacle(self, pos: Pos) -> tuple:
        # Calculate the vector to move away from the nearest obstacle
        min_distance = float('inf')
        nearest_obstacle = None

        for obstacle in self.obstacles:
            distance_to_obstacle = self.distance(pos, obstacle.pos)
            if distance_to_obstacle < min_distance:
                min_distance = distance_to_obstacle
                nearest_obstacle = obstacle

        if nearest_obstacle:
            # Calculate the vector away from the obstacle
            dx = pos.x - nearest_obstacle.pos.x
            dy = pos.y - nearest_obstacle.pos.y

            # Normalize the vector
            distance_to_obstacle = (dx ** 2 + dy ** 2) ** 0.5
            dx /= distance_to_obstacle
            dy /= distance_to_obstacle

            return dx, dy

        return 0, 0

    def distance(self, pos1: Pos, pos2: Pos) -> float:
        return ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2) ** 0.5
