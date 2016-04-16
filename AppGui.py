from tkinter import *
from tkinter import messagebox  # must be explicitly import
from PIL import Image
from agents import *
from search import *
from logic import *

class AppGui:
    def __init__(self, master, env):
        # wumpus environment
        self.env = env
        agents = env.agents
        if len(agents) is 1:
            self.agent = agents[0]
        else:
            self.agent = agents[1]

        master.bind('<Left>',self.MoveLeft)
        master.bind('<Right>',self.MoveRight)
        master.bind('<Up>',self.MoveUp)
        master.bind('<Down>',self.MoveDown)
        # the master frame
        self.frame = Frame(master)
        self.frame.pack()
        #self.frame.grid()

        self.toolbar = Frame(master);
        #self.toolbar.grid(row = 0, column = 0)
        self.toolbar.pack()

        self.bot_frame = Frame(master,background="black")
        #self.bot_frame.grid(row = 4, column = 0)
        self.bot_frame.pack()

        self.button = Button(self.toolbar, text="Quit", fg="red", command=self.frame.quit)
        self.button.grid(row = 0, column=4 )

        self.show = Button(self.toolbar, text="Show", command=self.updateGUI)
        self.show.grid(row = 2, column = 0)

        self.reveal_bt = Button(self.toolbar, text="Reveal All", command=self.reveal_all)
        self.reveal_bt.grid(row=2, column=1)

        #  self.reset_bt = Button(self.toolbar, text="Reveal All", command=self.updateGUI)
        #  self.reset_bt.grid(row=2, column=2)

        self.moveLeft = Button(self.toolbar, text="Left", command=self.MoveLeft)
        self.moveLeft.grid(row = 0, column = 0)

        self.moveRight = Button(self.toolbar, text="Right", command=self.MoveRight)
        self.moveRight.grid(row = 0, column = 2)

        self.moveUp = Button(self.toolbar, text="Up", command=self.MoveUp)
        self.moveUp.grid(row=0, column=1)

        self.moveDown = Button(self.toolbar, text="Down", command=self.MoveDown)
        self.moveDown.grid(row = 1, column = 1)

        self.testButtun = Button(self.toolbar, text="Test", command=self.testSearch)
        self.testButtun.grid(row = 3, column = 1)

        self.stepButtun = Button(self.toolbar, text="Step", command=self.execute_step)
        self.stepButtun.grid(row = 3, column = 2)

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
        self.updateGUI()  # Update UI at start of game

    def reveal_all(self):
        for i in range(0, self.env.x_end + 1):
             for j in range(0, self.env.y_end + 1):
                 self._widgets[i][j].is_reveal = True
        self.updateGUI()

    def lose_message(self):
        messagebox.showinfo("You lose", "Explore is dead.\nBetter luck next time.")

    def updateGUI(self):
        print(self.agent.location)
        print(self.agent.direction.direction)

        # if (self.agent.direction.direction == Direction.R):
        #     print('R')
        # if (self.agent.direction.direction == Direction.L):
        #     print('L')
        # if (self.agent.direction.direction == Direction.U):
        #     print('U')
        # if (self.agent.direction.direction == Direction.D):
        #     print('D')

        # test reveal
        # for i in range(0, self.env.x_end + 1):
        #     for j in range(0, self.env.y_end + 1):
        #         self._widgets[i][j].is_reveal = True

        for i in range( 0,  self.env.x_end+1):
            for j in range( 0,  self.env.y_end+1):
                # print("At ", i, " ", j, " = ")
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
        if self.env.in_danger(self.agent):
            self.lose_message()


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

    def execute_step(self):
        self.env.step()
        self.updateGUI()

    def testSearch(self):
        pos = self.agent.location
        direct = self.agent.direction.direction
        current = (pos,direct) # current position and current direction
        goal = [(1,3),(1,4)] # set of goals position
        allowed = [(1,1),(1,2),(1,3),(1,4)]
        plan = plan_route(current,goal,allowed)
        print(plan)
