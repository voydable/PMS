import datetime


class Vehicle:
    def __init__(self, license_plate, owner):
        self.license_plate = license_plate
        self.owner = owner
        self.entry_time = None
        self.exit_time = None


class User:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.vehicles = []

    def add_vehicle(self):
        license_plate = input("Enter your vehicle's license plate number: ")
        vehicle = Vehicle(license_plate, self)
        self.vehicles.append(vehicle)
        print(f"Vehicle with license plate {license_plate} has been added for {self.name}.")


class ParkingSpace:
    def __init__(self, space_id):
        self.space_id = space_id
        self.occupied = False
        self.vehicle = None
        self.reservation = None

    def occupy(self, vehicle):
        if not self.occupied:
            self.occupied = True
            self.vehicle = vehicle
            vehicle.entry_time = datetime.datetime.now()
            print(f"Space {self.space_id} occupied by {vehicle.license_plate}")
        else:
            print(f"Space {self.space_id} is already occupied.")

    def vacate(self):
        if self.occupied:
            self.vehicle.exit_time = datetime.datetime.now()
            print(f"Space {self.space_id} vacated by {self.vehicle.license_plate}")
            self.occupied = False
            self.vehicle = None
        else:
            print(f"Space {self.space_id} is already vacant.")

    def reserve(self, reservation):
        if not self.occupied:
            self.reservation = reservation
            print(f"Space {self.space_id} reserved for {reservation.user.name}")
        else:
            print(f"Space {self.space_id} is already occupied and cannot be reserved.")


class Reservation:
    def __init__(self, user2, start_time, end_time):
        self.user = user2
        self.start_time = start_time
        self.end_time = end_time
        self.payment = None


class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.spaces = [ParkingSpace(i) for i in range(1, capacity + 1)]
        self.occupied_spaces = 0
        self.users = []
        self.pricing_model = DynamicPricing()

    def park_vehicle(self):
        if not self.users:
            print("No registered users found. Please register first.")
            return

        user_name = input("Enter your name: ")
        user3 = next((u for u in self.users if u.name == user_name), None)

        if not user3:
            print("User not found. Please register first.")
            return

        if not user3.vehicles:
            print("You have no vehicles associated with your account. Please add a vehicle first.")
            return

        vehicle = user3.vehicles[0]

        for space in self.spaces:
            if not space.occupied:
                space.occupy(vehicle)
                self.occupied_spaces += 1
                print(f"Space {space.space_id} occupied by {vehicle.license_plate}")
                return

        print("Parking lot is full.")

    def vacate_space(self, space_id):
        space = self.spaces[space_id - 1]
        space.vacate()
        self.occupied_spaces -= 1

    def get_available_spaces(self):
        return self.capacity - self.occupied_spaces

    def get_occupied_spaces(self):
        return self.occupied_spaces

    def register_user(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        user2 = User(name, email, phone)
        self.users.append(user2)
        print(f"{name} has been registered as a user.")
        return user2

    def make_reservation(self, user2):
        start_time = input("Enter the start time for your reservation (YYYY-MM-DD HH:MM): ")
        end_time = input("Enter the end time for your reservation (YYYY-MM-DD HH:MM): ")
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        reservation = Reservation(user2, start_time, end_time)
        for space in self.spaces:
            if not space.occupied:
                space.reserve(reservation)
                return
        print("No available spaces for reservation.")

    def process_payment(self, vehicle):
        duration = vehicle.exit_time - vehicle.entry_time
        amount = self.pricing_model.calculate_fee(duration)
        payment = Payment(amount)
        print(f"Payment of {amount} processed for {vehicle.license_plate}")
        return payment


class DynamicPricing:
    def __init__(self):
        self.base_rate = 5  # Base rate per hour
        self.peak_multiplier = 2  # Multiplier during peak hours
        self.peak_hours = [(9, 17)]  # Peak hours range (9 AM - 5 PM)

    def calculate_fee(self, duration):
        total_hours = duration.total_seconds() / 3600
        fee = total_hours * self.base_rate
        for start, end in self.peak_hours:
            if duration.start.hour >= start and duration.end.hour < end:
                fee *= self.peak_multiplier
        return fee


class Payment:
    def __init__(self, amount):
        self.amount = amount
        self.timestamp = datetime.datetime.now()
        self.status = "Completed"


class AnalyticsEngine:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

    def generate_occupancy_report(self):
        occupancy_data = []
        for space in self.parking_lot.spaces:
            if space.vehicle:
                occupancy_data.append({
                    "space_id": space.space_id,
                    "license_plate": space.vehicle.license_plate,
                    "entry_time": space.vehicle.entry_time
                })
        return occupancy_data

    def generate_revenue_report(self):
        revenue = 0
        for space in self.parking_lot.spaces:
            if space.vehicle and space.vehicle.exit_time:
                duration = space.vehicle.exit_time - space.vehicle.entry_time
                amount = self.parking_lot.pricing_model.calculate_fee(duration)
                revenue += amount
        return revenue

    def generate_occupancy_report1(self, start_time, end_time):
        occupancy_data = []
        for space in self.parking_lot.spaces:
            if space.vehicle:
                entry_time = space.vehicle.entry_time
                exit_time = space.vehicle.exit_time or datetime.datetime.now()
                if entry_time >= start_time and exit_time <= end_time:
                    occupancy_data.append({
                        "space_id": space.space_id,
                        "entry_time": entry_time,
                        "exit_time": exit_time
                    })
        return occupancy_data

    def generate_revenue_report1(self, start_time, end_time):
        revenue = 0
        for space in self.parking_lot.spaces:
            if space.vehicle:
                entry_time = space.vehicle.entry_time
                exit_time = space.vehicle.exit_time
                if exit_time and start_time <= exit_time <= end_time:
                    duration = exit_time - entry_time
                    amount = self.parking_lot.pricing_model.calculate_fee(duration)
                    revenue += amount
        return revenue


def main():
    global user
    print("Welcome to the Parking Management System!")
    capacity = int(input("Enter the capacity of the parking lot: "))
    parking_lot = ParkingLot(capacity)

    while True:
        print("\nSelect an option:")
        print("1. Register as a user")
        print("2. Add a vehicle")
        print("3. Park a vehicle")
        print("4. Vacate a parking space")
        print("5. Make a reservation")
        print("6. View available spaces")
        print("7. View occupied spaces")
        print("8. Generate occupancy report")
        print("9. Generate revenue report")
        print("0. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            user = parking_lot.register_user()
        elif choice == 2:
            if not parking_lot.users:
                print("No registered users found. Please register first.")
            else:
                user_name = input("Enter your name: ")
                user = next((u for u in parking_lot.users if u.name == user_name), None)
                if user:
                    user.add_vehicle()
                else:
                    print("User not found. Please register first.")
        elif choice == 3:
            parking_lot.park_vehicle()
        elif choice == 4:
            while True:
                try:
                    space_id = int(input("Enter the space ID to vacate: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid space ID (integer).")

            if 1 <= space_id <= capacity:
                parking_lot.vacate_space(space_id)
            else:
                print("Invalid space ID. Please enter a space ID between 1 and ", capacity)

        elif choice == 5:
            if not parking_lot.users:
                print("No registered users found. Please register first.")
            else:
                user_name = input("Enter your name: ")
                user = next((u for u in parking_lot.users if u.name == user_name), None)
                if user:
                    parking_lot.make_reservation(user)
                else:
                    print("User not found. Please register first.")
        elif choice == 6:
            print("Available spaces:", parking_lot.get_available_spaces())
        elif choice == 7:
            print("Occupied spaces:", parking_lot.get_occupied_spaces())
        elif choice == 8:
            analytics_engine = AnalyticsEngine(parking_lot)
            occupancy_report = analytics_engine.generate_occupancy_report1()
            print("\nOccupancy Report:")
            for data in occupancy_report:
                print(
                    f"Space ID: {data['space_id']}, License Plate: {data['license_plate']}, Entry Time: {data['entry_time']}")
        elif choice == 9:
            analytics_engine = AnalyticsEngine(parking_lot)
            revenue = analytics_engine.generate_revenue_report1()
            print(f"\nRevenue Report:\nTotal Revenue: {revenue}")

        elif choice == 0:
            break


if __name__ == "__main__":
    main()
