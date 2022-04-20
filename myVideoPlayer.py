#!/usr/bin/env python3

import cv2
from threading import Thread
from ThreadingQueue import ThreadingQueue


# A function that will iterate through all the frames of a video
# and extract them.
def extract_frames(clip_file_name, read_frames_queue):
    count = 0  # Initializing the frame count
    vidcap = cv2.VideoCapture(clip_file_name)  # Opens the video clip
    success, image = vidcap.read()  # Read one frame
    print(f'Reading frame {count} {success}')

    # Iterating through all the frames in the video
    while success and count < 72:
        # Obtaining a encoded JPG encoded version of the frame
        success, jpg_image = cv2.imencode('.jpg', image)
        read_frames_queue.enqueue(jpg_image)  # Enqueuing the frame to the queue
        success, image = vidcap.read()  # Read next frame
        print(f'Reading frame {count}')
        count += 1  # Incrementing the frame count
    # Adding a NULL value at the end of the queue to indicate a end point
    read_frames_queue.enqueue(None)


# A function that will iterate through all the frames of the video and
# convert them to grayscale.
def convert_to_grayscale(read_frames_queue, gray_frames_queue):
    count = 0  # Initializing the frame count
    # Obtaining the first JPG encoded frame from the queue
    inputFrame = read_frames_queue.dequeue()

    # Iterating through the queue containing all the frames of the video
    while inputFrame is not None and count < 72:
        print(f'Converting frame {count}')
        # Decoding input frame to convert back to an image
        image = cv2.imdecode(inputFrame, cv2.IMREAD_UNCHANGED)
        # Converting the current image to grayscale
        grayscaleFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Encoding the current image to store it back onto the queue
        success, jpg_image = cv2.imencode('.jpg', grayscaleFrame)
        # Adding the image onto the gray_frames_queue
        gray_frames_queue.enqueue(jpg_image)
        count += 1  # Incrementing the frame count
        # Queueing the next JPG encoded frame
        inputFrame = read_frames_queue.dequeue()
    # Adding a NULL value at the end of the queue to indicate a end point
    gray_frames_queue.enqueue(None)


# A function that will display all frames of the video.
def display_frames(gray_frames_queue):
    frameDelay = 42  # Time delay between each frame
    count = 0  # Initialzing the frame count
    frame = gray_frames_queue.dequeue()  # Loads the first gray frame

    # Iterating through the queue containing all the frames of the video
    while frame is not None:
        print(f'Displaying frame {count}')
        # Decoding input frame to convert back to an image
        image = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
        # Display the frame in a window called "Video"
        cv2.imshow('Video', image)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break
        count += 1  # Incremeting the frame count
        frame = gray_frames_queue.dequeue()  # Reads the next JPG encoded frame
    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()


# *** Function that starts the program and takes the video name as input ***
def main(clip_file_name):
    readFramesQueue = ThreadingQueue(max_capacity=10)  # Initializing original video queue
    grayFramesQueue = ThreadingQueue(max_capacity=10)  # Initializing grayscale video queue

    # Creation and start of the 3 threads which will handle the respective methods
    extractThread = Thread(target=extract_frames, args=(clip_file_name, readFramesQueue)).start()
    greyFramesThread = Thread(target=convert_to_grayscale, args=(readFramesQueue, grayFramesQueue)).start()
    displayThread = Thread(target=display_frames, args=(grayFramesQueue,)).start()


# Running the program
main(clip_file_name="clip.mp4")