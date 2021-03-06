from helpers import *
from mobject import Mobject, Group
from simple_animations import MaintainPositionRelativeTo
import copy

class ContinualAnimation(object):
    CONFIG = {
        "start_up_time" : 1,
        "wind_down_time" : 1,
        "end_time" : np.inf,
    }
    def __init__(self, mobject, **kwargs):
        mobject = instantiate(mobject)
        assert(isinstance(mobject, Mobject))
        digest_config(self, kwargs, locals())
        self.internal_time = 0
        self.external_time = 0
        self.setup()
        self.update(0)

    def setup(self):
        #To implement in subclass
        pass

    def begin_wind_down(self, wind_down_time = None):
        if wind_down_time is not None:
            self.wind_down_time = wind_down_time
        self.end_time = self.external_time + self.wind_down_time

    def update(self, dt):
        #TODO, currenty time moves slower for a
        #continual animation during its start up
        #to help smooth things out.  Does this have
        #unwanted consequences?
        self.external_time += dt
        if self.external_time < self.start_up_time:
            dt *= float(self.external_time)/self.start_up_time
        elif self.external_time > self.end_time - self.wind_down_time:
            dt *= np.clip(
                float(self.end_time - self.external_time)/self.wind_down_time,
                0, 1
            )
        self.internal_time += dt
        self.update_mobject(dt)

    def update_mobject(self, dt):
        #To implement in subclass
        pass

    def copy(self):
        return copy.deepcopy(self)

class ContinualAnimationGroup(ContinualAnimation):
    CONFIG = {
        "start_up_time" : 0,
        "wind_down_time" : 0,
    }
    def __init__(self, *continual_animations, **kwargs):
        digest_config(self, kwargs, locals())
        self.group = Group(*[ca.mobject for ca in continual_animations])
        ContinualAnimation.__init__(self, self.group, **kwargs)

    def update_mobject(self, dt):
        for continual_animation in self.continual_animations:
            continual_animation.update(dt)

class AmbientRotation(ContinualAnimation):
    CONFIG = {
        "axis" : OUT,
        "rate" : np.pi/12, #Radians per second
    }

    def update_mobject(self, dt):
        self.mobject.rotate(dt*self.rate, axis = self.axis)

class AmbientMovement(ContinualAnimation):
    CONFIG = {
        "direction" : RIGHT,
        "rate" : 0.05, #Units per second
    }

    def update_mobject(self, dt):
        self.mobject.shift(dt*self.rate*self.direction)

class ContinualUpdateFromFunc(ContinualAnimation):
    def __init__(self, mobject, func, **kwargs):
        self.func = func
        ContinualAnimation.__init__(self, mobject, **kwargs)

    def update_mobject(self, dt):
        self.func(self.mobject)

class ContinualMaintainPositionRelativeTo(ContinualAnimation):
    def __init__(self, mobject, tracked_mobject, **kwargs):
        self.anim = MaintainPositionRelativeTo(mobject, tracked_mobject, **kwargs)
        ContinualAnimation.__init__(self, mobject, **kwargs)

    def update_mobject(self, dt):
        self.anim.update(0)













