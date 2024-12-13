import matplotlib.pyplot as plt
import numpy as np
from heapq import heappush, heappop
from scipy.spatial import distance

def a_star(grid, start, goal):
    open_list = []
    heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance.cityblock(start, goal)}

    while open_list:
        _, current = heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                if grid[neighbor[0], neighbor[1]] == 1:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + distance.cityblock(neighbor, goal)
                    heappush(open_list, (f_score[neighbor], neighbor))

    return None

def visualize_path(grid, path):
    grid_copy = grid.copy()
    for x, y in path:
        grid_copy[x, y] = 0.5

    plt.imshow(grid_copy, cmap="gray")
    plt.show()

def add_obstacles(grid, obstacles):
    for x, y in obstacles:
        grid[x, y] = 1

def main():
    grid_size = (20, 20)
    grid = np.zeros(grid_size)

    # Parameters
    start = (0, 0)
    goal = (19, 12)
    obstacles = [(5, i) for i in range(5, 15)] + [(i, 10) for i in range(10, 20)]

    add_obstacles(grid, obstacles)
    grid[7,12]=1
    path = a_star(grid, start, goal)
    if path:
        print("Path found:", path)
        visualize_path(grid, path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
