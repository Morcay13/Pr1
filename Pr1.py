import psutil
import os
import subprocess
import pyperclip
import time


#Parte 1: Exploración y Gestión de Procesos
#1. Listar Procesos Activos
def listar_procesos(nombres_procesos):
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if proc.info['name'] and any(nombre.lower() in proc.info['name'].lower() for nombre in nombres_procesos):
                print(f"Nombre: {proc.info['name']}, PID: {proc.info['pid']}, Memoria: {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

nombres = input("Introduce nombres de procesos separados por coma: ").split(',')


#2. Finalizar Procesos Específicos
listar_procesos([nombre.strip() for nombre in nombres])
def finalizar_proceso(nombre_proceso):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and nombre_proceso.lower() in proc.info['name'].lower():
                proc.terminate()
                proc.wait()  # Espera para confirmar terminación
                print(f"Proceso {proc.info['name']} (PID: {proc.info['pid']}) finalizado correctamente.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"No se pudo finalizar el proceso: {e}")
    print(f"Proceso {nombre_proceso} no encontrado.")

proceso_a_finalizar = input("Introduce el nombre del proceso a finalizar: ").strip()
finalizar_proceso(proceso_a_finalizar)


#Parte 2: Comunicación Interprocesos con Pipes
#1. Envío de Mensajes entre Procesos
def comunicacion_pipe():
    padre_a_hijo, hijo_a_padre = os.pipe(), os.pipe()

    if os.fork() == 0:  # Proceso hijo
        os.close(padre_a_hijo[1])
        mensaje = os.read(padre_a_hijo[0], 1024).decode()
        os.close(padre_a_hijo[0])

        respuesta = mensaje.upper()
        os.close(hijo_a_padre[0])
        os.write(hijo_a_padre[1], respuesta.encode())
        os.close(hijo_a_padre[1])
    else:  # Proceso padre
        os.close(padre_a_hijo[0])
        mensaje = "Hola desde el padre"
        os.write(padre_a_hijo[1], mensaje.encode())
        os.close(padre_a_hijo[1])

        os.close(hijo_a_padre[1])
        respuesta = os.read(hijo_a_padre[0], 1024).decode()
        os.close(hijo_a_padre[0])
        print(f"Respuesta del hijo: {respuesta}")


comunicacion_pipe()

#Parte 3: Ejecución de Programas Síncrona y Asíncrona
import subprocess
import time

def ejecutar_notepad(sincrono):
    inicio = time.time()
    proceso = subprocess.Popen("notepad.exe") if not sincrono else subprocess.run("notepad.exe")
    if not sincrono:
        print("Ejecución no bloqueante, continúa...")
        proceso.wait()  # Bloquea si se elige síncrono
    fin = time.time()
    print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")

modo = input("¿Desea ejecución síncrona (s/n)? ").strip().lower() == 's'
ejecutar_notepad(modo)

#Parte 4: Transferencia de Datos y Manipulación del Portapapeles
def verificar_portapapeles(intervalo=5):
    contenido_anterior = pyperclip.paste()
    while True:
        time.sleep(intervalo)
        contenido_actual = pyperclip.paste()
        if contenido_actual != contenido_anterior:
            print(f"El portapapeles ha cambiado: {contenido_actual}")
            contenido_anterior = contenido_actual

def descargar_archivo_ftp():
    # Cambia estos parámetros para tu servidor FTP
    ftp_comando = ["ftp", "-n", "ftp.dlptest.com"]
    proceso = subprocess.Popen(ftp_comando, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    comandos = "user anonymous anonymous\nget archivo.txt\nquit\n".encode()
    salida, _ = proceso.communicate(input=comandos)
    print(salida.decode())

    # Simular contenido descargado
    pyperclip.copy("Contenido del archivo descargado")

descargar_archivo_ftp()
verificar_portapapeles()


