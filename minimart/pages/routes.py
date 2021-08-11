from datetime import datetime

from flask import render_template

from minimart.pages import pages


@pages.route('/', methods=['GET'])
def home():
    title = 'Minimart - Home'
    year = datetime.utcnow().year
    return render_template('pages/home.html', title=title, year=year)

@pages.route('/about-us', methods=['GET'])
def about_us():
    title = 'Minimart - About us'
    year = datetime.utcnow().year
    return render_template('pages/about_us.html', title=title, year=year)


