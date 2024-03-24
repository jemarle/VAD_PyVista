# Autor: Jesús Martínez Leal
# Fecha de última edición: 24/03/2023
# Descripción: Script para visualizar las mallas de los pacientes y las variables seleccionadas por el usuario




# Importación de librerías necesarias

import pyvista as pv

# Función de callback para controlar la visibilidad de las mallas

class SetVisibilityCallback:
    
    """Helper callback to keep a reference to the actor being modified."""

    # Constructor de la clase
    
    def __init__(self, actor):
        self.actor = actor

    # Método para cambiar la visibilidad de la malla

    def __call__(self, state):
        self.actor.SetVisibility(state)


    
# Función de carga de pacientes y visualización de mallas

def cargar_paciente(paciente, idx, var1, var2):
    
    # Cargar los archivos
    
    path_patient = f'./Pacientes/{paciente}/'
    
    BZS = pv.read(path_patient + 'Border Zone Surface.vtk')
    CS = pv.read(path_patient + 'Core Surface.vtk')
    vT = pv.read(path_patient + 'ventricle_Tagged.vtk')

    # visualizar los nombres presentes para los data arrays en vT
    # print(vT.array_names)

    # Visualización de partes de ventrículo en cada paciente:
    
    plotter.subplot(0, idx)
    actores = [plotter.add_mesh(mesh, color = color, opacity = 0.5) for mesh, color in zip([BZS, CS, vT], ["blue", "red", "green"])]
    plotter.add_text(f"Paciente {paciente}", position = 'upper_left')

    namesZones = ["BZS", "CS", "vT"]
    text_colors = ["blue", "red", "green"]
    
    # Agregar botones de checkbox para controlar la visibilidad de las mallas
    
    size = 20
    position_y = 12

    for actor, color in zip(actores, text_colors):
        callback = SetVisibilityCallback(actor)
        plotter.add_checkbox_button_widget(
            callback,
            value = True,
            position = (5.0, position_y),
            size = size,
            border_size = 1,
            color_on = color,
            color_off = 'grey',
            background_color = 'grey',
        )
        position_y += size + (size // 10)
        
    # Texto para identificar botones
    
    for index, (variable, color) in enumerate(zip(namesZones, text_colors)):

        text = "\n \n" * (index + 1) + variable

        plotter.add_text(text, position='upper_left', font_size = 13, color = color)   
        
    # Visualización de la primera variable seleccionada por el usuario
    
    plotter.subplot(1, idx)
    
    if var1 == "fibers_OR":
        # Campo vectorial (flechas)
        
        centers = vT.points
        directions = vT["fibers_OR"]
        mag = 1
        actor_var1 = plotter.add_arrows(centers, directions, mag = mag, color = "black")
    else:
        # Campo de escalares
        actor_var1 = plotter.add_mesh(vT, scalars = var1, cmap = "viridis")
        
    plotter.add_text(var1, position = 'upper_left', font_size = 13, color = 'blue')

    # Visualización de la segunda variable seleccionada por el usuario
    
    plotter.subplot(2, idx)
    
    if var2 == "fibers_OR":
        # Campo vectorial (flechas)
        
        centers = vT.points
        directions = vT["fibers_OR"]
        mag = 1
        actor_var2 = plotter.add_arrows(centers, directions, mag = mag, color = "black")
    else:
        # Campo de escalares
        actor_var2 = plotter.add_mesh(vT, scalars = var2, cmap = "plasma")
        
    plotter.add_text(var2, position = 'upper_left', font_size = 13, color = 'red')
    
    return (BZS, CS, vT), (actor_var1, actor_var2)


# Crear el plotter

plotter = pv.Plotter(shape=(3, 3))





# --------------------- MODIFICAR AQUÍ PARA EL USUARIO --------------------- #


# Seleccione las variables entre las siguientes:
# ['scalars', 'DistEndoToEpi', 'EndoToEpi', 'Cell_type', 'fibers_OR', 'endo_Norm', 'epi_Norm', 'vector_LAxis', 'tagApexBase', 'DistApexToBase', '17_AHA', '34_pacing']

var1 = "DistEndoToEpi"
var2 = "fibers_OR"



# Llamada a la función principal con los pacientes a visualizar

for idx, paciente in enumerate(["p2", "p5", "p36"], start = 0):
    cargar_paciente(paciente, idx, var1, var2)

# Mostrar el objeto plotter

plotter.show()
