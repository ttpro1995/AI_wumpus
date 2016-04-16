from agents import *
from AppGui import *
from wumpus_map import *
from logic import *

def main():

    map = MapReader("wumpus_map.txt")

    explorer_kb = PropKB()
    explorer_plan = []
    mapsize = map.height
    explorer_program = KB_AgentProgram(explorer_kb,explorer_plan,mapsize)

    forward_program = AlwaysForwardProgram()

    wumpus_env = WumpusEnvironment(agent_program=forward_program, width=map.width+2, height=map.height+2, map_reader=map) #init the wumpus environment


    # gui
    root = Tk()
    app = AppGui(root, wumpus_env)
    root.mainloop()


if __name__ == "__main__":
    main()