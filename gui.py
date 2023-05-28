import customtkinter as ctk
from image_widget import *
from menu import Menu
from select_zone import selectZone
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageGrab

class App():
    def __init__(self):
        # Setup
        self.racine = ctk.CTk()
        self.racine.geometry('1000x600')
        self.racine.title("Paint Emulator")
        self.racine.minsize(800, 500)
        self.init_parameters()

        # Layout
        self.racine.rowconfigure(0, weight=1, uniform='a')
        self.racine.rowconfigure(1, weight=12, uniform='a')
        self.racine.rowconfigure(2, weight=1, uniform='a')
        self.racine.columnconfigure(0, weight=2, uniform='a')
        self.racine.columnconfigure(1, weight=6, uniform='a')

        # Widget
        self.racine.update()
        self.actual_ratio = self.racine.winfo_width() / 1000
        self.image_import = ImageImport(self.racine, self.create_img, self.import_image, 1000, 600, self.actual_ratio)

        # Canvas variables
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0
        self.image_output = None

        self.racine.mainloop()

    def init_parameters(self):
        '''
        Créer des paramètres
        '''

        # Parameters for Editing (Rotate, Flip) (if we have time, we may add Zoom function
        self.edit_vars = {
            'rotate' : ctk.StringVar(value="None"),
            'zoom': ctk.DoubleVar(value=0),
            'flip': ctk.StringVar(value="None"),
        }

        # Parameters for Coloring
        self.color_vars = {
            'red': ctk.StringVar(value='0'),
            'green': ctk.StringVar(value='0'),
            'blue': ctk.StringVar(value='0'),
            'hex': ctk.StringVar(value='#000000')
        }

        # Parameters for Drawing
        self.draw_vars = {
            'style' : ctk.StringVar(value="None"),
            'size' : ctk.DoubleVar(value=1)
        }

        # Parameters for Selecting Zones
        self.select_vars = {
            'select' : ctk.StringVar(value="Off"),
            'lang' : ctk.StringVar(value="English"),
            'clip': ctk.StringVar(value="None"),
            'operate' : ctk.IntVar(value=0)
        }

        # Parameters for Updating position and dimension
        self.state_vars = {
            'pos' : ctk.StringVar(value="0, 0"),
            'dim' : ctk.StringVar()
        }

        # Trace var changes
        for var in self.edit_vars.values():
            var.trace('w', self.manipulate_img)
        for var in self.select_vars.values():
            var.trace('w', self.manip_select_img)

    def manipulate_img(self, *args):
        '''
        Fonction pour éditer l'image (Rotation et Flip)
        '''

        self.get_current_info()

        # Rotate img
        if self.edit_vars['rotate'].get() == 'Left':
            self.image = self.image.rotate(90, expand=True)
            self.image_width, self.image_height = self.image_height, self.image_width
            self.reverse_current_info()
            self.calcul_resize()
        if self.edit_vars['rotate'].get() == 'Right':
            self.image = self.image.rotate(-90, expand=True)
            self.image_width, self.image_height = self.image_height, self.image_width
            self.reverse_current_info()
            self.calcul_resize()

        # Flip img
        if self.edit_vars['flip'].get() == 'X':
            self.image = ImageOps.mirror(self.image)
        if self.edit_vars['flip'].get() == 'Y':
            self.image = ImageOps.flip(self.image)
        if self.edit_vars['flip'].get() == 'Both':
            self.image = ImageOps.mirror(self.image)
            self.image = ImageOps.flip(self.image)

        self.place_img()

    def manip_select_img(self, *args):
        '''
        Fonction pour éditer l'image (Rotation et Flip)
        '''

        if self.select_vars['select'].get() == 'Off':
            self.selectManip.reset_select_rect()

        if self.select_vars['select'].get() == 'On':
            self.selectManip.selectRectangle.set(1)

        if self.select_vars['clip'].get() == 'Copy':
            self.selectManip.copy_selection()

        if self.select_vars['clip'].get() == 'Cut':
            self.selectManip.cut_selection()

        if self.select_vars['clip'].get() == 'Paste':
            self.selectManip.paste_selection()

        if self.select_vars['lang'].get():
            self.selectManip.langue = self.select_vars['lang'].get()

        if self.select_vars['operate'].get() == 1:
            self.selectManip.text_recognition()
            self.select_vars['operate'].set(0)

    def update_pos(self, event):
        '''
        Fonction pour mettre à jour la position (quand le curseur entre dans le Canvas)
        ----------
        Input:
            event: la motion du curseur dans le Canvas
        '''

        self.state_vars['pos'].set(f"{int(event.x * self.origin_width / self.image_width)}, {int(event.y * self.origin_height / self.image_height)}")

    def reset_pos(self, event):
        '''
        Fonction pour réinitialiser la position (quand le curseur sort du Canvas)
        ----------
        Input:
            event: l'action quittant le Canvas du pointeur de la souris
        '''

        self.state_vars['pos'].set(f"0, 0")

    def get_current_info(self):
        '''
        Fonction pour mettre à jour la dimension de l'image
        '''

        self.origin_width = self.original.size[0]
        self.origin_height = self.original.size[1]
        self.state_vars['dim'].set(f"{self.origin_width} x {self.origin_height}")

    def reverse_current_info(self):
        '''
        Fonction pour mettre à jour la dimension de l'image et le rapport de l'image quand on fait pivoter l'image
        '''

        self.origin_width, self.origin_height = self.origin_height, self.origin_width
        self.image_ratio = 1 / self.image_ratio
        self.state_vars['dim'].set(f"{self.origin_width} x {self.origin_height}")

    def update_current_img(self):
        '''
        Fonction pour mettre à jour l'image actuelle chaque fois que l'on a fini modifier/dessiner l'image
        '''

        self.image = self.resized_image

    def create_img(self, width, height, colordata):
        '''
        Fonction pour créer une nouvelle image
        ----------
        Input:
            width: le largeur de l'image
            height: l'hauteur de l'image
            colordata: paramètre de couleur qui contient d'information sur la couleur d'arrière-plan de la nouvelle image
        '''

        self.racine.title("Untitled - Paint")

        self.original = Image.new(mode='RGB', size=(width, height), color=colordata['hex'].get())
        self.get_current_info()
        
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]  # width / height

        self.image_import.grid_forget()
        self.open_image()

    def import_image(self, path):
        '''
        Fonction pour importer une image depuis le PC
        ----------
        Input:
            path: le chemin de l'image dans le PC
        '''

        # Change title
        new_title = self.get_filename(path) + " - Paint"
        self.racine.title(new_title)

        self.original = Image.open(path)
        self.get_current_info()

        self.image = self.original
        self.image_ratio = self.origin_width / self.origin_height   # width / height

        # Hide image import button
        self.image_import.grid_forget()
        self.open_image()

    def get_filename(self, path):
        '''
        Fonction pour obtenir le nom du fichier à partir du chemin de l'image
        ----------
        Input:
            path: le chemin de l'image dans le PC
        ----------
        Output:
            filenane: le nom du fichier
        '''

        i = len(path) - 1
        filename = ""
        while path[i] != "/" and i >= 0:
            filename = path[i] + filename
            i -= 1

        return filename

    def open_image(self):
        '''
        Fonction pour créer un canevas qui montre l'image et créer un Menu pour modifier/dessiner sur le canevas
        '''

        # Open image and create Close button + Menu
        self.image_output = ImageOutput(self.racine, self.draw_vars, self.color_vars,
                                        self.resize_image, self.update_pos,
                                        self.reset_pos, self.update_current_img)

        self.close_button = CloseOutput(self.racine, self.close_edit)
        self.menu_app = Menu(self.racine, self.edit_vars, self.draw_vars, self.color_vars, self.select_vars, self.export_image, self.update_current_img)
        self.state_bar = StateBar(self.racine, self.state_vars)

    def close_edit(self):
        '''
        Fonction pour fermer l'image
        '''

        # Hide image + close button + Menu
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu_app.grid_forget()
        self.state_bar.grid_forget()

        # Recreate import button
        self.image_import = ImageImport(self.racine, self.create_img, self.import_image, 1000, 600, self.actual_ratio)

        self.image_output = None

    def resize_image(self, event):
        '''
        Fonction pour redimensionner l'image quand on modifie la dimension de l'application
        ----------
        Input:
            event: le changements dans la taille du widget (Canevas)
        '''

        if self.image_output != None:
            # Current canvas ratio
            self.canvas_ratio = event.width / event.height

            # Current canvas size
            self.canvas_width = event.width
            self.canvas_height = event.height

            self.calcul_resize()

    def calcul_resize(self):
        '''
        Fonction pour redimensionner l'image avec une nouvelle largeur et une nouvelle hauteur
        '''

        # Canvas position
        self.x_root = self.racine.winfo_rootx() + self.image_output.winfo_x() + 1
        self.y_root = self.racine.winfo_rooty() + self.image_output.winfo_y() + 1

        # Resize image
        if self.canvas_ratio > self.image_ratio: # canvas is wider than the image
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
            self.x_root += int((self.canvas_width - self.image_width) / 2)

        else:  # canvas is taller than the image
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
            self.y_root += int((self.canvas_height - self.image_height) / 2)

        self.place_img()

    def place_img(self):
        '''
        Fonction pour afficher l'image redimensionnée sur le Canevas
        '''
        self.image_output.delete('all')
        self.resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(self.resized_image)

        self.dist_width_img_canvas = abs(self.image_width - self.canvas_width) / 2
        self.dist_height_img_canvas = abs(self.image_height - self.canvas_height) / 2

        self.draw_resized_image = ImageDraw.Draw(self.resized_image)
        self.image_output.add_pil_image(self.draw_resized_image, self.resized_image, self.dist_width_img_canvas, self.dist_height_img_canvas)
        self.selectManip = selectZone(self.racine, self.image_output, self.draw_resized_image, self.resized_image, self.x_root, self.y_root, self.dist_width_img_canvas, self.dist_height_img_canvas)

        self.image_output.create_image(self.canvas_width/2, self.canvas_height/2, image=self.image_tk)

    def export_image(self, name, file, path):
        '''
        Fonction pour exporter l'image
        ----------
        Input:
            name: le nom de la nouvelle image
            file: le type (.jpeg ou .png) de la nouvelle image
            path: le chemin du dossier où on peut enregistrer l'image
        '''
        export_var = f"{path}/{name}{file}"

        self.image.save(export_var)
        tk.messagebox.showinfo("Notice", "Save file successfully")
App()