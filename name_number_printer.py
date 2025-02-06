from settings import *


class PrintNameNumber:
    def __init__(self, root, progress_var, status_label, popup, style=None, page_size=PAGE_SIZE,
                 max_width=MAX_WIDTH, name_number_list=None, print_color="black", output_directory=None):
        
        if isinstance(page_size, dict):
            page_size = (page_size['width'], page_size['height'])

        if not style:
            raise ValueError("Select style: 'style' argument is required.")
        if not name_number_list or not isinstance(name_number_list, list):
            raise ValueError("Name and number list is required.")

        self.root = root
        self.popup = popup  # Store the popup window
        self.progress_var = progress_var
        self.status_label = status_label
        self.style = style
        self.page_size = page_size
        self.max_width = max_width
        self.name_number_list = name_number_list
        self.print_color = print_color
        self.output_directory = output_directory

        self.set_style(self.style)

        # Schedule image generation to start *after* GUI renders
        self.root.after(100, self.generate_prints)

    def set_style(self, style: str):
        self.style = STYLES.get(style)
        if self.style:
            self.name_font_path = self.style.get("name_font_path")
            self.name_font_size = self.style.get("name_size")
            self.number_font_path = self.style.get("number_font_path")
            self.number_font_size = self.style.get("number_size")

            self.name_font = ImageFont.truetype(self.name_font_path, self.name_font_size)
            self.number_font = ImageFont.truetype(self.number_font_path, self.number_font_size)

            self.name_y_padding = self.style.get("name_y_padding")
            self.number_y_padding = self.style.get("number_y_padding")

    def create_print_surface(self):
        self.page = Image.new('RGBA', self.page_size, color=(255, 255, 255, 255))
        self.print_surface = ImageDraw.Draw(self.page)

    def print_name(self, name):
        name_box = self.print_surface.textbbox((0, 0), name, font=self.name_font)
        name_width = name_box[2] - name_box[0]
        name_height = int(name_box[3] - name_box[1] + self.name_font_size * 1.0)

        name_surface = Image.new('RGBA', (name_width, name_height), color=(255, 255, 255, 0))
        name_image = ImageDraw.Draw(name_surface)

        name_image.text((0, 0), name, fill=self.print_color, font=self.name_font, anchor=None)

        if name_width > self.max_width:
            name_surface = name_surface.resize((self.max_width, name_height), Image.Resampling.LANCZOS)

        name_x_position = (self.page_size[0] - name_surface.width) // 2
        name_y_position = self.name_y_padding

        self.page.paste(name_surface, (name_x_position, name_y_position), name_surface)

    def print_number(self, number):
        number_box = self.print_surface.textbbox((0, 0), number, font=self.number_font)
        number_width = number_box[2] - number_box[0]
        number_height = int(number_box[3] - number_box[1] + self.number_font_size * 1.0)

        number_surface = Image.new('RGBA', (number_width, number_height), color=(255, 255, 255, 0))
        number_image = ImageDraw.Draw(number_surface)

        number_image.text((0, 0), number, fill=self.print_color, font=self.number_font, anchor=None)

        if number_width > self.max_width:
            number_surface = number_surface.resize((self.max_width, number_height), Image.Resampling.LANCZOS)

        number_x_position = (self.page_size[0] - number_surface.width) // 2
        number_y_position = self.number_y_padding

        self.page.paste(number_surface, (number_x_position, number_y_position), number_surface)

    def save_page(self, name, number, index):
        if self.output_directory:
            os.makedirs(self.output_directory, exist_ok=True)
            filename = f'[{index}] {name}_{number}.png'
            file_path = os.path.join(self.output_directory, filename)

            mirrored_img = self.page.transpose(Image.FLIP_LEFT_RIGHT)
            mirrored_img.save(file_path)
            print(f"Image saved as '{file_path}'")

    def generate_prints(self):
        total = len(self.name_number_list)
        self.progress_var.set(0)

        # Ensure the status_label exists before trying to update it
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="Starting...")  # Show initial message

        self.root.update_idletasks()  # Force UI update

        for i, (name, number) in enumerate(self.name_number_list, start=1):
            self.create_print_surface()
            self.print_name(name)
            self.print_number(number)
            self.save_page(name, number, i)

            # Update progress bar and status text
            progress = int((i / total) * 100)
            self.progress_var.set(progress)

            # Ensure the status_label exists before updating
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                self.status_label.config(text=f"Generating {i}/{total}...")

            self.root.update_idletasks()  # Ensure real-time UI updates

        # Final update after all images are generated
        self.progress_var.set(100)

        # Ensure the status_label exists before updating
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text="Done!")  # Show completion message


def show_progress_popup(root, name_number_list):
    # Create a popup window
    popup = tk.Toplevel(root)
    popup.title("Progress")
    popup.geometry("350x150")
    popup.transient(root)  # Keeps popup on top
    popup.grab_set()  # Prevents interaction with main window

    # Center popup on screen
    popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (350 // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (150 // 2)
    popup.geometry(f"+{x}+{y}")

    # Progress Bar UI
    progress_var = tk.IntVar()

    progress_label = tk.Label(popup, text="Progress:", font=("Arial", 12))
    progress_label.pack()

    progress_bar = ttk.Progressbar(popup, orient="horizontal", length=300, mode="determinate", variable=progress_var)
    progress_bar.pack(pady=10)

    status_label = tk.Label(popup, text="Initializing...", font=("Arial", 10))
    status_label.pack()

    # Initialize PrintNameNumber for each style
    for style in STYLES.keys():
        PrintNameNumber(root, progress_var, status_label, popup, style=style, name_number_list=name_number_list,
                        output_directory=f"samples/{style}")

    popup.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Generator")

    # Button to start process
    generate_button = tk.Button(root, text="Generate Images", command=lambda: show_progress_popup(root, [
        ('CHETAN', '7'), ('PRATHAP', '6'), ('KUSHAL', '19'), ('ANANTH', '3')
    ]), font=("Arial", 12), padx=10, pady=5)

    generate_button.pack(pady=20)

    root.mainloop()