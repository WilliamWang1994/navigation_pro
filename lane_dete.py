import cv2
import numpy as np


def do_canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) #预处理:讲彩色图变为灰度图
    # Applies a 5x5 gaussian blur with deviation of 0 to frame - not mandatory since Canny will do this for us
    blur = cv2.GaussianBlur(gray, (5, 5), 0) #高斯滤波去噪声
    # Applies Canny edge detector with minVal of 50 and maxVal of 150
    canny = cv2.Canny(blur, 50, 150) #canny边缘检测
    return canny


def do_segment(frame):
    # Since an image is a multi-directional array containing the relative intensities of each pixel in the image, we can use frame.shape to return a tuple: [number of rows, number of columns, number of channels] of the dimensions of the frame
    # frame.shape[0] give us the number of rows of pixels the frame has. Since height begins from 0 at the top, the y-coordinate of the bottom of the frame is its height
    height, width = frame.shape[:2]
    # Creates a triangular polygon for the mask defined by three (x, y) coordinates
    polygons = np.array([
                            [(0, height), (width, height), (width, int(height/2)), (0, int(height/2))]
                        ])
    # Creates an image filled with zero intensities with the same dimensions as the frame
    mask = np.zeros_like(frame)
    # Allows the mask to be filled with values of 1 and the other areas to be filled with values of 0
    cv2.fillPoly(mask, polygons, 255)
    # A bitwise and operation between the mask and frame keeps only the triangular area of the frame
    # cv2.imshow("mask", mask)
    segment = cv2.bitwise_and(frame, mask)
    return segment


def calculate_lines(frame, lines):
    # Empty arrays to store the coordinates of the left and right lines
    left = []
    right = []
    # Loops through every detected line
    for line in lines:
        # Reshapes line from 2D array to 1D array
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_intercept = parameters[1]
        # If slope is negative, the line is to the left of the lane, and otherwise, the line is to the right of the lane
        if slope < 0:
            left.append((slope, y_intercept))
        else:
            right.append((slope, y_intercept))
    # Averages out all the values for left and right into a single slope and y-intercept value for each line
    left_avg = np.average(left, axis=0)
    right_avg = np.average(right, axis=0)
    # Calculates the x1, y1, x2, y2 coordinates for the left and right lines
    left_line = calculate_coordinates(frame, left_avg)
    right_line = calculate_coordinates(frame, right_avg)
    return np.array([left_line, right_line])


def calculate_coordinates(frame, parameters):
    slope, intercept = parameters
    # Sets initial y-coordinate as height from top down (bottom of the frame)
    y1 = frame.shape[0]
    # Sets final y-coordinate as 150 above the bottom of the frame
    y2 = int(y1 - 150)
    # Sets initial x-coordinate as (y1 - b) / m since y1 = mx1 + b
    x1 = int((y1 - intercept) / slope)
    # Sets final x-coordinate as (y2 - b) / m since y2 = mx2 + b
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def visualize_lines(frame, lines):
    # Creates an image filled with zero intensities with the same dimensions as the frame
    lines_visualize = np.zeros_like(frame)
    # Checks if any lines are detected
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            # Draws lines between two coordinates with green color and 5 thickness
            cv2.line(lines_visualize, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return lines_visualize


def get_lane(frame):
    canny = do_canny(frame)  # canny边缘检测
    segment = do_segment(canny)  # 手工分割
    hough = cv2.HoughLinesP(segment, 2, np.pi / 180, 100, np.array([]), minLineLength=100, maxLineGap=50)
    lines = calculate_lines(frame, hough)
    return "left"


if __name__ == '__main__':
    # The video feed is read in as a VideoCapture object
    cap = cv2.VideoCapture("input.mp4")

    while cap.isOpened():
        # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
        ret, frame = cap.read()
        if not ret:
            break
        canny = do_canny(frame)  # canny边缘检测
        # cv2.imshow("canny", canny)
        # plt.imshow(frame)
        # plt.show()
        segment = do_segment(canny)  # 手工分割
        # cv2.imshow("segment", segment)
        # cv2.waitKey(0)
        hough = cv2.HoughLinesP(segment, 2, np.pi / 180, 100, np.array([]), minLineLength=100, maxLineGap=50)
        #  霍夫变换,确定车道线
        lines = calculate_lines(frame, hough)
        # Visualizes the lines
        lines_visualize = visualize_lines(frame, lines)  # 显示车道线
        # cv2.imshow("hough", lines_visualize)
        # cv2.waitKey(0)
        #  Overlays lines on frame by taking their weighted sums and adding an arbitrary scalar value of 1 as the gamma argument
        output = cv2.addWeighted(frame, 0.9, lines_visualize, 1, 1)  # 车道和原始图片叠加
        # Opens a new window and displays the output frame
        cv2.imshow("output", output)
        # Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    # The following frees up resources and closes all windows
    cap.release()
    cv2.destroyAllWindows()