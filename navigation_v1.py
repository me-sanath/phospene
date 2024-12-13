import cv2
import numpy as np
import matplotlib.pyplot as plt

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Replace with the URL provided by Camo app

# ORB Detector for feature detection and matching
orb = cv2.ORB_create()

# Initialize previous frame variables
prev_frame = None
prev_keypoints = None
prev_descriptors = None
trajectory = []  # Store the 2D positions of the camera (for map visualization)
obstacles = []  # Store detected obstacles positions (for visualization)

# Camera intrinsic parameters (example values, update for your camera)
K = np.array([[525.0, 0.0, 319.5],
              [0.0, 525.0, 239.5],
              [0.0, 0.0, 1.0]])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect and compute features
    keypoints, descriptors = orb.detectAndCompute(gray, None)

    if prev_frame is not None:
        # Match features between frames
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(prev_descriptors, descriptors)
        matches = sorted(matches, key=lambda x: x.distance)

        # Proceed only if there are enough matches
        if len(matches) >= 5:
            # Extract matched keypoints
            prev_pts = np.float32([prev_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            curr_pts = np.float32([keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            # Estimate the essential matrix
            E, mask = cv2.findEssentialMat(curr_pts, prev_pts, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
            if E is not None and E.shape == (3, 3):
                # Recover pose
                _, R, t, _ = cv2.recoverPose(E, curr_pts, prev_pts, K)

                # Update trajectory (camera position)
                if len(trajectory) == 0:
                    trajectory.append((0, 0))  # Start at the origin
                else:
                    # Update based on translation (assuming planar motion for simplicity)
                    last_pos = np.array(trajectory[-1])
                    new_pos = last_pos + np.array([t[0, 0], t[2, 0]])
                    trajectory.append(tuple(new_pos))

                # Detect obstacles (example: assuming obstacles are features with large displacement)
                obstacle_threshold = 20  # Threshold for detecting obstacles based on feature displacement
                for i, m in enumerate(matches):
                    if mask[i] and np.linalg.norm(curr_pts[i] - prev_pts[i]) > obstacle_threshold:
                        obstacles.append(tuple(curr_pts[i][0]))

            # Draw matches for visualization
            matched_frame = cv2.drawMatches(prev_frame, prev_keypoints, gray, keypoints, matches[:50], None)
            cv2.imshow("Feature Matches", matched_frame)
        else:
            print("Insufficient matches, skipping frame.")

    # Update the previous frame and keypoints
    prev_frame = gray
    prev_keypoints = keypoints
    prev_descriptors = descriptors

    # Stop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Convert trajectory to a NumPy array for plotting
trajectory = np.array(trajectory)
obstacles = np.array(obstacles)

# Visualize the 2D trajectory and obstacles (top-down view)
plt.figure(figsize=(10, 6))
plt.plot(trajectory[:, 0], -trajectory[:, 1], marker='o', label="Camera Trajectory")
if len(obstacles) > 0:
    plt.scatter(obstacles[:, 0], -obstacles[:, 1], color='red', label="Obstacles")
plt.title("Top-Down View of Camera Trajectory and Obstacles")
plt.xlabel("X (arbitrary units)")
plt.ylabel("Y (arbitrary units)")
plt.legend()
plt.grid()
plt.show()