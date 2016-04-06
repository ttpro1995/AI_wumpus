from agents import *
from AppGui import *

def main():
    wumpus_env = WumpusEnvironment(agent_program=None, width=10, height=10) #init the wumpus environment

    # loop though
    for i in range(wumpus_env.x_start,wumpus_env.x_end):
        for j in range(wumpus_env.y_start,wumpus_env.y_end):
            # print("At ",i ," ", j, " = ")
            thing_list = wumpus_env.list_things_at((i,j))  # get array of thing at location (i,j)
            thing_str = "" # string of thing's name
            for thing in thing_list:
                thing_str+= thing.__class__.__name__+"\n" # print string at current location
            # print(thing_str)

    # gui
    root = Tk()
    app = AppGui(root, wumpus_env)
    root.mainloop()


if __name__ == "__main__":
    main()