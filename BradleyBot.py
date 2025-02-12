from tools import  *
from objects import *
from routines import *

def distance_in_xz_plane(vector3):
    # Assuming vector3 has x, y, and z components
    x = vector3[0]
    z = vector3[2]
    return math.sqrt(x**2 + z**2)

class ExampleBot(GoslingAgent):

    def run(agent):
        if len(agent.stack) < 1:
            defaultThrottle(agent, 2400)
            if agent.me.boost < 25 and not agent.me.supersonic:
               all_boosts = agent.boosts
               large_boosts = [boost for boost in all_boosts if boost.large and boost.active]
               nearest_boost = min(large_boosts, key=lambda boost: ((boost.location - agent.me.location).magnitude()))
               agent.push(goto_boost(boost=nearest_boost))
            else:
                relative_target = agent.foes[0].location - agent.me.location
                local_target = agent.me.local(relative_target)

                steer_angle = defaultPD(agent, local_target)[2]
                if steer_angle > 5:
                    defaultThrottle(agent, 1400)
                if distance_in_xz_plane(agent.foes[0].location - agent.me.location) < 500 and steer_angle < 6.5:
                    if agent.foes[0].jumped:
                        agent.controller.jump = True
                    if agent.foes[0].doublejumped:
                        agent.controller.jump = True