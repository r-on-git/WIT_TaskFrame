

# Set up CSV writer
with open('facial_landmarks.csv', mode='w') as csv_file:
    fieldnames = ['frame', 'x0', 'y0', 'x1', 'y1', ..., 'x467', 'y467']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB for Mediapipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe Face Mesh
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw the face landmarks on the frame
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACE_CONNECTIONS)

                # Write the face landmarks to the CSV file
                row = {'frame': cap.get(cv2.CAP_PROP_POS_FRAMES)}
                for i, landmark in enumerate(face_landmarks.landmark):
                    row[f'x{i}'] = landmark.x
                    row[f'y{i}'] = landmark.y
                writer.writerow(row)