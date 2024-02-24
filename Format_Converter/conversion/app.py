from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        image = Image.open(file.stream)
        pdf_io = io.BytesIO()
        # Assuming the image can be directly converted to PDF without needing to specify page dimensions.
        image.convert('RGB').save(pdf_io, 'PDF', resolution=100.0)
        pdf_io.seek(0)
        # Correct use of download_name instead of attachment_filename
        return send_file(pdf_io, as_attachment=True, download_name='converted.pdf')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

if __name__ == '__main__':
    app.run(debug=True)
