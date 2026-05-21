import os
import json
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'premium_night_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

# --- MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True) # Added for specific images

class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Paid')
    items = db.relationship('OrderItem', backref='order', lazy=True)
    user = db.relationship('User', backref='orders')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), db.ForeignKey('order.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    vehicle = db.relationship('Vehicle')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def initialize_database():
    inspector = inspect(db.engine)
    if not inspector.has_table("vehicle"):
        db.create_all()
    else:
        # Check if image_url column exists, if not, add it via raw SQL
        columns = [col['name'] for col in inspector.get_columns('vehicle')]
        if 'image_url' not in columns:
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE vehicle ADD COLUMN image_url VARCHAR(255)"))
                conn.commit()
    
    # Create default admin if not exists
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
        admin_user = User(username='admin', password_hash=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
    
    # Map specific images to specific vehicles
    charger = Vehicle.query.get(2)
    if charger and not charger.image_url:
        charger.image_url = 'images/charger70.jpg'
        
    testarossa = Vehicle.query.get(6)
    if testarossa and not testarossa.image_url:
        testarossa.image_url = 'images/testarossa.jpg'
        
    skyline = Vehicle.query.get(8)
    if skyline and not skyline.image_url:
        skyline.image_url = 'images/skyliner34.jpg'
        
    db.session.commit()

# --- ROUTES: AUTH ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# --- ROUTES: MAIN ---
@app.before_request
def init_cart():
    if 'cart' not in session:
        session['cart'] = []

@app.route('/')
def index():
    search_query = request.args.get('q', '')
    filter_type = request.args.get('type', '')
    filter_brand = request.args.get('brand', '')
    sort_price = request.args.get('sort', '')

    query = Vehicle.query

    if search_query:
        query = query.filter(Vehicle.model.ilike(f'%{search_query}%'))
    if filter_type:
        query = query.filter_by(type=filter_type)
    if filter_brand:
        query = query.filter(Vehicle.brand.ilike(f'%{filter_brand}%'))
    
    if sort_price == 'asc':
        query = query.order_by(Vehicle.price.asc())
    elif sort_price == 'desc':
        query = query.order_by(Vehicle.price.desc())

    vehicles = query.all()
    
    brands = db.session.query(Vehicle.brand).distinct().all()
    brands = [b[0] for b in brands]
    types = db.session.query(Vehicle.type).distinct().all()
    types = [t[0] for t in types]

    return render_template('index.html', vehicles=vehicles, brands=brands, types=types)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Vehicle.query.get_or_404(car_id)
    return render_template('car.html', car=car)

# --- ROUTES: CART & CHECKOUT ---
@app.route('/cart')
def cart():
    cart_items = []
    total_price = 0
    for item_id in session.get('cart', []):
        car = Vehicle.query.get(item_id)
        if car:
            cart_items.append(car)
            total_price += car.price
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/cart/add/<int:car_id>', methods=['POST'])
def add_to_cart(car_id):
    if car_id not in session['cart']:
        session['cart'].append(car_id)
        session.modified = True
        flash('Vehicle added to cart.', 'success')
    else:
        flash('Vehicle is already in your cart.', 'error')
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:car_id>', methods=['POST'])
def remove_from_cart(car_id):
    if car_id in session['cart']:
        session['cart'].remove(car_id)
        session.modified = True
        flash('Vehicle removed from cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if not session.get('cart'):
        flash('Your cart is empty.', 'error')
        return redirect(url_for('index'))
        
    cart_items = [Vehicle.query.get(item_id) for item_id in session['cart']]
    total_price = sum(item.price for item in cart_items if item)

    if request.method == 'POST':
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')
        
        order_id = 'ORD-' + str(uuid.uuid4())[:8].upper()
        
        new_order = Order(
            id=order_id,
            user_id=current_user.id,
            shipping_address=address,
            payment_method=payment_method,
            total_price=total_price,
            status='Paid'
        )
        db.session.add(new_order)
        
        for item in cart_items:
            if item:
                order_item = OrderItem(order_id=order_id, vehicle_id=item.id, price=item.price)
                db.session.add(order_item)
                
        db.session.commit()
        
        session['cart'] = []
        session.modified = True
        
        return redirect(url_for('invoice', order_id=order_id))
        
    return render_template('checkout.html', total_price=total_price)

@app.route('/invoice/<order_id>')
@login_required
def invoice(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))
    return render_template('invoice.html', order=order)

# --- ROUTES: ADMIN ---
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('index'))
    vehicles = Vehicle.query.all()
    return render_template('admin/dashboard.html', vehicles=vehicles)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def admin_add_vehicle():
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        new_vehicle = Vehicle(
            type=request.form.get('type'),
            brand=request.form.get('brand'),
            model=request.form.get('model'),
            year=int(request.form.get('year')),
            price=int(request.form.get('price')),
            image_url=request.form.get('image_url') or None
        )
        db.session.add(new_vehicle)
        db.session.commit()
        flash('Vehicle added successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/vehicle_form.html', vehicle=None)

@app.route('/admin/edit/<int:car_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_vehicle(car_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    vehicle = Vehicle.query.get_or_404(car_id)
    if request.method == 'POST':
        vehicle.type = request.form.get('type')
        vehicle.brand = request.form.get('brand')
        vehicle.model = request.form.get('model')
        vehicle.year = int(request.form.get('year'))
        vehicle.price = int(request.form.get('price'))
        vehicle.image_url = request.form.get('image_url') or None
        db.session.commit()
        flash('Vehicle updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/vehicle_form.html', vehicle=vehicle)

@app.route('/admin/delete/<int:car_id>', methods=['POST'])
@login_required
def admin_delete_vehicle(car_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    vehicle = Vehicle.query.get_or_404(car_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        initialize_database()
    app.run(debug=True)
