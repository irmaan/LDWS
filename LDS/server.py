import cv2
import numpy as np
import socket
import sys
import threading

def display(socket):
    # OpenCV Code
    cap = cv2.VideoCapture(0)  # open the default camera
    img_height = 480
    img_width = 640
    img = np.zeros((img_height, img_width), dtype=np.uint8)
    img_gray = np.zeros((img_height, img_width), dtype=np.uint8)

    if not img.flags['C_CONTIGUOUS']:
        img = np.ascontiguousarray(img)

    img_size = img.size * img.itemsize
    bytes_sent = 0

    print("Image Size:", img_size)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Video processing
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Send processed image
        data = img_gray.tobytes()
        while bytes_sent < img_size:
            bytes_sent += socket.send(data[bytes_sent:])

    cap.release()

def main():
    # Networking stuff: socket, bind, listen
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print("usage: ./cv_video_srv [port] [capture device]\n"
              "port           : socket port (4097 default)\n"
              "capture device : (0 default)\n")
        return

    port = 4097
    cap_dev = 0

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        cap_dev = int(sys.argv[2])

    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_addr = ('', port)

    try:
        local_socket.bind(local_addr)
    except Exception as e:
        print("Can't bind() socket")
        return

    local_socket.listen(3)

    print("Waiting for connections...")
    print("Server Port:", port)

    while True:
        remote_socket, remote_addr = local_socket.accept()
        print("Connection accepted")

        thread = threading.Thread(target=display, args=(remote_socket,))
        thread.start()

if __name__ == "__main__":
    main()