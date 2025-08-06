
from flask import Flask, render_template, request, redirect, send_file, url_for
import os
from werkzeug.utils import secure_filename
from colorizer import colorize_image

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            output_path = colorize_image(filepath)
            
            # Convert paths to URL paths for templates
            input_url = url_for('static', filename=f'uploads/{filename}')
            output_filename = os.path.basename(output_path)
            output_url = url_for('static', filename=f'uploads/{output_filename}')
            
            return render_template('result.html', input_image=input_url, output_image=output_url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
