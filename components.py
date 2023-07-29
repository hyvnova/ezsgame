from ezsgame import *
import time


# Creating a component
class HitBox(Component):
    def __init__(self) -> None:
        self.on_collision: Signal = Signal()
        self._signal_name = f"hitbox_collision_{id(self)}"

    def mount(self, object: Object):
        self.object = object

    def check_collision(self):
        for other in World.objects:
            if other != self.object:
                if is_colliding(self.object, other):
                    self.on_collision.trigger(other)

    def activate(self):
        World.on_update.add(self._signal_name, self.check_collision)

    def deactivate(self):
        World.on_update.remove(self._signal_name)

    def remove(self):
        pass


class Health(Component):
    def __init__(
        self,
        min_health=0,
        max_health=100,
        current_health=100,
        damage=10,
        invincibility_time=0.5,
    ):
        self.min = min_health
        self.max = max_health
        self.health = current_health
        self.damage = damage

        self.invincibility_time = invincibility_time
        self.elapsed_time = 0
        self._signal_name = f"health_hitbox_{id(self)}"

        self.on_hit: Signal = Signal()
        self.on_heal: Signal = Signal()

    def mount(self, object: Object):
        self.object = object

        # add a hitbox to the object if it doesn't have one
        if HitBox not in self.object.components:
            self.object.components.add(HitBox())

    def activate(self):
        # add a trigger to the hitbox
        self.object.components[HitBox].on_collision.add(self._signal_name, self.hit)

    def deactivate(self):
        self.object.components[HitBox].on_collision.remove(self._signal_name)

    def hit(self, other):
        time_now = time.time()
        if time_now - self.elapsed_time < self.invincibility_time:
            return

        self.health -= self.damage

        if self.health < self.min:
            self.health = self.min

        self.on_hit.trigger(other)

        # invincibility time
        self.elapsed_time = time.time()

    def heal(self, amount):
        self.health += amount
        if self.health > self.max:
            self.health = self.max

        self.on_heal.trigger(amount)

    def remove(self):
        pass


class HealthBar(Component):
    def __init__(
        self, health: Health = None, show_percentage=False, relative_to_object=False
    ):
        self.health_comp = health or Health()

        self.graphics = Group(
            fill=Rect(Pos("center", "bottom"), Size("70%", "5%"), color="red"),
            border=Rect(
                Pos("center", "bottom"), Size("70%", "5%"), color="white", stroke=2
            ),
        )

        if show_percentage:
            # percentage should be next to the health bar and health bar should be a little bit smaller
            for obj in self.graphics.values():
                obj.size.width *= 0.9

            self.graphics.add(
                text=Text(
                    f"{self.health_comp.health}/{self.health_comp.max}",
                    Pos(
                        self.graphics["fill"].pos.x
                        + self.graphics["fill"].size.width - 100,
                        self.graphics["fill"].pos.y - 10,
                    ),
                    20,
                    color="white",
                )
            )

        for obj in self.graphics.values():
            obj.size *= 0.7

        self.relative_to_object = relative_to_object
        self._signal_name = f"healthbar_draw_{id(self)}"


    def draw(self):
        # update the health bar
        if self.relative_to_object:
            for obj in self.graphics.values():
                obj.pos = self.object.pos.copy()
                obj.pos.y += self.object.size.height + 20


        self.graphics["fill"].size.width = (
            self.health_comp.health / self.health_comp.max
        ) * self.graphics["border"].size.width

        if "text" in self.graphics:
            self.graphics["text"].text.set(f"{self.health_comp.health}/{self.health_comp.max}")

        self.graphics.draw()

    def mount(self, object: Object):
        self.object = object
        self.object.components.add(self.health_comp, force=True)

        if self.relative_to_object:
            for obj in self.graphics.values():
                obj.size *= (self.object.size.width / 100, self.object.size.height / 100)

                # make position relative to the object
                obj.pos = self.object.pos.copy()
                obj.pos.y += self.object.size.height + 20


    def activate(self):
        self.object.on_draw.add(self._signal_name, self.draw)  # draw the health bar

    def deactivate(self):
        self.object.on_draw.remove(self._signal_name)


class Controllable(Component):
    """
    Implementes a `Controller` in the object
    """

    def __init__(self, controller: Controller = None) -> None:
        self.controller = controller or Controller()
        self._signal_name = f"controllable_{id(self)}"

    def mount(self, object: Object):
        self.object: Object = object

    def update_pos(self):
        self.object.pos += self.get_speed()

    def activate(self):
        self.controller = Controller()
        World.on_update.add(self._signal_name[0], self.update_pos)

    def deactivate(self):
        World.on_update.remove(self._signal_name[0])
        self.controller = None

    def remove(self):
        del self.controller

    def get_speed(self):
        if self.controller:
            return self.controller.get_speed("simple")
        else:
            return 0, 0
