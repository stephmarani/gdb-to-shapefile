import os
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import geopandas
import time


class InputWindow:
    def __init__(self, win):
        self.min_x_coord_label = Label(win, text='Minimum X Coordinate')
        self.min_x_coord_entry = Entry()
        self.min_x_coord_label.place(x=5, y=50)
        self.min_x_coord_entry.place(x=200, y=50)

        self.min_y_coord_label = Label(win, text='Minimum Y Coordinate')
        self.min_y_coord_entry = Entry()
        self.min_y_coord_label.place(x=5, y=100)
        self.min_y_coord_entry.place(x=200, y=100)

        self.max_x_coord_label = Label(win, text='Maximum X Coordinate')
        self.max_x_coord_entry = Entry()
        self.max_x_coord_label.place(x=5, y=150)
        self.max_x_coord_entry.place(x=200, y=150)

        self.max_y_coord_label = Label(win, text="Maximum Y Coordinate")
        self.max_y_coord_entry = Entry()
        self.max_y_coord_label.place(x=5, y=200)
        self.max_y_coord_entry.place(x=200, y=200)

        self.file_name_message = StringVar()
        self.file_name_label = Label(win, text="GDB File folder location")
        self.file_name_entry = Entry(textvariable=self.file_name_message)
        self.file_name_button = Button(win, text='Select Unzipped Folder', command=self.upload_file)
        self.file_name_label.place(x=5, y=250)
        self.file_name_entry.place(x=200, y=250)
        self.file_name_button.place(x=420, y=250)

        self.b1 = Button(win, text='Generate ShapeFile', command=self.generate_file)
        self.b1.place(x=5, y=300)

        self.starting_message = StringVar()
        self.starting_message_label = Label(win, wraplength=500)
        self.starting_message_label.place(x=5, y=350)

        self.completion_message = StringVar()
        self.completion_message_label = Label(win, textvariable=self.completion_message, wraplength=500)
        self.completion_message_label.place(x=5, y=450)

    def generate_file(self):
        try:
            min_x_coord = float(self.min_x_coord_entry.get())
            min_y_coord = float(self.min_y_coord_entry.get())
            max_x_coord = float(self.max_x_coord_entry.get())
            max_y_coord = float(self.max_y_coord_entry.get())
            file_name = self.file_name_entry.get()

            if min_y_coord > max_y_coord:
                tkinter.messagebox.showinfo("Invalid Y coordinates",
                                            "The min Y coordinate is greater than the max, "
                                            "please double check coordinate ordering.")
                return

            if min_x_coord > max_x_coord:
                tkinter.messagebox.showinfo("Invalid X coordinates",
                                            "The min X coordinate is greater than the max, "
                                            "please double check coordinate ordering.")
                return

            if (min_x_coord < max_y_coord or min_x_coord < min_y_coord
                    or max_x_coord < max_y_coord or max_x_coord < min_y_coord):
                tkinter.messagebox.showinfo("Invalid coordinates",
                                            "The X coordinate values should be larger than the y, "
                                            "please check your axes.")
                return

            generated_folder = file_name + f"_GeneratedFiles{round(time.time())}"
            generated_file = generated_folder + "/Shapefile.shp"

            self.starting_message_label.config(text=f"Computing file from {file_name} with boundaries "
                                                    f"{min_x_coord}, {min_y_coord}, "
                                                    f"{max_x_coord}, {max_y_coord}. "
                                                    f"File will be written to {generated_file}")
            self.starting_message_label.update()

            os.mkdir(generated_folder)
            boundaries = (min_x_coord, min_y_coord, max_x_coord, max_y_coord)
            gbd_file = geopandas.read_file(file_name, bbox=boundaries)
            gbd_file.to_file(generated_file)

            self.completion_message.set(f"File successfully generated at {generated_file}")
            
        except Exception as ex:
            tkinter.messagebox.showinfo("Error",
                                        "Error occurred, please double check your boundaries and file location. "
                                        "Ensure that file is pointing to unzipped folder and not zip file."
                                        f"\nSpecific error: {ex}")

    def upload_file(self, event=None):
        filename = filedialog.askdirectory()
        self.file_name_message.set(filename)


if __name__ == '__main__':
    window = Tk()
    inputWindow = InputWindow(window)
    window.title('Generate Shapefile From GDB')
    window.geometry("600x700+10+10")
    window.mainloop()
