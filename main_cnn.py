from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import io
#from PIL import Image

app = FastAPI()

origins = [
    "http://192.168.239.116:20213",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ambil_gambar(binary_image, max_size=500, show=False):
    input_image = load_img(io.BytesIO(binary_image), target_size=(150, 150))
    img_tensor = img_to_array(input_image)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    return img_tensor

def mapping_pred(x: float, in_min: float, in_max: float, out_min: int, out_max: int):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

@app.get('/status')
async def status():
    return dict(msg='OK')

@app.post('/diagnosa-stroke')
async def main(file: bytes = File(...)):

    # print(str(file))

    model = load_model("model_cnn.h5")
    new_image = ambil_gambar(file)

    pred = model.predict(new_image)

    prediksi = 'Tidak Terindikasi Stroke'
    if pred[0][0] >= 0.5:
        prediksi = 'Terindikasi Stroke'

    persen = int(mapping_pred(pred[0][0], 0.0, 1.0, 0, 100))

    return JSONResponse(content={"message": prediksi, "percentage": persen}, status_code=200)

#if __name__ == "__main__":
 #   import uvicorn
  #  uvicorn.run(app, host="10.0.40.105", port=8080)
