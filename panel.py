import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox

#Créer un modèle d'interface commun pour chaque type de panneau
class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#cccecf')
        self.pack(fill='x', pady=4, padx=4, ipady=5, ipadx=5)

class SliderPanel(Panel):
    def __init__(self, parent, text, vardata, min_val, max_val):
        super().__init__(parent=parent)

        # Layout
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.vardata = vardata
        self.vardata.trace('w', self.update_text)
        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=7)

        self.val_label = ctk.CTkLabel(self, text=vardata.get())
        self.val_label.grid(column=1, row=0, sticky='E', padx=7)
        self.slider = ctk.CTkSlider(self,
                      fg_color='#696870', button_color="#1F7A8C", button_hover_color="#1b6b7a",
                      variable=self.vardata,
                      from_=min_val, to=max_val)
        self.slider.grid(row=1, column=0, columnspan=2, sticky='ew', padx=7, pady=4)

    def update_text(self, *args):
        new_val = round(self.vardata.get())
        self.slider.set(new_val)
        self.val_label.configure(text=f'{new_val}')

class SegmentPanel(Panel):
    def __init__(self, parent, text, vardata, options, reset_opt=True, defaut_val="None"):
        super().__init__(parent=parent)

        self.reset_opt = reset_opt
        self.defaut_val = defaut_val

        ctk.CTkLabel(self, text=text).pack()
        self.segment = ctk.CTkSegmentedButton(self, text_color="#FFF",
                                              selected_color="#1F7A8C", selected_hover_color="#1b6b7a",
                                              variable=vardata, values=options, command=self.revert_info)
        self.segment.pack(expand=True, fill='both', padx=6, pady=6)

    def revert_info(self, *args):
        if self.reset_opt:
            self.segment.set(self.defaut_val)

class SwitchPanel(Panel):
    def __init__(self, parent, *args):   #((var,text), (var,text), (var,text))
        super().__init__(parent=parent)

        for var, text in args:
            switch = ctk.CTkSwitch(self, text=text, variable=var, button_color='#1F6AA5', fg_color='#64686B')
            switch.pack(side='left', expand=True, fill='both', padx=4, pady=4)


class ColorPanel(Panel):
    def __init__(self, parent, colordata):
        super().__init__(parent=parent)

        self.colordata = colordata
        for data in self.colordata.values():
            data.trace('w', self.update_text)
        # Layout
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text="Color").grid(row=0, column=0, sticky='w', padx=7)

        self.color_btn = ctk.CTkButton(self, text_color=self.colordata['hex'].get(), hover=False, width=15,
                                       border_width=1, border_color='#FFF',
                                       fg_color=self.colordata['hex'].get())
        self.color_btn.grid(row=0, column=1, sticky='E', padx=6, pady=6)
        self.color_btn.bind('<Button-1>', self.colorPalette)

        rgb_frame = ctk.CTkFrame(self, fg_color='transparent')
        rgb_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=5, padx=5)

        rgb_frame.rowconfigure((0, 1, 2, 3), weight=1)
        rgb_frame.columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(rgb_frame, text="RGB Settings").grid(row=0, column=0, columnspan=3, sticky='nsew', padx=7)
        ctk.CTkLabel(rgb_frame, text="Red").grid(row=1, column=0, sticky='w', padx=4)
        ctk.CTkLabel(rgb_frame, text="Green").grid(row=1, column=1, sticky='w', padx=4)
        ctk.CTkLabel(rgb_frame, text="Blue").grid(row=1, column=2, sticky='w', padx=4)

        ctk.CTkEntry(rgb_frame, textvariable=self.colordata['red']).grid(row=2, column=0, sticky='w', padx=3)
        ctk.CTkEntry(rgb_frame, textvariable=self.colordata['green']).grid(row=2, column=1, sticky='w', padx=3)
        ctk.CTkEntry(rgb_frame, textvariable=self.colordata['blue']).grid(row=2, column=2, sticky='w', padx=3)

        self.output = ctk.CTkLabel(rgb_frame, text='(0, 0, 0)')
        self.output.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=3, padx=3)

    def reset_color(self, color):   # color <--- hex color
        (r, g, b) = self.hex_to_rgb(color)
        self.colordata['red'].set(r)
        self.colordata['green'].set(g)
        self.colordata['blue'].set(b)


    def update_text(self, *args):
        if self.colordata['red'].get() and self.colordata['green'].get() and self.colordata['blue'].get():
            r = self.colordata['red'].get() ; g = self.colordata['green'].get() ; b = self.colordata['blue'].get()
            if int(r) > 255:
                self.colordata['red'].set(r[:-1])
                messagebox.showerror('Error', 'RGB values have to be less than or equal to 255')
            elif int(g) > 255:
                self.colordata['green'].set(g[:-1])
                messagebox.showerror('Error', 'RGB values have to be less than or equal to 255')
            elif int(b) > 255:
                self.colordata['blue'].set(b[:-1])
                messagebox.showerror('Error', 'RGB values have to be less than or equal to 255')
            else:
                if self.colordata['hex'].get() != self.rgb_to_hex(int(r), int(g), int(b)):
                    self.colordata['hex'].set(self.rgb_to_hex(int(r), int(g), int(b)))
                hex = self.colordata['hex'].get()
                text = f"({r}, {g}, {b})"
                self.output.configure(text=text)

                # hex_color = self.rgb_to_hex(int(r), int(g), int(b))
                self.color_btn.configure(fg_color=hex, text_color=hex)

    def colorPalette(self, event):
        selectedColor = colorchooser.askcolor()
        if selectedColor != (None, None):
            self.color_btn.configure(fg_color=selectedColor[1], text_color=selectedColor[1])

            self.colordata['red'].set(selectedColor[0][0])
            self.colordata['green'].set(selectedColor[0][1])
            self.colordata['blue'].set(selectedColor[0][2])
            self.colordata['hex'].set(selectedColor[1])

    def hex_to_rgb(self, hex):
        hex = hex[1:]      # Remove letter '#' in hex
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal)

        return tuple(rgb)

    def rgb_to_hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

class TextRecogPanel(Panel):
    def __init__(self, parent, lang_vars, operate_vars, options):
        super().__init__(parent=parent)

        ctk.CTkLabel(self, text="Text Recogn.").pack(pady=5)
        DropdownPanel(self, lang_vars, options)
        StartAnalyseButton(self, operate_vars)

class DropdownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, vardata, options):
        super().__init__(master=parent,
                         values=options, variable=vardata,
                         text_color="#000000", fg_color='#FFF',
                         button_color='#BFDBF7',
                         button_hover_color='#ACC5DE',
                         dropdown_fg_color='#e1e5f2')
        self.pack(fill='x', padx=4, pady=4)

class StartAnalyseButton(ctk.CTkButton):
    def __init__(self, parent, operate_vars):
        super().__init__(master=parent, text="Start Analysing",
                         text_color='#FFF', fg_color="#1F7A8C", hover_color="#1b6b7a",
                         command=self.start)
        self.pack(pady=10)
        self.operate_vars = operate_vars

    def start(self):
        self.operate_vars.set(1)

class FileNamePanel(Panel):
    def __init__(self, parent, name_var, file_var):
        super().__init__(parent=parent)

        self.name_var = name_var
        self.name_var.trace('w', self.update_text)
        self.file_var = file_var

        ctk.CTkEntry(self, textvariable=self.name_var).pack(fill='x', padx=20, pady=5)
        frame = ctk.CTkFrame(self, fg_color='transparent')
        jpg_check = ctk.CTkCheckBox(frame, text='.jpg', fg_color='#1F7A8C', hover_color="#1b6b7a", variable=self.file_var, command=lambda: self.click('.jpg'), onvalue='jpg', offvalue='png')
        png_check = ctk.CTkCheckBox(frame, text='.png', fg_color='#1F7A8C', hover_color="#1b6b7a", variable=self.file_var, command=lambda: self.click('.png'), onvalue='png', offvalue='jpg')
        jpg_check.pack(side=tk.LEFT, fill='x', expand=True)
        png_check.pack(side=tk.LEFT, fill='x', expand=True)

        frame.pack(expand=True, fill='x', padx=20)

        # Preview text
        self.output = ctk.CTkLabel(self, text='')
        self.output.pack()

    def click(self, value):
        self.file_var.set(value)
        self.update_text()

    def update_text(self, *args):
        if self.name_var.get():
            text = self.name_var.get().replace(' ', '_') + self.file_var.get()
            self.output.configure(text=text)

class FilePathPanel(Panel):
    def __init__(self, parent, path_var):
        super().__init__(parent=parent)

        self.path_var = path_var

        ctk.CTkButton(self, text="Open Explorer", text_color='#FFF', fg_color="#1F7A8C", hover_color="#1b6b7a", command=self.open_file).pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.path_var).pack(expand=True, fill='both', padx=6, pady=6)

    def open_file(self):
        self.path_var.set(filedialog.askdirectory())

class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_func, name_var, file_var, path_var):
        super().__init__(master=parent, text="Save file",
                         text_color = '#FFF', fg_color = "#1F7A8C", hover_color = "#1b6b7a",
                         command=self.save)
        self.pack(side=tk.BOTTOM, pady=10)

        self.export_func = export_func
        self.name_var = name_var
        self.file_var = file_var
        self.path_var = path_var

    def save(self):
        self.export_func(self.name_var.get(), self.file_var.get(), self.path_var.get())
