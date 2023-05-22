# This is FaceForIO
import Interface
import OpenCvStream
import MediapipeStream
import CsvExport

import time

from tkinter import Tk


def wait_for_space():
    input("Press Space to continue...")

def start_Interface(opencv,mp):
    """
    starts main Interface with OpenCvStream and MediapipeStream Objects
    :param opencv: OpenCvStream Object
    :param mp: MediapipeStream Object
    :return: Interface object as: interface
    """
    interface = Interface.Interface(opencv, mp) #create interface Object
    interface.run()
    return interface, interface.task



if __name__ == "__main__":
    task = 'run Interface'
    selected_regions = None
    current_position = 0
    count=0
    opencv = OpenCvStream.OpenCvStream()  # create an instance of the OpenCvStream class
    mp = MediapipeStream.MediapipeStream() # create an instance of the MediapipeStream class
    csv_export = CsvExport.CsvExport()  # create an instance of the CsvExport class



    # Start reading from webcam and return as image_bgr
    image_bgr = opencv.get_image_bgr()
    while True:
        # image is transferred from bgr (opencv Format) to rgb (mediapipe Format)
        # and handed over frame by frame as 'image_rgb'
        image_rgb, reading = opencv.get_image_rgb(image_bgr)

        if task != 'calibrate':
            if not selected_regions or selected_regions is None:
                interface, task = start_Interface(opencv, mp)
                selected_regions, region_settings = interface.get_regions_settings()
            print("Selected regions:", selected_regions)
            print("Region settings:", region_settings)
            region = selected_regions
        if selected_regions :
            task = 'display_regions'
        # TODO fix this: head_position, task = interface.get_head_position
        if task == 'calibrate':
            head_positions = ["straight", "up", "down", "left", "right"]
            head_position = head_positions[current_position]
            count += 1
            if count == 31:
                interface, task = start_Interface(opencv, mp)
                head_positions = ["straight", "up", "down", "left", "right"]
                head_position = head_positions[current_position]
                current_position += 1
                count=0
                if current_position == 4:
                    task='run Interface'

        # image_rgb is handed over to the main MediapipeStream, where it is processed
        # (Landmarks tracked, drawn, exportet as .csv)

        mp.processMP(image_rgb, region, head_position, task)

        # image with Landmark annotations is transferred from rgb (mediapipe Format)
        # to bgr (opencv Format) and displayed via opencv
        if not opencv.show_image(image_rgb):
            break
