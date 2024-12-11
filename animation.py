import tkinter as tk
from tkinter import Canvas, Scrollbar

class Timeline(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Event handlers - for adding callback functions outside of this file
        self.add_keyframe_handler = [self.add_keyframe_ui] # Listing of functions to call when a new keyframe is added
                                       # Functions added to this listing must take a single argument, frame number
        self.remove_keyframe_handler = [] # Functions added to this listing must take a single argument, frame number
        self.select_frame_handler = [self.select_frame_ui]
        self.copy_frame_handler = [] # By default, no function attached. And no arguments needed
        self.paste_frame_handler = [] # ^^^

        self.canvas_height = 40  # Height for the timeline
        self.canvas_width = 800  # Default canvas width
        self.canvas_pad_x = 0
        self.canvas_pad_y = 5
        self.canvas = Canvas(self, height=self.canvas_height, bg="#f0f0f0", scrollregion=(0, 0, 1000, self.canvas_height))
        self.scrollbar = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="top", fill="both", expand=True, padx=self.canvas_pad_x, pady=self.canvas_pad_y)
        self.scrollbar.pack(side="bottom", fill="x")

        self.keyframes = []  # List to store keyframe markers
        self.frames = []  # List to store frame lines

        self.selected_frame = None  # Currently selected frame

        # Buttons for adding and removing keyframes
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x")

        self.add_keyframe_btn = tk.Button(self.button_frame, text="Add Keyframe", command=self.add_keyframe)
        self.add_keyframe_btn.pack(side="left")

        self.remove_keyframe_btn = tk.Button(self.button_frame, text="Remove Keyframe", command=self.remove_keyframe)
        self.remove_keyframe_btn.pack(side="left")

        self.copy_frame_btn = tk.Button(self.button_frame, text="Copy Frame", command=self.copy_frame)
        self.copy_frame_btn.pack(side="left")

        self.paste_frame_btn = tk.Button(self.button_frame, text="Paste Frame", command=self.paste_frame)
        self.paste_frame_btn.pack(side="left")

        self.padding_left = 20  # Initial left padding (can be changed)
        self.frame_spacing = 50  # Space between frames
        self.total_frames = 20  # Number of frames

        self.draw_frames()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Bind resize event to adjust canvas layout
        master.bind("<Configure>", self.on_resize)

    def draw_frames(self):
        # Calculate total width for frames based on padding and spacing
        total_width = self.padding_left + self.frame_spacing * (self.total_frames - 1) + 50  # Extra padding on right
        self.canvas.config(scrollregion=(0, 0, total_width, self.canvas_height))

        # Draw vertical lines to represent frames
        for i in range(self.total_frames):
            x = self.padding_left + i * self.frame_spacing
            frame = self.canvas.create_line(x, 0, x, self.canvas_height, fill="gray")  # Shorter lines
            self.frames.append(frame)

    def on_canvas_click(self, event):
        # Adjust event.x by the canvas's current scroll offset
        scroll_offset = self.canvas.canvasx(0)
        click_x = event.x + scroll_offset

        # Handle clicks on the canvas to select a frame
        for i, frame in enumerate(self.frames):
            x1, _, x2, _ = self.canvas.coords(frame)
            if x1 - 5 <= click_x <= x2 + 5:  # Click within the frame line area
                self.select_frame(i)
                break

    def add_keyframe_ui(self, frame_num):
        # Add a keyframe marker to the selected frame
        if self.selected_frame is not None:
            x = self.selected_frame * self.frame_spacing + self.padding_left
            # Get the coordinates of the selected frame line
            x1, y1, x2, y2 = self.canvas.coords(self.frames[self.selected_frame])
            # Calculate the center of the frame line
            center_y = (y1 + y2) // 2

            # Create the keyframe polygon centered around the frame line
            keyframe = self.canvas.create_polygon(
                x - 10, center_y,  # Top left
                x, center_y - 10,      # Top center
                x + 10, center_y,  # Top right
                x, center_y + 10,       # Bottom center
                fill="blue", outline="black"
            )
            self.keyframes.append((self.selected_frame, keyframe))

    def add_keyframe(self):
        # Calculate the frame number from the x-coordinate of the selected frame
        x = self.selected_frame * self.frame_spacing + self.padding_left
        frame_number = (x - self.padding_left) // self.frame_spacing
        for func in self.add_keyframe_handler:
            func(frame_number)

    def remove_keyframe(self):
        # Remove the keyframe at the selected frame
        if self.selected_frame is not None:
            for i, (frame_index, keyframe) in enumerate(self.keyframes):
                if frame_index == self.selected_frame:
                    self.canvas.delete(keyframe)
                    del self.keyframes[i]
                    break

    def select_frame_ui(self, frame_num):
        # Highlight the selected frame
        if self.selected_frame is not None:
            # Reset previous selection
            self.canvas.itemconfig(self.frames[self.selected_frame], fill="gray")

        self.selected_frame = frame_num
        self.canvas.itemconfig(self.frames[frame_num], fill="red")

    def select_frame(self, frame_num):
        for func in self.select_frame_handler:
            func(frame_num)

    def copy_frame(self):
        for func in self.copy_frame_handler:
            func()
    
    def paste_frame(self):
        for func in self.paste_frame_handler:
            func()

    def on_resize(self, event):
        # Adjust canvas layout when window is resized
        self.canvas.config(scrollregion=(0, 0, self.canvas.bbox("all")[2], self.canvas_height))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Timeline Element")
    root.geometry("800x90")  # Adjusted height for better view
    timeline = Timeline(root)
    root.mainloop()
