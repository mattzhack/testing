from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
import threading
import socket

class MikrotikRebootApp(App):
    # Credenciales hardcodeadas
    ROUTER_IP = "10.180.190.1"
    USERNAME = "itservicios"
    PASSWORD = "Roxana10_"
    
    def build(self):
        Window.size = (400, 500)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Título
        title = Label(
            text='[b]Reparador de Conexión Mikrotik[/b]',
            font_size=28,
            markup=True,
            size_hint=(1, 0.2),
            halign='center'
        )
        
        # Información
        info = Label(
            text=f'[b]Router:[/b] {self.ROUTER_IP}\n[b]Usuario:[/b] {self.USERNAME}\n[b]Contraseña:[/b] {self.PASSWORD}',
            font_size=20,
            markup=True,
            size_hint=(1, 0.3),
            halign='center'
        )
        
        # Botón principal
        self.repair_button = Button(
            text='[b]VERIFICAR CONEXIÓN[/b]',
            background_color=(0.2, 0.6, 1, 1),
            font_size=24,
            markup=True,
            size_hint=(1, 0.25),
            bold=True
        )
        self.repair_button.bind(on_press=self.check_connection)
        
        # Estado
        self.status_label = Label(
            text='Presiona el botón para verificar',
            font_size=18,
            size_hint=(1, 0.25),
            halign='center'
        )
        
        self.layout.add_widget(title)
        self.layout.add_widget(info)
        self.layout.add_widget(self.repair_button)
        self.layout.add_widget(self.status_label)
        
        return self.layout
    
    def show_popup(self, title, message):
        """Muestra un popup con información"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        content.add_widget(Label(text=message, font_size=18, halign='center'))
        
        close_btn = Button(
            text='Cerrar',
            size_hint=(1, 0.3),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.6)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
    
    def check_connection(self, instance):
        """Verifica si el router es accesible"""
        self.repair_button.disabled = True
        self.repair_button.text = '[b]VERIFICANDO...[/b]'
        self.status_label.text = 'Conectando al router...'
        
        def test_connection():
            try:
                # Probar puerto SSH (22)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                
                result = sock.connect_ex((self.ROUTER_IP, 22))
                
                if result == 0:
                    Clock.schedule_once(lambda dt: setattr(
                        self.status_label, 'text',
                        '[color=00FF00]✓ Router accesible (SSH activo)[/color]'
                    ))
                    Clock.schedule_once(lambda dt: setattr(
                        self.status_label, 'markup', True
                    ))
                    
                    # Mostrar instrucciones
                    Clock.schedule_once(lambda dt: self.show_popup(
                        '¡Conectado!',
                        f'Router {self.ROUTER_IP} accesible.\n\n'
                        f'Para reiniciar:\n'
                        f'1. SSH: itservicios@{self.ROUTER_IP}\n'
                        f'2. Contraseña: {self.PASSWORD}\n'
                        f'3. Comando: /system reboot\n\n'
                        f'O usa WinBox con la misma IP.'
                    ))
                else:
                    Clock.schedule_once(lambda dt: setattr(
                        self.status_label, 'text',
                        '[color=FF0000]✗ No se puede conectar[/color]\nVerifica la red o IP'
                    ))
                    Clock.schedule_once(lambda dt: setattr(
                        self.status_label, 'markup', True
                    ))
                
                sock.close()
                
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(
                    self.status_label, 'text',
                    f'Error: {str(e)[:50]}...'
                ))
            finally:
                Clock.schedule_once(lambda dt: setattr(
                    self.repair_button, 'disabled', False
                ))
                Clock.schedule_once(lambda dt: setattr(
                    self.repair_button, 'text', '[b]VERIFICAR DE NUEVO[/b]'
                ))
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=test_connection)
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    MikrotikRebootApp().run()
