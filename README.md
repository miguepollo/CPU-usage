# Raspberry Pi System Monitor

## Características

- Monitoreo en tiempo real de uso de CPU
- Visualización del porcentaje de memoria RAM utilizada
- Temperatura del procesador (solo en Raspberry Pi)
- Interfaz gráfica moderna y elegante

## Requisitos Previos

En Raspberry Pi:
1. Instalar Python 3
2. Instalar librerías requeridas:
```bash
pip3 install flask psutil
```

En la Máquina Cliente:
1. Instalar Python 3
2. Instalar librerías requeridas:
```bash
pip3 install requests tkinter
```

## Configuración

1. En Raspberry Pi:
   - Ejecutar el script del servidor: `python3 rpi_cpu_monitor_server.py`
   - Asegurarse de que el firewall permita conexiones entrantes en el puerto 5000
   - Anotar la dirección IP de la Raspberry Pi

2. En la Máquina Cliente:
   - Abrir `cpu_monitor_client.py`
   - Reemplazar `'192.168.1.100'` con la dirección IP real de la Raspberry Pi
   - Ejecutar el script: `python3 cpu_monitor_client.py`

## Notas
- Asegurarse de que ambos dispositivos estén en la misma red
- El servidor se ejecuta en el puerto 5000
- El cliente crea una interfaz gráfica que muestra el uso del sistema en tiempo real
