import tensorflow as tf
import numpy as np
import os
from PIL import Image

class ModelLoader:
    def __init__(self, model_path):
        self.model = None
        self.model_path = model_path
        self.class_names = [
            'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
            'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites',
            'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 
            'Tomato___Tomato_mosaic_virus', 'Tomato___healthy',
            'Corn___Common_rust', 'Corn___Northern_Leaf_Blight', 'Corn___healthy',
            'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy'
        ]
        self.load_model()
    
    def load_model(self):
        """Cargar el modelo entrenado"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print("✅ Modelo cargado exitosamente")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise e
    
    def preprocess_image(self, image_path):
        """Preprocesar imagen para el modelo"""
        try:
            # Cargar y redimensionar imagen
            img = Image.open(image_path)
            img = img.resize((224, 224))
            
            # Convertir a array y normalizar
            img_array = np.array(img)
            img_array = img_array / 255.0
            
            # Agregar dimensión del batch
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"❌ Error preprocesando imagen: {e}")
            raise e
    
    def predict(self, image_path):
        """Realizar predicción en una imagen"""
        try:
            # Preprocesar imagen
            processed_image = self.preprocess_image(image_path)
            
            # Realizar predicción
            predictions = self.model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Obtener nombre de la clase
            predicted_class = self.class_names[predicted_class_idx]
            
            return {
                'class': predicted_class,
                'confidence': confidence,
                'all_predictions': predictions[0].tolist()
            }
            
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
            raise e

class AgroAssistant:
    """Sistema de recomendaciones para agricultores"""
    
    def __init__(self):
        self.recommendations = {
            'Tomato___Bacterial_spot': {
                'diagnosis': 'Mancha Bacteriana del Tomate',
                'treatment': 'Aplicar bactericidas a base de cobre',
                'dosage': '2-3 gramos por litro de agua',
                'frequency': 'Cada 7-10 días',
                'prevention': 'Rotación de cultivos, usar semillas certificadas',
                'urgency': 'media_alta',
                'organic_alternative': 'Extracto de ajo o bicarbonato de sodio (3-4 gramos de sulfato de cobre por litro)'
            },
            'Tomato___Early_blight': {
                'diagnosis': 'Tizón Temprano del Tomate',
                'treatment': 'Fungicidas protectores (Clorotalonil)',
                'dosage': '1.5-2 ml por litro de agua',
                'frequency': 'Cada 10-14 días',
                'prevention': 'Eliminar restos de cultivo, mejorar ventilación',
                'urgency': 'media',
                'organic_alternative': 'Bicarbonato de sodio (1 cucharada por litro)'
            },
            'Tomato___Late_blight': {
                'diagnosis': 'Tizón Tardío del Tomate',
                'treatment': 'Fungicidas sistémicos (Metalaxyl)',
                'dosage': '2-2.5 ml por litro de agua',
                'frequency': 'Cada 5-7 días en condiciones húmedas',
                'prevention': 'Evitar riego por aspersión, podar hojas bajas',
                'urgency': 'alta',
                'organic_alternative': 'Cola de caballo o extracto de canela (4-5 gramos de oxicloruro de cobre por litro)'
            },
            'Tomato___healthy': {
                'diagnosis': 'Planta Saludable',
                'treatment': 'Mantenimiento preventivo',
                'dosage': 'No requiere tratamiento',
                'frequency': 'Monitoreo semanal',
                'prevention': 'Continuar con buenas prácticas agrícolas',
                'urgency': 'ninguna',
                'organic_alternative': 'Continuar con prácticas orgánicas'
            },
            
            'Tomato___Leaf_Mold': {
                'diagnosis': 'Moho de la Hoja del Tomate',
                'treatment': 'Fungicidas a base de azufre (Azoxistrobina, Tebuconazole)',
                'dosage': '2-3 gramos por litro de agua',
                'frequency': 'Cada 7-10 días',
                'prevention': 'Mejorar la circulación de aire, evitar el riego por aspersión',
                'urgency': 'media',
                'organic_alternative': 'Bicarbonato (Proporcion 1:9), leche diluida (100 ml de leche por litro de agua)'
            },
            'Tomato___Septoria_leaf_spot': {
                'diagnosis': 'Mancha de la Septoria',
                'treatment': 'Clorotalonil, Mancozeb',
                'dosage': '2 gramos por litro',
                'frequency': 'Cada 10 días',
                'prevention': 'Eliminar hojas infectadas, rotación de cultivos',
                'urgency': 'Media',
                'organic_alternative': 'Aceite de neem, extracto de canela (3-5 ml de aceite de neem por litro)'
            },
            'Tomato___Spider_mites': {
                'diagnosis': 'Ácaro de Dos Puntos',
                'treatment': 'Abamectina, Spiromesifen',
                'dosage': '0.5-1 ml por litro',
                'frequency': 'Cada 5-7 días (2-3 aplicaciones)',
                'prevention': 'Mantener humedad alta, control de malezas',
                'urgency': 'Alta',
                'organic_alternative': 'Jabón potásico, aceite de neem (5 ml de jabón potásico + 3 ml aceite neem por litro)'
            },
            'Tomato___Target_Spot': {
                'diagnosis': 'Mancha Blanco',
                'treatment': 'Azoxistrobina, Tebuconazole',
                'dosage': '1.5 ml por litro',
                'frequency': 'Cada 10-12 días',
                'prevention': 'Eliminar residuos, evitar exceso de nitrógeno',
                'urgency': 'Media',
                'organic_alternative': 'Extracto de cola de caballo, bicarbonato (20 gramos de cola de caballo seca por litro)'
            },
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
                'diagnosis': 'Virus del Rizado Amarillo',
                'treatment': 'Imidacloprid (solo para virus)',
                'dosage': '0.5 ml por litro para control de mosca',
                'frequency': 'Aplicaciones preventivas cada 15 días',
                'prevention': 'Mallas anti-insectos, eliminar plantas infectadas',
                'urgency': 'Muy Alta',
                'organic_alternative': 'Aceite de neem para control de vector (5 ml aceite neem por litro)'
            },
            'Tomato___Tomato_mosaic_virus': {
                'diagnosis': 'Virus del Mosaico del Tomate',
                'treatment': 'Elimine las plantas infectadas, para las semillas Fosfato Trisódico',
                'dosage': '100 gramos por litro',
                'frequency': 'Lo antes posible para evitar la propagación',
                'prevention': 'Semillas certificadas, desinfección de herramientas',
                'urgency': 'Muy Alta',
                'organic_alternative': 'Calentar las semillas a 70°C durante 4 días o a 82-85°C durante 24 horas'
            },
            
            'Corn___Common_rust': {
                'diagnosis': 'Roya Común del Maíz',
                'treatment': 'Fungicidas triazoles',
                'dosage': '0.8-1.2 litros por hectárea',
                'frequency': 'Aplicar preventivamente',
                'prevention': 'Usar variedades resistentes, rotación de cultivos',
                'urgency': 'media',
                'organic_alternative': 'Bicarbonato de sodio o aceite de neem'
            },
            'Potato___Early_blight': {
                'diagnosis': 'Tizón Temprano de la Papa',
                'treatment': 'Fungicidas protectores',
                'dosage': '1.5-2 gramos por litro',
                'frequency': 'Cada 10-12 días',
                'prevention': 'Eliminar tubérculos infectados',
                'urgency': 'media',
                'organic_alternative': 'Extracto de cola de caballo'
            }
        }
    
    def get_recommendation(self, predicted_class, confidence):
        """Obtener recomendación basada en la predicción"""
        if predicted_class in self.recommendations:
            rec = self.recommendations[predicted_class].copy()
            rec['confidence'] = f"{confidence * 100:.2f}%"
            
            # Ajustar recomendación basada en confianza
            if confidence < 0.7:
                rec['warning'] = 'Baja confianza - considerar nueva evaluación'
            elif confidence > 0.9:
                rec['urgency'] = 'alta'
            
            return rec
        else:
            return {
                'diagnosis': 'Enfermedad no identificada',
                'treatment': 'Consultar con especialista agrícola',
                'confidence': f"{confidence * 100:.2f}%",
                'warning': 'No se encontró recomendación específica para esta enfermedad'
            }