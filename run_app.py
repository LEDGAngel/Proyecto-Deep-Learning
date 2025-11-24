#!/usr/bin/env python3
"""
Script para ejecutar la aplicación completa
"""

import os
import subprocess
import sys
import webbrowser
from threading import Timer

def check_dependencies():
    """Verificar dependencias y directorios"""
    try:
        import tensorflow
        import flask
        print("✅ Todas las dependencias están instaladas")
        
        required_dirs = ['Backend', 'Frontend']
        required_files = { 
            'Backend': ['app.py', 'requirements.txt'],
            'Frontend': ['index.html', 'styles.css', 'app.js']
        }
        
        print("📁 Verificando estructura de directorios...")
        
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                print(f"❌ Error: No se encuentra el directorio '{dir_name}'")
                return False
        
        for dir_name, files in required_files.items():
            for file in files:
                file_path = os.path.join(dir_name, file)
                if not os.path.exists(file_path):
                    print(f"❌ Error: No se encuentra el archivo '{file_path}'")
                    return False
        
        print("✅ Estructura de directorios correcta")
        return True
    
    except ImportError as e:
        print(f"❌ Error de dependencias: {e}")
        print("📦 Instalando dependencias...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias")
            return False

def start_backend():
    """Iniciar servidor backend"""
    print("🚀 Iniciando servidor backend...")
    os.chdir('backend')
    subprocess.Popen([sys.executable, "app.py"])
    os.chdir('..')

def start_frontend():
    """Abrir frontend en el navegador"""
    def open_browser():
        webbrowser.open('http://localhost:5000')
    
    # Esperar un poco para que el servidor inicie
    Timer(3, open_browser).start()

def main():
    """Función principal"""
    print("🌱 Iniciando AgroDetect Application...")
    
    # Verificar estructura de directorios
    if not os.path.exists('backend'):
        print("❌ Error: No se encuentra el directorio 'backend'")
        return
    
    if not os.path.exists('frontend'):
        print("❌ Error: No se encuentra el directorio 'frontend'")
        return
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Verificar que existe el modelo
    model_path = 'Backend/models/mejor_modelo_cultivos.h5'
    if not os.path.exists(model_path):
        print("⚠️ Advertencia: No se encuentra el modelo entrenado")
        print("💡 Coloca tu modelo entrenado en: backend/models/modelo_entrenado.h5")
    
    # Iniciar aplicación
    start_backend()
    start_frontend()
    
    print("✅ Aplicación iniciada correctamente")
    print("🌐 Frontend disponible en: http://localhost:5000")
    print("🔧 Backend API disponible en: http://localhost:5000/api")
    print("\nPresiona Ctrl+C para detener la aplicación")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")