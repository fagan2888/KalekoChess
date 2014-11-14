
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from Tkinter import Tk, Canvas, Frame, BOTH, NW, Label
from PIL import Image, ImageTk

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Test Canvas")        
        self.pack(fill=BOTH, expand=1)
        
        self.img = Image.open("../img/blackp.gif")
        self.photo = ImageTk.PhotoImage(self.img)

        #kaleko
        canvas = Canvas(self,width=self.img.size[0]+20,
            height=self.img.size[1]+20)
        canvas.create_image(10, 10, anchor=NW, image=self.photo)
        canvas.pack(fill=BOTH, expand=1)


root = Tk()
ex = Example(root)
root.mainloop()




if __name__ == '__main__':
    main()

