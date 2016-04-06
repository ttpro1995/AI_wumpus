from tkinter import *
from tkinter import messagebox  # must be explicitly import
from PIL import Image
from agents import *

class AppGui:
    def __init__(self, master, env):
        # wumpus environment
        self.env = env
        agents = env.agents
        if len(agents) is 1:
            self.agent = agents[0]
        else :
            self.agent = agents[1]

        master.bind('<Left>',self.MoveLeft)
        master.bind('<Right>',self.MoveRight)
        master.bind('<Up>',self.MoveUp)
        master.bind('<Down>',self.MoveDown)
        # the master frame
        self.frame = Frame(master)
        self.frame.grid()

        self.toolbar = Frame(master);
        self.toolbar.grid(row = 0)

        self.bot_frame = Frame(master,background="black")
        self.bot_frame.grid(row = 4)

        self.button = Button(self.toolbar, text="Quit", fg="red", command=self.frame.quit)
        self.button.grid(row = 0, column= 5 , padx = 30)

        self.show = Button(self.toolbar, text="Show", command=self.updateGUI)
        self.show.grid(row = 0, column = 0, padx = 40)

        self.moveLeft = Button(self.toolbar, text="Left", command=self.MoveLeft)
        self.moveLeft.grid(row = 0, column = 1)

        self.moveRight = Button(self.toolbar, text="Right", command=self.MoveRight)
        self.moveRight.grid(row = 0, column = 3)

        self.moveUp = Button(self.toolbar, text="Up", command=self.MoveUp)
        self.moveUp.grid(row = 0, column = 2)

        self.moveDown = Button(self.toolbar, text="Down", command=self.MoveDown)
        self.moveDown.grid(row = 1, column = 2)



        #self.can = Canvas(self.bot_frame)
        #self.can.grid(row=0, column=0)
        #photo = PhotoImage(file='apple.gif')
        #self.can.photo = photo
        #self.can.create_image(0, 0, image=photo)

        self._widgets = []
        for r in range(0,self.env.x_end +1):
            cur_row = []
            for c in range(0,self.env.y_end +1):
                label = Label(self.bot_frame, text="%s/%s" % (r, c),
                              borderwidth=1, width=7, height= 3)
                label.grid(row=r, column=c,sticky ="nsew", padx=1, pady=1)
                label.is_reveal = False
                cur_row.append(label)
            self._widgets.append(cur_row)


    def updateGUI(self):
        # test reveal
        # for i in range(0, self.env.x_end + 1):
        #     for j in range(0, self.env.y_end + 1):
        #         self._widgets[i][j].is_reveal = True

        for i in range( 0,  self.env.x_end+1):
            for j in range( 0,  self.env.y_end+1):
                print("At ", i, " ", j, " = ")
                thing_list =  self.env.list_things_at((i, j))  # get array of thing at location (i,j)
                thing_str = ""  # string of thing's name
                cur_cell = self._widgets[i][j]

                if cur_cell.is_reveal:
                    cur_cell.config(background="pink") # set reveal cell (except one with explorer to pink)

                # loop through all object
                for thing in thing_list:
                    thing_name = thing.__class__.__name__

                    # Reveal cell if Explorer (player) stand in that cell
                    if thing_name is "Explorer":
                        cur_cell.is_reveal = True  # reveal the current position of player
                        cur_cell.config(background="red") # set it to red

                    # set cell to black at wall
                    if thing_name is "Wall":
                        cur_cell.config(background="black")

                    if thing_name is not "Explorer": # we indicate explore as red, so no need to write here
                        thing_str += thing_name + "\n"  # append list of object into string

                # config cell
                if cur_cell.is_reveal:
                    cur_cell.config(text=thing_str)
                else:
                    cur_cell.config(text="")



    def Forward(self):

        self.env.execute_action(agent=self.agent, action="Forward");
        self.updateGUI()

    def MoveRight(self, event = None):
        if self.agent.direction.direction == Direction.R:
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.L:
             self.agent.direction = self.agent.direction + Direction.R
             self.agent.direction = self.agent.direction + Direction.R
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.U:
             self.agent.direction = self.agent.direction + Direction.R
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.D:
             self.agent.direction = self.agent.direction + Direction.L
             self.agent.direction = self.agent.direction + Direction.R
        self.env.execute_action(agent=self.agent, action="Forward")
        self.updateGUI()


    def MoveLeft(self, event = None):
        if self.agent.direction.direction == Direction.R:
             self.agent.direction = self.agent.direction + Direction.L
        elif self.agent.direction.direction == Direction.L:
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.U:
             self.agent.direction = self.agent.direction
        elif self.agent.direction.direction == Direction.D:
             self.agent.direction = self.agent.direction + Direction.R
             self.agent.direction = self.agent.direction + Direction.R

        self.env.execute_action(agent=self.agent, action="Forward");
        self.updateGUI()


    def MoveUp(self, event = None):
        if self.agent.direction.direction == Direction.R:
             self.agent.direction = self.agent.direction + Direction.R
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.L:
             self.agent.direction = self.agent.direction
        elif self.agent.direction.direction == Direction.U:
             self.agent.direction = self.agent.direction + Direction.L
        elif self.agent.direction.direction == Direction.D:
             self.agent.direction = self.agent.direction + Direction.R

        self.env.execute_action(agent=self.agent, action="Forward")
        self.updateGUI()

    def MoveDown(self, event = None):
        if self.agent.direction.direction == Direction.R:
             self.agent.direction = self.agent.direction
        elif self.agent.direction.direction == Direction.L:
             self.agent.direction = self.agent.direction + Direction.R
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.U:
             self.agent.direction = self.agent.direction + Direction.R
        elif self.agent.direction.direction == Direction.D:
             self.agent.direction = self.agent.direction + Direction.L

        self.env.execute_action(agent=self.agent, action="Forward")
        self.updateGUI()


    def say_hi(self):
        textbox_text = self.text.get(1.0, END)
        mes = "Hi " + textbox_text + "I am Pusheen the cat";
        messagebox.showinfo("Hi", mes)

