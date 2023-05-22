import CsvExport
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
    def __init__(self):
        self.csv_export = CsvExport.CsvExport()
        self.row_data = [478]
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection()
        self.landmarks = []
        self.frame_id = 0
        self.header_written = False
        self.nosetip = 4
        self.ref_vert_top = 10

    def get_frame_id(self):
        return self.frame_id

    def select_lm(self, region):
        eye_left = [362, 385, 387, 263, 373, 380]
        eye_right = [33, 160, 158, 133, 153, 144]
        nosetip = 4
        ref_vert_top = 10

        if region == 'eye_left':
            selected_lm = eye_left
        elif region == 'eye_right':
            selected_lm = eye_right
        elif region == 'nosetip':
            selected_lm = nosetip
        elif region == 'ref_vert_top':
            selected_lm = ref_vert_top
        else:
            print("Invalid region")
            # TODO errorHandling here

        return selected_lm

    def select_lm_connections(self, region):
        selected_lm_connections = set()
        FACEMESH_REF_VERTICAL = frozenset([(10, 0)])
        FACEMESH_NOSETIP = frozenset([(4, 5)])
        FACEMESH_BETWEEN_EYES = frozenset([(6, 168)])
        if 'leftEyebrow' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_LEFT_EYEBROW)
        if 'rightEyebrow' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_RIGHT_EYEBROW)
        if 'bothEyebrows' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_RIGHT_EYEBROW)
            selected_lm_connections.update(face_mesh.FACEMESH_LEFT_EYEBROW)
        if 'leftEye' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_LEFT_EYE)
        if 'rightEye' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_RIGHT_EYE)
        if 'bothEyes' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_RIGHT_EYE)
            selected_lm_connections.update(face_mesh.FACEMESH_LEFT_EYE)
        if 'mouth' in region:
            selected_lm_connections.update(face_mesh.FACEMESH_LIPS)
        if 'noseTip' in region:
            selected_lm_connections.update(FACEMESH_NOSETIP)
        if 'refVertical' in region:
            selected_lm_connections.update(FACEMESH_REF_VERTICAL)
        if 'refBetweenEyes' in region:
            selected_lm_connections.update(FACEMESH_BETWEEN_EYES)
        if region is None:
            selected_lm_connections = None
        return frozenset(selected_lm_connections)

    def drawPartLM(self, region, image_rgb, face_landmarks):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        drawing_spec = None  # set to None, so that not all LMs are drawn
        # use this, to display all 477 LM´s:
        # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        selected_lm_connections = self.select_lm_connections(region)

        mp_drawing.draw_landmarks(
            image=image_rgb,
            landmark_list=face_landmarks,
            connections=frozenset(selected_lm_connections),  # draws connections between a Tupel of LM´s
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        # print(str(region) + "Landmarks drawn")

    def get_image_shape(self, image_rgb):
        image_height, image_width, image_depth = image_rgb.shape
        # print('image height is(image.shape):', image_height)
        # print('image width is:(image.shape):', image_width)
        return image_height, image_width

    def absolute_lm(self, image_rgb, lm_xyz):
        image_height, image_width = self.get_image_shape(image_rgb)
        abs_lm_x = image_width * lm_xyz.x
        abs_lm_y = image_height * lm_xyz.y
        return abs_lm_x, abs_lm_y

    def distance(self, point_1, point_2):
        """
        returns the distance between two landmarks,
        calculates euclidian distance based on x and y values
        Formula: sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5

        :Point1 (x,y) point_1:
        :Point2 (x,y) point_2:
        : distance between point_1 and point_2 return: dist
        """
        dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5  # euclidian distance is calculated
        return dist

    def abs_distance_from_lms(self, lm1, lm2, image_rgb, face_landmarks):
        """
        returns the absolute distance between two landmarks,
        calculates absolute x and y coordinates first by x*image_width and y*image_height, here: 460*640,
        then calculates euclidian distance based on these values
        Formula: sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
        :param lm1:Landmark1(0-477)
        :param lm2:Landmark2(0-477)
        :param image_rgb: imageFrame in rgb
        :param face_landmarks: Landmark Dict with format (x: , y: , z: )
        :return: absolute distance between lm1 and lm2 as: abs_dist
        """
        point_1 = self.get_abs_point_from_single_lm(lm1, image_rgb, face_landmarks)
        point_2 = self.get_abs_point_from_single_lm(lm2, image_rgb, face_landmarks)
        abs_dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5  # euclidian distance is calculated
        print(f"distance between {lm1}-{lm2}is:", abs_dist)

        return abs_dist

    def get_abs_lm_xy(self, image_rgb, single_lm_coord):
        abs_lm_x, abs_lm_y = self.absolute_lm(image_rgb, single_lm_coord)
        # print("**get_abs_lm_xy called**\nLM coordinates are:\n ",single_lm_coord,"absolute x:", abs_lm_x, "\nabsolute y:", abs_lm_y)
        return abs_lm_x, abs_lm_y

    def get_abs_point(self, abs_lm_x, abs_lm_y):
        abs_point = (abs_lm_x, abs_lm_y)
        print("**get_abs_point called**\n"
              "absolute Point is:", abs_point)
        return abs_point

    def get_lm_coord(self, single_lm, face_landmarks):
        single_lm_coord = face_landmarks.landmark[single_lm]  # hier wird auf die einzelnen LM zugegriffen
        # print("**get_lm_coord called**\nLM",single_lm,"coordinates are:\n", single_lm_coord)
        return single_lm_coord

    def get_lm_coord_xy(self, single_lm, face_landmarks):
        lm_xyz = face_landmarks.landmark[single_lm]
        lm_x = 1 * lm_xyz.x
        lm_y = 1 * lm_xyz.y
        # print("**get_lm_coord called**\nLM",single_lm,"coordinates are:\n", single_lm_coord)
        return lm_x, lm_y

    # self.get_lm_coord(self, 4, face_landmarks)

    def get_abs_point_from_single_lm(self, single_lm, image_rgb, face_landmarks):
        single_lm_coord = self.get_lm_coord(single_lm, face_landmarks)
        abs_lm_x, abs_lm_y = self.get_abs_lm_xy(image_rgb, single_lm_coord)
        self.get_abs_point(abs_lm_x, abs_lm_y)
        abs_point = (abs_lm_x, abs_lm_y)
        print("LM", single_lm, "coordinates:\n"
                               "absolute x:", abs_lm_x, "\n"
                                                        "absolute y:", abs_lm_y)
        return abs_point

    # self.get_abs_point_from_single_lm(4, image_rgb, face_landmarks)

    def start_face_mesh(self, image_rgb):
        """
        starts mediapipe facemesh and returns frame containing the image with 477 Landmarks
        :param image_rgb: takes image in rgb format
        :return: frame containing the image with 477 Landmarks: image_face_mesh
        """
        # instance of face_mesh is created
        mp_face_mesh = mp.solutions.face_mesh

        # parameters for face_mesh are set
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                static_image_mode=False,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:
            # This is where the magic happens: 477 Landmarks are tracked with face_mesh
            image_face_mesh = face_mesh.process(image_rgb)

        return image_face_mesh

    def get_face_landmarks(self, image_rgb):
        image_face_mesh = self.start_face_mesh(image_rgb)
        face_landmarks = image_face_mesh.multi_face_landmarks
        return face_landmarks

    def processMP(self, image_rgb, region):
        image_face_mesh = self.start_face_mesh(image_rgb)
        # TODO auslagern und implement into csvExport.write_row
        #
        #  def calibrate_alignment(position):
        #     # Führen Sie hier den eigentlichen Kalibrierungscode basierend auf der Position durch
        #     print(f"Calibrating {position}...") # Beispielhaftes Ausgabe-Statement

        # check, if face_mesh has detected a face and Landmarks are drawn
        if image_face_mesh.multi_face_landmarks:

            filename = 'all_Lms'
            self.header_written = self.csv_export.write_header_all_lms(filename, 'abs_dist_nosetip_vert_top')

            for face_landmarks in image_face_mesh.multi_face_landmarks:
                abs_dist_nosetip_vert_top = self.abs_distance_from_lms(self.nosetip, self.ref_vert_top, image_rgb,
                                                                       face_landmarks)
                csv_data = str(abs_dist_nosetip_vert_top) + ';'
                self.csv_export.write_row_from_lms(filename, self.frame_id, face_landmarks, csv_data)

                # TODO Funktion zum aufnehmen der einzelnen kopfpositionen in jeweils einer eigenen csv datei

                # **Funktionsaufruf** drawpartLM()  hier werden die ausgewählten LM´s eingezeichnet
                self.drawPartLM(region, image_rgb, face_landmarks)

        self.frame_id += 1
        print("******************* frame", +self.frame_id, " handled ********************+")


if __name__ == "__main__":
    pass

# **Funktionsaufruf** Algorithm for calculating the euclidian distance, region, threshold and duration as parameters

# Es müssen nur die Landmarks welche für die Distanzberechnung herangeogen werden normalisiert weredn.

# TODO als einzelne Funktion: Berechnung als funktionsaufrauf auslagern -> dort dann auf Schwellwert über/unterschreitung prüfen
# mit euklidischer distanz die werte berechnen

# TODO als einzelne Funktion: zudem auf die eingestellte Dauer prüfen, bevor die gewählte aktion z.b. Mausklick ausgeführt wird

# TODO als einzelne Funktion: nur die landmarks einzeichnen, welche auch verwendet werden .

# für die gewählte aktion z.b. Mausklick kann eine vorgegebene Library (Package Mouse and Keybaord)
# als Klassen verwendet werden, auf die dann hier zugegriffen wird
