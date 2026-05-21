from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'premium_rush_secret_night' # Required for session and flash messages

def load_vehicles():
    data_path = os.path.join(app.root_path, 'data', 'vehicles.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def save_vehicles(vehicles):
    data_path = os.path.join(app.root_path, 'data', 'vehicles.json')
    with open(data_path, 'w') as f:
        json.dump(vehicles, f, indent=4)

@app.before_request
def initialize_session():
    if 'balance' not in session:
        session['balance'] = 2000000
    if 'garage' not in session:
        session['garage'] = []

@app.route('/')
def index():
    vehicles = load_vehicles()
    return render_template('index.html', vehicles=vehicles, balance=session['balance'])

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    vehicles = load_vehicles()
    car = next((c for c in vehicles if c['id'] == car_id), None)
    if not car:
        flash("Vehicle not found in the showroom.", "error")
        return redirect(url_for('index'))
    return render_template('car.html', car=car, balance=session['balance'])

@app.route('/buy/<int:car_id>', methods=['POST'])
def buy_car(car_id):
    vehicles = load_vehicles()
    car = next((c for c in vehicles if c['id'] == car_id), None)
    
    if not car:
        flash("Vehicle not found.", "error")
        return redirect(url_for('index'))
        
    if session['balance'] >= car['price']:
        session['balance'] -= car['price']
        
        # We don't remove from the main list so other users/sessions can see it,
        # but in a single-player game you might remove it from the showroom.
        # Since the user agreed to keep it in memory, we'll just add it to garage.
        session['garage'].append(car)
        session.modified = True
        
        flash(f"Transaction successful! You now own the {car['brand']} {car['model']}.", "success")
        
        # If we really want to remove from showroom, we'd update vehicles.json
        # vehicles.remove(car)
        # save_vehicles(vehicles)
        
        return redirect(url_for('garage'))
    else:
        flash("Insufficient funds. You cannot afford this vehicle.", "error")
        return redirect(url_for('car_detail', car_id=car_id))

@app.route('/garage')
def garage():
    return render_template('garage.html', garage=session['garage'], balance=session['balance'])

if __name__ == '__main__':
    app.run(debug=True)
