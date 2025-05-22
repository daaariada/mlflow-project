import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import mlflow
import mlflow.pyfunc

# Настройки
UPLOAD_FOLDER = 'app/static/output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

mlflow.set_tracking_uri("file:///mlruns")
mlflow.set_experiment("YOLOv8 Object Detection")
mlflow.set_experiment_tags({"description": "Object detection with YOLOv8"})

model = YOLO("yolo11n.pt")  # pretrained YOLO11n model

# Инициализация Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Функция проверки расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Проверяем, загрузил ли пользователь файл
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Сохраняем файл
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            results = model([input_path])  # return a list of Results objects
            print(input_path)

            # Сначала создаем output_path
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'negative_' + filename)
            
            for result in results:
                boxes = result.boxes
                masks = result.masks
                keypoints = result.keypoints
                probs = result.probs
                obb = result.obb
                result.show()
                result.save(filename=f"{output_path}")

            # Теперь можно логировать в MLflow
            with mlflow.start_run():
                mlflow.log_param("model", "YOLOv8n")
                mlflow.log_param("input_image", filename)
                mlflow.log_artifact(output_path, artifact_path="processed_images")
                mlflow.log_metric("detected_objects", len(results[0].boxes))
                mlflow.log_metric("inference_time_ms", results[0].speed["inference"])

            return render_template('index.html', original_image=filename, processed_image='negative_' + filename)

    return render_template('index.html', original_image=None, processed_image=None)

# Отдаём файл для скачивания
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Запуск приложения
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
