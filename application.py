from flask import Flask, render_template, request, url_for, json, send_file, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
ALLOWED_EXTENSIONS = {'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    img_count = 10
    json_url = os.path.join(app.root_path, "static/data", "update.json")
    data = json.load(open(json_url))
    export_dict = {}
    if request.method == 'POST':
        imageID = data["id"]
        imageDelay = data["delay"]
        for x in range(img_count):
            imageName = 'image_' + str(x+1)
            file = request.files[imageName]
            id_name = "id_" + str(x+1)
            delay_name = "delay_" + str(x+1)
            if (request.form[delay_name]):
                imageDelay[x] = float(request.form[delay_name]) * 1e6
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = imageName + ".bmp"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imageID[x] += 1
                if imageID[x] > 255:
                    imageID[x] = 1
        export_dict["id"] = imageID
        export_dict["delay"] = imageDelay
        with open(json_url, 'w') as f:
            #json.dump(request.form, f)
            json.dump(export_dict, f)
        return render_template('index.html', img_count=img_count, data=data)
    if request.method == 'GET':
        return render_template('index.html', img_count=img_count, data=data)
#hide id? and autoupdate
#css to rotate image
#unique image urls - change arduino code to update based on unique file name
# - need json file to display file name


# https://stackoverflow.com/questions/42091097/flask-save-data-from-forms-to-json-file
# https://stackoverflow.com/questions/21133976/flask-load-local-json
# https://stackoverflow.com/questions/54033296/how-to-access-local-file-in-flask
# https://flask.palletsprojects.com/en/1.0.x/api/#flask.send_from_directory
# https://stackoverflow.com/questions/62906140/displaying-json-in-the-html-using-flask-and-local-json-file
# https://stackoverflow.com/questions/40246702/displaying-a-txt-file-in-my-html-using-python-flask
# https://www.reddit.com/r/flask/comments/31kk7n/af_displaying_contents_of_text_file_on_webpage/
# https://stackoverflow.com/questions/20061774/rotate-an-image-in-image-source-in-html
@app.route('/file2.json')
def download_file():
    return send_file("file.json")

@app.route('/update.json')
def test():
    json_url = os.path.join(app.root_path, "static/data", "update.json")
    with open(json_url, "r") as f:
        content = f.read()
    return render_template('content.html', content=content)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS