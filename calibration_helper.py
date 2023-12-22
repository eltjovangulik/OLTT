#The first part of the calibration is to create a Python script to display alternating black and white patterns on a local Windows device. The patterns should change at a strict time frame, allowing the QT Py and light sensor to measure the time between the patterns.

import tkinter as tk
import time

def alternate_colors():
    """
    Function to alternate the canvas background color between white and black.
    This alternation continues indefinitely in a loop.
    """
    current_color = 'white'
    while True:
        # Change the canvas background color
        canvas.config(bg=current_color)

        # Update the root window to reflect the color change
        root.update()

        # Pause for 0.5 seconds before changing the color again
        time.sleep(0.5)

        # Toggle the color for the next iteration
        current_color = 'black' if current_color == 'white' else 'white'

def on_key_press(event):
    """
    Function to handle key press events.
    Specifically, it allows the user to press the 'Escape' key to exit.
    """
    if event.keysym == 'Escape':
        root.destroy()  # Close the application

# Create the main window
root = tk.Tk()
root.attributes('-fullscreen', True)  # Set the window to full-screen mode

# Create a canvas widget, which will be used to display the colors
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)  # Make the canvas expand to fill the window

# Bind the 'Escape' key to the on_key_press function for graceful exit
root.bind('<KeyPress>', on_key_press)

# Schedule the alternate_colors function to run after 1 second
root.after(1000, alternate_colors)

# Start the Tkinter event loop
root.mainloop()
