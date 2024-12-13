import cv2
import numpy as np
import matplotlib.pyplot as plt

# Parameters for visualization
MAP_SIZE = 500  # Size of the map (500x500 pixels)
MAP_SCALE = 10  # Scaling factor (1 pixel = 10 cm)

# Initialize an empty map
map_image = np.ones((MAP_SIZE, MAP_SIZE), dtype=np.uint8) * 255  # White map
robot_position = [MAP_SIZE // 2, MAP_SIZE // 2]  # Start at the center

# Draw obstacles on the map
def draw_obstacle(map_img, x, y):
    cv2.circle(map_img, (x, y), 2, 0, -1)  # Black dot represents an obstacle

# SLAM loop using camera feed
def run_slam():
    # Open the camera
    cap = cv2.VideoCapture("./data/feed.mp4")

    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect edges in the frame
        edges = cv2.Canny(gray, 50, 150)

        # Find contours (obstacles)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Approximate the contour
            approx = cv2.approxPolyDP(contour, 3, True)

            for point in approx:
                # Transform point to map scale
                x, y = point[0]
                map_x = int(robot_position[0] + (x - frame.shape[1] // 2) / MAP_SCALE)
                map_y = int(robot_position[1] + (y - frame.shape[0] // 2) / MAP_SCALE)

                # Draw the obstacle
                if 0 <= map_x < MAP_SIZE and 0 <= map_y < MAP_SIZE:
                    draw_obstacle(map_image, map_x, map_y)

        # Show the map in real-time
        cv2.imshow('Live SLAM Map', map_image)

        # Show the camera frame with edges
        cv2.imshow('Camera View', edges)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Visualize the final map using Matplotlib
    plt.figure(figsize=(8, 8))
    plt.imshow(map_image, cmap='gray')
    plt.title('Mapped Environment')
    plt.show()

if __name__ == "__main__":
    run_slam()
