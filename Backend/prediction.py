import os
from datetime import datetime
import json

class PredictionLogger:
    """Sistema de logging para predicciones"""
    
    def __init__(self, log_file='predictions_log.json'):
        self.log_file = log_file
    
    def log_prediction(self, image_filename, prediction_result, recommendation):
        """Registrar predicción en archivo JSON"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'image_filename': image_filename,
            'prediction': prediction_result,
            'recommendation': recommendation
        }
        
        # Cargar logs existentes o crear nuevo archivo
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        
        # Agregar nueva entrada
        logs.append(log_entry)
        
        # Guardar logs
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return log_entry

class ImageValidator:
    """Validador de imágenes"""
    
    def __init__(self):
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        self.max_file_size = 16 * 1024 * 1024  # 16MB
    
    def validate_image(self, file):
        """Validar archivo de imagen"""
        if not file:
            return False, "No se proporcionó archivo"
        
        # Verificar extensión
        if '.' not in file.filename:
            return False, "Archivo sin extensión"
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in self.allowed_extensions:
            return False, f"Extensión no permitida: {extension}"
        
        # Verificar tamaño (aproximado)
        file.seek(0, 2)  # Ir al final del archivo
        file_size = file.tell()
        file.seek(0)  # Volver al inicio
        
        if file_size > self.max_file_size:
            return False, "Archivo demasiado grande"
        
        return True, "Válido"