import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageTk, ImageOps
import random
import math
import asyncio

from designtool.filesave import *
from designtool.colorconversion import *
from lightslib.LightsController import LightsController

controller = LightsController()
asyncio.run(controller.connect(run_simul_on_fail=False))

# Load the circle sprite and prepare colored versions
def load_circle_sprites(sprite_path, colors, scale_factor=0.5):
    base_circle = Image.open(sprite_path).convert("RGBA")
    resized_circle = base_circle.resize(
        (int(base_circle.width * scale_factor), int(base_circle.height * scale_factor)),
        Image.Resampling.LANCZOS  # High-quality resizing
    )
    sprites = {}
    for color in colors:
        tinted_circle = ImageOps.colorize(resized_circle.split()[3], black="black", white=color)
        sprites[color] = ImageTk.PhotoImage(tinted_circle)
    return sprites, resized_circle

# Dynamically add a new sprite for a color
def add_sprite_for_color(color):
    if color not in circle_sprites:
        tinted_circle = ImageOps.colorize(base_circle.split()[3], black="black", white=color)
        circle_sprites[color] = ImageTk.PhotoImage(tinted_circle)

# Calculate the distance from the cursor to the center of the circle in the widget
def distance_to_circle_center(widget, event):
    widget_x, widget_y = widget.winfo_rootx(), widget.winfo_rooty()
    cursor_x, cursor_y = event.x_root, event.y_root
    circle_center_x = widget_x + widget.winfo_width() / 2
    circle_center_y = widget_y + widget.winfo_height() / 2
    return math.sqrt((cursor_x - circle_center_x) ** 2 + (cursor_y - circle_center_y) ** 2)

# Handle erasing on mouse hover with proximity check
def on_mouse_drag_erase(event):
    if erase_mode and mouse_down:
        widget = root.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Label):
            distance = distance_to_circle_center(widget, event)
            if distance <= circle_radius:
                widget.config(image=circle_sprites["#1a1a1a"])  # Erase the color
                widget.color = "#1a1a1a"

# Handle painting on mouse hover with proximity check
def on_mouse_drag_paint(event):
    if paint_mode and mouse_down:
        widget = root.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Label):
            distance = distance_to_circle_center(widget, event)
            if distance <= circle_radius:
                add_sprite_for_color(selected_color)
                widget.config(image=circle_sprites[selected_color])
                widget.color = selected_color

# Updated on_mouse_drag function to handle erase mode
def on_mouse_drag(event):
    if paint_mode:
        on_mouse_drag_paint(event)
    elif erase_mode:
        on_mouse_drag_erase(event)

# Handle mouse click for starting the paint mode
def on_mouse_press(event):
    global mouse_down
    mouse_down = True
    on_mouse_drag(event)  # Paint the first circle immediately on press

# Handle mouse release to stop painting
def on_mouse_release(event):
    global mouse_down
    mouse_down = False

# Clear all circles on the grid
def clear_grid():
    for row in range(rows):
        for col in range(cols):
            labels[row][col].config(image=circle_sprites["#1a1a1a"])
            labels[row][col].color = "#1a1a1a"


# Launch a color picker tool
def choose_color():
    global selected_color
    color_code = colorchooser.askcolor(title="Choose Color")[1]  # Returns a tuple (rgb, hex)
    if color_code:
        selected_color = color_code
        add_sprite_for_color(selected_color)
        color_picker_button.config(bg=selected_color)

# Toggle paint mode
def toggle_paint_mode():
    global paint_mode, erase_mode
    paint_mode = not paint_mode
    erase_mode = False # Disable erase mode when paint mode is activated
    erase_button.config(relief=tk.RAISED)  # Reset erase button
    paint_bucket_button.config(relief=tk.SUNKEN if paint_mode else tk.RAISED)

# Toggle erase mode
def toggle_erase_mode():
    global erase_mode, paint_mode
    erase_mode = not erase_mode
    paint_mode = False  # Disable paint mode when erase mode is activated
    paint_bucket_button.config(relief=tk.RAISED)  # Reset paint button
    erase_button.config(relief=tk.SUNKEN if erase_mode else tk.RAISED)

# Create the main window
root = tk.Tk()
root.title("Lights Design Tool")

# Parameters for the grid
rows, cols = 20, 20
circle_padding = 0  # Removed padding
colors = ['#1a1a1a'] # This list of colors will expand as we draw circles of different colors
selected_color = "white"  # Default selected color
paint_mode = False
erase_mode = False  # Track whether erase mode is active
mouse_down = False  # Track whether the mouse button is pressed

# Load circle sprites
circle_sprites, base_circle = load_circle_sprites("designtool/circle.png", colors)
circle_radius = base_circle.width / 2  # Calculate the radius of the circles

# Create a frame for the toolbar
toolbar = tk.Frame(root, bg="lightgray", padx=5, pady=5)
toolbar.pack(fill=tk.X)

# Add "Clear Grid" button
clear_button = tk.Button(toolbar, text="Clear Grid", command=clear_grid)
clear_button.pack(side=tk.LEFT, padx=5)

# Add "Send Config" button
send_button = tk.Button(toolbar, text="Send Config")
send_button.pack(side=tk.LEFT, padx=5)

# Add "Save to File" button
save_button = tk.Button(toolbar, text="Save to File")
save_button.pack(side=tk.LEFT, padx=5)

# Add colored square icon (color picker)
color_picker_button = tk.Button(
    toolbar, text="  ", bg=selected_color, width=3, command=choose_color
)
color_picker_button.pack(side=tk.LEFT, padx=5)

# Add paint bucket icon (toggle paint mode)
paint_bucket_icon = ImageTk.PhotoImage(Image.open("designtool/paint_bucket.png").resize((24, 24)))
paint_bucket_button = tk.Button(toolbar, image=paint_bucket_icon, command=toggle_paint_mode)
paint_bucket_button.pack(side=tk.LEFT, padx=5)

# Add erase icon (toggle erase mode)
erase_icon = ImageTk.PhotoImage(Image.open("designtool/erase_icon.png").resize((24, 24)))
erase_button = tk.Button(toolbar, image=erase_icon, command=toggle_erase_mode)
erase_button.pack(side=tk.LEFT, padx=5)

# Create a frame to hold the grid
frame = tk.Frame(root, bg="white")
frame.pack()

# Store references to the Labels
labels = [[None for _ in range(cols)] for _ in range(rows)]

# Create the grid of labels with sprites
for row in range(rows):
    for col in range(cols):
        color = random.choice(colors)
        label = tk.Label(frame, image=circle_sprites[color], bg="white", borderwidth=0)
        label.color = color  # Track the current color
        label.grid(row=row, column=col, padx=circle_padding, pady=circle_padding)
        label.bind("<Button-1>", on_mouse_press)
        label.bind("<B1-Motion>", on_mouse_drag)
        label.bind("<ButtonRelease-1>", on_mouse_release)
        labels[row][col] = label


def labels_to_grid(labels):
    """
    Convert a 2D array of labels into a grid of hexadecimal values.

    Args:
        labels (list of list of tk.Label): A 2D array of tkinter Label widgets.

    Returns:
        list of list of str: A 2D array of 2-digit hexadecimal strings.
    """
    # Initialize an empty grid with dimensions transposed
    grid = [[None for _ in range(len(labels))] for _ in range(len(labels[0]))]

    for i, row in enumerate(labels):
        for j, label in enumerate(row):
            # Get the color of the label (assuming it is stored as an RGB tuple)
            color_code = label.color  # label.color is expected to be an RGB tuple
            if not color_code.startswith('#'):
                color_code = root.winfo_rgb(label.color)

            # Convert the RGB color to a 2-digit hexadecimal value
            hex_value = rgb_to_hex(color_code)

            # Assign the transposed value
            grid[j][i] = hex_value

    return grid

# Placeholder function for sending the grid configuration
async def send_config():
    print("Send Config: Current grid configuration sent!")  # Replace with actual functionality
    await controller.drawFrame(labels_to_grid(labels))

def send_button_callback():
    asyncio.run(send_config())

def save_button_callback():
    file_path = filedialog.asksaveasfilename(defaultextension=".lcf", filetypes=[("Lights creation file", "*.lcf"), ("All files", "*.*")])
    if file_path:
        save_grid_to_file(labels_to_grid(labels), file_path)

send_button.configure(command=send_button_callback)
save_button.configure(command=save_button_callback)

# Run the Tkinter main loop
root.mainloop()
