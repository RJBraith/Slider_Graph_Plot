import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('ggplot')

import tkinter as tk


class Application(tk.Frame):

    fig = Figure(figsize = (6,6), dpi= 90)
    ax = fig.add_subplot(111)
    length = 400

    
    def __init__(self, master= None):
        super().__init__(master)
        self.master = master
        self.flipY = tk.IntVar(self)
        self.flipX = tk.IntVar(self)
        self.grid(columnspan= 4, rowspan= 10)
        self.create_widgets()
        self.create_plot()


    def create_widgets(self):
        # Creating Sliders & Buttons
        self.powerX = tk.Scale(self, from_= 0, to= 10, orient= tk.HORIZONTAL, label= 'Power of X', resolution=0.1, length= self.length)
        self.xOffset = tk.Scale(self, from_= -50, to= 50, orient= tk.HORIZONTAL, label= 'X Offset', resolution= 1, length= self.length)
        self.yOffset = tk.Scale(self, from_= -50, to= 50, orient= tk.HORIZONTAL, label= 'Y Offset', resolution= 1, length= self.length)

        self.upperXLimitSlider = tk.Scale(self, from_=0, to= 20, orient= tk.HORIZONTAL, label= 'X Max', resolution= 1)
        self.lowerXLimitSlider = tk.Scale(self, from_=-20, to= 0, orient= tk.HORIZONTAL, label= 'X Min', resolution= 1)
        self.upperXLimitSlider.set(10)
        self.lowerXLimitSlider.set(-10)

        self.upperYLimitSlider = tk.Scale(self, from_=0, to= 200, orient= tk.HORIZONTAL, label= 'Y Max', resolution= 1)
        self.lowerYLimitSlider = tk.Scale(self, from_=-200, to= 0, orient= tk.HORIZONTAL, label= 'Y Min', resolution= 1)
        self.upperYLimitSlider.set(100)
        self.lowerYLimitSlider.set(-100)
        
        self.quitButton = tk.Button(self, text= 'Quit', command= quit)

        self.flipYBox = tk.Checkbutton(self, variable= self.flipY, text= 'Flip Along Y-Axis')
        self.flipXBox = tk.Checkbutton(self, variable= self.flipX, text= 'Flip Along X-Axis')

        # Geometry Management
        self.powerX.grid(columnspan= 3, column= 0, row= 0)
        self.xOffset.grid(columnspan= 3, column= 0, row= 1)
        self.yOffset.grid(columnspan= 3, column= 0, row= 2)

        self.quitButton.grid(column= 2, row=3)

        self.upperXLimitSlider.grid(column= 4, row= 0, padx= 5, pady= 5)
        self.lowerXLimitSlider.grid(column= 4, row= 1, padx= 5, pady= 5)

        self.upperYLimitSlider.grid(column= 4, row= 2, padx= 5, pady= 5)
        self.lowerYLimitSlider.grid(column= 4, row= 3, padx= 5, pady= 5)

        self.flipYBox.grid(column= 0, row=3)
        self.flipXBox.grid(column= 1, row=3)


    def calculatePlotValues(self, x: int, powerX: float, xOffset: float, yOffset: float, flipY: int, flipX: int, /) -> float:   
        if flipY == 0:
            if flipX == 0:
                return 1 * ((((1 * x) + xOffset) ** powerX) + yOffset)
            if flipX == 1:
                return 1 * ((((-1 * x) + xOffset) ** powerX) + yOffset)
        if flipY == 1:
            if flipX == 0:
                return -1 * ((((1 * x) + xOffset) ** powerX) + yOffset)
            if flipX == 1:
                return -1 * ((((-1 * x) + xOffset) ** powerX) + yOffset)

    def stringifyGraphEquation(self) -> str:
        arg1 = '-' if self.flipY.get() == 1 else ''
        arg2 = '-' if self.flipX.get() == 1 else ''
        arg3 = '+' if self.xOffset.get() >= 0 else '-'
        arg4 =  abs(self.xOffset.get())
        arg5 = self.powerX.get()
        arg6 =  '+' if self.yOffset.get() >= 0 else '-'
        arg7 = abs(self.yOffset.get())

        return 'Y = {}({}X {} {})^{} {} {}'.format(arg1, arg2, arg3, arg4, arg5, arg6, arg7)



    def create_plot(self):
        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(columnspan= 3, column= 0, row= 5, padx= 10, pady= 10)

        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(columnspan= 3, column= 0, row= 6)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
        toolbar.update()

    
    def animate(self, i):
        plotValues = [self.calculatePlotValues(x, self.powerX.get(), self.xOffset.get(), self.yOffset.get(), self.flipY.get(), self.flipX.get()) for x in range(self.lowerXLimitSlider.get(), self.upperXLimitSlider.get() + 1, 1)]

        self.ax.clear()

        self.ax.plot(range(self.lowerXLimitSlider.get(), self.upperXLimitSlider.get() + 1), plotValues)

        self.ax.set_title(self.stringifyGraphEquation())
        self.ax.set_xlabel('X Axis')
        self.ax.set_xticks(range(self.lowerXLimitSlider.get(), self.upperXLimitSlider.get() + 1, 2))
        self.ax.set_ylabel('Y Axis')
        self.ax.set_ylim(self.lowerYLimitSlider.get(), self.upperYLimitSlider.get())


root = tk.Tk()
app = Application(master= root)
app.master.title('Live-Plot Slider GUI')
ani = animation.FuncAnimation(app.fig, app.animate, interval= 500)
app.mainloop()
