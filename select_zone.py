import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
from txt_recogn import *
from image_widget import PasteButtons
import time

# Une classe specifique pour selectionner une zone sur le canevas
class selectZone():
    def __init__(self, root, canvas, draw_image, image, x_root, y_root, dist_w, dist_h):
        self.root = root
        self.canvas = canvas
        self.draw_image = draw_image
        self.image = image
        self.x_root = x_root
        self.y_root = y_root
        self.dist_w = int(dist_w)
        self.dist_h = int(dist_h)

        self.mission = None
        self.selectRectangle = tk.IntVar(value=0)
        self.selectRectangle.trace('w', self.bind_canvas)

        self.rect = None
        self.image_select = None
        self.image_copied = None

        self.langue = "eng"
        self.paste_tk = []

    def bind_canvas(self, *args):
        '''
        Fonction pour Lier le canevas avec des fonctions lorsque les utilisateurs commencent à sélectionner des zones
        '''

        if self.selectRectangle.get() == 1:
            self.b1 = self.canvas.bind("<Button-1>", self.b1_action)
            self.b1_motion = self.canvas.bind("<B1-Motion>", self.b1_motion_action)
            self.b1_release = self.canvas.bind("<ButtonRelease-1>", self.b1_release_action)

    def b1_action(self, event):
        '''
        Fonction lors d'un clic gauche sur le canevas
        ----------
        Input:
            event: le clic gauche sur le canevas
        '''

        if self.selectRectangle.get() == 1 and self.mission != 'Paste':
            if self.rect != None:
                self.canvas.delete(self.rect)

            self.select_start = (event.x, event.y)
            self.rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y,
                                                     dash=(7,1,1,1), outline="grey", width=2)

    def b1_motion_action(self, event):
        '''
        Fonction lorsque la souris est déplacée sur le canevas
        ----------
        Input:
            event: la souris est déplacée sur le canevas avec le bouton gauche de la souris enfoncé
        '''


        if self.selectRectangle.get() == 1 and self.mission != 'Paste':  # quand les utilisateurs sélectionnent des zones
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.rect, self.select_start[0], self.select_start[1], event.x, event.y)

        if self.selectRectangle.get() == 1 and self.mission == 'Paste':   # quand les utilisateurs collent
            self.event_paste = event
            self.canvas.delete(self.rect)
            self.canvas.delete(self.paste_image)
            self.paste_image = self.canvas.create_image(event.x, event.y, image=self.img_tk)
            self.rect = self.canvas.create_rectangle(event.x - self.w / 2, event.y - self.h / 2, event.x + self.w / 2,
                                                     event.y + self.h / 2,
                                                     dash=(7, 1, 1, 1), outline="grey", width=2)

    def b1_release_action(self, event):
        '''
        Fonction lorsque le bouton gauche de la souris est relâché
        ----------
        Input:
            event: le bouton gauche de la souris est relâché
        '''

        if self.selectRectangle.get() == 1 and self.mission != 'Paste':
            self.x_start = self.x_root + self.select_start[0]
            self.y_start = self.y_root + self.select_start[1]

            self.x_end = self.x_root + self.select_end[0]
            self.y_end = self.y_root + self.select_end[1]

            self.image_select = self.image.crop((self.select_start[0]-self.dist_w, self.select_start[1]-self.dist_h, self.select_end[0]-self.dist_w, self.select_end[1]-self.dist_h))


    def reset_select_rect(self):
        '''
        Fonction pour réinitialiser les valeurs lorsque les utilisateurs arrêtent de sélectionner des zones
        '''
        self.canvas.delete(self.rect)
        self.selectRectangle.set(0)
        self.rect = None
        self.image_select = None
        self.image_copied = None

    def text_recognition(self):
        '''
        Fonction d'analyse des textes sur la zone sélectionnée
        '''

        if self.image_select != None:

            self.text_detector = TextDetector(self.image_select)
        else:
            messagebox.showerror('Error', 'You didn\'t chose any image to analyse. Please try again')

    def copy_selection(self):
        '''
        Fonction pour copier la zone sélectionnée
        '''
        if self.image_select != None:
            self.image_copied = self.image_select
            messagebox.showinfo("Copy Selected Zone", "The selected zone has been copied to the clipboard.")
        else:
            messagebox.showerror('Error', 'You didn\'t chose any image to copy. Please try again')

    def cut_selection(self):
        '''
        Fonction pour couper la zone sélectionnée
        '''
        if self.image_select != None:
            self.image_copied = self.image_select

            self.canvas.delete(self.rect)
            self.canvas.create_rectangle(self.select_start[0], self.select_start[1], self.select_end[0], self.select_end[1], fill="white", outline="white")
            self.draw_image.rectangle([self.select_start[0]-self.dist_w, self.select_start[1]-self.dist_h, self.select_end[0]-self.dist_w, self.select_end[1]-self.dist_h], fill="white", outline="white")
            self.rect = self.canvas.create_rectangle(self.select_start[0], self.select_start[1], self.select_end[0], self.select_end[1],
                                                     dash=(7,1,1,1), outline="grey", width=2)

            messagebox.showinfo("Copy Selected Zone", "The selected zone has been copied to the clipboard.")

        else:
            messagebox.showerror('Error', 'You didn\'t chose any image to analyse. Please try again')

    def paste_selection(self):
        '''
        Fonctions de collage de zone copiée
        '''
        if self.image_copied != None:
            self.canvas.delete(self.rect)

            self.paste_variable = tk.StringVar()
            self.paste_variable.trace('w', self.paste_func)

            self.paste_buttons = PasteButtons(self.root, self.paste_variable, ["Save", "Cancel"])

            self.img_tk = ImageTk.PhotoImage(self.image_copied)

            self.paste_image = self.canvas.create_image(self.x_start, self.y_start, image=self.img_tk)
            self.mission = 'Paste'

            self.h = self.img_tk.height()
            self.w = self.img_tk.width()
            self.rect = self.canvas.create_rectangle(self.x_start - self.w / 2, self.y_start - self.h / 2, self.x_start + self.w / 2, self.y_start + self.h / 2,
                                                     dash=(7,1,1,1), outline="grey", width=2)
            self.event_paste = (self.x_start, self.y_start)

            self.canvas.bind("<B1-Motion>", self.b1_motion_action)
        else:
            messagebox.showerror('Error', 'You didn\'t copy any image. Please try again')

    def paste_func(self, *args):
        '''
        Fonction lorsque l'utilisateur clique sur 'Enregistrer' ou 'Annuler'
        '''

        if self.paste_variable.get() != 'Stop Paste':
            self.canvas.delete(self.paste_image)
            self.canvas.delete(self.rect)
            self.mission = None
            self.paste_buttons.grid_forget()

        if self.paste_variable.get() == 'Save':
            self.paste()
        self.paste_variable.set("Stop Paste")

    def paste(self):
        '''
        Fonction pour coller
        '''
        self.paste_tk.append(self.img_tk)
        self.canvas.create_image(self.event_paste.x, self.event_paste.y, image=self.paste_tk[len(self.paste_tk)-1])

        self.image.paste(self.image_copied, (self.event_paste.x - int(self.w / 2) - self.dist_w, self.event_paste.y - int(self.h / 2) - self.dist_h)) #self.event_paste.x-self.dist_w, self.event_paste.y-self.dist_h

