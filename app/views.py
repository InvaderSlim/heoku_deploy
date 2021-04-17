"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from .forms import UploadForm
import pickle
import pandas as pd


conscientiousness = pickle.load(open('models/Conscientiousness.pkl', 'rb'))
agree = pickle.load(open('models/agreeableness.pkl', 'rb'))
emotional = pickle.load(open('models/emotionalStability.pkl', 'rb'))
extraversion = pickle.load(open('models/extraversion.pkl', 'rb'))
intellect = pickle.load(open('models/intellectImagination.pkl', 'rb'))



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    root_dir = os.getcwd()
    # Instantiate your form class
    form = UploadForm()

    # Validate file upload on submit
    if request.method == 'POST' and form.validate_on_submit():
    # if request.method == 'POST':
        # Get file data and save to your uploads folder
        cf = form.upload.data
        # filename = secure_filename(cf.filename)

        data = pd.read_csv(cf)
        X = data.drop(labels=["Extraversion","Emotional_Stability","Conscientiousness","Intellect_Imagination"], axis=1)
        
        pred_consc = conscientiousness.predict(X)
        pred_agree = agree.predict(X)
        pred_emotion = emotional.predict(X)
        pred_extra = extraversion.predict(X)
        pred_intellect = intellect.predict(X)

        # if filename != '':
        #     file_ext = os.path.splitext(filename)[1]
        #     if file_ext not in app.config['ALLOWED_EXTENSIONS']:
        #         flash('Invalid format, try again')
        
        # cf.save(os.path.join( 
        #     root_dir, app.config['UPLOAD_FOLDER'], filename
        # ))
        flash('Successful', 'success')
        # return redirect(url_for('home'))
        return render_template('home.html',
         pred_data_c = 'Predicted Conscientiousness is {}'.format(pred_consc),
          pred_data_a = 'Predicted Agreeableness is {}'.format(pred_agree),
          pred_data_em = 'Predicted Emotional Stability is {}'.format(pred_emotion),
          pred_data_ex = 'Predicted Extraversion is {}'.format(pred_extra),
          pred_data_i = 'Predicted Intellect Imagination is {}'.format(pred_intellect)
          )          

    if request.method == 'GET':
        return render_template('upload.html', form=form)

    return render_template('upload.html', 
        form=form,
        template="form-template")


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
