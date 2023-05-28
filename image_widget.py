import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, Canvas
from panel import *
from Draw import *
from PIL import Image, ImageTk

# Classe pour créer un page d'accueil dont le type de la classe est un Frame
class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, create_img, import_func, width, height, ratio):
        super().__init__(master=parent)

        self.parent = parent
        self.create_img= create_img
        self.import_func = import_func
        self.ratio = ratio
        self.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')

        self.bind("<Configure>", self.resize_background)

        # Add bg
        self.bg_image = ctk.CTkImage(light_image=Image.open("./img/bg.png"))
        self.label1 = ctk.CTkLabel(self, text=" ", image=self.bg_image)
        self.label1.place(x=0, y=0)

        self.btn_frame = ctk.CTkFrame(self, fg_color=('#FFF','#FFF'),bg_color='#FFF') 
        self.btn_frame.pack(expand=True)

        # Create new image
        self.new_win = None
        self.newbtn = ctk.CTkButton(self.btn_frame, text="New File", text_color='#FFF', fg_color="#1F7A8C", hover_color="#1b6b7a")
        self.newbtn.grid(row=0, column=0, sticky='nsew', pady=10)
        self.newbtn.bind('<Button-1>', self.info_input)

        # Open an existed image
        self.openbtn = ctk.CTkButton(self.btn_frame, text="Open Image", text_color='#FFF', fg_color="#1F7A8C", hover_color="#1b6b7a")
        self.openbtn.grid(row=1, column=0, sticky='nsew', pady=10)
        self.openbtn.bind('<Button-1>', self.open_dialog)

    def resize_background(self, event):
        '''
        Fonction pour redimensionner l'image de fond
        ----------
        Input:
            event: le changements dans la taille du cadre du page d'accueil
        '''
        width = event.width / self.ratio
        height = event.height / self.ratio
        self.bg_image.configure(size=(width, height))
        self.label1.configure(image=self.bg_image)

    def info_input(self, event):
        '''
        Fonction pour créer une nouvelle fenêtre pour laquelle on entre des informations de la nouvelle image
        ----------
        Input:
            event: le clic gauche sur le bouton "New File"
        '''

        if self.new_win is None or not self.new_win.winfo_exists():
            self.new_win = ctk.CTkToplevel(self.parent, width=200, height=300)
            self.new_win.resizable(0, 0)
            self.new_win.focus()

            self.input_width = ctk.IntVar(value=300)
            self.input_height = ctk.IntVar(value=200)

            SliderPanel(self.new_win, "Width", self.input_width, 0, 2000)
            SliderPanel(self.new_win, "Height", self.input_height, 0, 2000)

            self.color_info = {
                'red': ctk.StringVar(value='255'),
                'green': ctk.StringVar(value='255'),
                'blue': ctk.StringVar(value='255'),
                'hex' : ctk.StringVar(value='#FFF')
            }
            ColorPanel(self.new_win, self.color_info)

            self.submit_btn = ctk.CTkButton(self.new_win, text="Create", text_color='#FFF', fg_color="#1F7A8C", hover_color="#1b6b7a")
            self.submit_btn.pack(pady=4, padx=4)
            self.submit_btn.bind('<Button-1>', self.submit)
        else:
            self.new_win.focus()

    def submit(self, event):
        '''
        Fonction pour obtenir les informations d'une nouvelle image et fermer la nouvelle fenêtre
        ----------
        Input:
            event: le gauche clic sur le bouton "Create"
        '''

        self.create_img(self.input_width.get(), self.input_height.get(), self.color_info)
        self.new_win.destroy()

    def open_dialog(self, event):
        '''
        Fonction pour créer une boîte de dialogue pour demander le chemin de l'image existante que les utilisateurs souhaitent ouvrir
        ----------
        Input:
            event: le gauche clic sur le bouton "Open Image"
        '''
        path = filedialog.askopenfile(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.import_func(path.name)

# Classe pour créer une surface permettant de dessiner ; cette classe est un widget Canvas
class ImageOutput(Canvas):
    def __init__(self, parent, drawdata, colordata, resize_image, update_pos, reset_pos, update_current):
        super().__init__(master=parent, bg='#EBEBEB',   #242424
                         bd=0, highlightthickness=0,
                         relief='ridge')
        self.grid(row=1, column=1, sticky='nsew', padx=8, pady=8)

        self.drawdata = drawdata
        self.colordata = colordata
        for data in list(self.drawdata.values()) + list(self.colordata.values()):
            data.trace('w', self.select)

        self.update_current = update_current

        self.bind('<Motion>', update_pos)
        self.bind('<Leave>', reset_pos)
        self.bind('<Configure>', resize_image)

    def add_pil_image(self, image_draw, img_pil, dist_w, dist_h):
        '''
        Fonction pour créer un objet dans la classe Draw (du fichier Draw.py) afin de dessiner sur le canevas
        ----------
        Input:
            image_draw: un module ImageDraw fournit des graphiques 2D simples (ligne, rectangle, ovale, etc.) pour l'objet Image
            img_pil: un objet PIL Image
            dist_w: différence de largeur entre l'objet Canvas et l'objet Image
            dist_h: différence de hauteur entre l'objet Canvas et l'objet Image
        '''

        self.draw = DrawCanvas(self, image_draw, self.update_current, img_pil, dist_w, dist_h)

    def select(self, *args):
        '''
        Fonction pour dessiner des graphiques 2D sur le canevas et l'Image
        '''
        if self.drawdata['style'].get() == 'None':
            self.draw.selectOption = 'None'

        if self.drawdata['style'].get() == 'Brush':
            self.draw.selectOption = 'Brush'

            self.bind('<B1-Motion>', lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.draw_circle(event, color, size))
            self.bind('<ButtonRelease-1>', self.draw.update_new_line)

        elif self.drawdata['style'].get() == 'Line':
            self.draw.selectOption = 'Line'

            self.bind("<Button-1>", lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.start_line(event, color, size))
            self.bind("<B1-Motion>", self.draw.draw_line)
            self.bind("<ButtonRelease-1>", self.draw.end_line)

        elif self.drawdata['style'].get() == 'Oval':
            self.draw.selectOption = 'Oval'
            self.bind("<Button-1>", lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.start_oval(event, color, size))
            self.bind("<B1-Motion>", self.draw.draw_oval)
            self.bind("<ButtonRelease-1>", self.draw.end_oval)

        elif self.drawdata['style'].get() == 'Rectangle':
            self.draw.selectOption = 'Rectangle'

            self.bind("<Button-1>", lambda event, color=self.colordata['hex'].get(), size=self.drawdata['size'].get():
                                    self.draw.start_rect(event, color, size))
            self.bind("<B1-Motion>", self.draw.draw_rect)
            self.bind("<ButtonRelease-1>", self.draw.end_rect)

        elif self.drawdata['style'].get() == 'Eraser':
            self.draw.selectOption = 'Eraser'
            self.bind("<B1-Motion>", lambda event, size=self.drawdata['size'].get(): self.draw.erase(event,size))

# Des options de collage (Enregistrer ou Annuler) quand on colle une image sur Canvas
class PasteButtons(ctk.CTkSegmentedButton):
    def __init__(self, parent, variable, options):
        super().__init__(master=parent, variable=variable, values=options)

        self.grid(row=0, column=1, pady=2)

# Bouton pour fermer l'image
class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent,
                         command=close_func,
                         text='x', text_color='#022b3a',
                         fg_color='transparent',
                         width=30, height=30,
                         corner_radius=0, hover_color='#D43422')
        self.grid(row=0, column=1, sticky='e', padx=5)

# Barre d'état (affiche la position du curseur sur le canevas et la dimension de l'image)
class StateBar(ctk.CTkFrame):
    def __init__(self, parent, vardata):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=2, column=1, sticky='nsew')

        self.vardata = vardata
        for var in self.vardata.values():
            var.trace('w', self.update_label)

        self.label1 = ctk.CTkLabel(self, text=self.vardata['pos'].get())
        self.label2 = ctk.CTkLabel(self, text=self.vardata['dim'].get())

        self.label1.pack(side=tk.LEFT, padx=6)
        self.label2.pack(side=tk.RIGHT, padx=6)

    def update_label(self, *args):
        '''
        Fonction pour mettre à jour la position du curseur sur l'étiquette
        '''

        self.label1.configure(text=self.vardata['pos'].get())
        self.label2.configure(text=self.vardata['dim'].get())