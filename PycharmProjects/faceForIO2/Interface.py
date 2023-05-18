import tkinter as tk
import OpenCvStream


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("FaceForIO")
        self.geometry("400x300")

        self.var_eyebrow_right = tk.IntVar()
        self.var_eyebrow_left = tk.IntVar()
        self.var_both_eyebrows = tk.IntVar()
        self.var_blink_right = tk.IntVar()
        self.var_blink_left = tk.IntVar()
        self.var_blink_both = tk.IntVar()
        self.var_open_mouth = tk.IntVar()

        self.label_title = tk.Label(self, text="FaceForIO")
        self.label_title.place(x=200, y=10, anchor="center")

        self.label_select_input = tk.Label(self, text="Select input variables")
        self.label_select_input.place(x=200, y=40, anchor="center")

        self.checkbox_eyebrow_right = tk.Checkbutton(self, text="Eyebrow Right", variable=self.var_eyebrow_right)
        self.checkbox_eyebrow_right.place(x=180, y=80)

        self.checkbox_eyebrow_left = tk.Checkbutton(self, text="Eyebrow Left", variable=self.var_eyebrow_left)
        self.checkbox_eyebrow_left.place(x=30, y=80)

        self.checkbox_both_eyebrows = tk.Checkbutton(self, text="Both Eyebrows", variable=self.var_both_eyebrows)
        self.checkbox_both_eyebrows.place(x=30, y=140)

        self.checkbox_blink_right = tk.Checkbutton(self, text="Blink Right", variable=self.var_blink_right)
        self.checkbox_blink_right.place(x=180, y=110)

        self.checkbox_blink_left = tk.Checkbutton(self, text="Blink Left", variable=self.var_blink_left)
        self.checkbox_blink_left.place(x=30, y=110)

        self.checkbox_blink_both = tk.Checkbutton(self, text="Blink Both", variable=self.var_blink_both)
        self.checkbox_blink_both.place(x=180, y=140)

        self.checkbox_open_mouth = tk.Checkbutton(self, text="Open Mouth", variable=self.var_open_mouth)
        self.checkbox_open_mouth.place(x=30, y=170)

        self.next_button = tk.Button(self, text="Next", command=self.next_window)
        self.next_button.place(x=350, y=250, anchor="se")
        self.stream = OpenCvStream.OpenCvStream()  # create an instance of the openCvStream class

    @property
    def next_window(self):
        self.withdraw()
        self.region = ""
        if self.var_eyebrow_right.get() == 1:
            self.region += "Eyebrow Right, "
        if self.var_eyebrow_left.get() == 1:
            self.region += "Eyebrow Left, "
        if self.var_both_eyebrows.get() == 1:
            self.region += "Both Eyebrows, "
        if self.var_blink_right.get() == 1:
            self.region += "Blink Right, "
        if self.var_blink_left.get() == 1:
            self.region += "Blink Left, "
        if self.var_blink_both.get() == 1:
            self.region += "Blink Both, "
        if self.var_open_mouth.get() == 1:
            self.region += "Open Mouth, "

        self.region = self.region[:-2]

        selected_vars = self.region.split(", ")

        for var in selected_vars:
            new_window = tk.Toplevel(self)
            new_window.title("Settings")
            new_window.geometry("400x300")
            label_selected = tk.Label(new_window, text="Selected: " + var)
            label_selected.place(x=50, y=20)
            label_threshold = tk.Label(new_window, text="Threshold:")
            label_threshold.place(x=50, y=60)

            threshold_slider = tk.Scale(new_window, from_=0, to=1, orient="horizontal", resolution=0.05,
                                        tickinterval=0.05)
            threshold_slider.place(x=150, y=60)

            label_duration = tk.Label(new_window, text="Duration in ms:")
            label_duration.place(x=50, y=100)

            duration_slider = tk.Scale(new_window, from_=0, to=0.1, resolution=0.01, orient="horizontal")
            duration_slider.place(x=150, y=100)

            start_button = tk.Button(new_window, text="Start",
                                     command=lambda: self.stream.readCamera(self.region))
            start_button.place(x=350, y=250, anchor="se")

        return self.region
     #   def start_faceMeshAdapted(self):
    #        threshold = self.threshold_slider.get()
      #      duration = self.duration_slider.get()
      #      selected = self.var_selected
            # call faceMeshAdapted.py with the threshold, duration and selected variables as arguments
            # import subprocess
            # subprocess.call(["python", "faceMeshAdapted.py", threshold, duration, selected])

if __name__ == "__main__":
    app = Interface()
    app.mainloop()