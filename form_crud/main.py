import flet as ft
from clientes import Clientes
import pandas as pd
from fpdf import FPDF
import re
import datetime

# Clase personalizada para generar PDFs
class PDF(FPDF):
    def header(self):
        # Encabezado del PDF: establece fuente y título centrado
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Tabla de Datos', 0, 1, 'C')

    def footer(self):
        # Pie de página con el número de página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Clase principal para el formulario de cliente y operaciones CRUD
class ClientForm(ft.UserControl):
    # Método para validar si el correo tiene un formato válido
    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    # Constructor que configura los componentes del formulario
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        self.data = Clientes()  # Base de datos de clientes
        self.selected__row = None  # Almacena la fila seleccionada para editar o borrar

        # Campos de entrada para los datos del cliente
        self.name = ft.TextField(label="Nombre", border_color="blue")
        self.age = ft.TextField(
            label="Edad",
            border_color="blue",
            input_filter=ft.NumbersOnlyInputFilter(),  # Solo permite números
            max_length=2  # Limita la longitud a 2 caracteres
        )
        self.email = ft.TextField(label="Correo", border_color="blue")
        self.phone = ft.TextField(
            label="Telefono",
            border_color="blue",
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=10
        )

        # Diálogo de alerta para mostrar mensajes de error
        self.alert_dialog = ft.AlertDialog()

        # Campo de búsqueda para filtrar clientes por nombre
        self.search_filed = ft.TextField(
            label="Buscar por nombre",
            suffix_icon=ft.icons.SEARCH,
            border=ft.InputBorder.UNDERLINE,
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            on_change=self.search_data,  # Llama a `search_data` en cada cambio
        )

        # Configuración de la tabla de clientes con columnas personalizadas
        self.data_table = ft.DataTable(
            expand=True,
            border=ft.border.all(2, "blue"),
            data_row_color={ft.MaterialState.SELECTED: "blue", ft.MaterialState.PRESSED: "black"},
            border_radius=10,
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("Nombre", color="blue", weight="bold")),
                ft.DataColumn(ft.Text("Edad", color="blue", weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Correo", color="blue", weight="bold")),
                ft.DataColumn(ft.Text("Telefono", color="blue", weight="bold")),
            ]
        )
        # Muestra los datos actuales en la tabla
        self.show_data()

        # Contenedor del formulario de entrada
        self.form = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            col=4,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Ingrese sus datos", size=40, text_align="center", font_family="roboto"),
                    self.name, self.age, self.email, self.phone,
                    # Botones de acción: Guardar, Actualizar y Borrar
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.TextButton(text="Guardar", icon=ft.icons.SAVE, style=ft.ButtonStyle(color="white", bgcolor="blue"), on_click=self.add_data),
                                ft.TextButton(text="Actualizar", icon=ft.icons.UPDATE, style=ft.ButtonStyle(color="white", bgcolor="blue"), on_click=self.update_data),
                                ft.TextButton(text="Borrar", icon=ft.icons.DELETE, style=ft.ButtonStyle(color="white", bgcolor="blue"), on_click=self.delete_data)
                            ]
                        )
                    )
                ]
            )
        )

        # Contenedor de la tabla y los botones de búsqueda/exportación
        self.table = ft.Container(
            bgcolor="#222222",
            border_radius=10,
            col=8,
            padding=10,
            content=ft.Column(
                controls=[
                    # Barra de búsqueda y botones para PDF y Excel
                    ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                self.search_filed,
                                ft.IconButton(tooltip="Editar", icon=ft.icons.EDIT, icon_color="white", on_click=self.edit_filed_text),
                                ft.IconButton(tooltip="Descargar en PDF", icon=ft.icons.PICTURE_AS_PDF, icon_color="white", on_click=self.save_pdf),
                                ft.IconButton(tooltip="Descargar en EXCEL", icon=ft.icons.SAVE_ALT, icon_color="white", on_click=self.save_excel)
                            ]
                        )
                    ),
                    ft.Column(expand=True, scroll="auto", controls=[ft.ResponsiveRow([self.data_table])])
                ]
            )
        )

        # Distribución general de la interfaz en una fila responsiva
        self.conent = ft.ResponsiveRow(controls=[self.form, self.table])

    # Muestra un mensaje de error en el diálogo de alerta
    def show_alert(self, message):
        self.alert_dialog.content = ft.Text(message)
        self.page.dialog = self.alert_dialog
        self.alert_dialog.open = True
        self.page.update()

    # Muestra la lista de clientes en la tabla
    def show_data(self):
        self.data_table.rows = []
        for x in self.data.get_clients():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,  # Selección de filas
                    cells=[
                        ft.DataCell(ft.Text(x[1])),  # Nombre
                        ft.DataCell(ft.Text(str(x[2]))),  # Edad
                        ft.DataCell(ft.Text(x[3])),  # Correo
                        ft.DataCell(ft.Text(str(x[4])))  # Telefono
                    ]
                )
            )
        self.update()

    # Añade un nuevo cliente si los datos son válidos y no existe ya
    def add_data(self, e):
        name = self.name.value
        age = str(self.age.value)
        email = self.email.value
        phone = str(self.phone.value)

        # Verifica que los campos no estén vacíos y que el correo sea válido
        if len(name) > 0 and len(age) > 0 and len(email) > 0 and len(phone) > 0:
            if not self.is_valid_email(email):
                self.show_alert("El correo electrónico no es válido.")
                return
    
            # Verifica si el cliente ya existe por nombre
            client_exist = False
            for row in self.data.get_clients():
                if row[1] == name:
                    client_exist = True
                    break
            if not client_exist:
                # Si no existe, lo añade y limpia el formulario
                self.limpiador()
                self.data.add_clients(name, age, email, phone)
                self.show_data()
            else:
                self.show_alert("El cliente ya existe.")
        else:
            self.show_alert("Todos los campos son obligatorios.")

    # Selecciona una fila de la tabla y guarda la información
    def get_index(self, e):
        e.control.selected = not e.control.selected

        name = e.control.cells[0].content.value
        for row in self.data.get_clients():
            if row[1] == name:
                self.selected__row = row
                break
        
        self.update()

    # Llena el formulario con los datos del cliente seleccionado para editar
    def edit_filed_text(self, e):
        try:
            self.name.value = self.selected__row[1]
            self.age.value = self.selected__row[2]
            self.email.value = self.selected__row[3]
            self.phone.value = self.selected__row[4]
            self.update()
        except TypeError:
            self.show_alert("Seleccione un cliente para editar.")

    # Actualiza los datos del cliente seleccionado
    def update_data(self, e):
        if self.selected__row:
            name = self.name.value
            age = str(self.age.value)
            email = self.email.value
            phone = str(self.phone.value)
            if len(name) > 0 and len(age) > 0 and len(email) > 0 and len(phone) > 0:
                self.limpiador()
                self.data.update_clients(self.selected__row[0], name, age, email, phone)
                self.show_data()
            else:
                self.show_alert("Todos los campos son obligatorios.")
        else:
            self.show_alert("Seleccione un cliente para actualizar.")

    # Filtra los clientes por nombre en la tabla
    def search_data(self, e):
        search = self.search_filed.value.lower()
        name = list(filter(lambda x: search in x[1].lower(), self.data.get_clients()))
        self.data_table.rows = []
        if self.search_filed.value:
            if len(name) > 0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed=self.get_index,
                            cells=[
                                ft.DataCell(ft.Text(x[1])),
                                ft.DataCell(ft.Text(str(x[2]))),
                                ft.DataCell(ft.Text(x[3])),
                                ft.DataCell(ft.Text(str(x[4]))),
                            ]
                        )
                    )
                self.update()
            else:
                self.show_alert("No se encontraron resultados.")
        else:
            self.show_data()
            
    # Elimina el cliente seleccionado
    def delete_data(self, e):
        if self.selected__row:
            client_id = self.selected__row[0]
            self.data.delete_clients(client_id)
            self.limpiador()
            self.show_data()
            self.selected__row = None
        else:
            self.show_alert("Seleccione un cliente para borrar.")

    # Limpia el formulario después de cada operación
    def limpiador(self):
        self.name.value = ""
        self.age.value = ""
        self.email.value = ""
        self.phone.value = ""

    # Guarda la tabla en un archivo PDF
    def save_pdf(self, e):
        pdf = PDF()
        pdf.add_page()
        column_widths = [10,40, 20, 80, 40]
        data = self.data.get_clients()
        header = ("ID", "NOMBRE", "EDAD", "CORREO", "TELEFONO")
        data.insert(0, header)
        for row in data:
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), border=1)
            pdf.ln()
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)

    # Exporta la tabla a un archivo Excel
    def save_excel(self, e):
        file_name = datetime.datetime.now().strftime("DATA %Y-%m-%d_%H-%M-%S") + ".xlsx"
        contacts = self.data.get_clients()
        df = pd.DataFrame(contacts, columns=["ID", "Nombre", "Edad", "Correo", "Teléfono"])
        df.to_excel(file_name, index=False)

    # Método de construcción que retorna el formulario y la tabla
    def build(self):
        return self.conent

# Configuración de la ventana principal
def main(page: ft.Page):
    page.bgcolor = "black"
    page.title = "CRUD SQLite"
    page.window_min_height = 500
    page.window_min_width = 100
    page.add(ClientForm(page))
