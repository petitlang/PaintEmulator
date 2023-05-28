import customtkinter as ctk
from panel import *
from select_zone import *

# Un menu pour modifier, dessiner, sélectionner des zones et exporter un fichier
class Menu(ctk.CTkTabview):
    def __init__(self, parent, edit_vars, draw_vars, color_vars, select_vars, export_func, update_func):
        super().__init__(master=parent, text_color="#FFF",
                         segmented_button_selected_color="#1F7A8C", segmented_button_selected_hover_color="#1b6b7a",
                         command=self.reset_valeurs)
        self.grid(row=0, column=0, rowspan=3, sticky='nsew', pady=8, padx=8)

        # Vars
        self.edit_vars = edit_vars
        self.draw_vars = draw_vars
        self.color_vars = color_vars
        self.select_vars = select_vars

        self.update_func = update_func

        # Tabs
        self.add('Edit')
        self.add('Draw')
        self.add('Select')
        self.add('Export')

        # Widget
        EditFrame(self.tab('Edit'), edit_vars)
        DrawFrame(self.tab('Draw'), draw_vars, color_vars)
        SelectFrame(self.tab('Select'), select_vars)
        ExportFrame(self.tab('Export'), export_func)

    def reset_valeurs(self):
        '''
        Fonction pour réinitialiser des valeurs
        '''
        self.draw_vars['style'].set("None")
        self.select_vars['select'].set("Off")
        self.update_func()

# Un cadre pour les options d'édition
class EditFrame(ctk.CTkFrame):
    def __init__(self, parent, edit_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        SegmentPanel(self, 'Rotate', edit_vars['rotate'], ["Left", "Right"])
        SegmentPanel(self, 'Flip', edit_vars['flip'], ["X", "Y", "Both"])

# Un cadre pour les options de dessin
class DrawFrame(ctk.CTkFrame):
    def __init__(self, parent, draw_vars, color_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.draw_style = draw_vars['style']
        self.draw_style.trace('w', self.reset_style)
        self.drawDropdown = DropdownPanel(self, draw_vars['style'], ['None', 'Brush', 'Line', 'Rectangle', 'Oval', 'Eraser'])
        self.size_slider = SliderPanel(self, 'Size', draw_vars['size'], 1, 50)
        self.color_panel = ColorPanel(self, color_vars)

    def reset_style(self, *args):
        '''
        Fonction pour réinitialiser des valeurs
        '''

        if self.draw_style.get() == "None":
            self.drawDropdown.set('None')
            self.size_slider.slider.set(1)

# Un cadre pour les options de sélection de zones
class SelectFrame(ctk.CTkFrame):
    def __init__(self, parent, select_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.select_select_vars = select_vars['select']
        self.select_select_vars.trace('w', self.reset_select)

        self.selectSegment = SegmentPanel(self, 'Select', select_vars['select'], ["On", "Off"], reset_opt=False)
        SegmentPanel(self, 'Clipboard', select_vars['clip'], ["Cut", "Copy", "Paste"])
        TextRecogPanel(self, select_vars['lang'], select_vars['operate'], ["English", "French"])

    def reset_select(self, *args):
        '''
        Fonction pour réinitialiser des valeurs
        '''
        if self.select_select_vars.get() == "None":
            self.selectSegment.segment.set("Off")

# Un cadre pour les options d'exportation d'image
class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, export_func):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # Data
        self.name_var = ctk.StringVar()
        self.file_var = ctk.StringVar(value=".jpg")
        self.path_var = ctk.StringVar()

        # Widgets
        FileNamePanel(self, self.name_var, self.file_var)
        FilePathPanel(self, self.path_var)
        SaveButton(self, export_func, self.name_var, self.file_var, self.path_var)