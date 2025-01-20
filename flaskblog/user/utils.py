
import os
import secrets
from flask import url_for
from flask_mail import Message
from flaskblog import mail
from flask import current_app
from PIL import Image


def save_picture(form_picture):
 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    output_size= (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # Save the uploaded file
    i.save(picture_path)
    return picture_fn



def send_resetEmail(user):
    
        token = user.get_reset_token()
        msg = Message("Password Reset Request", sender='noreply@demo.com',
                    recipients=[user.email])
        msg.html = f''' <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
        <title>Password Reset</title>
      </head>
      <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f7ff;">
        <div style="max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden;">
          <header style="background-color: #4CAF50; padding: 20px; text-align: center; color: white; font-size: 24px;">
            Password Reset Request
          </header>
          <main style="padding: 20px;  text-align: center;">
            <p style='text-align: center;' >Hi {user.username},</p>
            <p style='text-align: center;' >We received a request to reset your password. Click the link below to reset it:</p>
            <a href="{url_for('users.reset_token', token=token, _external=True)}" style="display: inline-block; margin: 20px 0; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; text-align: center;">Reset Password</a>
            <p>If you did not request this, please ignore this email and your password will remain unchanged.</p>
          </main>
          <footer style="background-color: #f1f1f1; padding: 10px; text-align: center; font-size: 12px;">
            
            <p>&copy; 2024 Flask Blog. All rights reserved.</p>
          </footer>
        </div>
      </body>
    </html>
        '''

        mail.send(msg)
 