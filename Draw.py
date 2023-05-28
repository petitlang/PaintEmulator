import tkinter as tk
import math

# Une classe contient des fonctions pour dessiner sur le canevas et l'image
class DrawCanvas():
    def __init__(self, canvas, draw_image, update_current, img=None, dist_w=0, dist_h=0):
        self.canvas = canvas
        self.draw_image = draw_image
        self.update_current = update_current

        self.selectOption = 'None'

        #self.line_new=[(100,100),(140,96),(200,110)]
        #self.line_new=[]
        #self.t=0

        self.x_old=-1
        self.y_old=-1
        self.x_older=-1
        self.y_older=-1

        self.color = 'black'
        self.size = 2
        self.image = img
        self.dist_w = int(dist_w)
        self.dist_h = int(dist_h)

        #self.line_list = []
        #self.rect_list = []
        #self.oval_list = []

    # Fonctions pour l'outil Pinceau
    def draw_circle(self,event, color='black', size=5):
        if self.selectOption == 'Brush':
            if False:
                print('???')
                dist_modified=math.sqrt((event.x-self.x_old)**2+(event.y-self.y_old)**2)/50-2
                point_size=-dist_modified/math.sqrt(1+dist_modified**2)*5+7
                drawed_point=self.canvas.create_oval((event.x, event.y, event.x, event.y), outline='red',width=int(point_size))
                self.draw_image.ellipse([(event.x-self.dist_w, event.y-self.dist_h), (event.x-self.dist_w, event.y-self.dist_h)], outline='red',width=int(point_size))
                self.canvas.create_line([self.x_old,self.y_old,event.x,event.y], fill='blue', width=int(point_size))
                self.draw_image.line([(self.x_old-self.dist_w,self.y_old-self.dist_h),(event.x-self.dist_w,event.y-self.dist_h)], fill='blue', width=int(point_size))

            if self.x_older!=-1 and (event.x!=self.x_old or event.y!=self.y_old):
                #print('!!!')
                x1,y1=self.x_older,self.y_older
                x2,y2=self.x_old,self.y_old
                x3,y3=event.x,event.y
                x12=(x1+x2)/2
                y12=(y1+y2)/2
                x32=(x3+x2)/2
                y32=(y3+y2)/2
                A=x1*y2-y1*x2+x2*y3-y2*x3+x3*y1-y3*x1
                A*=2
                if A==0: A=0.1
                
                dist_modified=math.sqrt((x1-x3)**2+(y1-y3)**2)/50-1.4
                arc_size=-dist_modified/math.sqrt(1+dist_modified**2)*size/2+size*3/4+2
                
                pil_cadre = (x12-self.dist_w, y12-self.dist_h, x32-self.dist_w, y32-self.dist_h)
                self.draw_image.line(pil_cadre, fill=color, width=int(arc_size))

                if  A==0.1 :
                    #self.canvas.create_oval(x3-arc_size/2,y3-arc_size/2,x3+arc_size/2,y3+arc_size/2,fill=color,outline=color)
                    #pil_cadre = (x3-arc_size/2-self.dist_w, y3-arc_size/2-self.dist_h, x3+arc_size/2-self.dist_w, y3+arc_size/2-self.dist_h)
                    #self.draw_image.ellipse(pil_cadre, fill=color, outline=color, width=int(arc_size))
                    #arc_size+=2
                    self.canvas.create_line(x1,y1,x3,y3,fill=color,width=arc_size)
                else:
                    B=-((x1**2+y1**2)*(y3-y2)+(x2**2+y2**2)*(y1-y3)+(x3**2+y3**2)*(y2-y1))
                    C=(x1**2+y1**2)*(x3-x2)+(x2**2+y2**2)*(x1-x3)+(x3**2+y3**2)*(x2-x1)
                    D=(x1**2+y1**2)*(x2*y3-x3*y2)+(x2**2+y2**2)*(x3*y1-x1*y3)+(x3**2+y3**2)*(x1*y2-x2*y1)
                    x_cen=int(B/A)
                    y_cen=int(C/A)
                    R=int(math.sqrt(B**2+C**2+2*A*D)/A)

                    cadre=(x_cen-R,y_cen-R,x_cen+R,y_cen+R)
                    angle0=-math.atan2(y12-y_cen,x12-x_cen)/math.pi*180
                    angle1=-math.atan2(y32-y_cen,x32-x_cen)/math.pi*180
                    angle=angle1-angle0
                    if angle>200: angle-=360
                    if angle<-200: angle+=360
                    self.canvas.create_arc(cadre, start=angle0, extent=angle, outline=color, style="arc",width=arc_size)
                    arc_size-=2
                    self.canvas.create_oval(x12-arc_size/2,y12-arc_size/2,x12+arc_size/2,y12+arc_size/2,fill=color,outline=color)
                    self.canvas.create_oval(x32-arc_size/2,y32-arc_size/2,x32+arc_size/2,y32+arc_size/2,fill=color,outline=color)
                    
                
                if False:
                    pil_cadre = (cadre[0]-self.dist_w, cadre[1]-self.dist_h, cadre[2]-self.dist_w, cadre[3]-self.dist_h)
                    angle=-int(angle)
                    angle0=-int(angle0)
                    if angle0<0: angle0+=360
                    if angle>0: 
                        self.draw_image.arc(pil_cadre, start=angle0, end=min(angle0+angle,359), fill=color, width=int(arc_size))
                        if angle0+angle>360: self.draw_image.arc(pil_cadre, start=0, end=angle0+angle-360, fill=color, width=int(arc_size))
                    if angle<0: 
                        self.draw_image.arc(pil_cadre, start=max(angle0+angle,0), end=angle0, fill=color, width=int(arc_size))
                        if angle0+angle<0: self.draw_image.arc(pil_cadre, start=angle0+angle+360, end=359, fill=color, width=int(arc_size))
            #self.t+=1
            #self.line_new.append((event.x,event.y))
            self.x_older=self.x_old
            self.y_older=self.y_old
            self.x_old=event.x
            self.y_old=event.y

    def update_new_line(self,event):
        #if self.selectOption == 'Brush':
            #line2draw=self.fit_line(self.line_new)
            #self.canvas.create_line(100,100,110,106,120,110,fill="green",width=5)



            #print(self.line_new)
            #self.line_new=[]
            #self.t=0
        self.x_older=-1
        self.y_older=-1
        self.x_old=-1
        self.y_old=-1


    # def end_brush(self, event):
    #

    #def fit_line(point):

    # Fonctions pour l'outil Ligne
    def start_line(self, event, color='black', size=2):
        if self.selectOption == 'Line':
            self.color = color
            self.size = size
            self.select_start = (event.x, event.y)
            self.line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill=self.color, width=self.size)


    def draw_line(self, event):
        if self.selectOption == 'Line':
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.line, self.select_start[0], self.select_start[1], event.x, event.y)

    def end_line(self, event):
        if self.selectOption == 'Line':
            line = self.draw_image.line([(self.select_start[0]-self.dist_w, self.select_start[1]-self.dist_h), (self.select_end[0]-self.dist_w, self.select_end[1]-self.dist_h)], fill=self.color, width=int(self.size))

    # Fonctions pour l'outil Rectangle
    def start_rect(self, event, color='black', size=2):
        if self.selectOption == 'Rectangle':
            self.color = color
            self.size = size
            self.select_start = (event.x, event.y)
            self.rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=self.color, width=self.size)

    def draw_rect(self, event):
        if self.selectOption == 'Rectangle':
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.rect, self.select_start[0], self.select_start[1], event.x, event.y)

    def end_rect(self, event):
        if self.selectOption == 'Rectangle':
            self.swap_start_end_point()
            rect = self.draw_image.rectangle([(self.select_start[0]-self.dist_w, self.select_start[1]-self.dist_h), (self.select_end[0]-self.dist_w, self.select_end[1]-self.dist_h)], outline=self.color, width=int(self.size))
            # self.image.show()

    # Fonctions pour l'outil ovale
    def start_oval(self, event, color='black', size=2):
        if self.selectOption == 'Oval':
            self.color = color
            self.size = size
            self.select_start = (event.x, event.y)
            self.oval = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=self.color, width=self.size)

    def draw_oval(self, event):
        if self.selectOption == 'Oval':
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.oval, self.select_start[0], self.select_start[1], event.x, event.y)

    def end_oval(self, event):
        if self.selectOption == 'Oval':
            self.swap_start_end_point()
            self.draw_image.ellipse([(self.select_start[0]-self.dist_w, self.select_start[1]-self.dist_h), (self.select_end[0]-self.dist_w, self.select_end[1]-self.dist_h)], outline=self.color, width=int(self.size))
            # self.image.show()

    def swap_start_end_point(self):
        '''
        Fonction pour échangez les attributs select_start et select_end pour obtenir le coin supérieur gauche et le coin inférieur droit
        '''
        start = self.select_start
        end = self.select_end
        if start[0] < end[0] and start[1] > end[1]:
            self.select_start = (start[0], end[1])
            self.select_end = (end[0], start[1])

        elif start[0] > end[0] and start[1] < end[1]:
            self.select_start = (end[0], start[1])
            self.select_end = (start[0], end[1])

        elif start[0] > end[0] and start[1] > end[1]:
            self.select_start = (end[0], end[1])
            self.select_end = (start[0], start[1])



    # Fonctions pour l'outil Gomme
    def erase(self, event, size=10):
        if self.selectOption == 'Eraser':
            x, y = event.x, event.y
            self.canvas.create_rectangle(x-size, y-size, x+size, y+size, fill="white", outline="white")
            self.draw_image.rectangle([(x - size - self.dist_w, y - size - self.dist_h), (x + size - self.dist_w, y + size - self.dist_h)],
                                      outline="white", fill="white")


"""
        for i in range(1,len(self.line_new)-1):

            x1,y1=self.line_new[i-1]
            x2,y2=self.line_new[i]
            x3,y3=self.line_new[i+1]

            A=x1*y2-y1*x2+x2*y3-y2*x3+x3*y1-y3*x1
            A*=2
            B=-((x1**2+y1**2)*(y3-y2)+(x2**2+y2**2)*(y1-y3)+(x3**2+y3**2)*(y2-y1))
            C=(x1**2+y1**2)*(x3-x2)+(x2**2+y2**2)*(x1-x3)+(x3**2+y3**2)*(x2-x1)
            D=(x1**2+y1**2)*(x2*y3-x3*y2)+(x2**2+y2**2)*(x3*y1-x1*y3)+(x3**2+y3**2)*(x1*y2-x2*y1)
            if A==0: 
                if D>0: A=0.1
                else: A=-0.1
            x_cen=int(B/A)
            y_cen=int(C/A)
            R=int(math.sqrt(B**2+C**2+2*A*D)/A)

            dist_modified=math.sqrt((x1-x3)**2+(y1-y3)**2)/50-2
            arc_size=-dist_modified/math.sqrt(1+dist_modified**2)*5+7
            cadre=(x_cen-R,y_cen-R,x_cen+R,y_cen+R)
            angle0=-math.atan2(y1+y2-2*y_cen,x1+x2-2*x_cen)/math.pi*180
            angle1=-math.atan2(y3+y2-2*y_cen,x3+x2-2*x_cen)/math.pi*180
            angle=angle1-angle0
            if angle>200: angle-=360
            if angle<-200: angle+=360
            if A!=0.1 and A!=-0.1:self.canvas.create_arc(cadre, start=angle0, extent=angle, style="arc",width=arc_size)
"""

