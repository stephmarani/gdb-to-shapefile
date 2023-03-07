import importlib
import os
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
import geopandas


class InputWindow:
    def __init__(self, win):
        self.min_x_coord_label = Label(win, text='Minimum X Coordinate:')
        self.min_x_coord_entry = Entry()
        self.min_x_coord_label.place(x=10, y=50)
        self.min_x_coord_entry.place(x=175, y=50)

        self.min_y_coord_label = Label(win, text='Minimum Y Coordinate:')
        self.min_y_coord_entry = Entry()
        self.min_y_coord_label.place(x=10, y=100)
        self.min_y_coord_entry.place(x=175, y=100)

        self.max_x_coord_label = Label(win, text='Maximum X Coordinate:')
        self.max_x_coord_entry = Entry()
        self.max_x_coord_label.place(x=10, y=150)
        self.max_x_coord_entry.place(x=175, y=150)

        self.max_y_coord_label = Label(win, text="Maximum Y Coordinate:")
        self.max_y_coord_entry = Entry()
        self.max_y_coord_label.place(x=10, y=200)
        self.max_y_coord_entry.place(x=175, y=200)

        self.file_name_message = StringVar()
        self.file_name_label = Label(win, text="GDB file folder location:")
        self.file_name_entry = Entry(textvariable=self.file_name_message)
        self.file_name_button = Button(win, text='Select Unzipped Folder', command=self.upload_gdb_folder)
        self.file_name_label.place(x=10, y=250)
        self.file_name_entry.place(x=175, y=250)
        self.file_name_button.place(x=320, y=245)

        self.generated_file_folder_message = StringVar()
        self.generated_file_folder_label = Label(win, text="Generated file folder location:")
        self.generated_file_folder_entry = Entry(textvariable=self.generated_file_folder_message)
        self.generated_file_folder_button = Button(win, text='Select Folder', command=self.upload_generated_folder)
        self.generated_file_folder_label.place(x=10, y=300)
        self.generated_file_folder_entry.place(x=175, y=300)
        self.generated_file_folder_button.place(x=320, y=295)

        self.generated_file_name_label = Label(win, text='Generated file name:')
        self.generated_file_name_entry = Entry()
        self.generated_file_name_label.place(x=10, y=350)
        self.generated_file_name_entry.place(x=175, y=350)

        self.b1 = Button(win, text='Generate Shapefile', command=self.generate_file)
        self.b1.place(x=10, y=400)

        self.starting_message = StringVar()
        self.starting_message_label = Label(win, wraplength=500)
        self.starting_message_label.place(x=10, y=500)

        self.completion_message = StringVar()
        self.completion_message_label = Label(win, textvariable=self.completion_message, wraplength=500)
        self.completion_message_label.place(x=10, y=600)

    def generate_file(self):
        try:
            min_x_coord = float(self.min_x_coord_entry.get())
            min_y_coord = float(self.min_y_coord_entry.get())
            max_x_coord = float(self.max_x_coord_entry.get())
            max_y_coord = float(self.max_y_coord_entry.get())
            file_name = self.file_name_entry.get()
            generated_folder_name = self.generated_file_folder_entry.get()
            generated_file_name = self.generated_file_name_entry.get()

            if generated_file_name is None or generated_file_name is None or file_name is None:
                tkinter.messagebox.showinfo("Invalid generated file name",
                                            "A valid file name and folder is required for the "
                                            "generated file to go in.")
                return

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

            generated_folder = generated_folder_name
            generated_file = generated_folder + "/" + generated_file_name

            self.starting_message_label.config(text=f"Computing file from {file_name} with boundaries "
                                                    f"{min_x_coord}, {min_y_coord}, "
                                                    f"{max_x_coord}, {max_y_coord}. "
                                                    f"File will be written to {generated_file}")
            self.starting_message_label.update()

            boundaries = (min_x_coord, min_y_coord, max_x_coord, max_y_coord)
            gbd_file = geopandas.read_file(file_name, bbox=boundaries)
            gbd_file.to_file(generated_file)

            self.completion_message.set(f"File successfully generated at {generated_file}")

        except Exception as ex:
            tkinter.messagebox.showinfo("Error",
                                        "Error occurred, please double check your boundaries and file location. "
                                        "Ensure that file is pointing to unzipped folder and not zip file."
                                        f"\nSpecific error: {ex}")

    def upload_gdb_folder(self, event=None):
        filename = filedialog.askdirectory()
        self.file_name_message.set(filename)

    def upload_generated_folder(self, event=None):
        filename = filedialog.askdirectory()
        self.generated_file_folder_message.set(filename)


if __name__ == '__main__':
    if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()

    window = Tk()
    window.lift()
    inputWindow = InputWindow(window)
    window.title('Generate Shapefile From GDB')
    window.geometry("600x700+10+10")
    window.mainloop()
