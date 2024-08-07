from eoms import app
from flask import jsonify
import os
from werkzeug.utils import secure_filename
import eoms.model.db as db

# This module handles file uploading to server

# Config for file upload folder and allowed file format
UPLOAD_FOLDER = './eoms/static/images/product_images'
UPLOAD_FOLDER_FOR_PRODUCT = './eoms/static/images/product'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_FOR_PRODUCT'] = UPLOAD_FOLDER_FOR_PRODUCT

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image_by_product_code(machine_id, product_code, image):
    # Set upload folder using user id 
    # Create the folder if not exist
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(product_code))
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Check if file exists and format meets requirement
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        # Rename file namee using <product_code> format
        filename = f"{machine_id.lower()}.{filename.split('.')[-1]}"
        # Save image file in new folder
        image.save(os.path.join(upload_folder, filename))
        filename = secure_filename(filename)
        # Add image record to db
        cursor = db.get_cursor()
        query = """UPDATE machine
                SET photo = %(image)s
                WHERE machine_id = %(machine_id)s;
                """
        cursor.execute(
            query,
            {
                "machine_id": machine_id,
                "image": filename
            }
        )
        if cursor.rowcount == 1:
            return jsonify({'message': 'success'})
    else:
        return jsonify({'error': 'Something went wrong uploading image'}), 500
    
def upload_product_image(product_code, image):
        # Set upload folder using user id 
        # Create the folder if not exist
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER_FOR_PRODUCT'])
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        # Check if file exists and format meets requirement
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # Rename file namee using <product_code> format
            filename = f"{product_code.lower()}.{filename.split('.')[-1]}"
            # Save image file in new folder
            image.save(os.path.join(upload_folder, filename))
            filename = secure_filename(filename)
            # Add image record to db
            cursor = db.get_cursor()
            query = """UPDATE product
                    SET image = %(image)s
                    WHERE product_code = %(product_code)s;
                    """
            cursor.execute(
                query,
                {
                    "product_code": product_code,
                    "image": filename
                }
            )
            
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})