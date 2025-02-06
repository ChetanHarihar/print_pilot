from settings import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure window properties
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.title("Print Pilot")
        self.resizable(False, False)  # Disable resizing
        ctk.set_appearance_mode("Light")  # Set the theme appearance mode
        self.configure(fg_color="#E5E4E2")

        # Bind the close button (X button) to the `on_closing` function
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        self.selected_file_path = ''
        self.output_folder_path = ''
        self.selected_style = ''

        """
        Initialize the user interface.
        """
        # Label to do selection
        ctk.CTkLabel(master=self, text="Enter the details to generate print", font=("Arial", 18), fg_color="#E5E4E2").pack(pady=(20,10))

        # file selection frame
        file_sel_frame = ctk.CTkFrame(master=self, fg_color="#E5E4E2")
        file_sel_frame.pack(pady=10)

        # Label for file selection
        ctk.CTkLabel(master=file_sel_frame, text="Select file: ", font=("Arial", 14), fg_color="#E5E4E2").pack(side='left', padx=5)

        # Entry for file input
        self.input_file_path = ctk.CTkEntry(master=file_sel_frame, font=("Arial", 14), fg_color="white", width=300)
        self.input_file_path.pack(side='left', padx=5)

        # Button to add file
        self.add_file_btn = ctk.CTkButton(master=file_sel_frame, text="Add file", width=0, command=self.add_file)
        self.add_file_btn.pack(side='left', padx=5)

        # folder selection frame
        folder_sel_frame = ctk.CTkFrame(master=self, fg_color="#E5E4E2")
        folder_sel_frame.pack(pady=10)

        # Label for file selection
        ctk.CTkLabel(master=folder_sel_frame, text="Select folder: ", font=("Arial", 14), fg_color="#E5E4E2").pack(side='left', padx=5)

        # Entry for file input
        self.output_path = ctk.CTkEntry(master=folder_sel_frame, font=("Arial", 14), fg_color="white", width=300)
        self.output_path.pack(side='left', padx=5)

        # Button to add file
        self.sel_folder_btn = ctk.CTkButton(master=folder_sel_frame, text="Select folder", width=0, command=self.add_folder)
        self.sel_folder_btn.pack(side='left', padx=5)

        # color selection frame
        color_sel_frame = ctk.CTkFrame(master=self, fg_color="#E5E4E2")
        color_sel_frame.pack(pady=10)

        # Label for color selection
        ctk.CTkLabel(master=color_sel_frame, text="Select color: ", font=("Arial", 14), fg_color="#E5E4E2").pack(side='left', padx=5)

        # ComboBox for selecting color
        self.color_combobox = ctk.CTkComboBox(master=color_sel_frame, values=COLORS)
        self.color_combobox.set("black")  # Set default color
        self.color_combobox.pack(side='left', padx=5)

        # Label for style selection
        ctk.CTkLabel(master=self, text="Select style: ", font=("Arial", 14), fg_color="#E5E4E2").pack(pady=(10,0))

        # Scrollable frame for displaying styles
        self.view_styles_scrollbar_frame = ctk.CTkFrame(master=self)
        self.view_styles_scrollbar_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Create canvas
        self.canvas = ctk.CTkCanvas(master=self.view_styles_scrollbar_frame, highlightthickness=0)
        
        # Create vertical scrollbar
        self.vertical_scrollbar = ctk.CTkScrollbar(
            master=self.view_styles_scrollbar_frame,
            orientation="vertical",
            command=self.canvas.yview
        )

        # Configure canvas scroll command
        self.canvas.configure(yscrollcommand=self.vertical_scrollbar.set)

        # Pack scrollbar and canvas properly
        self.vertical_scrollbar.pack(side="right", fill="y", padx=(0, 0))
        self.canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Frame to hold the styles inside the canvas
        self.styles_frame = ctk.CTkFrame(master=self.canvas, corner_radius=10, fg_color="white")
        
        # Create canvas window
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.styles_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )

        # Bind canvas configure event
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.styles_frame.bind('<Configure>', self.on_frame_configure)

        # Load styles into the scrollable frame
        self.load_styles()

        # Button to generate prints
        self.generate_btn = ctk.CTkButton(master=self, text="Generate", font=('Arial', 14), command=self.generate_print)
        self.generate_btn.pack(pady=(10,20))

    def on_canvas_configure(self, event):
        """Handle canvas resize event"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_styles(self, folder_path="styles"):
        # Get the path of all the images
        images = [file for file in os.listdir(folder_path)]

        row = 0
        col = 0

        self.checkbutton_vars = []  # Reset the list of checkbutton variables
        self.image_paths = []  # Reset the list of image paths
        self.style_checkboxes = []  # New list to keep track of checkboxes

        for image_file in images:
            image_path = os.path.join(folder_path, image_file)

            # Use CTkImage for better scaling on HighDPI displays
            img = Image.open(image_path)
            img = img.resize((100, 120), Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 120))

            self.image_paths.append(image_path)

            # Create a CTkFrame for each style
            frame = ctk.CTkFrame(master=self.styles_frame, fg_color="white")
            frame.grid(row=row, column=col, padx=15, pady=10)

            # Display the image using CTkLabel with CTkImage
            img_label = ctk.CTkLabel(frame, image=ctk_image, text="")
            img_label.pack()

            # Extract the style name
            style_name = os.path.basename(image_path)
            style_name, _ = os.path.splitext(style_name)

            # Use a CTk checkbox
            check_var = ctk.StringVar(value="off")  # Use StringVar for CTkCheckbox
            self.checkbutton_vars.append(check_var)

            style_checkbox = ctk.CTkCheckBox(
                frame,
                variable=check_var,
                text=style_name,
                onvalue="on",
                offvalue="off",
                fg_color="blue",
                hover_color="lightblue",
                text_color="black",
                command=lambda i=style_name, var=check_var: self.on_style_select(var, i),
            )
            style_checkbox.pack()
            
            # Store the checkbox for single-select management
            self.style_checkboxes.append(style_checkbox)

            # Arrange the frame layout in a grid
            if col == 1:
                col = 0
                row += 1
            else:
                col += 1

    def on_style_select(self, var, style_name):
        """
        Handle the selection or deselection of a style checkbox.
        Ensures only one style can be selected at a time.
        """
        # If the current checkbox is being checked
        if var.get() == "on":
            self.selected_style = style_name
            # Uncheck all other checkboxes
            for checkbox_var in self.checkbutton_vars:
                if checkbox_var != var:
                    checkbox_var.set("off")
        else:
            self.selected_style = ''

    def add_file(self):
        # Open a dialog to select a file
        selected_file = tk.filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx")])
        if selected_file:  # Ensure a file is selected
            self.selected_file_path = selected_file
            self.input_file_path.delete(0, "end")
            self.input_file_path.insert(0, self.selected_file_path)

    def add_folder(self):
        # Open a dialog to select a folder
        output_folder = tk.filedialog.askdirectory()
        if output_folder:
            self.output_folder_path = output_folder
            self.output_path.delete(0, "end")
            self.output_path.insert(0, self.output_folder_path)

    def generate_print(self):
        # check if it is a excel file
        _, ext = os.path.splitext(self.selected_file_path)
        isexcel = ext.lower() in (".xls", ".xlsx")
        # check if the excel file path exists
        if not os.path.exists(self.selected_file_path) and isexcel:
            messagebox.showerror("Error", "Invalid file path or no file selected!")
            return
        # check if the output folder path exists
        if not os.path.exists(self.output_folder_path):
            messagebox.showerror("Error", "Invalid folder path or no folder selected!")
            return
        # get color
        color = self.color_combobox.get()
        # check style
        if not self.selected_style:
            messagebox.showerror("Error", "Select a style to print.")
            return
        
        # after all checks generate the print
        self.names_and_numbers_list = self.extract_names_and_numbers(self.selected_file_path)
        print(self.names_and_numbers_list)

    def extract_names_and_numbers(self, file_path):
        """
        Extracts names and numbers from all sheets in an Excel file.
        
        Args:
            file_path (str): Path to the Excel file.
            
        Returns:
            list: A list of tuples containing name and number pairs from all sheets.
        """
        # Read all sheets into a dictionary (sheet_name=None reads all sheets)
        sheets_dict = pd.read_excel(file_path, sheet_name=None, dtype=str, header=None)  # Read as strings without headers

        # Initialize an empty list to store the tuples
        result_list = []

        # Iterate over each sheet
        for sheet_name, df in sheets_dict.items():
            # Drop rows with any NaN values
            df_cleaned = df.dropna()

            # Iterate over each row and look for potential name-number pairs
            for index, row in df_cleaned.iterrows():
                # Iterate through each pair of columns in the row to detect name and number
                for i in range(len(row)-1):
                    # Heuristic: Assume a "name" is a string and the next value is a "number" (numeric string)
                    if isinstance(row[i], str) and isinstance(row[i+1], (str, int, float)):
                        try:
                            # Try to interpret the second value as a number (preserve leading zeros)
                            number = str(int(float(row[i+1])))  # Handle float-like numbers
                            name = row[i]
                            result_list.append((name, row[i+1]))
                        except ValueError:
                            # If it cannot be converted to a valid number, skip the pair
                            continue

        return result_list

    def on_closing(self):
        """
        Handle the close button event with a confirmation dialog.
        """
        if messagebox.askokcancel("Quit", "Do you want to close the application?"):
            self.destroy()  # Close the application


if __name__ == "__main__":
    app = App()
    app.mainloop()