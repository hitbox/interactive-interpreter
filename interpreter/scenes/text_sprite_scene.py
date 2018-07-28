import textwrap
import pygame as pg

from ..font import Font
from ..sprites import TextSprite
from .base import BaseScene

_text = textwrap.dedent("""
    Hello and welcome to the text sprite demo!

    Dragging the circle handles of the box will resize the box and the text inside should wrap.

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque aliquam interdum est nec finibus. Duis mattis in nisi eget dapibus. Maecenas a hendrerit augue. Nunc vitae scelerisque eros. Sed et dapibus magna, eget dignissim felis. Proin lobortis at est non malesuada. Fusce vehicula feugiat lectus volutpat fermentum. Donec auctor risus leo, mattis mollis orci tincidunt sed. Sed finibus sem risus, eget pretium ex fringilla vitae. Proin varius, nisl vel efficitur aliquam, orci ligula molestie nulla, eu rutrum dui lectus in sem. Suspendisse consequat quam id suscipit commodo. Nam aliquam, purus vitae iaculis sollicitudin, quam justo iaculis arcu, vel auctor lorem risus eget nisl. Nulla quis efficitur urna, non lacinia justo. Nunc accumsan leo in sem dapibus lobortis.

    Ut vehicula felis et est finibus vehicula. In venenatis a urna at elementum. Donec leo leo, cursus ut mi sed, tristique consequat est. Phasellus ornare massa sit amet quam hendrerit fringilla. Quisque non dapibus felis. Proin in aliquet purus, id euismod dolor. Suspendisse lacus enim, imperdiet at viverra viverra, lacinia quis libero.

    Nulla ultrices metus sem, ut sollicitudin ipsum iaculis sed. Etiam accumsan urna sit amet massa dignissim congue. Aliquam ac mauris mattis, rutrum elit ut, dapibus diam. Nullam a placerat turpis. Morbi tincidunt enim mi, vitae suscipit nisl dapibus eget. Suspendisse pretium tempor dignissim. Nam dignissim purus a maximus laoreet. Vestibulum erat urna, pellentesque ac nisi id, pellentesque tempus lacus. Fusce at convallis sapien. Nunc gravida tellus ullamcorper imperdiet lobortis.

    In lacus felis, rutrum ac dignissim quis, varius at tortor. Mauris luctus quam ultrices enim pharetra auctor. Quisque molestie ex vitae nisl venenatis, ac sodales eros dignissim. Curabitur euismod turpis quam, id mattis enim accumsan eu. Vivamus mattis turpis ligula, nec lobortis ipsum porta et. Nullam magna justo, ullamcorper vitae neque sit amet, facilisis tristique sem. Vestibulum rutrum ex ac semper ornare. Cras ornare rhoncus felis, at tincidunt turpis pretium at. Vivamus maximus sollicitudin justo ac feugiat. Etiam auctor id felis quis feugiat. Sed tempor commodo faucibus. Sed sed urna in nisl egestas finibus. Donec vitae pulvinar ante. Sed ut leo viverra, ullamcorper est sed, volutpat eros. Sed rutrum, tortor at efficitur feugiat, nunc quam tincidunt sem, quis convallis velit nisl a nisi.

    Donec maximus tincidunt mauris, sit amet gravida nisi varius ut. Sed risus magna, semper eget odio id, pharetra faucibus sapien. Nam ac accumsan felis. Aliquam erat volutpat. Vestibulum non mi vitae enim efficitur ornare eu vitae elit. Proin augue tellus, aliquam ac gravida vitae, lacinia at massa. Pellentesque eleifend vehicula arcu ac molestie.
    """
)

class TextSpriteScene(BaseScene):

    def __init__(self, inside):
        super().__init__()
        self.textsprite = TextSprite(
            Font(),
            _text,
            inside,
        )
        self.add(self.textsprite)

        for handle in inside.handles.values():
            self.add(handle)
