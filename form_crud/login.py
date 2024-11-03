# login.py
import flet as ft
from usuarios import check_user  # Verifica que esta función esté bien implementada
from main import ClientForm  # Asegúrate de importar correctamente

def main(page: ft.Page):
    # Configuración inicial de la ventana
    page.window_min_height = 500
    page.window_min_width = 100
    page.window.center()
    page.padding = 0
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.email_value = ""
    page.password_value = ""

    # Función para manejar el login
    def login(e):
        email = page.email_value
        password = page.password_value
        print(f"Verificando usuario: {email}")  # Debugging: imprime el correo
        if check_user(email, password):
            print("Usuario verificado, cargando la interfaz principal...")  # Debugging
            page.clean()  # Limpiar la página actual
            page.add(ClientForm(page))  # Añadir la nueva interfaz
            page.update()  # Actualizar la página
        else:
            show_error_dialog("Correo electrónico o contraseña incorrectos")

    # Función para mostrar un diálogo de error
    def show_error_dialog(message):
        error_dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog())]
        )
        page.dialog = error_dialog
        page.dialog.open = True
        page.update()

    # Función para cerrar el diálogo
    def close_dialog():
        page.dialog.open = False
        page.update()

    # Diseño del formulario de inicio de sesión centrado
    login_form = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Column(controls=[
                    ft.Container(
                        ft.Image(
                            src='logo.png',
                            width=70,
                        ),
                        padding=ft.padding.only(150, 20)
                    ),
                    ft.Text(
                        'Iniciar Sesión',
                        width=360,
                        size=30,
                        weight='w900',
                        text_align='center',
                        color="white"
                    ),
                    ft.Container(
                        ft.TextField(
                            width=280,
                            height=40,
                            hint_text='Correo electrónico',
                            border='underline',
                            color='white',
                            prefix_icon=ft.icons.EMAIL,
                            on_change=lambda e: setattr(page, "email_value", e.control.value)
                        ),
                        padding=ft.padding.only(20, 10)
                    ),
                    ft.Container(
                        ft.TextField(
                            width=280,
                            height=40,
                            hint_text='Contraseña',
                            border='underline',
                            color='white',
                            prefix_icon=ft.icons.LOCK,
                            password=True,
                            on_change=lambda e: setattr(page, "password_value", e.control.value)
                        ),
                        padding=ft.padding.only(20, 10)
                    ),
                    ft.Container(
                        ft.Checkbox(
                            label='Recordar contraseña',
                            check_color='white',
                            label_style=ft.TextStyle(color="white")
                        ),
                        padding=ft.padding.only(40),
                    ),
                    ft.Container(
                        ft.ElevatedButton(
                            content=ft.Text(
                                'INICIAR',
                                color='black',
                                weight='w500',
                            ),
                            width=280,
                            bgcolor='white',
                            on_click=login  # Llama a la función de inicio de sesión
                        ),
                        padding=ft.padding.only(25, 10)
                    ),
                    ft.Container(
                        ft.Row([
                            ft.Text('¿No tiene una cuenta?', color="white"),
                            ft.TextButton('Crear una cuenta', style=ft.ButtonStyle(color="white")),
                        ], spacing=8),
                        padding=ft.padding.only(40)
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                bgcolor="blue",
                width=380,
                height=460,
                border_radius=20,
                padding=20
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=10,
    )

    # Contenedor principal con la imagen de fondo
    background = ft.Container(
        content=login_form,
        image_src="form_crud/fondoAzul.jpg",  # Ruta de la imagen de fondo
        image_fit=ft.ImageFit.COVER,  # Ajusta la imagen al tamaño del contenedor
        expand=True  # Expande el contenedor para cubrir toda la página
    )

    # Agregar el contenedor principal a la página
    page.add(background)

# Ejecuta la aplicación desde login.py como punto de inicio
ft.app(target=main)
