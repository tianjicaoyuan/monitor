from flask import request, Flask,render_template
import os, subprocess
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

class AddCamera(FlaskForm):
    netWorkName = StringField('networkName', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('next')


@app.route('/camera', methods=['GET'])
def camera():
    name="http://www.baidu.com/"
    return render_template('test.html', name=name)


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['video']
    cameraName = request.form['cameraname']
    videoPath = request.form['videoPath']
    if upload_file:
        filename = cameraName + videoPath
        picpath = os.path.join('F:/flasky/app/static/uploads/', filename)
        f = open(picpath+'.h264', 'wb')
        f.write(upload_file.read())
        f.close()
        subprocess.call("D:/soft/ffmpeg/bin/ffmpeg.exe -i %s %s" % (picpath+'.h264', picpath+'.mp4'), shell=True)
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def addCamera():
    form = AddCamera()
    filePath="/etc/wpa_supplicant/wpa_supplicant.conf"
    if form.validate_on_submit():
        subprocess.call('echo network={ >> %s' % (filePath), shell=True)
        subprocess.call('echo \tssid="%s" >> %s' % (form.netWorkName, filePath), shell=True)
        subprocess.call('echo \tkey_mgmt=WPA-PSK >> %s' % (filePath), shell=True)
        subprocess.call('echo \tpsk="%s" >> %s' % (form.password, filePath), shell=True)
        subprocess.call('echo } >> %s' % (filePath), shell=True)
        subprocess.call("sudo mv /etc/network/interfaces /etc/network/interfaces1", shell=True)
        subprocess.call("sudo mv /etc/network/interfaces2 /etc/network/interfaces", shell=True)
        subprocess.call("sudo mv /etc/network/interfaces1 /etc/network/interfaces2", shell=True)
        subprocess.call("sudo mv /etc/dhcpcd.conf /etc/dhcpcd1.conf", shell=True)
        subprocess.call("sudo mv /etc/dhcpcd2.conf /etc/dhcpcd.conf", shell=True)
        subprocess.call("sudo mv /etc/dhcpcd1.conf /etc/dhcpcd2.conf", shell=True)
        subprocess.call("sudo reboot", shell=True)
    return render_template('Camera.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)