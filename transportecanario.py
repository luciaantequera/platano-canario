import threading
import time
import random

# --- RECURSOS COMPARTIDOS (Plataformas de destino) ---
# Aquí almacenaremos quién está en la plataforma.
plataformas_caoticas = {"Gran Canaria": "", "Tenerife": ""}
plataformas_seguras = {"Gran Canaria": "", "Tenerife": ""}

# Candados (Locks) para el sistema seguro
locks_destinos = {
    "Gran Canaria": threading.Lock(),
    "Tenerife": threading.Lock()
}

# --- 1. SISTEMA CAÓTICO (Provocando el fallo) ---
def teletransporte_inseguro(viajero, origen, destino):
    print(f"[CAOS] {viajero} ({origen}) iniciando viaje a {destino}...")
    
    # Simulamos el tiempo de viaje
    time.sleep(random.uniform(0.1, 0.3)) 
    
    # LECTURA DEL ESTADO ACTUAL (Condición de carrera inminente)
    ocupante_actual = plataformas_caoticas[destino]
    
    # Simulamos un pequeño retraso en la materialización para forzar el solapamiento
    time.sleep(0.1) 
    
    # ESCRITURA (Fusión de strings si hay alguien más)
    if ocupante_actual == "":
        plataformas_caoticas[destino] = f"{viajero}_{origen}"
    else:
        # ¡Desastre! Se fusionan
        plataformas_caoticas[destino] = f"{ocupante_actual} + {viajero}_{origen} (MUTANTE!)"
    
    print(f"[CAOS] Llegada registrada en {destino}.")

# --- 2. SISTEMA SEGURO (Sincronizado) ---
def teletransporte_seguro(viajero, origen, destino):
    print(f"[SEGURO] {viajero} ({origen}) solicitando viaje a {destino}...")
    
    # Solicitar el candado de la plataforma de destino (Exclusión mutua)
    with locks_destinos[destino]: # Esto equivale a adquirir y liberar el Lock
        print(f"[SEGURO] {viajero} ha bloqueado la plataforma de {destino}. Materializándose...")
        
        # Simulamos el viaje y la materialización segura
        time.sleep(random.uniform(0.1, 0.3))
        
        # Como tenemos el Lock, nadie más puede escribir o leer aquí a la vez
        plataformas_seguras[destino] = f"{viajero}_{origen}"
        print(f"[SEGURO] {viajero} ha llegado a {destino} de una pieza. Liberando plataforma...")
        
        # Limpiamos la plataforma para el siguiente (opcional, para simular que sale de la cabina)
        time.sleep(0.1)
        plataformas_seguras[destino] = ""

# --- EJECUCIÓN DE LAS PRUEBAS ---
if __name__ == "__main__":
    viajeros = [
        ("Ayoze", "Canarion", "Tenerife"),
        ("Eusebio", "Murciano", "Tenerife"),
        ("Jonay", "Tinerfeno", "Gran Canaria"),
        ("Paco", "Murciano", "Gran Canaria")
    ]

    print("--- INICIANDO PRUEBA CAOTICA (SIN SINCRONIZACION) ---")
    hilos_caos = []
    for v, o, d in viajeros:
        # Creamos un hilo por cada viajero
        h = threading.Thread(target=teletransporte_inseguro, args=(v, o, d))
        hilos_caos.append(h)
        h.start()

    for h in hilos_caos:
        h.join() # Esperamos a que todos terminen

    print("\nRESULTADOS DEL CAOS (Estado de las plataformas):")
    for isla, resultado in plataformas_caoticas.items():
        print(f" - {isla}: {resultado}")

    print("\n" + "="*50 + "\n")

    print("--- INICIANDO PRUEBA SEGURA (CON LOCKS) ---")
    hilos_seguros = []
    for v, o, d in viajeros:
        h = threading.Thread(target=teletransporte_seguro, args=(v, o, d))
        hilos_seguros.append(h)
        h.start()

    for h in hilos_seguros:
        h.join()
        
    print("\nTodos los viajes seguros completados sin incidentes mutantes.")