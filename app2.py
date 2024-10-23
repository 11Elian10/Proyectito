import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as tb
import configparser
import os

class HexViewerEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("View/Edit HEX")
        self.root.geometry("600x400")

        # Obtener ruta de AppData
        self.config_dir = os.path.join(os.getenv('APPDATA'), 'HexViewerEditor')
        os.makedirs(self.config_dir, exist_ok=True)  # Crear la carpeta si no existe
        self.config_path = os.path.join(self.config_dir, 'config.ini')

        # Cargar configuraciones desde config.ini
        self.config = configparser.ConfigParser()
        self.load_config()

        # Validar que el tema sea válido; si no, usar 'litera'
        available_themes = ['litera', 'darkly', 'cyborg', 'flatly', 'journal']
        theme = self.config['AppSettings'].get('theme', 'litera')
        if theme not in available_themes:
            theme = 'litera'
            self.config['AppSettings']['theme'] = 'litera'
            self.save_config()

        # Set theme from config
        self.style = tb.Style(theme)

        # Create menu (File Menu)
        self.create_menu()

        # Home screen elements
        self.create_home_screen()

    def load_config(self):
        """Cargar configuraciones desde el archivo config.ini o crear el archivo por defecto."""
        if not os.path.exists(self.config_path):
            # Si el archivo config.ini no existe, creamos uno por defecto
            self.config['AppSettings'] = {'theme': 'litera', 'last_opened_file': 'None'}
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
        else:
            self.config.read(self.config_path)

    def save_config(self):
        """Guardar las configuraciones en el archivo config.ini."""
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def create_menu(self):
        """Crear el menú desplegable File con las opciones."""
        menu_bar = tk.Menu(self.root)
        
        # Menú File
        file_menu = tk.Menu(menu_bar, tearoff=0)
        
        # Opción de 'Abrir' para abrir un archivo de texto y codificar
        file_menu.add_command(label="Abrir archivo de texto", command=self.open_file_and_convert)
        
        # Opción de 'Configuraciones' para abrir la ventana de ajustes
        file_menu.add_command(label="Configuraciones", command=self.open_settings)
        
        # Opción de 'Salir' para cerrar la aplicación
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Añadir el menú 'File' al menú principal
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Configurar la barra de menú en la ventana principal
        self.root.config(menu=menu_bar)

    def create_home_screen(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Nombre de la aplicación
        label = ttk.Label(self.root, text="View/Edit HEX", font=("Helvetica", 18))
        label.pack(pady=20)

        # Botón para iniciar la pantalla del editor
        start_button = ttk.Button(self.root, text="Iniciar", command=self.create_editor_screen)
        start_button.pack(pady=10)

        # Botón para abrir configuraciones
        settings_button = ttk.Button(self.root, text="Ajustes", command=self.open_settings)
        settings_button.pack(pady=10)

        # Botón para salir
        exit_button = ttk.Button(self.root, text="Salir", command=self.root.quit)
        exit_button.pack(pady=10)

    def create_editor_screen(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Etiqueta para la entrada de texto normal
        input_label = ttk.Label(self.root, text="Texto normal:")
        input_label.pack(pady=5)

        # Entrada de texto normal
        self.text_input = ttk.Entry(self.root, width=50)
        self.text_input.pack(pady=5)

        # Botón para convertir texto a hexadecimal
        convert_to_hex_button = ttk.Button(self.root, text="Convertir a Hexadecimal", command=self.convert_to_hex)
        convert_to_hex_button.pack(pady=10)

        # Etiqueta para mostrar el resultado en hexadecimal
        hex_label = ttk.Label(self.root, text="Texto hexadecimal:")
        hex_label.pack(pady=5)

        # Cuadro de texto para mostrar el resultado en hexadecimal
        self.hex_output = tk.Text(self.root, height=5, width=50, font=("Courier", 12))
        self.hex_output.pack(pady=10)

        # Etiqueta para la entrada de texto hexadecimal
        hex_input_label = ttk.Label(self.root, text="Texto hexadecimal (para convertir a texto):")
        hex_input_label.pack(pady=5)

        # Entrada de texto hexadecimal
        self.hex_input = ttk.Entry(self.root, width=50)
        self.hex_input.pack(pady=5)

        # Botón para convertir hexadecimal a texto
        convert_to_text_button = ttk.Button(self.root, text="Convertir a Texto", command=self.convert_to_text)
        convert_to_text_button.pack(pady=10)

        # Botón de "Volver" para regresar a la pantalla de inicio
        back_button = ttk.Button(self.root, text="Volver", command=self.create_home_screen)
        back_button.pack(pady=10)

    def convert_to_hex(self):
        input_text = self.text_input.get()
        if input_text:
            hex_output = input_text.encode('utf-8').hex()
            self.hex_output.delete(1.0, tk.END)  # Limpiar el cuadro de salida
            self.hex_output.insert(tk.END, hex_output)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa algún texto.")

    def convert_to_text(self):
        hex_input = self.hex_input.get()
        if hex_input:
            try:
                bytes_object = bytes.fromhex(hex_input)
                text_output = bytes_object.decode('utf-8')
                messagebox.showinfo("Texto", f"Texto convertido: {text_output}")
            except ValueError:
                messagebox.showwarning("Advertencia", "El texto hexadecimal no es válido.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa texto hexadecimal.")

    def open_file_and_convert(self):
        """Abrir archivo de texto y convertir su contenido a hexadecimal."""
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_input.delete(0, tk.END)
                self.text_input.insert(0, content)
                self.convert_to_hex()  # Convertir el contenido a hexadecimal automáticamente
            # Guardar la ruta del archivo en config.ini
            self.config['AppSettings']['last_opened_file'] = file_path
            self.save_config()

    def open_settings(self):
        """Abrir la ventana de configuraciones para cambiar el tema."""
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Botones para cambiar el tema
        light_button = ttk.Button(self.root, text="Tema Claro", command=self.set_light_theme)
        light_button.pack(pady=10)

        dark_button = ttk.Button(self.root, text="Tema Oscuro", command=self.set_dark_theme)
        dark_button.pack(pady=10)

        # Botón para volver a la pantalla de inicio
        back_button = ttk.Button(self.root, text="Volver", command=self.create_home_screen)
        back_button.pack(pady=10)

    def set_light_theme(self):
        """Cambiar al tema claro."""
        self.style.theme_use('litera')
        self.config['AppSettings']['theme'] = 'litera'
        self.save_config()

    def set_dark_theme(self):
        """Cambiar al tema oscuro."""
        self.style.theme_use('darkly')
        self.config['AppSettings']['theme'] = 'darkly'
        self.save_config()


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tb.Window(themename="litera")
    app = HexViewerEditorApp(root)
    root.mainloop()
