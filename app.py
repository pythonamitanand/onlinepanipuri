
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from pyngrok import ngrok

app = Flask(__name__)
app.secret_key = 'MYONLINEPANIPURI08012025'
db = Database()

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    plates = int(request.form.get('plates', 0))
    total_amount = plates * 50  # Assuming ₹50 per plate
    return render_template('checkout.html', plates=plates, total_amount=total_amount)

@app.route('/place_order', methods=['POST'])
def place_order():
    mobile = request.form.get('mobile')
    address = request.form.get('address')
    plates = int(request.form.get('plates'))
    total_amount = plates * 50

    print(address)
    

    order_id = db.place_order(mobile, address, plates, total_amount)
    flash('Order placed successfully! Your order ID is: ' + str(order_id))
    return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == "admin" and password == "12345":  # Replace with secure authentication
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    orders = db.get_orders()
    return render_template('admin_dashboard.html', orders=orders)

@app.route('/admin/update_order_status/<int:order_id>/<status>')
@admin_required
def update_order_status(order_id, status):
    db.update_order_status(order_id, status)
    flash('Order status updated successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_payment_status/<int:order_id>/<status>')
@admin_required
def update_payment_status(order_id, status):
    db.update_payment_status(order_id, status)
    flash('Payment status updated successfully!')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

public_url = ngrok.connect(5000)
print(f" * Public URL: {public_url}")    
