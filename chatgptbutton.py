import tkinter as tk

def change_color():
    # Toggle the color between red and green
    if button["bg"] == "red":
        button.configure(bg="green")
    else:
        button.configure(bg="red")

# Create the main window
root = tk.Tk()

# Create a button widget
button = tk.Button(root, text="Change Color", command=change_color, bg="red")
button.pack(pady=20)

# Start the event loop
root.mainloop()