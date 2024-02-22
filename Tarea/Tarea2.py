import pyvista as pv

class SetVisibilityCallback:
    """Helper callback to keep a reference to the actor being modified."""

    def __init__(self, actor):
        self.actor = actor

    def __call__(self, state):
        self.actor.SetVisibility(state)

# Función para cargar los archivos y generar los botones de checkbox para un paciente
def cargar_paciente(paciente, idx):
    # Cargar los archivos
    BZS = pv.read(f'./{paciente}/Border Zone Surface.vtk')
    CS = pv.read(f'./{paciente}/Core Surface.vtk')
    vT = pv.read(f'./{paciente}/ventricle_Tagged.vtk')

    # Agregar las mallas al subplot correspondiente
    
    
    plotter.subplot(0, idx)
    actores = [plotter.add_mesh(mesh, color=color, opacity=0.5) for mesh, color in zip([BZS, CS, vT], ["blue", "red", "green"])]
    plotter.add_text(f"Paciente {paciente}", position='upper_left')

    # Agregar botones de checkbox para controlar la visibilidad de las mallas
    size = 20
    position_y = 12

    for actor, color in zip(actores, ["blue", "red", "green"]):
        callback = SetVisibilityCallback(actor)
        plotter.add_checkbox_button_widget(
            callback,
            value=True,
            position=(5.0, position_y),
            size=size,
            border_size=1,
            color_on=color,
            color_off='grey',
            background_color='grey',
        )
        position_y += size + (size // 10)
    
    
    
    
    
    plotter.subplot(1, idx)
    
    var = ["DistEndoToEpi", "DistApexToBase", "Cell_type", "endo_Norm", "epi_Norm"]
    
    # Crear múltiples copias de la malla vT
    vT_copies = [vT.copy() for _ in var]
    cmap_list = ["coolwarm" for _ in var]
    
    # Agregar cada copia al plotter con los datos escalares correspondientes
    actores2 = [plotter.add_mesh(vT_copy, scalars=vT_copy[var_i], cmap=cmap)
    for vT_copy, var_i, cmap in zip(vT_copies, var, cmap_list)]   
    
    
    # Agregar botones de checkbox para controlar la visibilidad de las mallas
    size = 20
    position_y = 12

    for actor, color in zip(actores2, ["blue", "red", "green", "orange", "black"]):
        callback = SetVisibilityCallback(actor)
        plotter.add_checkbox_button_widget(
            callback,
            value=True,
            position=(5.0, position_y),
            size=size,
            border_size=1,
            color_on=color,
            color_off='grey',
            background_color='grey',
        )
        position_y += size + (size // 10)
        
    def reverse_list(lst):
        return lst[::-1]

    # Colocar los colores en el orden inverso
    text_colors = reverse_list(["blue", "red", "green", "orange", "black"])

    # Iterar sobre cada variable en var
    for index, (variable, color) in enumerate(zip(var, text_colors)):
        # Concatenar el texto con saltos de línea adicionales
        text = "\n \n" * index + variable
        # Agregar el texto con la posición 'upper_left' y el color correspondiente
        plotter.add_text(text, position='upper_left', font_size=13, color=color)



    plotter.subplot(2, idx)
    
    centers = vT.points
    
    directions = vT["fibers_OR"]
    mag = 1
    
    # Agregar cada copia al plotter con los datos escalares correspondientes
    actores3 = [plotter.add_arrows(centers, directions, mag = mag, color = "black")]
    
    
    # Agregar botones de checkbox para controlar la visibilidad de las mallas
    size = 20
    position_y = 12

    for actor, color in zip(actores3, ["blue"]):
        callback = SetVisibilityCallback(actor)
        plotter.add_checkbox_button_widget(
            callback,
            value=True,
            position=(5.0, position_y),
            size=size,
            border_size=1,
            color_on=color,
            color_off='grey',
            background_color='grey',
        )
        position_y += size + (size // 10)
        


    
# Crear el plotter
plotter = pv.Plotter(shape=(3, 3))

# Cargar los pacientes y sus respectivas mallas
for idx, paciente in enumerate(["p2", "p5", "p36"], start = 0):
    print(idx)
    print(paciente)
    cargar_paciente(paciente, idx)

# Visualizar
plotter.show()