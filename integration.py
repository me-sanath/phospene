import asyncio
from bluetooth_beacon_detection import discover_devices_with_rssi
from object_detection import main as detect_objects
from navigation_v2 import run_slam
from path_finder import a_star, add_obstacles
from tts_llm import cues_generate

def main():
    # Step 1: BLE Detection
    asyncio.run(discover_devices_with_rssi())  # For BLE

    # Step 2: Object Detection
    detect_objects()  # Detect and send objects

    # Step 3: SLAM Navigation
    run_slam()  # Generate map and obstacles

    # Step 4: Pathfinding (adjust with a grid and start/goal)
    grid = np.zeros((20, 20))  # Example grid
    start = (0, 0)
    goal = (19, 12)
    obstacles = [(5, i) for i in range(5, 15)] + [(i, 10) for i in range(10, 20)]
    add_obstacles(grid, obstacles)
    path = a_star(grid, start, goal)

    # Step 5: Generate Audio Cues (using the path and detected obstacles)
    if path:
        for step in path:
            obstacle = "some obstacle"  # Replace with actual obstacle detection
            navigation_cue = "move left"
            print(cues_generate(obstacle, navigation_cue))

if __name__ == "__main__":
    main()
