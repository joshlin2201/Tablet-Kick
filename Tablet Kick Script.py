import tkinter as tk
from tkinter import ttk
import time
import threading
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput import keyboard

class TabletKickApp:
    def __init__(self, master):
        self.master = master
        master.title("Tablet Kick Controller")

        self.is_active = False
        self.action_in_progress = False  # Flag to disable key press while macro is running
        self.throw_key = tk.StringVar(value='q')  # Default to 'q'
        self.kick_key = tk.StringVar(value='f')  # Default to 'f'
        self.activation_key = tk.StringVar(value='f')  # Default to 'f' (same as kick)
        self.delay = 0.06  # Set permanent delay between kick and throw to 0.06 seconds

        self.setup_ui()

        # Keyboard and Mouse controllers for pynput
        self.keyboard_controller = KeyboardController()
        self.mouse_controller = MouseController()

        # Keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.detect_activation_key)
        self.keyboard_listener.start()

    def setup_ui(self):
        # Setup UI components for configuring keys
        config_options = [
            ("Key assigned to \"throw\" and \"item in slot one\"", self.throw_key),
            ("Key assigned to \"kick\"", self.kick_key),
            ("Set Tablet Kick Key (usually same as kick)", self.activation_key)
        ]
        for label_text, variable in config_options:
            tk.Label(self.master, text=label_text).pack()
            button = tk.Button(self.master, text="Press to Set", command=lambda var=variable: self.set_key(var))
            button.pack()
            tk.Label(self.master, textvariable=variable).pack()

        self.activate_button = tk.Button(self.master, text="Activate Macro (OFF)", command=self.toggle_macro)
        self.activate_button.pack()

    def set_key(self, var):
        # Start a listener to set the specified variable to the pressed key
        listener = keyboard.Listener(on_press=lambda e: self.capture_key(e, var))
        listener.start()

    def capture_key(self, key, var):
        # Capture key press and assign it to the appropriate variable
        try:
            if isinstance(key, keyboard.KeyCode):
                var.set(key.char)
            elif key == keyboard.Key.left:
                var.set('left click')
            else:
                var.set(str(key))
        except AttributeError:
            var.set(str(key))

        return False  # Stop listener

    def detect_activation_key(self, key):
        # Ignore activation key if macro is running
        try:
            if self.action_in_progress:
                print("Macro is already running, ignoring key press.")
                return  # Ignore key press if action is in progress
            
            # If macro is active and the right key is pressed, start the macro immediately
            if key.char == self.activation_key.get() and self.is_active and not self.action_in_progress:
                self.perform_tablet_kick()  # Call the macro function directly without delay
                self.action_in_progress = True  # Prevent further key presses while macro is running
                print("Macro started immediately.")
        except AttributeError:
            pass

    def toggle_macro(self):
        # Toggle the macro activation state and update the button text
        self.is_active = not self.is_active
        status_text = "ON" if self.is_active else "OFF"
        self.activate_button.config(text=f"Activate Macro ({status_text})")

    def perform_tablet_kick(self):
        # Simulate a kick and throw action with a delay in between
        print("Performing tablet kick...")

        # Simulate kick action (press the kick key)
        self.keyboard_controller.press(self.kick_key.get())
        self.keyboard_controller.release(self.kick_key.get())

        # Delay for the throw action (left click or other throw key)
        threading.Timer(self.delay, self.throw_action).start()

    def throw_action(self):
        # Perform the throw action
        if self.throw_key.get() == 'left click':
            self.mouse_controller.click(Button.left, 1)  # Left mouse click
        else:
            self.keyboard_controller.press(self.throw_key.get())
            self.keyboard_controller.release(self.throw_key.get())

        # Reset action_in_progress after the macro finishes
        self.action_in_progress = False
        print("Macro finished, activation key is enabled again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TabletKickApp(root)
    root.mainloop()
