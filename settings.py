import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLES_FOLDER = os.path.join(BASE_DIR, "styles")
FONTS_FOLDER = os.path.join(BASE_DIR, "fonts")

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650

A4_SIZE = {"width": 8.27, "height": 11.69}

DPI = 300

PAGE_SIZE = {"width": int (A4_SIZE['width'] * DPI), "height": int (A4_SIZE['height'] * DPI)}

MAX_WIDTH = 2280

COLORS = ["black", "red", "navy"]

STYLES = {"Antonio":{"name_font_path":f"{FONTS_FOLDER}/Antonio-Bold.ttf", 
                     "name_size":500, 
                     "number_font_path":f"{FONTS_FOLDER}/Antonio-Regular.ttf", 
                     "number_size":2700, 
                     "name_y_padding":10, 
                     "number_y_padding":200}, 

          "Antonio & GUSHELINK Outline":{"name_font_path":f"{FONTS_FOLDER}/Antonio-Bold.ttf", 
                                         "name_size":500, 
                                         "number_font_path":f"{FONTS_FOLDER}/gushelink.outline.ttf", 
                                         "number_size":3300, 
                                         "name_y_padding":10, 
                                         "number_y_padding":200}, 

          "Calibri bold & Antonio":{"name_font_path":f"{FONTS_FOLDER}/calibri-bold.ttf", 
                                    "name_size":690, 
                                    "number_font_path":f"{FONTS_FOLDER}/Antonio-Regular.ttf", 
                                    "number_size":2700, 
                                    "name_y_padding":70, 
                                    "number_y_padding":200}, 

          "Calibri bold & GUSHELINK Outline":{"name_font_path":f"{FONTS_FOLDER}/calibri-bold.ttf", 
                                              "name_size":690, 
                                              "number_font_path":f"{FONTS_FOLDER}/gushelink.outline.ttf", 
                                              "number_size":3300, 
                                              "name_y_padding":70, 
                                              "number_y_padding":200}, 

          "Swis721 Blk BT Cond & Antonio":{"name_font_path":f"{FONTS_FOLDER}/Swiss721BT-BlackCondensed.ttf",
                                            "name_size":610, 
                                            "number_font_path":f"{FONTS_FOLDER}/Antonio-Regular.ttf", 
                                            "number_size":2700, 
                                            "name_y_padding":100, 
                                            "number_y_padding":200}, 
                                            
          "Swis721 Blk BT Cond & GUSHELINK Outline":{"name_font_path":f"{FONTS_FOLDER}/Swiss721BT-BlackCondensed.ttf", 
                                                     "name_size":610, 
                                                     "number_font_path":f"{FONTS_FOLDER}/gushelink.outline.ttf", 
                                                     "number_size":3300, 
                                                     "name_y_padding":100, 
                                                     "number_y_padding":200}}