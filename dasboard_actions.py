import cv2
from ultralytics import YOLO
import os
import numpy as np

# Load the YOLO model
model = YOLO('actions.pt')  # Ensure 'cons.pt' is in the correct directory

# Initialize video capture
video_path = 1 # Update this path as needed
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error opening video stream or file"

# Get video properties for output file
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
output_file = os.path.join('.', 'runs for actions', 'live1.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
  
threshold = 0.60


# Function to create a dashboard on the frame
def create_dashboard(frame, running_count, laying_count, running_warning, laying_warning):
    dashboard_height = 120  # Height of the dashboard
    dashboard_width = 200   # Width of the dashboard
    dashboard = np.zeros((dashboard_height, dashboard_width, 3), dtype="uint8")
    dashboard_color = (50, 50, 50)  # Dark gray background

    cv2.rectangle(dashboard, (0, 0), (dashboard_width, dashboard_height), dashboard_color, -1)

    cv2.putText(dashboard, f"Running: {running_count}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    cv2.putText(dashboard, f"Laying: {laying_count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    if running_warning:
        cv2.putText(dashboard, running_warning, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    if laying_warning:
        cv2.putText(dashboard, laying_warning, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    frame[0:dashboard_height, frame.shape[1] - dashboard_width:frame.shape[1]] = dashboard
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break
    running_count = 0
    laying_count = 0
    running_warning = ""
    laying_warning = "" 
    # Reset counters for each frame

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold and int(class_id) in [1, 2, 4, 7, 8]:

            if int(class_id) == 1:
                color, class_name = (0, 0, 128), "Run"
                running_count +=1
                running_warning = "Warning: Running Detected!"
            elif int(class_id) == 2:
                color, class_name = (255, 0, 0), "sit"
            elif int(class_id) == 4:
                color, class_name = (0, 165, 255), "walk"
            elif int(class_id) == 7:
                color, class_name = (255, 255, 0), "stand"
            elif int(class_id) == 8:
                color, class_name = (0, 0, 255), "laying"   
                laying_count += 1 
                laying_warning = "Warning: Laying Detected!"
    
            #elif int(class_id) == 5:  # Person
             #   color, class_name = (255, 255, 0), "Person"
              #  person_id = (int(x1), int(y1), int(x2), int(y2))
               # new_tracked_ids.append(person_id)

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f"{class_name}: {score:.2f}", (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)


    # Create and display the dashboard
    combined_frame = create_dashboard(frame, running_count, laying_count, running_warning, laying_warning)
    out.write(combined_frame)
    cv2.imshow('Live Object Detection with Dashboard', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
out.release()
cap.release()
cv2.destroyAllWindows()
