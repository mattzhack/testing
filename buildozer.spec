[app]

# Información básica
title = Reparador Mikrotik
package.name = mikrotikreboot
package.domain = com.itservicios
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

# Versión
version = 1.0

# Requerimientos (MÍNIMOS para que compile)
requirements = python3==3.8.10, kivy==2.1.0

# Configuración Android
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.ndk_api = 21

# Permisos
android.permissions = INTERNET

# Otras configuraciones
orientation = portrait
fullscreen = 0

# Logs (útil para debug)
log_level = 2

[buildozer]
# Tiempo de espera para compilación (aumentado)
build_timeout = 1800
