product_profile_image = request.files['product_profile_image']
product_filename = product_profile_image.filename
if product_filename != '':
    file_ext = os.path.splitext(product_filename)[1]
    if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
        abort(400)
    product_filename.save(os.path.join('static/product_profiles', ))
product_other_images = request.files.getlist('product_other_images')
for product_other_image in product_other_images:
    if product_other_image.filename != '':
        product_other_image.save(product_other_image.filename)
