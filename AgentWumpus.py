


from utils import *  # noqa
import agents
from search import *

import itertools
import re
from collections import defaultdict
import GenerateSentence
from time import *
import sys
import GenerateSentence
from logic import  *




heading_num_to_str = {0: 'North', 1: 'West', 2: 'South', 3: 'East'}
heading_str_to_num = {'North': 0, 'West': 1, 'South': 2, 'East': 3}

class AgentWumpus:

    def __init__(self, KB,plan,mapsize):
        self.time = 0
        self.initial_heading = "East"
        self.initial_location = (1,1)
        self.belief_location = self.initial_location
        self.belief_heading = self.initial_heading
        self.KB = KB
        self.plan = plan
        self.mapsize = mapsize
        self.unvisited = [(x,y)
                          for x in range(1,self.mapsize+1)
                          for y in range(1,self.mapsize+1)]
        self.create_wumpus_KB()

    def create_wumpus_KB(self):
            # if self.verbose:
            print("HWA.create_wumpus_KB(): adding initial wumpus axioms")
            axioms = GenerateSentence.initial_wumpus_axioms(self.belief_location[0],self.belief_location[1],
                                                            self.mapsize, heading_str(self.belief_heading))
            # if self.verbose:
            #     start_time = clock()
            #     print "    total number of axioms={0}".format(len(axioms))
            # kb = PropKB_SAT()
            for sentence in axioms:
                self.KB.tell(sentence)
            meowmeowmeow = 1
            # if self.keep_axioms:
            #     self.KB.axioms = axioms
            # if self.verbose:
            #     end_time = clock()
            #     print "    total number of clauses={0}".format(len(kb.clauses))
            #     print "          >>> time elapsed: {0}".format(end_time-start_time)
            # return kb



    def KB_AgentProgram(self):
        """A generic logical knowledge-based agent program. [Fig. 7.1]

        inputs: percept, a list, [stench,breeze,glitter,bump,scream]

        persistent: KB, a knowledge base, initially the atemporal “wumpus physics”
                    t, a counter, initially 0, indicating time
                    plan, an action sequence, initially empty
        """
        steps = itertools.count()


        def program(percept):
            print("start program with percept ")
            print(percept)
            t = next(steps)
            current = (1, 1)  # current position
            mKB = self.KB

            # if self.verbose:
            print("HWA.agent_program(): at time {0}".format(self.time))

            # update belief location and heading based on current KB knowledge state
            # if self.verbose:
            print("     HWA.infer_and_set_belief_location()")
            infer_and_set_belief_location()
            # if self.verbose:
            print("     HWA.infer_and_set_belief_heading()")
            infer_and_set_belief_heading()

            percept_sentence = make_percept_sentence(percept)
            # if self.verbose:
            print("     HWA.agent_program(): kb.tell(percept_sentence):")
            print("         {0}".format(percept_sentence))
            self.KB.tell(percept_sentence) # update the agent's KB based on percepts
            # if self.keep_axioms:
            #     self.kb.axioms.append(percept_sentence)

            # if self.verbose:
            #     clauses_before = len(self.kb.clauses)
            print("     HWA.agent_program(): Prepare to add temporal axioms")
            #     print "         Number of clauses in KB before: {0}".format(clauses_before)
            add_temporal_axioms()

            safe = []

            # If Glitter, Grab gold and leave
            if self.KB.ask(Expr(percept_glitter_str(self.time))):
                # if self.verbose: print "   HWA.agent_program(): Grab gold and leave!"
                safe = find_OK_locations()
                # if self.verbose: start_time = clock()
                self.plan = [action_grab_str(None)] \
                            + plan_route(self.belief_location, self.belief_heading,
                                         [self.initial_location], safe) \
                            + [action_climb_str(None)]
                # if self.verbose:
                #     end_time = clock()
                #     print "          >>> time elapsed while executing plan_route():" \
                #           + " {0}".format(end_time-start_time)

            # Update safe locations only if we don't have a plan
            if self.plan:
                # if self.verbose:
                print( "   HWA.agent_program(): Already have plan" \
                          + " (with {0} actions left),".format(len(self.plan)) \
                          + " continue executing...")
            elif safe == None:
                print( "   HWA.agent_program(): No current plan, find one...")
                safe = find_OK_locations()

            # Visit unvisited safe square
            if not self.plan:
                # if self.verbose:
                print( "   HWA.agent_program(): Plan to visit safe square...")
                unvisited = update_unvisited_locations() # find_unvisited_locations()
                safe_unvisited = list(set(unvisited).intersection(set(safe)))
                # if self.verbose:
                #     self.display_locations_utility(safe_unvisited, prop=state_loc_str,
                #                                    title="Safe univisited locations:")
                #     start_time = clock()
                self.plan = plan_route(self.belief_location, self.belief_heading ,safe_unvisited, safe)
                # if self.verbose:
                #     end_time = clock()
                    # print "          >>> time elapsed while executing plan_route():" \
                    #       + " {0}".format(end_time-start_time)



            # Shoot wumpus to try to clear path
            # if not self.plan and self.KB.ask(Expr(state_have_arrow_str(self.time))):
            #     # if self.verbose:
            #     print("   HWA.agent_program(): Plan to shoot wumpus...")
            #     possible_wumpus = self.find_possible_wumpus_locations()
            #     # if self.verbose: start_time = clock()
            #     self.plan = plan_shot(self.belief_location, self.belief_heading, possible_wumpus, safe)
            #     # if self.verbose:
            #     #     end_time = clock()
            #     #     print "          >>> time elapsed while executing plan_shot():" \
            #     #           + " {0}".format(end_time-start_time)
            # # No safe choice, take risk with an unknown square


            if not self.plan:
                print("   HWA.agent_program(): No safe choice, take risk...")
                not_unsafe = find_not_unsafe_locations()

                # print "univisited: ", unvisited

                not_unsafe_unvisited = list(set(self.unvisited).intersection(set(not_unsafe)))

                # print "not_unsafe_unvisited", not_unsafe_unvisited
                # print "safe", safe

                safe_and_not_unsafe_unvisited = list(set(safe).union(set(not_unsafe_unvisited)))

                # print "safe_and_not_unsafe_unvisited", safe_and_not_unsafe_unvisited

                # if self.verbose: start_time = clock()
                self.plan = plan_route(self.belief_location, self.belief_heading , not_unsafe_unvisited,
                                       safe_and_not_unsafe_unvisited)
                # if self.verbose:
                #     end_time = clock()
                #     print "          >>> time elapsed while executing plan_route():" \
                #           + " {0}".format(end_time-start_time)
            # No choices left, leave!
            if not self.plan:
                # if self.verbose:
                print("   HWA.agent_program(): No choices left, leave!...")
                    # start_time = clock()
                self.plan = plan_route(self.belief_location, self.belief_heading ,
                                       self.initial_location, safe) \
                            + [action_climb_str(None)]
                # if self.verbose:
                #     end_time = clock()
                #     print "          >>> time elapsed while executing plan_route():" \
                #           + " {0}".format(end_time-start_time)

            # if self.verbose:
            print("   HWA.agent_program(): Plan:\n    {0}".format(self.plan))

            action = self.plan.pop(0) # take next action in plan

            # if self.verbose:
            print("   HWA.agent_program(): Action: {0}".format(action))

            # update KB with selected action
            self.KB.tell(add_time_stamp(action, self.time))
            # if self.keep_axioms:
            #     self.kb.axioms.append(add_time_stamp(action, self.time))

            self.time += 1 # advance the agent's time
            return action



        def update_unvisited_locations():
            """ This cheats in the sense of not being fully based on inference,
            but is far more efficient
            (1) relies on global record of unvisited states
            (2) only checks for visiting based on the current time step
                (rather than from the beginning of time)
            Could make even more efficient by making no inference at all, by
            keeping track of current belief location and just subtracting that
            from self.unvisited.  But what's the fun in that ??! """
            # if self.verbose:
            print("     HWA.update_unvisited_locations()")

            for (x,y) in self.unvisited:
                query = Expr(state_loc_str(x,y,self.time))
                vis_query_result = self.KB.ask(query)
                if vis_query_result:
                    self.unvisited.remove((x,y))
            # if self.verbose:
            #     end_time = clock()
            #     print "          >>> time elapsed while making unvisited locations" \
            #           + " queries: {0}".format(end_time-start_time)
            #     for vis_loc in self.unvisited:
            #         display_env.add_thing(Proposition(expr('~Vis'),'F'),(x,y))
            return self.unvisited


        def find_OK_locations():
            # if self.verbose:
            print("     HWA.find_OK_locations()")

            # wumpus_alive_query()

            # display_env = WumpusEnvironment(self.width, self.height)
            # start_time = clock()
            safe_loc = []
            for x in range(1,self.mapsize+1):
                for y in range(1,self.mapsize+1):
                    query = Expr(state_OK_str(x,y,self.time))
                    result = self.KB.ask(query)
                    if result:
                        safe_loc.append((x,y))
                    # if self.verbose:
                    #     if result == None:
                    #         display_env.add_thing(Proposition(query,'?'),(x,y))
                    #     else:
                    #         display_env.add_thing(Proposition(query,result),(x,y))
            # if self.verbose:
            #     end_time = clock()
            #     print "          >>> time elapsed while making OK location queries:" \
            #           + " {0}".format(end_time-start_time)
            #     print display_env.to_string(self.time, title="Find OK locations queries")
            return safe_loc


        def make_percept_sentence(percept, t):
            percepts_list = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']
            axiom = []
            check = [False, False, False, False, False]
            for p in percept:
                p_name = p.__class__.__name__
                for i in range(len(percepts_list)):
                    if p_name == percepts_list[i]:
                        check[i] = True
            for i in range(len(check)):
                if check[i]:
                    str_axiom = percepts_list[i] + str(t)
                    axiom.append(Expr(str_axiom))
                else:
                    str_axiom = percepts_list[i] + str(t)
                    axiom.append(~Expr(str_axiom))

            conj = conj_axiom_list(axiom)
            return conj


        def find_possible_wumpus_locations():
            # if self.verbose:
            print("     HWA.find_possible_wumpus_locations()")
                # display_env = WumpusEnvironment(self.width, self.height)
                # start_time = clock()
            possible_wumpus_loc = []
            for x in range(1,self.mapsize+1):
                for y in range(1,self.mapsize+1):
                    query = Expr(wumpus_str(x,y))
                    result = self.KB.ask(query)
                    if result != False:
                        possible_wumpus_loc.append((x,y))
                    # if self.verbose:
                    #     if result == None:
                    #         display_env.add_thing(Proposition(query,'?'),(x,y))
                    #     else:
                    #         display_env.add_thing(Proposition(query,result),(x,y))
            # if self.verbose:
            #     end_time = clock()
            #     print "          >>> time elapsed while making possible wumpus location queries:" \
            #           + " {0}".format(end_time-start_time)
            #     print display_env.to_string(self.time, title="Possible Wumpus Location queries")
            #     print "Possible locations: {0}".format(possible_wumpus_loc)
            return possible_wumpus_loc


        def find_not_unsafe_locations():
            # if self.verbose:
            print("   HWA.find_not_unsafe_locations()")
            # display_env = WumpusEnvironment(self.width, self.height)
            # start_time = clock()
            not_unsafe = []
            for x in range(1,self.mapsize + 1):
                for y in range(1,self.mapsize + 1):
                    query = Expr(state_OK_str(x,y,self.time))
                    result = self.KB.ask(query)
                    if result != False:
                        not_unsafe.append((x,y))
                    # if self.verbose:
                    #     if result != False:
                    #         if result == None:
                    #             display_env.add_thing(Proposition(query,'?'),(x,y))
                    #         else:
                    #             display_env.add_thing(Proposition(query,'T'),(x,y))
            # if self.verbose:
            #     end_time = clock()
            #     print "          >>> time elapsed while making not unsafe location queries:" \
            #           + " {0}".format(end_time-start_time)
            #     print display_env.to_string(self.time, title="Not Unsafe Location queries")
                # print "Not Unsafe locations: {0}".format(not_unsafe)
            return not_unsafe

        def infer_and_set_belief_location():
            # if self.verbose: start_time = clock()
            self.belief_location = None
            for x in range(1,self.mapsize+1):
                for y in range(1,self.mapsize + 1):
                    query = Expr('L{0}_{1}_{2}'.format(x, y, self.time))
                    result = self.KB.ask(query)
                    if result:
                        parts = str(query).split('_')
                        self.belief_location =  (int(parts[0][1:]), int(parts[1]))
            if not self.belief_location:
                # if self.verbose:
                print ("        --> FAILED TO INFER belief location, assuming at initial location (entrance).")
                self.belief_location = self.initial_location



        def infer_and_set_belief_heading():
            self.belief_heading = None
            # if self.verbose: start_time = clock()
            if self.KB.ask(Expr(state_Facing_north_str(self.time))):
                self.belief_heading = heading_str_to_num['North']
            elif self.KB.ask(Expr(state_Facing_west_str(self.time))):
                self.belief_heading = heading_str_to_num['West']
            elif self.KB.ask(Expr(state_Facing_south_str(self.time))):
                self.belief_heading = heading_str_to_num['South']
            elif self.KB.ask(Expr(state_Facing_east_str(self.time))):
                self.belief_heading = heading_str_to_num['East']

            else:
                print ("        --> FAILED TO INFER belief heading, assuming initial heading.")
                self.belief_heading = self.initial_heading


        def add_temporal_axioms():
            # if self.verbose:
            print( "       HWA.add_temporal_axioms()")
            axioms = GenerateSentence.genOKSquareLogic(self.time,self.mapsize)       # OKtx,y ⇔ ¬Px,y ∧ ¬(Wx,y ∧ WumpusAlivet) .
            if True:
                ax_so_far = len(axioms)
                print ("           number of location_OK axioms:         {0}".format(ax_so_far))
            axioms += GenerateSentence.genPerceptToKnowLedgeSentence(self.time,self.mapsize)     # Ltx,y ⇒ (Breezet ⇔ Bx,y)  Ltx,y ⇒ (Stencht ⇔ Sx,y) .
            # axioms += generate_stench_percept_and_location_axioms(self.time,1,self.width,1,self.height)
            # if self.verbose:
            #     new_ax_so_far = len(axioms)
            #     perc_to_loc = new_ax_so_far - ax_so_far
            #     print "           number of percept_to_loc axioms:      {0}".format(perc_to_loc)
            #     ax_so_far = new_ax_so_far
            axioms += GenerateSentence.generate_at_location_ssa(self.time,self.belief_location[0],self.belief_location[1],
                                              self.mapsize,
                                            heading_str(self.belief_heading))
            # if self.verbose:
            #     new_ax_so_far = len(axioms)
            #     local_loc_at = new_ax_so_far - ax_so_far
            #     print "           number of at_location ssa axioms:     {0}".format(local_loc_at)
            #     ax_so_far = new_ax_so_far
            axioms += GenerateSentence.generate_non_location_ssa(self.time)
            # if self.verbose:
            #     new_ax_so_far = len(axioms)
            #     remaining_ssa_at_time = new_ax_so_far - ax_so_far
            #     print "           number of non-location ssa axioms:    {0}".format(remaining_ssa_at_time)
            #     ax_so_far = new_ax_so_far
            axioms += GenerateSentence.generate_mutually_exclusive_axioms(self.time)
            # if self.verbose:
            #     new_ax_so_far = len(axioms)
            #     mutually_exclusive = new_ax_so_far - ax_so_far
            #     print ("           number of mutually_exclusive axioms:  {0}".format(mutually_exclusive))
            #
            # if self.verbose: print ("       Total number of axioms being added:  {0}".format(len(axioms)))

            for sentence in axioms:
                self.KB.tell(sentence)
            # if self.keep_axioms:
            #      self.kb.axioms += axioms

        return program





def conj_axiom_list(axiom_list):
    r = axiom_list[0]
    for a in axiom_list:
        if a is not r:
            r = r & a
    return  r

def disj_axiom_list(axiom_list):
    r = axiom_list[0]
    for a in axiom_list:
        if a is not r:
            r = r | a
    return  r




def heading_str(heading):
        """Overkill!  But once I got started, I couldn't stop making it safe...
        Ensure that heading is a valid heading 'string' (for the logic side),
        as opposed to the integer form for the WumpusEnvironment side.
        """
        if isinstance(heading,int):
            if 0 <= heading <= 3:
                return heading_num_to_str[heading]
            else:
                print("Not a valid heading int (0 <= heading <= 3), got: {0}".format(heading))
                sys.exit(0)
        elif isinstance(heading,str):
            headings = heading_str_to_num.keys()
            if heading in headings:
                return heading
            else:
                print("Not a valid heading str (one of {0}), got: {1}".format(headings,heading))
                sys.exit(0)
        else:
            print("Not a valid heading:", heading)
            sys.exit(0)








def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)


def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)


def state_Facing_north_str(t):
    "Facing North at time <t>"
    return 'FacingNorth{0}'.format(t)
def state_Facing_east_str(t):
    "Facing East at time <t>"
    return 'FacingEast{0}'.format(t)
def state_Facing_south_str(t):
    "Facing South at time <t>"
    return 'FacingSouth{0}'.format(t)
def state_Facing_west_str(t):
    "Facing West at time <t>"
    return 'FacingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)


def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')



def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)
# ________________________________________________________________________

