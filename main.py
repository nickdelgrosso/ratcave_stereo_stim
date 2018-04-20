import pyglet
import pyglet.gl as gl
from pyglet.window import key
import ratcave as rc
import numpy as np

window = pyglet.window.Window(resizable=True)
max_x = 1

bg_data = np.ones(shape=(2000, 3), dtype=np.float32)
bg_data[:, :2] = np.random.uniform(-max_x, max_x, (len(bg_data), 2))

bg_mesh = rc.Mesh.from_incomplete_data(bg_data, position=(0, 0, -.5))
bg_mesh.uniforms['diffuse'] = 1., 1, 1
# bg_mesh.scale.xyz = 3.
bg_mesh.drawmode = rc.POINTS
bg_mesh.dynamic = True
bg_mesh.point_size = 4

fg_mesh = rc.Mesh.from_incomplete_data(bg_data, position=(0, 0, -2.5))
fg_mesh.uniforms['diffuse'] = 1., 1, 1
# bg_mesh.scale.xyz = 3.
fg_mesh.drawmode = rc.POINTS
fg_mesh.dynamic = True
fg_mesh.point_size = 4
fg_mesh.scale.xyz = 5, 5, 1.

blocker1 = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
blocker1.parent = bg_mesh
blocker1.uniforms['diffuse'] = (0.,) * 3
blocker1.uniforms['flat_shading'] = True
blocker1.position.xyz = -.66, 0, -.001
blocker1.scale.xyz = .6, .9, 1.
bg_mesh.update()

blocker2 = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane')
blocker2.parent = bg_mesh
blocker2.uniforms['diffuse'] = (0.,) * 3
blocker2.uniforms['flat_shading'] = True
blocker2.position.xyz = .66, 0, -.001
blocker2.scale.xyz = .6, .9, 1.
bg_mesh.update()

# cam = rc.Camera(projection=rc.OrthoProjection())
cam = rc.default_camera

# import ipdb; ipdb.set_trace()

fps_display = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():


    window.clear()
    with rc.default_shader:

        cam.position.x = .02
        with cam:
            gl.glColorMask(True, False, False, True)
            fg_mesh.draw()
            blocker1.draw()
            blocker2.draw()
            bg_mesh.draw()



        cam.position.x = -.02
        with cam:
            gl.glColorMask(False, False, True, True)
            fg_mesh.draw()
            blocker1.draw()
            blocker2.draw()
            bg_mesh.draw()

    gl.glColorMask(True, True, True, True)
    fps_display.draw()


tt = 0.
pos = 0.
off = 2.5
off2 = 1.
def randomize_dots(dt):
    global tt
    tt += dt


    # new_verts = np.hstack((verts[:, :2] np.zeros((len(bg_data), 1))))
    pos = np.sin(tt) / 2.9
    bg_mesh.position.x = pos
    blocker1.update()
    blocker2.update()
    fg_mesh.update()
    width = .05

    verts = bg_mesh.vertices
    new_verts = np.hstack((np.random.uniform(-max_x, max_x, (len(bg_data), 2)) / 2., np.zeros((len(bg_data), 1)))) * 1.5



    mask = np.all(((0 - width) < new_verts[:, 0], new_verts[:, 0] < (0 + width)), axis=0)
    new_verts[mask, 2] = -200.5
    # new_verts[mask, :2] *= [off, 2.5]
    # new_verts[mask, 0] -= off * pos
    # new_verts[mask, 0] *= off2
    # new_verts[mask, 0] += off * pos

    fg_mesh.vertices[:, :2] = new_verts[:, :2]

    # new_verts[mask, :2] -= .02
    verts[:] = new_verts
pyglet.clock.schedule(randomize_dots)


@window.event
def on_key_release(val, mod):
    global off
    global off2
    shift = .02
    if val == key.UP:
        off += shift
    elif val == key.DOWN:
        off -= shift
    elif val == key.LEFT:
        off2 -= shift
    elif val == key.RIGHT:
        off2 += shift
    print(off, off2)

pyglet.clock.schedule(lambda dt: dt)
pyglet.app.run()
