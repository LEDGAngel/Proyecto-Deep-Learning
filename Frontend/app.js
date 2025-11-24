// Configuración
const API_BASE_URL = 'http://localhost:5000/api';

// Elementos DOM
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const previewContainer = document.getElementById('previewContainer');
const analyzeSection = document.getElementById('analyzeSection');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const systemStatus = document.getElementById('systemStatus');

// Estado de la aplicación
let currentImageFile = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    checkSystemHealth();
    setupEventListeners();
});

function setupEventListeners() {
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // File input change
    imageInput.addEventListener('change', handleFileSelect);
    
    // Click en área de upload
    uploadArea.addEventListener('click', () => imageInput.click());
}

// Drag and Drop handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleImageFile(files[0]);
    }
}

// File selection handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleImageFile(file);
    }
}

function handleImageFile(file) {
    // Validar tipo de archivo
    if (!file.type.startsWith('image/')) {
        showError('Por favor, selecciona un archivo de imagen válido.');
        return;
    }
    
    // Validar tamaño (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('La imagen es demasiado grande. Máximo 16MB.');
        return;
    }
    
    currentImageFile = file;
    
    // Mostrar preview
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        previewContainer.style.display = 'block';
        uploadArea.style.display = 'none';
        analyzeSection.style.display = 'block';
        resultsSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    currentImageFile = null;
    imageInput.value = '';
    previewContainer.style.display = 'none';
    uploadArea.style.display = 'block';
    analyzeSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

async function analyzeImage() {
    if (!currentImageFile) {
        showError('Por favor, selecciona una imagen primero.');
        return;
    }
    
    // Mostrar loading
    analyzeBtn.disabled = true;
    loadingSpinner.style.display = 'block';
    resultsSection.style.display = 'none';
    
    try {
        const formData = new FormData();
        formData.append('image', currentImageFile);
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error en la predicción');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        showError(`Error al analizar la imagen: ${error.message}`);
    } finally {
        analyzeBtn.disabled = false;
        loadingSpinner.style.display = 'none';
    }
}

function displayResults(data) {
    const { prediction, recommendation } = data;
    
    // Actualizar diagnóstico
    document.getElementById('diseaseName').textContent = recommendation.diagnosis;
    document.getElementById('confidenceValue').textContent = recommendation.confidence;
    
    // Actualizar recomendaciones
    document.getElementById('treatmentText').textContent = recommendation.treatment;
    document.getElementById('dosageText').textContent = recommendation.dosage;
    document.getElementById('frequencyText').textContent = recommendation.frequency;
    document.getElementById('preventionText').textContent = recommendation.prevention;
    document.getElementById('organicText').textContent = recommendation.organic_alternative;
    
    // Manejar advertencias
    const warningCard = document.getElementById('warningCard');
    const warningText = document.getElementById('warningText');
    
    if (recommendation.warning) {
        warningText.textContent = recommendation.warning;
        warningCard.style.display = 'flex';
    } else {
        warningCard.style.display = 'none';
    }
    
    // Mostrar resultados
    resultsSection.style.display = 'block';
    
    // Scroll a resultados
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

async function checkSystemHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.model_status === 'loaded') {
            systemStatus.textContent = '✅ Modelo funcionando';
            systemStatus.style.color = '#3bf41aff';
        } else {
            systemStatus.textContent = '⚠️ Modelo no disponible';
            systemStatus.style.color = '#e74c3c';
        }
    } catch (error) {
        systemStatus.textContent = '❌ Error de conexión';
        systemStatus.style.color = '#e74c3c';
    }
}

function showError(message) {
    alert(`Error: ${message}`);
}

// Funciones adicionales para estadísticas
async function getSystemStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        console.log('Estadísticas del sistema:', data);
        return data;
    } catch (error) {
        console.error('Error obteniendo estadísticas:', error);
    }
}

// Exportar para uso global (si es necesario)
window.clearImage = clearImage;
window.analyzeImage = analyzeImage;