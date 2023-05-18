# import cv2
import csv
import os.path

import mediapipe as mp
from mediapipe.python.solutions import face_mesh


# import sys

# threshold = sys.argv[1]
# duration = sys.argv[2]
# var = sys.argv[3]

# print("Threshold:", threshold)
# print("Duration:", duration)
# print("Selected variable:", var)


class MediapipeStream:
    def __init__(self, region):
        # Initialize the MediaPipe Face Detection model
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection()

        self.selected_lm = self.selectLM(region)
        self.landmarks = []
        self.frameid = 0

        # self.get_image_shape()

    '''def drawLandmarks(self, image):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)'''

    def selectLM(self, region):
        FACEMESH_LIPS = frozenset([(61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
                                   (17, 314), (314, 405), (405, 321), (321, 375),
                                   (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
                                   (37, 0), (0, 267),
                                   (267, 269), (269, 270), (270, 409), (409, 291),
                                   (78, 95), (95, 88), (88, 178), (178, 87), (87, 14),
                                   (14, 317), (317, 402), (402, 318), (318, 324),
                                   (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
                                   (82, 13), (13, 312), (312, 311), (311, 310),
                                   (310, 415), (415, 308)])

        FACEMESH_LEFT_EYE = frozenset([(263, 249), (249, 390), (390, 373), (373, 374),
                                       (374, 380), (380, 381), (381, 382), (382, 362),
                                       (263, 466), (466, 388), (388, 387), (387, 386),
                                       (386, 385), (385, 384), (384, 398), (398, 362)])

        FACEMESH_LEFT_EYEBROW = frozenset([(276, 283), (283, 282), (282, 295),
                                           (295, 285), (300, 293), (293, 334),
                                           (334, 296), (296, 336)])

        FACEMESH_RIGHT_EYE = frozenset([(33, 7), (7, 163), (163, 144), (144, 145),
                                        (145, 153), (153, 154), (154, 155), (155, 133),
                                        (33, 246), (246, 161), (161, 160), (160, 159),
                                        (159, 158), (158, 157), (157, 173), (173, 133)])

        FACEMESH_RIGHT_EYEBROW = frozenset([(46, 53), (53, 52), (52, 65), (65, 55),
                                            (70, 63), (63, 105), (105, 66), (66, 107)])

        FACEMESH_REF_VERTICAL = frozenset([(10, 0)])

        FACEMESH_NOSETIP = frozenset([(4, 5)])

        FACEMESH_BETWEEN_EYES = frozenset([(6, 168)])

        if region == 'leftEyebrow':
            selected_lm = face_mesh.FACEMESH_LEFT_EYEBROW
        elif region == 'rightEyebrow':
            selected_lm = face_mesh.FACEMESH_RIGHT_EYEBROW
        elif region == 'leftEye':
            selected_lm = face_mesh.FACEMESH_LEFT_EYE
        elif region == 'rightEye':
            selected_lm = face_mesh.FACEMESH_RIGHT_EYE
        elif region == 'noseTip':
            selected_lm = FACEMESH_NOSETIP
        elif region == 'lips':
            selected_lm = face_mesh.FACEMESH_LIPS
        elif region == 'refVertical':
            selected_lm = FACEMESH_REF_VERTICAL
        elif region == 'refBetweenEyes':
            selected_lm = FACEMESH_BETWEEN_EYES
        else:
            print("Invalid region")
            # TODO errorHandling here

        return selected_lm

    def drawPartLM(self, region, image, face_landmarks):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        selected_lm = self.selectLM(region)

        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=selected_lm,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        print(region + "Landmarks drawn")

    def get_image_shape(self, image):
        image_height, image_width, image_depth = image.shape
        # print('image height is(image.shape):', image_height)
        # print('image width is:(image.shape):', image_width)
        return image_height, image_width

    def absolute_lm(self, image, lm_xyz):
        image_height, image_width = self.get_image_shape(image)
        abs_lm_x = image_width * lm_xyz.x
        abs_lm_y = image_height * lm_xyz.y
        return abs_lm_x, abs_lm_y

    def distance(self, point_1, point_2):
        dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
        return dist

    def get_abs_lm_xy(self, image, single_lm_coord):
        abs_lm_x, abs_lm_y = self.absolute_lm(image, single_lm_coord)
        # print("**get_abs_lm_xy called**\nLM coordinates are:\n ",single_lm_coord,"absolute x:", abs_lm_x, "\nabsolute y:", abs_lm_y)
        return abs_lm_x, abs_lm_y

    def get_abs_point(self, abs_lm_x, abs_lm_y):
        abs_point = (abs_lm_x, abs_lm_y)
        print("**get_abs_point called**\n"
              "absolute Point is:", abs_point)
        return abs_point

    def output_to_csv(self,landmark_dict):
        with open(os.path.abspath(".") + "\\extractedData\\landmarks.csv", mode='w', newline='') as csv_file:
            fieldnames = ['frameid', 'landmark', 'x', 'y', 'abs_x', 'abs_y']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            #for self.frameid, landmarks_dict in enumerate(self.landmarks):
                for landmark_idx, landmark_data in landmark_dict.items():
            for i in range(478):

                header_string = f'frame_id,lm_000_x,lm_000_y,lm_001_x,lm_001_y,...,nose_dist,nose_ear'

                writer.writerow({
                    'frameid': f'{self.frameid}',
                    'landmark': f'{i}',
                    'x': landmark_dict[i]['x'],
                    'y': landmark_dict[i]['y'],
                    'abs_x': landmark_dict[i]['abs_x'],
                    'abs_y': landmark_dict[i]['abs_y']
                })


    def get_lm_coord(self, single_lm, face_landmarks):
        single_lm_coord = face_landmarks.landmark[single_lm]  # hier wird auf die einzelnen LM zugegriffen
        # print("**get_lm_coord called**\nLM",single_lm,"coordinates are:\n", single_lm_coord)
        return single_lm_coord

    def get_abs_point_from_single_lm(self, single_lm,image,face_landmarks):
        single_lm_coord = self.get_lm_coord(single_lm,face_landmarks)
        abs_lm_x, abs_lm_y = self.get_abs_lm_xy(image, single_lm_coord)
        self.get_abs_point(abs_lm_x, abs_lm_y)
        abs_point = (abs_lm_x, abs_lm_y)
        print("LM", single_lm, "coordinates:\n"
                               "absolute x:", abs_lm_x, "\n"
                                "absolute y:", abs_lm_y)
        return abs_point

    def processMP(self, image, region):
        # instance of face_mesh is created
        mp_face_mesh = mp.solutions.face_mesh

        # parameters for facemesh are set
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                static_image_mode=False,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:
            print("mp Parameters set")

            # For performance improvement the frame is set as not writeable to pass by reference.
            image.flags.writeable = False
            vid_face_mesh = face_mesh.process(image)
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            '''
            # solution, that draws only selected_lm without iterating through all Lm´s , might be faster

            if vid_face_mesh.multi_face_landmarks:
                for self.selected_lm in vid_face_mesh.multi_face_landmarks: # multi_face_landmarks is the full list of all LMs
                    self.drawPartLM(region, image, self.selected_lm) 
            '''

            if vid_face_mesh.multi_face_landmarks:
                #filename="test1"
                landmark_dict = {}
                for face_landmarks in vid_face_mesh.multi_face_landmarks:
                    for idx, landmark in enumerate(face_landmarks.landmark):
                        # Get landmark coordinates
                        landmark_x = landmark.x
                        landmark_y = landmark.y
                        # Get absolute landmark coordinates
                        abs_lm_x, abs_lm_y = self.absolute_lm(image, landmark)
                        landmark_dict[idx] = {'x': landmark_x, 'y': landmark_y, 'abs_x': abs_lm_x,
                                              'abs_y': abs_lm_y}
                    self.landmarks.append(landmark_dict)
                    # draws all possible landmarks and their connections in greyscale
                    # mp_drawing.draw_landmarks(
                    #    image=image,
                    #    landmark_list=face_landmarks,
                    #    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    #    landmark_drawing_spec=None,
                    #    connection_drawing_spec=mp_drawing_styles
                    #    .get_default_face_mesh_tesselation_style())
                    # **Funktionsaufruf** drawpartLM()  hier werden die ausgewählten LM´s eingezeichnet
                    self.drawPartLM(region, image, face_landmarks)
                    # print("drawPartLM('" + region, "') called")
                self.output_to_csv(landmark_dict)


                # get_lm_coord(self, 4)

                self.get_abs_point_from_single_lm(4,image, face_landmarks)

                '''
                lm_eyelid_left = face_landmarks.landmark[282]
                abs_lm_x_eyelid_left, abs_lm_y_eyelid_left = self.absolute_lm(image, lm_eyelid_left)
                abs_point_eyelid_left =  (abs_lm_x_eyelid_left, abs_lm_y_eyelid_left)
                #print("Nosetip absolute x:", abs_lm_x_eyelid_left, "absolute y:", abs_lm_y_eyelid_left)

            # **Funktionsaufruf** distance()
                # distance_nosetip_eyelid_left = self.distance(abs_point_eyelid_left, abs_point)

                # print(distance_nosetip_eyelid_left)
                '''

            self.frameid + 1

        print("******************* frame", +self.frameid, " handled ********************+")

# **Funktionsaufruf** Algorithm for calculating the euclidian distance, region, threshold and duration as parameters

# Es müssen nur die Landmarks welche für die Distanzberechnung herangeogen werden normalisiert weredn.

# TODO als einzelne Funktion: Berechnung als funktionsaufrauf auslagern -> dort dann auf Schwellwert über/unterschreitung prüfen
# mit euklidischer distanz die werte berechnen

# TODO als einzelne Funktion: zudem auf die eingestellte Dauer prüfen, bevor die gewählte aktion z.b. Mausklick ausgeführt wird

# TODO als einzelne Funktion: nur die landmarks einzeichnen, welche auch verwendet werden .

# für die gewählte aktion z.b. Mausklick kann eine vorgegebene Library (Package Mouse and Keybaord)
# als Klassen verwendet werden, auf die dann hier zugegriffen wird
