import cv2
import numpy as np
import socket
import sys

def main():
    # Networking stuff: socket, connect
    if len(sys.argv) < 3:
        print("Usage: cv_video_cli <serverIP> <serverPort>")
        return

    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])

    sokt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverAddr = (serverIP, serverPort)

    try:
        sokt.connect(serverAddr)
    except Exception as e:
        print("connect() failed!")
        return

    # OpenCV Code
    img = np.zeros((480, 640), dtype=np.uint8)
    imgSize = img.size * img.itemsize
    iptr = img.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    bytes = 0
    key = -1

    if not img.flags['C_CONTIGUOUS']:
        img = np.ascontiguousarray(img)

    print("Image Size:", imgSize)

    cv2.namedWindow("CV Video Client", cv2.WINDOW_NORMAL)

    while key != ord('q'):
        data = sokt.recv(imgSize, socket.MSG_WAITALL)
        if len(data) == 0:
            break
        np.copyto(iptr, np.frombuffer(data, dtype=np.uint8))
        cv2.imshow("CV Video Client", img)
        key = cv2.waitKey(10)

    sokt.close()

if __name__ == "__main__":
    main()