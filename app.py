from flask import Flask, render_template

from wtform_fields import RegistrationForm

app = Flask(__name__)

app.secret_key = 'replace key later'
url = 'postgres://atybdepvdbtiss:eff908bf955faa4f2363bfca5f52db6fddc399aa15cc609510332bdbcdb6eeaf@ec2-54-220-35-19.eu-west-1.compute.amazonaws.com:5432/d1lqgh91p1te6o'


@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    return render_template('index.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
