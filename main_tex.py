import pyglet
import pyglet.gl as gl
from pyglet.window import key
import ratcave as rc
import numpy as np
from scipy.misc import imsave

eye_dist = .01
perc_white = .3
noise_resolution = 2048
stim_size = .02
moving_stimulus = True
noise_generation = True

window = pyglet.window.Window(resizable=True, vsync=False)
shader = rc.Shader.from_file('default.vert', 'noise.frag')

noise_fname = 'noise.jpg'
# noise_img = np.repeat((np.random.random(size=(noise_resolution,) * 2) < perc_white)[..., None].astype(np.uint8) * 255, 3, axis=2)
noise_img = np.repeat((np.random.gamma(3, 30, size=(noise_resolution,) * 2))[..., None].astype(np.uint8), 3, axis=2)

imsave(noise_fname, noise_img)
noise_tex = rc.Texture.from_image(noise_fname)


bg = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Cylinder', position=(0, 0, 0))
bg.uniforms['diffuse'] = 1., 1., 1.
bg.uniforms['flat_shading'] = True
bg.uniforms['tex_offset'] = np.random.random(size=2).astype(np.float32)
bg.textures.append(noise_tex)
edge_dist = bg.vertices[:, 0].max() * bg.scale.x
print(edge_dist)

fg = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane', position=(0, 0, 0))
# fg.vertices[:, 1] *= 100
fg.texcoords[:] *= stim_size * 1.75
fg.uniforms['diffuse'] = 1., 1., 1.
fg.textures.append(noise_tex)
fg.parent = bg
fg.scale.xyz = stim_size, stim_size, 1
fg.position.z = -.2
fg.update()


cam = rc.default_camera
cam.projection.fov_y = 35.


fps_display = pyglet.window.FPSDisplay(window)

focus_dist = -1.
@window.event
def on_key_release(sym, mod):
    global focus_dist
    if sym == key.UP:
        focus_dist += .05
    elif sym == key.DOWN:
        focus_dist -= .05
    print(focus_dist)


@window.event
def on_draw():
    window.clear()
    with shader:
        for x, mask in zip((-eye_dist / 2., eye_dist / 2.), [(True, False, False, True), (False, True, True, True)]):
            cam.position.x = x
            # cam.look_at(0, 0, np.mean([fg.position.z, -edge_dist]))
            # cam.look_at(0, 0, focus_dist)
            cam.look_at(0, 0, -0.35)
            # cam.look_at(0, 0, fg.position.z)
            # cam.look_at(0, 0, -edge_dist)
            with cam:
                gl.glColorMask(*mask)
                bg.draw()
                fg.draw()

    gl.glColorMask(True, True, True, True)
    fps_display.draw()


tt = 0.
def update_time(dt):
    global tt
    tt += dt
pyglet.clock.schedule(update_time)


def rotate_cylinder(dt, speed):
    # bg.rotation.y += speed * dt
    bg.rotation.y = np.sin(tt * speed) * 10
    fg.position.y = np.cos(tt * speed) * .04
    fg.update()
if moving_stimulus:
    pyglet.clock.schedule(rotate_cylinder, speed=3)



def randomize_noise(dt):
    bg.uniforms['tex_offset'] = np.random.random(size=2).astype(np.float32)
    fg.uniforms['tex_offset'] = np.random.random(size=2).astype(np.float32)
if noise_generation:
    pyglet.clock.schedule(randomize_noise)

pyglet.clock.schedule(lambda dt: dt)
pyglet.app.run()
