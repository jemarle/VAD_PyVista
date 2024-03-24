# Autor: Jesús Martínez Leal
# Fecha de última edición: 24/03/2023
# Descripción: Este script muestra un conejito en 3D con 9 subplots, cada uno con una modificación diferente del conejito



# Importación de librerías necesarias

import pyvista as pv
from pyvista import examples

#bunny = examples.download_bunny_coarse() ejemplo menos pesado
bunny = pv.read('bunny.stl')

#cpos = [
#    (0.3914, 0.4542, 0.7670),
#    (0.0243, 0.0336, -0.0222),
#    (-0.2148, 0.8998, -0.3796)] descomentar esto para usar el menos pesado

# Crear una copia del conejito para modificarlo sin afectar al original

bunnymod = bunny.copy()

bunny['altura'] = bunny.points[:, 2]


plotter = pv.Plotter(shape = (3, 3)) # Definimos la forma en subplots



# Subplot 00 (normal)

plotter.subplot(0, 0)
plotter.add_mesh(bunny)

# Subplot 10 (plano cortante)

plotter.subplot(1, 0)
plotter.add_mesh_clip_plane(bunnymod)  

# Subplot 01 (decimate)

def update_decimated_mesh(value):
    global decimatedBunnyActor
    decimated = bunnymod.extract_geometry().triangulate().decimate(target_reduction=value)
    plotter.subplot(0, 1)
    plotter.remove_actor(decimatedBunnyActor)
    decimatedBunnyActor = plotter.add_mesh(decimated)

plotter.subplot(0, 1)
decimatedBunnyActor = plotter.add_mesh(bunnymod.extract_geometry().triangulate())
target_reduction_slider = plotter.add_slider_widget(update_decimated_mesh, value=0.5, rng=[0.1, 0.99], title = "Reducción con el decimate")

# Subplot 11 (smoothing)

def update_smooth_mesh(value):
    global smoothedBunnyActor
    smoothed = bunnymod.extract_geometry().triangulate().smooth(n_iter=int(value), relaxation_factor=0.1)
    plotter.subplot(1, 1)
    plotter.remove_actor(smoothedBunnyActor)
    smoothedBunnyActor = plotter.add_mesh(smoothed)

plotter.subplot(1, 1)
smoothedBunnyActor = plotter.add_mesh(bunnymod.extract_geometry().triangulate())
smooth_iterations_slider = plotter.add_slider_widget(update_smooth_mesh, value=100, rng=[100, 750], title = "Parámetro de suavizado")
 
# Subplot 20 (translate)

def update_translate_bunny(value):
    global bunny_translation_actor
    bunny_translation_actor.SetPosition(value, 0, 0)

plotter.subplot(2, 0)
bunny_translation_actor = plotter.add_mesh(bunnymod.extract_geometry().triangulate())

translate_slider = plotter.add_slider_widget(update_translate_bunny, value=0, rng=[-55, 55], title="Translate X")


# Subplot 21 (visibilidad)

def toggle_bunny_vis(flag):
    bunny_actor.SetVisibility(flag)

plotter.subplot(2, 1)
bunny_actor = plotter.add_mesh(bunnymod)
bunny_visibility_checkbox = plotter.add_checkbox_button_widget(toggle_bunny_vis, value=True, color_on = 'green')


# subplot 02 (más control en cortes)

plotter.subplot(0, 2)
plotter.add_mesh_clip_box(bunnymod) 

# subplot 12 (cambio color conejito)

plotter.subplot(1, 2)
plotter.add_mesh(bunnymod, color = 'yellow')

# subplot 22 (algunas opciones más de plotter.add_mesh())

plotter.subplot(2,2)
plotter.add_mesh(bunnymod, style = 'wireframe', line_width = 5, point_size = 0.1)
plotter.add_text("Conejo cableado")

plotter.link_views() # unir vistas de todas.

plotter.show()
#plotter.show(cpos = cpos) descomentar esto con el menos pesado
