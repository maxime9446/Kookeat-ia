from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from io import BytesIO
from PIL import Image, ImageStat
import tensorflow as tf

# Charger le modèle Keras/TensorFlow
model = tf.keras.models.load_model("model.h5")

app = FastAPI()

# Configuration des CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class PredictResponse(BaseModel):
    prediction: str

async def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(await file.read()))
    return image

def replace_transparency(image, dominant_color):
    """
    Remplace les pixels transparents par la couleur dominante ou sa couleur opposée.
    """
    # Si la couleur dominante est plus proche du blanc, utilisez sa couleur opposée pour une meilleure visibilité
    # Sinon, utilisez la couleur dominante elle-même
    if sum(dominant_color) > (255 * 3) / 2:
        fill_color = tuple(255 - c for c in dominant_color)  # Couleur opposée
    else:
        fill_color = dominant_color  # Couleur dominante

    # Remplacer les pixels transparents
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        bg = Image.new("RGB", image.size, fill_color)
        bg.paste(image, mask=alpha)
        return bg
    else:
        return image

def get_dominant_color(image):
    """
    Calcule la couleur dominante des pixels non transparents.
    """
    # Convertir en RGB si nécessaire
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Calculer la couleur moyenne, en excluant les pixels complètement transparents si l'image est RGBA
    stat = ImageStat.Stat(image)
    r, g, b = map(lambda x: int(x / stat.count[0]), stat.sum)
    return (r, g, b)


categories = ['drink', 'food', 'other']  # Liste des catégories possibles

@app.post("/predict/", response_model=PredictResponse)
async def predict(file: UploadFile = File(...)):
    image = await read_imagefile(file)
    # Prétraiter l'image ici (par exemple, redimensionnement, normalisation, etc.)
    # La préparation dépend de la manière dont le modèle a été entraîné
    # Exemple : image = image.resize((224, 224))
    image = image.resize((480, 480))

    dominant_color = get_dominant_color(image)
    image = replace_transparency(image, dominant_color)
    
    # Convertir l'image en un array numpy pour la prédiction
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)  # Faire correspondre la forme attendue par le modèle
    
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction, axis=1)
    predicted_class_label = categories[predicted_class_index[0]]  # Obtenez le label de la catégorie prédite
    
    return {"prediction": predicted_class_label}

@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}
