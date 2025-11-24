from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from model_loader import ModelLoader, AgroAssistant
from prediction import PredictionLogger, ImageValidator

# Configuración de la aplicación
app = Flask(__name__, static_folder='../frontend',
            template_folder='../frontend')
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración
UPLOAD_FOLDER = '../uploads'
MODEL_PATH = 'models/mejor_modelo_cultivos.h5'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
FRONTEND_FOLDER = '../frontend'

# Crear directorios necesarios
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models', exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Inicializar componentes
try:
    model_loader = ModelLoader(MODEL_PATH)
    agro_assistant = AgroAssistant()
    prediction_logger = PredictionLogger()
    image_validator = ImageValidator()
    print("🚀 Sistema de cultivos inicializado exitosamente")
except Exception as e:
    print(f"❌ Error inicializando sistema: {e}")
    model_loader = None

@app.route('/')
def home():
    """Servir la página principal del frontend"""
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Servir archivos estáticos (CSS, JS, imágenes)"""
    return send_from_directory(FRONTEND_FOLDER, path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    model_status = 'loaded' if model_loader and model_loader.model else 'error'
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'message': 'Sistema operativo'
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint principal para predicciones"""
    if model_loader is None:
        return jsonify({'error': 'Modelo no disponible'}), 500
    
    # Verificar que se envió un archivo
    if 'image' not in request.files:
        return jsonify({'error': 'No se proporcionó imagen'}), 400
    
    file = request.files['image']
    
    # Validar archivo
    is_valid, validation_message = image_validator.validate_image(file)
    if not is_valid:
        return jsonify({'error': validation_message}), 400
    
    try:
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Realizar predicción
        prediction_result = model_loader.predict(filepath)
        
        # Obtener recomendación
        recommendation = agro_assistant.get_recommendation(
            prediction_result['class'], 
            prediction_result['confidence']
        )
        
        # Registrar predicción
        prediction_logger.log_prediction(filename, prediction_result, recommendation)
        
        # Preparar respuesta
        response = {
            'success': True,
            'prediction': prediction_result,
            'recommendation': recommendation,
            'filename': filename
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        return jsonify({'error': f'Error procesando imagen: {str(e)}'}), 500
    
    finally:
        # Limpiar archivo temporal
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"⚠️ Error limpiando archivo temporal: {e}")

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Obtener lista de clases disponibles"""
    if model_loader:
        return jsonify({
            'classes': model_loader.class_names,
            'count': len(model_loader.class_names)
        })
    else:
        return jsonify({'error': 'Modelo no disponible'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas del sistema"""
    try:
        if os.path.exists('predictions_log.json'):
            with open('predictions_log.json', 'r') as f:
                logs = json.load(f)
            total_predictions = len(logs)
        else:
            total_predictions = 0
        
        return jsonify({
            'total_predictions': total_predictions,
            'model_loaded': model_loader is not None,
            'classes_available': len(model_loader.class_names) if model_loader else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir archivos subidos (para desarrollo)"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Manejo de errores
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'Archivo demasiado grande'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

if __name__ == '__main__':
    print("🌱 Iniciando servidor de API...")
    app.run(host='0.0.0.0', port=5000, debug=True)