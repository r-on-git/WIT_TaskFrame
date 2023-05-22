"""
Class for representing test data, not needed if real landmarks are used.
"""
import os


class CsvExport:
    def __init__(self):
        self.header_written = False
        self.sep = ";"

    # header_string=f'frame_id{sep}lm_000_x{sep}lm_000_y{sep}lm_001_x{sep}lm_001_y{sep}nose_dist{sep}nose_ear'
    # header_string=f'frame_id{sep}lm_000_x{sep}lm_000_y{sep}lm_001_x{sep}lm_001_y'

    """
    Writes the header line to the file 'filename'.csv
    """

    def write_header_all_lms(self, filename, header_string_addition):
        """
        writes the header of the "filename".csv file with all Landmarks
        in format: frame_id;lm_000_x;lm_000y;lm_001_x;...lm_477_y;additional_column
        for Data Export
        :param self:
        :param  filename: name String of the file "filename".csv
        :param header_string_addition: a String that will be added as a column headline at the end after all 477 LM´s x,y
        set it to None if not needed
        :return: Bool: header_written=True to check if the header is already set
        """
        if self.header_written:
            return self.header_written

        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}" + ".csv", 'w', newline='') as csv_file:
            header_string = f'frame_id'
            for lm_id in range(478):
                header_string += f"{self.sep}lm_{lm_id:03d}_x{self.sep}lm_{lm_id:03d}_y"
            if header_string_addition:
                header_string = header_string + self.sep + header_string_addition
            csv_file.writelines(header_string + "\r\n")
            self.header_written = True
            print("header written")
            return self.header_written

    def write_header_from_lm(self, filename, frame_id, lm_id):
        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}" + ".csv", 'w', newline='') as csv_file:
            for lm_id in range(478):
                header_string = f"{self.sep}lm_{lm_id:03d}_x{self.sep}lm_{lm_id:03d}_y"
                csv_file.writelines(header_string + "\r\n")

    """
    Writes a row line with the given data to the file "filename".csv
    """

    def write_row(self, filename, frame_id, row_data):
        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}.csv", 'a', newline='') as csv_file:
            row = f"{frame_id}"
            for lm_id in range(len(row_data)):
                row = row + self.sep
                row = row + f"{row_data[lm_id]['lm_x']}{sep}{row_data[lm_id]['lm_y']}"
            csv_file.writelines(row + "\r\n")

    def calculate_mean(self, values):
        return sum(values) / len(values)

    def calculate_std(self, values, mean):
        squared_diff = [(val - mean) ** 2 for val in values]
        variance = sum(squared_diff) / len(values)
        std_deviation = variance ** 0.5
        return std_deviation

    def write_row_from_lm(self, filename, frame_id, lm_id, lm):
        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}.csv", 'a', newline='') as csv_file:
            row = f"{frame_id}" + self.sep + f"{lm_id}" + self.sep + str(lm.x) + self.sep + str(lm.y)
            csv_file.writelines(row + "\r\n")

    def write_row_from_lms(self, filename, frame_id, face_landmarks, data):
        """

        :param filename:
        :param frame_id:
        :param face_landmarks:
        :param data:
        :return:
        """

        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}.csv", 'a', newline='') as csv_file:
            row = f"{frame_id}" + self.sep
            for lm_id, lm in enumerate(face_landmarks.landmark):
                row += str(lm.x) + self.sep + str(lm.y) + self.sep
            row += str(data)
            csv_file.writelines(row + "\r\n")


    def write_row_from_lms_for_30fps(self, filename, frame_id, face_landmarks, data):
        """

        :param filename:
        :param frame_id:
        :param face_landmarks:
        :param data:
        :return:
        """

        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}.csv", 'a', newline='') as csv_file:
            row = f"{frame_id}" + self.sep
            for lm_id, lm in enumerate(face_landmarks.landmark):
                row += str(lm.x) + self.sep + str(lm.y) + self.sep
            row += str(data)
            current_frame_id = frame_id
            if current_frame_id <= 90:  # corresponds to about 3 sec at 30fp/s
                csv_file.writelines(row + "\r\n")
                current_frame_id += 1


    def write_row_from_abs_lms(self, filename, frame_id, face_landmarks, image_rgb):
        with open(os.path.abspath(".") + "\\extractedData\\" + f"{filename}.csv", 'a', newline='') as csv_file:
            row = f"{frame_id}" + self.sep
            for lm in enumerate(face_landmarks.landmark):
                row += str(lm.x) + self.sep + str(lm.y) + self.sep
            csv_file.writelines(row + "\r\n")


if __name__ == "__main__":
    pass
