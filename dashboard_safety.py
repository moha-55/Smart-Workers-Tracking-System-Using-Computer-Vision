import cv2
from ultralytics import YOLO
import os
import numpy as np

# Load the YOLO model
model = YOLO('cons.pt')  # Ensure 'cons.pt' is in the correct directory

# Initialize video capture
video_path = 1 # Update this path as needed
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error opening video stream or file"

# Get video properties for output file
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
output_file = os.path.join('.', 'runs for safety', 'live1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
  # Additional width for dashboard

# Initialize a list to store trackers and their corresponding IDs
trackers = []
tracked_ids = []

# Detection threshold
threshold = 0.60

def create_dashboard(frame, no_hardhat_count, no_vest_count, person_count, warning_message1, warning_message2):
    dashboard_height = 120  # New height of the dashboard
    dashboard_width = 200   # New width of the dashboard
    dashboard = np.zeros((dashboard_height, dashboard_width, 3), dtype="uint8")
    color = (50, 50, 50)  # BGR format
    cv2.rectangle(dashboard, (0, 0), (dashboard_width, dashboard_height), color, -1)
    # Adjust text positions and maybe reduce font size if necessary
    cv2.putText(dashboard, f"No Hardhat: {no_hardhat_count}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
    cv2.putText(dashboard, f"No Vest: {no_vest_count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
    cv2.putText(dashboard, f"Person Count: {person_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
    
    if warning_message1:
        cv2.putText(dashboard, warning_message1, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    if warning_message2:
        cv2.putText(dashboard, warning_message2, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    
    
    # Position the dashboard in the top right corner
    frame[0:dashboard_height, frame.shape[1] - dashboard_width:frame.shape[1]] = dashboard

    return frame



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Object detection
    results = model(frame)[0]
    no_hardhat_count = 0
    no_vest_count = 0
    warning_message1 = ""
    warning_message2 = ""
    new_tracked_ids = []

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold and int(class_id) in [0, 2, 4, 7]:
            color, class_name = (0, 255, 0), "Unknown"  # Default color and label

            if int(class_id) == 0:
                color, class_name = (0, 255, 0), "Hardhat"
            elif int(class_id) == 2:
                color, class_name = (0, 0, 255), "NO-Hardhat"
                no_hardhat_count += 1
                warning_message1 = "Warning: No Hardhat!"
            elif int(class_id) == 4:
                color, class_name = (0, 255, 255), "NO-Safety Vest"
                no_vest_count += 1
                warning_message2 = "Warning: No Safety Vest!"
            elif int(class_id) == 7:
                color, class_name = (255, 0, 255), "Safety Vest"
            #elif int(class_id) == 5:  # Person
             #   color, class_name = (255, 255, 0), "Person"
              #  person_id = (int(x1), int(y1), int(x2), int(y2))
               # new_tracked_ids.append(person_id)

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f"{class_name}: {score:.2f}", (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

        if score > threshold and int(class_id) == 5:
            person_id = (int(x1), int(y1), int(x2), int(y2))  # Unique ID for each person based on initial position
            new_tracked_ids.append(person_id)

            if person_id not in tracked_ids:
                # Initialize new tracker for 'Person'
                tracker = cv2.TrackerCSRT_create()
                bbox = (int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1))
                tracker.init(frame, bbox)
                trackers.append(tracker)

    # Update tracking for each person
    person_count = 0  # Counting the number of persons being tracked
    for tracker, person_id in zip(trackers, tracked_ids):
        success, bbox = tracker.update(frame)
        if success:
            x1, y1, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (255, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            person_count += 1

    # Update the list of tracked IDs
    tracked_ids = new_tracked_ids

    # Display person count
    #cv2.putText(frame, f'Person Count: {person_count}', (30, height - 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 0), 2)


    # Create and display dashboard
    combined_frame = create_dashboard(frame, no_hardhat_count, no_vest_count, person_count, warning_message1, warning_message2)
    out.write(combined_frame)
    cv2.imshow('Live Object Detection with Dashboard', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
out.release()
cap.release()
cv2.destroyAllWindows()
