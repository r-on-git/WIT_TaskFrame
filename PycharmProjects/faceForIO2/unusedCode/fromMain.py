'''


def calibrate_alignment(position):
    print(f"Calibrating {position}...") # Beispielhaftes Ausgabe-Statement



# calibrate_3sec for use with terminal

def calibrate_3sec():
    print("Press Space to start calibrating")
    wait_for_space()

    print("Look straight into the camera and hold steady for 3 sec.")
    wait_for_space()
    time.sleep(3)
    calibrate_alignment("straight")

    print("Stay centered in front of the camera, move your head up and hold steady for 3 sec.")
    wait_for_space()
    time.sleep(3)
    calibrate_alignment("up")

    print("Stay centered in front of the camera, move your head down and hold steady for 3 sec.")
    wait_for_space()
    time.sleep(3)
    calibrate_alignment("down")

    print("Stay centered in front of the camera, move your head left and hold steady for 3 sec.")
    wait_for_space()
    time.sleep(3)
    calibrate_alignment("left")

    print("Stay centered in front of the camera, move your head right and hold steady for 3 sec.")
    wait_for_space()
    time.sleep(3)
    calibrate_alignment("right")
'''