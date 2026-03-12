import sys
import time
import os
from playsound3 import playsound

def typewriter_effect(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    audio_file_path = os.path.join(current_directory, 'Clair de Lune.mp3')

    playsound(audio_file_path, block=False)

    vehicles_data = [
        {"id": 1, "type": "Tuner", "brand": "Mitsubishi", "model": "Lancer Evolution IX MR", "year": 2005, "price": 45000},
        {"id": 2, "type": "Muscle", "brand": "Dodge", "model": "Charger R/T", "year": 1970, "price": 65000},
        {"id": 3, "type": "Exotic", "brand": "Lamborghini", "model": "Gallardo Superleggera", "year": 2007, "price": 500000},
        {"id": 4, "type": "Muscle", "brand": "Ford", "model": "Mustang GT", "year": 1969, "price": 60000},
        {"id": 5, "type": "Tuner", "brand": "Subaru", "model": "Impreza WRX STI", "year": 2006, "price": 35000},
        {"id": 6, "type": "Exotic", "brand": "Ferrari", "model": "Testarossa", "year": 1985, "price": 250000},
        {"id": 7, "type": "Muscle", "brand": "Chevrolet", "model": "Chevelle SS", "year": 1970, "price": 70000},
        {"id": 8, "type": "Tuner", "brand": "Nissan", "model": "Skyline GT-R R34", "year": 1999, "price": 50000},
        {"id": 9, "type": "Exotic", "brand": "Porsche", "model": "Carrera GT", "year": 2003, "price": 250000},
        {"id": 10, "type": "Muscle", "brand": "Pontiac", "model": "GTO Judge", "year": 1969, "price": 65000},
        {"id": 11, "type": "Tuner", "brand": "Mazda", "model": "RX-7 FD", "year": 1992, "price": 40000},
        {"id": 12, "type": "Exotic", "brand": "McLaren", "model": "F1", "year": 1993, "price": 1000000},
        {"id": 13, "type": "Muscle", "brand": "Dodge", "model": "Challenger R/T", "year": 1971, "price": 70000},
        {"id": 14, "type": "Tuner", "brand": "Toyota", "model": "Supra MK4", "year": 1993, "price": 50000},
        {"id": 15, "type": "Exotic", "brand": "Bugatti", "model": "Veyron", "year": 2005, "price": 900000},
        {"id": 16, "type": "Muscle", "brand": "Chevrolet", "model": "Camaro SS", "year": 1969, "price": 75000},
        {"id": 17, "type": "Tuner", "brand": "Honda", "model": "Civic Type R EK9", "year": 1997, "price": 30000},
        {"id": 18, "type": "Exotic", "brand": "Pagani", "model": "Zonda F", "year": 2006, "price": 500000},
        {"id": 19, "type": "Muscle", "brand": "Ford", "model": "Shelby GT500", "year": 1967, "price": 85000},
        {"id": 20, "type": "Tuner", "brand": "Mitsubishi", "model": "Eclipse GSX", "year": 1995, "price": 25000},
        {"id": 21, "type": "Muscle", "brand": "Plymouth", "model": "Hemi Cuda", "year": 1970, "price": 105000},
        {"id": 22, "type": "Muscle", "brand": "Plymouth", "model": "Road Runner", "year": 1970, "price": 65000},
        {"id": 23, "type": "Tuner", "brand": "Nissan", "model": "350Z", "year": 2003, "price": 32000},
        {"id": 24, "type": "Tuner", "brand": "Nissan", "model": "240SX (S13)", "year": 1989, "price": 18000},
        {"id": 25, "type": "Tuner", "brand": "Honda", "model": "NSX", "year": 1992, "price": 65000},
        {"id": 26, "type": "Tuner", "brand": "Acura", "model": "Integra Type R", "year": 1999, "price": 20000},
        {"id": 27, "type": "Tuner", "brand": "Infiniti", "model": "G35", "year": 2003, "price": 30000},
        {"id": 28, "type": "Exotic", "brand": "Porsche", "model": "911 GT2", "year": 2008, "price": 300000},
        {"id": 29, "type": "Tuner", "brand": "Volkswagen", "model": "Golf GTI", "year": 2005, "price": 24000},
        {"id": 30, "type": "Tuner", "brand": "Lexus", "model": "IS-F", "year": 2008, "price": 58000},
        {"id": 31, "type": "Tuner", "brand": "Toyota", "model": "Corolla GT-S (AE86)", "year": 1986, "price": 15000},
        {"id": 32, "type": "Muscle", "brand": "Dodge", "model": "Viper SRT10", "year": 2006, "price": 90000},
        {"id": 33, "type": "Exotic", "brand": "Aston Martin", "model": "DB9", "year": 2003, "price": 150000},
        {"id": 34, "type": "Exotic", "brand": "Lotus", "model": "Elise", "year": 2005, "price": 45000},
        {"id": 35, "type": "Muscle", "brand": "Pontiac", "model": "GTO", "year": 2005, "price": 35000},
        {"id": 36, "type": "Tuner", "brand": "Mazda", "model": "RX-8", "year": 2004, "price": 30000},
        {"id": 37, "type": "Exotic", "brand": "Mercedes-Benz", "model": "SLR McLaren", "year": 2003, "price": 450000},
        {"id": 38, "type": "Tuner", "brand": "Honda", "model": "S2000", "year": 2000, "price": 25000},
        {"id": 39, "type": "Tuner", "brand": "Nissan", "model": "Silvia S15", "year": 2002, "price": 20000},
        {"id": 40, "type": "Muscle", "brand": "Chevrolet", "model": "Corvette Z06", "year": 2006, "price": 100000},
        {"id": 41, "type": "Muscle", "brand": "Chevrolet", "model": "Camaro Concept", "year": 2006, "price": 50000},
        {"id": 42, "type": "Tuner", "brand": "Nissan", "model": "GT-R (R35)", "year": 2007, "price": 80000},
        {"id": 43, "type": "Exotic", "brand": "BMW", "model": "M3 E46", "year": 2001, "price": 45000},
        {"id": 44, "type": "Exotic", "brand": "BMW", "model": "M3 E92", "year": 2007, "price": 65000},
        {"id": 45, "type": "Tuner", "brand": "Mitsubishi", "model": "Lancer Evolution X", "year": 2008, "price": 40000},
        {"id": 46, "type": "Exotic", "brand": "BMW", "model": "M3 GTR (NFS Hero Edition)", "year": 2001, "price": 1500000},
        {"id": 47, "type": "Tuner", "brand": "Nissan", "model": "Skyline GT-R R34 (Mantis)", "year": 1999, "price": 350000},
        {"id": 48, "type": "Muscle", "brand": "Chevrolet", "model": "Chevelle Malibu (The Driver Edition)", "year": 1973, "price": 120000},
        {"id": 49, "type": "Muscle", "brand": "Ford", "model": "Mustang GT (Razor Custom)", "year": 2005, "price": 200000},
        {"id": 50, "type": "Exotic", "brand": "Audi", "model": "R8 (Le Mans Quattro)", "year": 2006, "price": 400000}
    ]

    player_balance = 2000000
    purchased_cars = []

    typewriter_effect("Welcome to the Premium Motor Deluxe.")
    typewriter_effect("If you want to buy a vehicle, you can check the View Showroom menu in order to get the Vehicle ID")
    
    while True:
        typewriter_effect("\n" + "=" * 55)
        typewriter_effect(f"Current Balance: ${player_balance:,}")
        typewriter_effect("1. View Showroom")
        typewriter_effect("2. Buy a Vehicle")
        typewriter_effect("3. View Vehicle Information")
        typewriter_effect("4. View Personal Garage")
        typewriter_effect("5. Leave Showroom")
        typewriter_effect("=" * 55)

        try:
            choice = int(input("\nEnter your choice (1/2/3/4/5): "))
            
            if choice == 1:
                typewriter_effect("\n" + "-" * 55)
                if len(vehicles_data) == 0:
                    typewriter_effect("The showroom is currently empty.")
                else:
                    for vehicle in vehicles_data:
                        print(f"[{vehicle['id']}] {vehicle['brand']} {vehicle['model']} - ${vehicle['price']:,}")
                typewriter_effect("-" * 55)
                time.sleep(1)
                
            elif choice == 2:
                car_id = int(input("Enter the vehicle ID you want to buy: "))
                selected_car = None
                
                for vehicle in vehicles_data:
                    if vehicle["id"] == car_id:
                        selected_car = vehicle
                        break
                        
                if selected_car:
                    confirm = input(f"Are you sure you want to buy the {selected_car['brand']} {selected_car['model']} for ${selected_car['price']:,}? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        if player_balance >= selected_car["price"]:
                            player_balance -= selected_car["price"]
                            typewriter_effect(f"\nTransaction successful! You now own the {selected_car['brand']} {selected_car['model']}.")
                            purchased_cars.append(selected_car)
                            vehicles_data.remove(selected_car)
                        else:
                            typewriter_effect("\nInsufficient funds. You cannot afford this vehicle.")
                    else:
                        typewriter_effect("\nTransaction cancelled.")
                else:
                    typewriter_effect("\nVehicle not found in the showroom.")
                    
            elif choice == 3:
                car_id = int(input("Enter the vehicle ID you want to inspect: "))
                selected_car = None
                
                for vehicle in vehicles_data:
                    if vehicle["id"] == car_id:
                        selected_car = vehicle
                        break
                        
                if selected_car:
                    typewriter_effect("\n" + "-" * 55)
                    typewriter_effect("VEHICLE INFORMATION")
                    typewriter_effect(f"Brand: {selected_car['brand']}")
                    typewriter_effect(f"Model: {selected_car['model']}")
                    typewriter_effect(f"Year: {selected_car['year']}")
                    typewriter_effect(f"Class: {selected_car['type']}")
                    typewriter_effect(f"Price: ${selected_car['price']:,}")
                    
                    if selected_car["type"] == "Tuner":
                        typewriter_effect("Description: Highly customizable and nimble. Perfect for tight corners and street racing.")
                    elif selected_car["type"] == "Muscle":
                        typewriter_effect("Description: Raw V8 power and heavy chassis. Dominates in straight-line acceleration and drag strips.")
                    elif selected_car["type"] == "Exotic":
                        typewriter_effect("Description: Million-dollar engineering. Incredible top speed and breathtaking aerodynamic design.")
                    typewriter_effect("-" * 55)
                    time.sleep(1)
                else:
                    typewriter_effect("\nVehicle not found in the showroom.")
                    
            elif choice == 4:
                typewriter_effect("\n" + "-" * 55)
                typewriter_effect("=== YOUR PERSONAL GARAGE ===")
                if len(purchased_cars) == 0:
                    typewriter_effect("Your garage is currently empty. Go buy some cars!")
                else:
                    for car in purchased_cars:
                        typewriter_effect(f"- {car['brand']} {car['model']} ({car['year']}) - [{car['type']}]")
                typewriter_effect("-" * 55)
                time.sleep(1)

            elif choice == 5:
                typewriter_effect("\n" + "=" * 55)
                typewriter_effect("Leaving the showroom...")
                typewriter_effect("Vehicles parked in your garage:")
                
                if len(purchased_cars) == 0:
                    typewriter_effect("- You didn't buy any vehicles today.")
                else:
                    for car in purchased_cars:
                        typewriter_effect(f"- {car['brand']} {car['model']} ({car['year']})")
                        
                typewriter_effect("\nThank you for visiting. Enjoy the night drive.")
                sys.exit()
                
            else:
                typewriter_effect("\nInvalid input. Please select a valid option.")
                
        except ValueError:
            typewriter_effect("\nSystem Error: Numerical input required.")

if __name__ == "__main__":
    main()