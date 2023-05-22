import tkinter as tk
from tkinter import messagebox


class Interface:
    def __init__(self,opencv,mp):
        self.task = 'run_Interface'
        self.selected_regions = []
        self.region_settings = {}
        self.head_positions = ["straight", "up", "down", "left", "right"]
        self.current_position = 0

        self.root = tk.Tk()
        self.root.title("FaceForIO")
        self.root.geometry("400x300")

        self.var_eyebrow_left = tk.IntVar()
        self.var_eyebrow_right = tk.IntVar()
        self.var_both_eyebrows = tk.IntVar()
        self.var_left_eye = tk.IntVar()
        self.var_right_eye = tk.IntVar()
        self.var_both_eyes = tk.IntVar()
        self.var_mouth = tk.IntVar()

        self.label_title = tk.Label(self.root, text="FaceForIO")
        self.label_title.place(x=200, y=10, anchor="center")

        self.label_select_input = tk.Label(self.root, text="Select input variables")
        self.label_select_input.place(x=200, y=40, anchor="center")

        self.checkbox_eyebrow_left = tk.Checkbutton(self.root, text="Left Eyebrow", variable=self.var_eyebrow_left)
        self.checkbox_eyebrow_left.place(x=30, y=80)

        self.checkbox_eyebrow_right = tk.Checkbutton(self.root, text="Right Eyebrow", variable=self.var_eyebrow_right)
        self.checkbox_eyebrow_right.place(x=180, y=80)

        self.checkbox_both_eyebrows = tk.Checkbutton(self.root, text="Both Eyebrows", variable=self.var_both_eyebrows)
        self.checkbox_both_eyebrows.place(x=30, y=140)

        self.checkbox_left_eye = tk.Checkbutton(self.root, text="Left Eye", variable=self.var_left_eye)
        self.checkbox_left_eye.place(x=180, y=110)

        self.checkbox_right_eye = tk.Checkbutton(self.root, text="Right Eye", variable=self.var_right_eye)
        self.checkbox_right_eye.place(x=30, y=110)

        self.checkbox_both_eyes = tk.Checkbutton(self.root, text="Both Eyes", variable=self.var_both_eyes)
        self.checkbox_both_eyes.place(x=180, y=140)

        self.checkbox_mouth = tk.Checkbutton(self.root, text="Mouth", variable=self.var_mouth)
        self.checkbox_mouth.place(x=30, y=170)

        self.next_button = tk.Button(self.root, text="Next", command=self.open_settings)
        self.next_button.place(x=350, y=250, anchor="se")

        self.calibrate_button = tk.Button(self.root, text="Calibrate", command=self.open_calibration)
        self.calibrate_button.place(x=10, y=250, anchor="sw")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def open_settings(self):
        self.selected_regions = []

        if self.var_eyebrow_left.get() == 1:
            self.selected_regions.append("leftEyebrow")
        if self.var_eyebrow_right.get() == 1:
            self.selected_regions.append("rightEyebrow")
        if self.var_both_eyebrows.get() == 1:
            self.selected_regions.append("bothEyebrows")
        if self.var_left_eye.get() == 1:
            self.selected_regions.append("leftEye")
        if self.var_right_eye.get() == 1:
            self.selected_regions.append("rightEye")
        if self.var_both_eyes.get() == 1:
            self.selected_regions.append("bothEyes")
        if self.var_mouth.get() == 1:
            self.selected_regions.append("mouth")

        if len(self.selected_regions) == 0:
            messagebox.showinfo("No Region Selected", "Please select at least one region.")
        else:
            self.root.withdraw()
            self.region_settings = {}
            self.configure_settings(0)

    def configure_settings(self, index):
        if index >= len(self.selected_regions):
            self.show_selected_regions()
            return

        region = self.selected_regions[index]

        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x200")

        label_selected = tk.Label(settings_window, text="Selected: " + region)
        label_selected.place(x=50, y=20)

        label_threshold = tk.Label(settings_window, text="Threshold:")
        label_threshold.place(x=50, y=60)

        threshold_slider = tk.Scale(settings_window, from_=0, to=1, orient="horizontal", resolution=0.05,
                                    tickinterval=0.05)
        threshold_slider.place(x=150, y=60)

        label_duration = tk.Label(settings_window, text="Duration in ms:")
        label_duration.place(x=50, y=100)

        duration_slider = tk.Scale(settings_window, from_=0, to=0.1, resolution=0.01, orient="horizontal")
        duration_slider.place(x=150, y=100)

        def next_clicked():
            self.save_settings(index, region, threshold_slider.get(), duration_slider.get())
            settings_window.destroy()

        next_button = tk.Button(settings_window, text="Next", command=next_clicked)
        next_button.place(x=350, y=150, anchor="se")

        settings_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_settings(self, index, region, threshold, duration):
        self.region_settings[region] = (threshold, duration)
        self.configure_settings(index + 1)

    def show_selected_regions(self):
        self.root.withdraw()

        result_window = tk.Toplevel(self.root)
        result_window.title("Selected Regions")
        result_window.geometry("400x300")

        label_selected = tk.Label(result_window, text="Selected Regions:")
        label_selected.place(x=50, y=20)

        label_thresholds = tk.Label(result_window, text="Thresholds:")
        label_thresholds.place(x=200, y=20)

        label_durations = tk.Label(result_window, text="Durations:")
        label_durations.place(x=300, y=20)

        row = 40
        for region in self.selected_regions:
            threshold, duration = self.region_settings.get(region, (0, 0))

            label_region = tk.Label(result_window, text=region)
            label_region.place(x=50, y=row)

            label_threshold = tk.Label(result_window, text=threshold)
            label_threshold.place(x=200, y=row)

            label_duration = tk.Label(result_window, text=duration)
            label_duration.place(x=300, y=row)

            row += 20

        start_button = tk.Button(result_window, text="Start", command=self.start)
        start_button.place(x=350, y=250, anchor="se")

        result_window.protocol("WM_DELETE_WINDOW", self.on_close)
        result_window.focus()
        # result_window.bind('<Return>', lambda event: self.start())

    def start(self):

        self.root.destroy()

    def get_selected_regions(self):
        return self.selected_regions

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()

    def get_regions_settings(self):
        """

        :return:
        """
        selected_regions = self.get_selected_regions()
        region_settings = {}
        for region in selected_regions:
            threshold, duration = self.region_settings[region]
            region_settings[region] = {
                'threshold': threshold,
                'duration': duration
            }
        return selected_regions, region_settings


    def open_calibration(self):
        self.task = 'calibrate'
        calibrate_window = tk.Toplevel(self.root)
        calibrate_window.title("Calibrate")
        calibrate_window.geometry("400x200")

        head_position = self.head_positions[self.current_position] #TODO currentProblem with headposition
        if self.current_position >= len(self.head_positions):
            self.root.unbind("<Key>") #TODO überprüfen ob notwendig
            return

        if self.current_position == 0:
            label_instructions = tk.Label(calibrate_window, text="Look straight into the camera\n"
                                                                 "and press space,\n"
                                                                 "then hold steady for 3 sec.")
            self.current_position += 1
        else:
            label_instructions = tk.Label(calibrate_window, text="Stay centered in front of the camera,\n"
                                                                 f"move your head {head_position} and hold steady for 3 sec.")
            self.current_position += 1
        label_instructions.pack(pady=20)

        self.next_button = tk.Button(calibrate_window, text="start callibration", command=self.get_head_position)
        self.next_button.place(x=350, y=150, anchor="se")

        return head_position, self.task




    def get_head_position(self):
        self.task = 'calibrate'
        self.root.destroy()
        return self.task




