

# ./workbench.py

# Importa el módulo 'os' para trabajar con rutas del sistema de archivos.
import os

# Importa los módulos de FreeCAD. `FreeCAD` para la funcionalidad principal (no-GUI) y `FreeCADGui` para la interfaz gráfica.
import FreeCAD, FreeCADGui

# Importa las funciones de registro de eventos desde un módulo personalizado 'Utils.logger'.
# Estas funciones permiten un registro de información y errores estandarizado para el entorno.
from Utils.logger import log_info, log_error

# Importa la función para registrar todos los comandos y la lista de comandos registrados.
# Estos se encuentran en el paquete `Commands`, que presumiblemente escanea un directorio de comandos.
from Commands.__init__ import register_all_commands, REGISTERED_COMMANDS

# Define la clase `ElectricalWorkbenchClass` que hereda de `FreeCADGui.Workbench`.
# Esta herencia es obligatoria para que FreeCAD la reconozca como un entorno de trabajo.
class ElectricalWorkbenchClass(FreeCADGui.Workbench):

    def __init__(self):
        """
        Constructor de la clase. Se ejecuta cuando FreeCAD carga la definición del entorno de trabajo.
        Aquí se configuran las propiedades estáticas de la clase, como el nombre, la descripción y el ícono.
        """
        # Establece el nombre que se mostrará en el menú desplegable de entornos de trabajo.
        self.__class__.MenuText = "Electrical"
        
        # Proporciona una descripción que se mostrará como una pista de herramienta (tooltip).
        self.__class__.ToolTip = "Electrical Workbench"
        
        # Establece el ícono del entorno de trabajo. Hay varias opciones:
        #
        # Opcional (comentado): Cargar un ícono SVG desde la ruta del proyecto.
        # Esto sería el método preferido para íconos de alta resolución.
        # self.__class__.Icon = "resources/icons/EW_icon.svg"
        #
        # Opcional (comentado): Método más robusto para construir la ruta del ícono,
        # garantizando que funcione en diferentes sistemas operativos.
        # self.__class__.Icon = os.path.join(os.path.dirname(__file__), "resources", "icons", "EW_icon.svg")    
        
        # La implementación actual utiliza un ícono incrustado en formato XPM.
        # XPM es un formato de imagen basado en texto, útil para imágenes pequeñas
        # y asegura que el ícono esté siempre disponible sin depender de archivos externos.
        self.__class__.Icon = """
/* XPM */
static char * ew_letters_xpm[] = {
"16 16 2 1",        # Define la resolución (16x16), colores (2) y hot-spots (1).
" 	c None",       # Define el color de fondo como transparente.
".	c #000000",    # Define el color del punto como negro.
"                ",
"                ",
"  ...........   ",
"  ...........   ",
"  ...     ...   ",
"  ...     ...   ",
"  ...     ...   ",
"  ...     ...   ",
"  ...     ...   ",
"  ... ... ...   ",
"  ... ... ...   ",
"  ... ... ...   ",
"  ... ... ...   ",
"  ...........   ",
"  ...........   ",
"                "};
"""
        # Utiliza la función de registro para indicar que el entorno de trabajo se está inicializando.
        log_info(".", "workbench.py", "Inicializando Electrical Workbench")
        
    def Initialize(self):
        """
        Se llama cuando el entorno de trabajo se activa por primera vez en la sesión de FreeCAD.
        Es aquí donde se registran los comandos y se construyen los menús y barras de herramientas.
        """
        try:
            # Llama a la función `register_all_commands` para registrar dinámicamente todos los comandos.
            # Esta función probablemente escanea un directorio de comandos (`./Commands`).
            registered_commands = register_all_commands()
        except Exception as e:
            # En caso de error durante el registro, lo notifica al usuario y detiene la inicialización.
            log_error(".", "workbench.py", f"Error registrando comandos: {e}")
            return

        if not registered_commands:
            # Si no se encontró ningún comando para registrar, emite una advertencia.
            log_error(".", "workbench.py", "No se pudo registrar los comandos. Por favor, revisa ./Commands/*")
            return

        # Crea un menú llamado "Electrical Tools" y le agrega los comandos registrados dinámicamente.
        self.appendMenu("Electrical Tools", registered_commands)
        
        # Crea una barra de herramientas llamada "Electrical Tools" y le agrega los mismos comandos.
        self.appendToolbar("Electrical Tools", registered_commands)

        # Informa que los comandos se han registrado correctamente, mostrando cuáles son.
        log_info(".", "workbench.py", f"Comandos registrados: [{' | '.join(registered_commands)}]")

    def GetClassName(self):
        """
        Este método devuelve el nombre de la clase C++ subyacente que maneja el entorno de trabajo.
        Para los entornos de trabajo creados completamente en Python, se debe devolver "Gui::PythonWorkbench".
        """
        return "Gui::PythonWorkbench"