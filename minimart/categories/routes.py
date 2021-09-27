from datetime import datetime

from flask import render_template, request, redirect, current_app, url_for
from flask_login import login_required, current_user

from minimart import csrf
from minimart.models import db, Category
from minimart.categories import categories


@csrf.include
@login_required
@categories.route('/post', methods=['GET', 'POST'])
def create_category():
    title = 'Minimart - Create'
    year = datetime.utcnow().year
    if current_user.get_role() == 'user':
        return render_template('no_permission.html', title=title, year=year)
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category_description = request.form.get('category_description')

        category = Category(name=category_name, description=category_description)
        db.session.add(category)
        db.session.commit()
        redirect(url_for('categories.categories_list'))
    return render_template('categories/create_category.html', title=title, year=year)


@login_required
@categories.route('/get', methods=['GET', 'POST'])
def categories_list():
    title = 'Minimart - List'
    year = datetime.utcnow().year
    if current_user.get_role() == 'user':
        return render_template('no_permission.html', title=title, year=year)
    return render_template('categories_list.html', title=title, year=year)


@csrf.include
@login_required
@categories.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_category(id):
    title = 'Minimart - Delete'
    year = datetime.utcnow().year
    if current_user.get_role() == 'user':
        return render_template('no_permission.html', title=title, year=year)
    if request.method == 'POST':
        category = Category.query.filter_by(id=id).first()
    return render_template('delete_category.html', title=title, year=year)


@csrf.include
@login_required
@categories.route('/patch/<int:id>')
def update_category(id):
    title = 'Minimart - Patch'
    year = datetime.utcnow().year
    if current_user.get_role() == 'user':
        return render_template('no_permission.html', title=title, year=year)
    if request.method == 'POST':
        category = Category.query.filter_by(id=id).first()
        category_name = request.form.get('category_name')
        category_description = request.form.get('category_description')
    return render_template('update_category.html', title=title, year=year)
