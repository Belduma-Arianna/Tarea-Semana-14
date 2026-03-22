Import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


class AplicacionAgenda:
    def __init__(self, ventana):
        # Configuracion basica de la ventana
        self.ventana = ventana
        self.ventana.title("Mi Agenda Personal")
        self.ventana.geometry("650x450")

        # --- Seccion para ingresar datos (Inputs) ---
        self.frame_datos = ttk.LabelFrame(self.ventana, text=" Detalles de la Tarea ", padding=10)
        self.frame_datos.pack(fill="x", padx=15, pady=10)

        # Labels y campos de texto para el usuario
        ttk.Label(self.frame_datos, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_sel = DateEntry(self.frame_datos, width=12, date_pattern='dd/mm/yyyy')
        self.fecha_sel.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_datos, text="Hora:").grid(row=0, column=2, padx=5, pady=5)
        self.campo_hora = ttk.Entry(self.frame_datos, width=10)
        self.campo_hora.insert(0, "08:00")  # Pongo una hora sugerida
        self.campo_hora.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.frame_datos, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
        self.campo_desc = ttk.Entry(self.frame_datos, width=50)
        self.campo_desc.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # --- Seccion de la tabla (Visualizacion) ---
        self.frame_tabla = ttk.Frame(self.ventana, padding=10)
        self.frame_tabla.pack(fill="both", expand=True)

        # Definir las columnas de la tabla Treeview
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("F", "H", "D"), show='headings')
        self.tabla.heading("F", text="Fecha")
        self.tabla.heading("H", text="Hora")
        self.tabla.heading("D", text="Evento / Tarea")

        # Ajustar el tamaño de cada columna manualmente
        self.tabla.column("F", width=100, anchor="center")
        self.tabla.column("H", width=80, anchor="center")
        self.tabla.column("D", width=350)

        self.tabla.pack(side="left", fill="both", expand=True)

        # Agregar el scrollbar por si hay muchos eventos
        scroll = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        # --- Seccion de botones de accion ---
        self.frame_control = ttk.Frame(self.ventana, padding=10)
        self.frame_control.pack(fill="x")

        # Botones para las funciones principales
        ttk.Button(self.frame_control, text="Agregar Evento", command=self.guardar_evento).pack(side="left", padx=5)
        ttk.Button(self.frame_control, text="Eliminar Seleccionado", command=self.borrar_evento).pack(side="left",
                                                                                                      padx=5)
        ttk.Button(self.frame_control, text="Salir", command=self.ventana.destroy).pack(side="right", padx=5)

    def guardar_evento(self):
        # Obtener lo que el usuario escribio
        f = self.fecha_sel.get()
        h = self.campo_hora.get()
        d = self.campo_desc.get()

        # Validar que no dejen la descripcion vacia
        if not d:
            messagebox.showwarning("Aviso", "Por favor, escribe de qué trata el evento")
            return

        # Insertar los datos al final de la tabla
        self.tabla.insert("", "end", values=(f, h, d))

        # Limpiar el campo de texto para el siguiente registro
        self.campo_desc.delete(0, tk.END)

    def borrar_evento(self):
        # Seleccionar la fila marcada por el usuario
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showinfo("Info", "Selecciona una fila de la lista para borrar")
            return

        # Pedir confirmacion antes de eliminar definitivamente
        res = messagebox.askyesno("Confirmar", "¿Estas seguro de eliminar este evento?")
        if res:
            for item in seleccion:
                self.tabla.delete(item)


if __name__ == "__main__":
    # Iniciar la aplicacion
    root = tk.Tk()
    app = AplicacionAgenda(root)
    root.mainloop()
