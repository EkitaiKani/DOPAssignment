from werkzeug.security import generate_password_hash

password1 = generate_password_hash('password1')
password2 = generate_password_hash('password2')
adminpassword = generate_password_hash('supersecretpassword')

print(password1)
print(password2)
print(adminpassword)