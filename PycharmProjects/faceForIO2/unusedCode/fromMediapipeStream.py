

''' output:to:csv Funktion 1.0
def output_to_csv(self, landmark_dict):
    with open(os.path.abspath(".") + "\\extractedData\\landmarks.csv", mode='w', newline='') as csv_file:
        fieldnames = ['frameid', 'landmark', 'x', 'y', 'abs_x', 'abs_y']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        # for self.frameid, landmarks_dict in enumerate(self.landmarks):
        # for landmark_idx, landmark_data in landmark_dict.items():
        for i in range(478):
            header_string = f'frame_id,lm_000_x,lm_000_y,lm_001_x,lm_001_y,...,nose_dist,nose_ear'

            writer.writerow({
                'frameid': f'{self.frame_id}',
                'landmark': f'{i}',
                'x': landmark_dict[i]['x'],
                'y': landmark_dict[i]['y'],
                'abs_x': landmark_dict[i]['abs_x'],
                'abs_y': landmark_dict[i]['abs_y']
            })
'''

'''version to write to csv with dictionary
landmark_dict = {}
for face_landmarks in image_face_mesh.multi_face_landmarks:
    for lm_id, lm in enumerate(face_landmarks.landmark):
        # print("drawPartLM('" + region, "') called")
        # Get landmark coordinates
        lm_x = lm.x
        lm_y = lm.y

        # Get absolute landmark coordinates
        abs_lm_x, abs_lm_y = self.absolute_lm(image_rgb, lm)
        landmark_dict[lm_id] = {'lm_x': lm_x, 'lm_y': lm_y, 'abs_x': abs_lm_x,
                                'abs_y': abs_lm_y}
    self.landmarks.append(landmark_dict)
    #self.output_to_csv(landmark_dict)
filename = 'testdata2'
CsvExport.write_header(self, filename)
CsvExport.write_row(self, filename,self.frame_id, landmark_dict)
'''

'''
# draws all possible landmarks and their connections in greyscale
for face_landmarks in image_face_mesh.multi_face_landmarks:
     mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_tesselation_style())
'''

'''
# solution, that draws only selected_lm without iterating through all Lm´s , might be faster

if image_face_mesh.multi_face_landmarks:
    for self.selected_lm in image_face_mesh.multi_face_landmarks: # image_face_mesh.multi_face_landmarks returns the full list of all LMs as NormalizedLandmark Object
        self.drawPartLM(region, image, self.selected_lm) 
'''

'''# implemented in
    def abs_distance_from_lms(self, lm1, lm2, image_rgb, face_landmarks):
    # code snippet to use dist_lm1_lm2 as a specific name and trigger for certain events
        dist_name = f"dist_{lm1}_{lm2}"  # Generate the variable name with lm1 and lm2 values
        locals()[dist_name] = dist  # Create a variable with the generated name and assign dist value to it
        if dist_name == 'dist_lm1_lm2':
            # specific task for specific distances
            pass
'''


'''calculate mean and std deviation with import statistics 
lm_x = [[] for _ in range(478)]
lm_y = [[] for _ in range(478)]

for face_landmarks in image_face_mesh.multi_face_landmarks:
    CsvExport.write_row_from_lms(self, filename, self.frame_id, face_landmarks)

    for lm_id, lm in enumerate(face_landmarks.landmark):
        lm_x[lm_id].append(lm.x)
        lm_y[lm_id].append(lm.y)

lm_x_mean = []
lm_x_stdev = []
lm_y_mean = []
lm_y_stdev = []

for lm_id in range(len(lm_x)):
    x_values = lm_x[lm_id]
    y_values = lm_y[lm_id]

    x_mean = statistics.mean(x_values)
    x_stdev = statistics.stdev(x_values) if len(x_values) >= 2 else 0.0
    y_mean = statistics.mean(y_values)
    y_stdev = statistics.stdev(y_values) if len(y_values) >= 2 else 0.0

    lm_x_mean.append(x_mean)
    lm_x_stdev.append(x_stdev)
    lm_y_mean.append(y_mean)
    lm_y_stdev.append(y_stdev)

for lm_id in range(len(lm_x_mean)):
    print(f"lm_id: {lm_id}, lm.x Mean: {lm_x_mean[lm_id]}, lm.x Stdev: {lm_x_stdev[lm_id]}")
    print(f"lm_id: {lm_id}, lm.y Mean: {lm_y_mean[lm_id]}, lm.y Stdev: {lm_y_stdev[lm_id]}")
'''

''' first implementation of select_lm_connections, only one region can be selected here
def select_lm_connections(self, region):
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
    for region in region:
        if region == 'leftEyebrow':
            select_lm_connections = face_mesh.FACEMESH_LEFT_EYEBROW
        elif region == 'rightEyebrow':
            select_lm_connections = face_mesh.FACEMESH_RIGHT_EYEBROW
        elif region == 'bothEyebrows':
            select_lm_connections = face_mesh.FACEMESH_RIGHT_EYEBROW + face_mesh.FACEMESH_LEFT_EYEBROW
        elif region == 'leftEye':
            select_lm_connections = face_mesh.FACEMESH_LEFT_EYE
        elif region == 'rightEye':
            select_lm_connections = face_mesh.FACEMESH_RIGHT_EYE
        elif region == 'bothEyes':
            select_lm_connections = face_mesh.FACEMESH_RIGHT_EYE + face_mesh.FACEMESH_LEFT_EYE
        elif region == 'noseTip':
            select_lm_connections = FACEMESH_NOSETIP
        elif region == 'mouth':
            select_lm_connections = face_mesh.FACEMESH_LIPS
        elif region == 'refVertical':
            select_lm_connections = FACEMESH_REF_VERTICAL
        elif region == 'refBetweenEyes':
            select_lm_connections = FACEMESH_BETWEEN_EYES
        elif region is None:
            select_lm_connections = None
        else:
            print("Invalid region, lefteyebrow will be selected")
            select_lm_connections = face_mesh.FACEMESH_LEFT_EYEBROW
            TODO: Error handling here
            return select_lm_connections
    '''