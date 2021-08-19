from minimart.dashboard import dashboard
from flask import render_template, redirect, url_for
from flask_login import login_required


@dashboard.route('')
@login_required
def main():
    return 'DASHBOARD'
