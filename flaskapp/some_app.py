from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import net as neuronet
from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json
import lxml.etree as ET

app = Flask(__name__)

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfV7JkrAAAAAE3icdT__B7p__-FXBoGNNWyJZzl'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfV7JkrAAAAAKAiVNyOWd9aS3EufwYJ4RZmqeI8'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}


bootstrap = Bootstrap(app)
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные, если они не введены
 # или неверны
 openid = StringField('openid', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.



@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

@app.route("/apixml",methods=['GET', 'POST'])
def apixml():
 #парсим xml файл в dom
 dom = ET.parse("./static/xml/file.xml")
 # парсим шаблон в dom
 xslt = ET.parse("./static/xml/file.xslt")
 # получаем трансформер
 transform = ET.XSLT(xslt)
 # преобразуем xml с помощью трансформера xslt
 newhtml = transform(dom)
 # преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
 strfile = ET.tostring(newhtml)
 return strfile

@app.route("/data_to")
def data_to():
 some_pars = {'user': 'Ivan', 'color': 'red'}
 some_str = 'Hello my dear friends!'
 some_value = 10
 return render_template('simple.html',some_str = some_str, some_value = some_value,some_pars=some_pars)

@app.route("/apinet",methods=['GET', 'POST'])
def apinet():
 neurodic = {}
 # проверяем, что в запросе json данные
 if request.mimetype == 'application/json':
  # получаем json данные
  data = request.get_json()
  # берем содержимое по ключу, где хранится файл
  # закодированный строкой base64
  # декодируем строку в массив байт, используя кодировку utf-8
  # первые 128 байт ascii и utf-8 совпадают, потому можно
  filebytes = data['imagebin'].encode('utf-8')
  # декодируем массив байт base64 в исходный файл изображение
  cfile = base64.b64decode(filebytes)
  # чтобы считать изображение как файл из памяти, используем BytesIO
  img = Image.open(BytesIO(cfile))
  decode = neuronet.getresult([img])
  neurodic = {}
  for elem in decode:
   neurodic[elem[0][1]] = str(elem[0][2])
   print(elem)
 # пример сохранения переданного файла
 # handle = open('./static/f.png','wb')
 # handle.write(cfile)
 # handle.close()
 # преобразуем словарь в json-строку
 ret = json.dumps(neurodic)
 # готовим ответ пользователю
 resp = Response(response=ret,
 status=200,
 mimetype="application/json")
 # возвращаем ответ
 return resp

@app.route("/net", methods=['GET', 'POST'])
def net():
    form = NetForm()
    filename = None
    neurodic = {}

    if form.validate_on_submit():
        # Сохраняем загруженный файл
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        form.upload.data.save(filename)

        # Открываем только что загруженное изображение
        img = Image.open(filename)

        # Передаем ОДНО изображение в нейросеть (в списке)
        decode = neuronet.getresult([img])

        # Очищаем и заполняем словарь результатами
        neurodic.clear()
        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]

    return render_template('net.html', form=form, image_name=filename, neurodic=neurodic)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)