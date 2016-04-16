

from wumpus_map import *

from AgentWumpus import *
from AppGui import *

def main():

    map = MapReader("wumpus_map.txt")

    explorer_kb = PropKB()
    explorer_plan = []
    mapsize = map.height

    #
    # forward_program = AlwaysForwardProgram()
    #


    agentWumpus = AgentWumpus(explorer_kb, explorer_plan,mapsize)
    explorer_program = agentWumpus.KB_AgentProgram()
    wumpus_env = WumpusEnvironment(agent_program=explorer_program, width=map.width+2, height=map.height+2, map_reader=map) #init the wumpus environment

    #
    #
    # # gui
    root = Tk()
    app = AppGui(root, wumpus_env)
    root.mainloop()



if __name__ == "__main__":
    main()