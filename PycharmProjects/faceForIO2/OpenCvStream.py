import cv2
import mediapipe as mp
from mediapipe.python.solutions import face_mesh

import MediapipeStream


class OpenCvStream:

    def __init__(self):
        # instance of mediapipe is created
        self.mp = MediapipeStream.MediapipeStream()
        self.image_bgr = cv2.VideoCapture(0)
        self.image_rgb= self.get_image_rgb(self.image_bgr)

    def get_image_bgr(self):
        """
        creates VideoCapture Object from opencv and reads video Frame from webcam(0),

        :return: image frame in bgr format as image_bgr
        """

        image_bgr = cv2.VideoCapture(0)
        return image_bgr

    def get_image_rgb(self, image_bgr):
        """
        takes image in bgr format and converts it to rgb format,
        also checks if VideoCapture is open and reading, when not reading, process is ignored
        :param image_bgr:
        :param reading:
        :return: image in rgb format
        """
        while image_bgr.isOpened():
            reading, image_bgr = image_bgr.read()
            if not reading:
                print("empty Camera Frame, ignoring Process")
                continue
                # TODO error handling (when this is executed the following error occurs,
                # File "C:\Users\koend\PycharmProjects\faceForIO2\OpenCvStream.py",
                # line 33, in get_image_rgb     while image_bgr.isOpened():
                # AttributeError: 'numpy.ndarray' object has no attribute 'isOpened')

            # For performance improvement the frame is set as not writeable to pass by reference.
            image_bgr.flags.writeable = False
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            # For performance improvement the frame is set as not writeable to pass by reference.
            image_rgb.flags.writeable = False
            return image_rgb, reading

    def show_image(self, image):
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
        if cv2.waitKey(1) & 0xFF == 27:
            return False
        return True

    def readCamera(self, region):
        # reads video Frame from webcam(0)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("empty Camera Frame, ignoring Process")
                continue
            # TODO als Funktion 'get_image' auslagern und in main aufrufen?!
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # TODO dann auch processMP in main aufrufen und image übergeben
            self.mp.processMP(image, region)
            print("processMP called")

            # nicht mehr notwendig, da in mediapipe stream verwendet wird
            # vidFaceMesh = face_mesh.process(image) # als funktionsaufrauf auslagern
            # alle koordinaten werden hier ausgelesen
            # TODO dann dies auch als Funktion 'show_image' auslagern und ebenfalls in main aufrufen
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
            if cv2.pollKey() & 0xFF == 27:
                break
        cap.release()


if __name__ == "__main__":
    pass

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
