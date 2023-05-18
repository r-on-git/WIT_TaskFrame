"""
Class for representing test data, not needed if real landmarks are used.
"""
class LMCoord:
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x=x
        self.y=y

frame_id=0
sep=";"
#header_string=f'frame_id{sep}lm_000_x{sep}lm_000_y{sep}lm_001_x{sep}lm_001_y{sep}nose_dist{sep}nose_ear'
#header_string=f'frame_id{sep}lm_000_x{sep}lm_000_y{sep}lm_001_x{sep}lm_001_y'
header_string=f'frame_id'
for idx in range(478):
    header_string+=f"{sep}lm_{idx:03d}_x{sep}lm_{idx:03d}_y"

"""
Writes the header line to the file some.csv
"""
def write_header():
    frame_id=0
    with open('some.csv', 'w', newline='') as f:
        f.writelines(header_string + "\r\n")

"""
Writes a row line with the given data to the file some.csv
"""
def write_row(row_data):
    global frame_id
    with open('some.csv', 'a', newline='') as f:
        row=f"{frame_id}"
        for lm_id in range(len(row_data)):
            row=row+sep
            row = row+f"{row_data[lm_id].x}{sep}{row_data[lm_id].y}"

        f.writelines(row+"\r\n")
        frame_id=frame_id+1

if __name__ == "__main__":
    write_header()
    # Erzeugen von Testdaten
    test_lm_data=[LMCoord(10,20),LMCoord(30,50)]
    for frame_id in range(100):
        write_row(test_lm_data)
