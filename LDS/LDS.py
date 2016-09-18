
import cv2
import numpy as np

# Define the function for Hough Transform
def HoughTransform(img_crop, detected_edges):
    # Create an empty image to store the detected lines
    img_hlines = img_crop.copy()

    # Perform Hough Line Transform on the edge-detected image
    lines = cv2.HoughLinesP(detected_edges, 1, np.pi / 180, 50, 30, 10)

    # Draw the detected lines on the image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img_hlines, (x1, y1), (x2, y2), (0, 255, 255), 2, cv2.LINE_AA)

    return img_hlines

# Define the function for Canny Thresholding
def CannyThreshold(lowThreshold, ratio, kernel_size):
    # Reduce noise with a kernel size of 3x3
    detected_edges = cv2.GaussianBlur(img_mask, (3, 3), 0)

    # Apply Canny edge detection
    detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * ratio, kernel_size)

    # Display the Canny edge-detected image
    cv2.imshow(window_name, detected_edges)

    # Call the Hough Transform function to draw lines on the edge-detected image
    img_hlines = HoughTransform(img_crop, detected_edges)

    # Display the image with detected lines
    cv2.imshow("detected lines", img_hlines)

# Load the video stream
cap = cv2.VideoCapture("..\\resources\\2.mp4")

# Check if the video stream is opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

# Create a window to display the frames
cv2.namedWindow("Frame")

# Create a window to display the edge-detected image
window_name = "Edge Map"
cv2.namedWindow(window_name)

# Initialize Canny threshold parameters
lowThreshold = 210
ratio = 3
kernel_size = 3

# Create a trackbar for the Canny threshold
cv2.createTrackbar("Min Threshold:", window_name, lowThreshold, 255, lambda x: None)

# Loop over the video frames
while True:
    # Read the next frame from the video stream
    ret, img = cap.read()

    # If the frame is empty, break the loop
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Crop the image to the region of interest
    roi = (0, 325, img.shape[1], img.shape[0] - 455)
    img_crop = img[roi[0]:roi[1], roi[2]:roi[3]]

    # Convert the cropped image to grayscale
    img_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)

    # Create masks for yellow and white colors
    mask_hsv_yellow = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
    mask_white = cv2.inRange(img_gray, np.mean(img_gray) + (255 - np.mean(img_gray)) / 3.5, 255)
    mask_hsv_yellow = cv2.inRange(mask_hsv_yellow, (20, 85, 85), (30, 255, 255))

    # Combine the yellow and white masks
    img_mask = cv2.bitwise_or(mask_white, mask_hsv_yellow)

    # Apply Gaussian blur to the mask
    img_mask = cv2.GaussianBlur(img_mask, (5, 5), 0)

    # Display the original frame
    cv2.imshow("Frame", img)

    # Display the cropped image
    cv2.imshow("Crop", img_crop)

    # Display the grayscale image
    cv2.imshow("Gray", img_gray)

    # Display the mask image
    cv2.imshow("Mask", img_mask)

    # Call the Canny Threshold function when the trackbar value changes
    lowThreshold = cv2.getTrackbarPos("Min Threshold:", window_name)
    CannyThreshold(lowThreshold, ratio, kernel_size)

    # Check if the user pressed the ESC key
    if cv2.waitKey(1) == 27:
        break

# When everything is done, release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()