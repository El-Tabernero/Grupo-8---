
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import time
from logic import calcular_demora, calcular_total
from data import opciones_cafeteria, opciones_comidas

class CafeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Cafetería - El Informatorio')
        self.root.geometry('750x450')
        self.root.resizable(0, 0)
        self.root.config(bg="#f2e3d5")  # Color de fondo suave 

        # Cargar la imagen de fondo principal
        self.fondo_imagen = PhotoImage(file="cafebar.png")
        self.label_fondo = tk.Label(self.root, image=self.fondo_imagen)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Cargar la imagen para la barra lateral
        self.fondo_barra = PhotoImage(file="cafe_baner.png")
        self.frame_boton = tk.Frame(self.root, bg="#b5886e", bd=5)
        self.frame_boton.pack(side=tk.LEFT, fill=tk.Y)
        self.label_fondo_barra = tk.Label(self.frame_boton, image=self.fondo_barra)
        self.label_fondo_barra.place(x=0, y=0, relwidth=1, relheight=1)

        self.pedido = []
        self.create_widgets()

    def create_widgets(self):
        # Mensaje de bienvenida
        self.label_bienvenida = tk.Label(self.root, text="¡Bienvenido a nuestra Cafetería y Restaurante!", font=('Arial Black', 14), bg="#6F4C3E", fg="#FFFFFF")
        self.label_bienvenida.pack(pady=10)

        # Botones de la barra lateral con menús desplegables
        self.menubutton_cafeteria = tk.Menubutton(self.frame_boton, text="Cafetería", bg="#e0b28d", font=('Arial', 12))
        self.menubutton_cafeteria.menu = tk.Menu(self.menubutton_cafeteria, tearoff=0)
        self.menubutton_cafeteria["menu"] = self.menubutton_cafeteria.menu
        for item, precio in opciones_cafeteria.items():
            self.menubutton_cafeteria.menu.add_command(label=f"{item} - ${precio}",
                                                       command=lambda item=item, precio=precio: self.agregar_item(item, precio))
        self.menubutton_cafeteria.pack(pady=10, padx=10)

        self.menubutton_comidas = tk.Menubutton(self.frame_boton, text="Comidas", bg="#e0b28d", font=('Arial', 12))
        self.menubutton_comidas.menu = tk.Menu(self.menubutton_comidas, tearoff=0)
        self.menubutton_comidas["menu"] = self.menubutton_comidas.menu
        for item, precio in opciones_comidas.items():
            self.menubutton_comidas.menu.add_command(label=f"{item} - ${precio}",
                                                     command=lambda item=item, precio=precio: self.agregar_item(item, precio))
        self.menubutton_comidas.pack(pady=10, padx=10)

        # Botón para finalizar pedido
        self.boton_finalizar = tk.Button(self.frame_boton, text="Finalizar Pedido", command=self.mostrar_resumen,
                                         bg="#e0b28d", font=('Arial', 12))
        self.boton_finalizar.pack(pady=10, padx=10)

        # Botón desplegable "Síguenos"
        self.menubutton_redes = tk.Menubutton(self.frame_boton, text="Síguenos", bg="#e0b28d", font=('Arial', 12))
        self.menubutton_redes.menu = tk.Menu(self.menubutton_redes, tearoff=0)
        self.menubutton_redes["menu"] = self.menubutton_redes.menu
        self.menubutton_redes.menu.add_command(label="Facebook", command=lambda: self.abrir_red_social("Facebook"))
        self.menubutton_redes.menu.add_command(label="Instagram", command=lambda: self.abrir_red_social("Instagram"))
        self.menubutton_redes.menu.add_command(label="TikTok", command=lambda: self.abrir_red_social("TikTok"))
        self.menubutton_redes.pack(pady=10, padx=10)

        # Reloj al final de la barra lateral
        self.reloj = tk.Label(self.frame_boton, font=('Arial', 12), bg="#b5886e")
        self.reloj.pack(side=tk.BOTTOM, pady=10)
        self.actualizar_hora()

        # Pedido actual
        self.label_pedido_actual = tk.Label(self.root, text="Pedido Actual:", font=('Arial', 12), bg="#f2e3d5")
        self.label_pedido_actual.pack(pady=10)

        # Frame para contener la lista de pedidos y la scrollbar
        self.frame_lista_pedido = tk.Frame(self.root)
        self.frame_lista_pedido.pack(pady=10)

        # Scrollbar vertical
        self.scrollbar_pedido = tk.Scrollbar(self.frame_lista_pedido, orient=tk.VERTICAL)
        self.scrollbar_pedido.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox para mostrar el pedido actual
        self.lista_pedido_actual = tk.Listbox(self.frame_lista_pedido, font=('Arial', 12), height=5, width=50, bg="#fff3e9",
                                              yscrollcommand=self.scrollbar_pedido.set)
        self.lista_pedido_actual.pack(side=tk.LEFT)

        # Configurar scrollbar para que funcione con la Listbox
        self.scrollbar_pedido.config(command=self.lista_pedido_actual.yview)

        self.boton_eliminar_item = tk.Button(self.root, text="Eliminar Item", command=self.eliminar_item,
                                             bg="#e0b28d", font=('Arial', 12))
        self.boton_eliminar_item.pack(pady=10)

        # Botón para nuevo pedido o salir
        self.boton_nuevo_pedido = tk.Button(self.root, text="Nuevo Pedido o Salir", command=self.nuevo_pedido_o_salir,
                                            bg="#e0b28d", font=('Arial', 12))
        self.boton_nuevo_pedido.pack(pady=10)

    def actualizar_hora(self):
        tiempo_actual = time.strftime('%H:%M:%S')
        self.reloj.config(text=tiempo_actual)
        self.root.after(1000, self.actualizar_hora)

    def agregar_item(self, item, precio):
        self.pedido.append((item, precio))
        self.actualizar_pedido_actual()

    def actualizar_pedido_actual(self):
        self.lista_pedido_actual.delete(0, tk.END)
        for item, precio in self.pedido:
            self.lista_pedido_actual.insert(tk.END, f"{item} - ${precio}")

    def eliminar_item(self):
        seleccionados = self.lista_pedido_actual.curselection()
        if seleccionados:
            for i in seleccionados[::-1]:
                self.lista_pedido_actual.delete(i)
                del self.pedido[i]
            self.actualizar_pedido_actual()

    def mostrar_resumen(self):
        if self.pedido:
            self.total = calcular_total(self.pedido)
            self.demora = calcular_demora(self.pedido)
            mensaje = f"Su total es: ${self.total}\nLa demora estimada es: {self.demora} minutos"
            messagebox.showinfo("Resumen de Pedido", mensaje)
        else:
            messagebox.showwarning("Pedido Vacío", "No ha seleccionado ningún ítem.")

    def nuevo_pedido_o_salir(self):
        respuesta = messagebox.askquestion("Nuevo Pedido o Salir", "¿Desea generar un nuevo pedido?")
        if respuesta == 'yes':
            self.pedido.clear()
            self.actualizar_pedido_actual()
        else:
            self.root.quit()

    def abrir_red_social(self, red_social):
        messagebox.showinfo("Red Social", f"Abriendo {red_social}...")

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeApp(root)
    root.mainloop()
