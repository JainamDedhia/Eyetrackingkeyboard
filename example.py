import cv2
from gaze_tracking import GazeTracking
import pyautogui

# Initialize the gaze tracking object
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Get screen width and height
screen_width, screen_height = pyautogui.size()

# Smoothing factor for cursor movement
smooth_factor = 0.1

# Initial cursor position (center of the screen)
current_x, current_y = screen_width // 2, screen_height // 2

while True:
    # Read frame from webcam
    _, frame = webcam.read()
    
    # Refresh gaze tracking with the current frame
    gaze.refresh(frame)

    # Annotate the frame with gaze direction
    new_frame = gaze.annotated_frame()
    text = ""

    # Determine gaze direction
    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    # Display gaze direction on the frame
    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)

    # Get gaze coordinates
    horizontal_ratio = gaze.horizontal_ratio()
    vertical_ratio = gaze.vertical_ratio()

    # Handle cases where gaze ratios might be None
    if horizontal_ratio is None:
        horizontal_ratio = 0.5  # Default to center
    if vertical_ratio is None:
        vertical_ratio = 0.5  # Default to center

    # Convert gaze coordinates to screen coordinates
    target_x = int(screen_width * (1 - horizontal_ratio))
    target_y = int(screen_height * vertical_ratio)

    # Smooth the cursor movement
    current_x = int(current_x * (1 - smooth_factor) + target_x * smooth_factor)
    current_y = int(current_y * (1 - smooth_factor) + target_y * smooth_factor)

    # Move the cursor
    pyautogui.moveTo(current_x, current_y)

    # Display the annotated frame
    cv2.imshow("Demo", new_frame)

    # Exit the loop when the 'esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()
