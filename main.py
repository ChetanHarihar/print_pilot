from settings import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure window properties
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        # Set the title
        self.title("Print Pilot")
        # Set CTk appearance mode
        ctk.set_appearance_mode("Light")
        # Bind the close button (X button) to the `on_closing` function
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Show a confirmation dialog
        if messagebox.askokcancel("Quit", "Do you want to close the application?"):
            self.destroy()  # Close the window if 'OK' is clicked

if __name__ == "__main__":
    app = App()
    app.mainloop()