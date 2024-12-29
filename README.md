# Indoor Navigation System with Audio Cues for the Visually Impaired
## Description
This project implements an indoor navigation system that provides real-time audio cues for visually impaired individuals. Using a combination of SLAM (Simultaneous Localization and Mapping), object detection, pathfinding algorithms, and text-to-speech integration, it assists users in navigating complex indoor environments safely.

## Features
- __Simultaneous Localization and Mapping (SLAM):__ Real-time mapping of the environment using camera feeds.
- __Object Detection:__ Identification and localization of obstacles or key objects using YOLOv5.
- __Pathfinding:__ Efficient route computation using the A* algorithm.
- __Audio Cues:__ AI-powered text-to-speech instructions for navigation and obstacle avoidance.
- __Dynamic Obstacle Updates:__ Adaptability to dynamic changes in the environment.

## Installation
 
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/indoor-navigation.git
   cd indoor-navigation
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have a camera connected and a video feed available (feed.mp4 for testing).
4. Set up the .env file for the Groq API key:
   ```makefile
   GROQ_KEY=your_api_key
   ```
## Tech Implementation
1. SLAM (navigation_v2.py):
- Captures video feed to map the environment using edge detection and contour mapping.
- Creates a scalable map and visualizes it in real-time.
2. Object Detection (object_detection.py):

- Utilizes YOLOv5 for object detection.
- Sends real-time object data to a server (optional).
3. Pathfinding (path_finder.py):

- Employs the A* algorithm to compute the shortest path, avoiding obstacles.
- Visualizes the computed path over a grid.
4. Text-to-Speech and Audio Cues (tts_llm.py):

- Converts detected obstacles and navigation instructions into concise audio cues.
- Uses the Groq API for generating responses.

## Screenshots
![image](https://github.com/user-attachments/assets/787f5941-8b08-4950-9fe5-b758e5777488)
![image](https://github.com/user-attachments/assets/3b2e8b26-eb76-4835-b271-116dc2ba0c49)
![image](https://github.com/user-attachments/assets/e0f68184-b018-4152-972a-07d0bb9ba3bc)
![image](https://github.com/user-attachments/assets/785a735e-6dc8-46b5-ba8b-a0460ed1f33f)
![image](https://github.com/user-attachments/assets/5c3a91cb-4c01-401a-8b77-7ff23800a991)




## Future Scope
- Integration with LiDAR for more precise mapping and obstacle detection.
- Improved audio feedback using advanced language models for personalized navigation assistance.
- Support for multi-floor navigation using elevator and stairway detection.
- Mobile application integration for broader accessibility.
- Enhanced object detection with a custom-trained model for indoor-specific items.
