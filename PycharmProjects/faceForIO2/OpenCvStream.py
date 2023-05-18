import cv2
import mediapipe as mp
from mediapipe.python.solutions import face_mesh

import MediapipeStream


class OpenCvStream:

    def __init__(self, region):
        # instance of mediapipe is created
        self.stream = MediapipeStream.MediapipeStream(region)
        self.cap = cv2.VideoCapture(0)

    def readCamera(self, region):
        # reads video Frame from webcam(0)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("empty Camera Frame, ignoring Process")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            self.stream.processMP(image, region)
            print("processMP called")

          # nicht mehr notwendig, da in mediapipe stream verwendet wird
            # vidFaceMesh = face_mesh.process(image) # als funktionsaufrauf auslagern
            # alle koordinaten werden hier ausgelesen

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
            if cv2.pollKey() & 0xFF == 27:
                break
        cap.release()

'''
#idea to make this class modular and call only when the video should be displayed:
        def show_frame(self, frame):
            cv2.imshow('OpenCV Stream', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                cv2.destroyAllWindows()
                return None

        def stop(self):
            self.cap.release()

        def get_frame(self):
            ret, frame = self.cap.read()
            return frame
'''

