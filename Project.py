import io
import datetime

rooms = []
bookings = []
guests = []
running = True


def getRoomByNumber(num):
    for room in rooms:
        if room.room_number == num:
            return room


def getGuestById(guest_id):
    for guest in guests:
        if guest.guest_id == guest_id:
            return guest


def getGuestByNames(f_n, l_n):
    for guest in guests:
        if guest.first_name == f_n and guest.last_name == l_n:
            return guest
    raise NoGuest


def getBookingByGuestDateRoom(guest, date_in, date_out, room):
    r = getRoomByNumber(room)
    for booking in bookings:
        if booking.date_in == date_in and booking.date_out == date_out and booking.guest == guest and booking.room == r:
            return booking
    raise NoBooking


class NoBooking(Exception):
    pass


class NoGuest(Exception):
    pass


class Room:

    def __init__(self, room_number, room_type):
        self.room_number = room_number
        self.room_type = room_type
        rooms.append(self)

    def __repr__(self):
        return str(self.__class__.__name__) + " " + str(self.room_number) + " is " + self.room_type + " type"

    def checkIfRoomCreated(num):
        for room in rooms:
            if room.room_number == num:
                return True
        return False


class Booking:
    last_b_id = 0

    def __init__(self, date_in, date_out, guest, room_number):
        self.date_in = date_in
        self.date_out = date_out
        Booking.last_b_id += 1
        self.last_b_id = Booking.last_b_id
        self.guest = guest
        self.room = getRoomByNumber(room_number)
        bookings.append(self)

    def __repr__(self):
        return str(
            self.__class__.__name__) + " with id " + str(self.last_b_id) + " for room " + str(
            self.room.room_number) + ", check-in " + str(self.date_in.date()) + ", check-out " + str(
            self.date_out.date()) + " for guest " + self.guest.first_name + " " + self.guest.last_name


class Guest:
    guest_id = 0

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        Guest.guest_id += 1
        self.guest_id = Guest.guest_id
        self.registered_on = datetime.datetime.now()
        guests.append(self)

    def __repr__(self):
        return str(
            self.__class__.__name__) + " " + self.first_name + " " + self.last_name + " was registered on " + str(
            self.registered_on.date())

    def checkIfGuestAlreadyCreated(f_n, l_n):
        for guest in guests:
            if guest.first_name == f_n and guest.last_name == l_n:
                return True
        return False


def wrongCommand():
    print("Wrong command. Please try again.")

# Create some data
date_in1 = datetime.datetime.strptime("2021-01-01", '%Y-%m-%d')
date_out1 = datetime.datetime.strptime("2021-01-15", '%Y-%m-%d')
date_in2 = datetime.datetime.strptime("2021-02-01", '%Y-%m-%d')
date_out2 = datetime.datetime.strptime("2021-02-03", '%Y-%m-%d')
Room(123, "economy")
Room(999, "luxury")
Booking(date_in1, date_out1, Guest("Bill", "Gates"), 123)
Booking(date_in2, date_out2, Guest("Lara", "Croft"), 999)


print("Welcome to Aqua Disco Hotel")
while (running):
    print()
    print("Available commands:")
    print(
        "add, remove, show list, exit")
    command = input()

    if command == "add":
        print("Available commands:")
        print("guest, room, booking")
        command = input()

        if command == "guest":

            print("Enter first name")
            first_n = input()
            print("Enter last name")
            last_n = input()
            if Guest.checkIfGuestAlreadyCreated(first_n, last_n):
                guest = getGuestByNames(first_n, last_n)
                print("Guest with such first and last names was already created on " + str(guest.registered_on))
                continue
            Guest(first_n, last_n)
            print("The guest " + first_n + " " + last_n + " was created")

        elif command == "room":

            print("Enter room number:")
            try:
                room_number = int(input())
            except ValueError:
                print("The room number should be a positive integer. The room was not created.")
                continue
            if Room.checkIfRoomCreated(room_number):
                print("The room with this number was already created before.")
                continue
            print("Enter room type/class:")
            # room_type = str(input())
            room_type = input()
            if len(room_type) >= 20:
                print("The room type should be a string, not more than 20 letters long. The room was not created")
                continue
            Room(room_number, room_type)

        elif command == "booking":
            print("Enter room number:")
            try:
                room_number = int(input())
            except ValueError:
                print("The room number should be a positive integer. The room was not created")
                continue
            if not Room.checkIfRoomCreated(room_number):
                print("The room does not exist.")
                continue

            print("Specify the check-in date in the format YYYY-MM-DD (e.g 2021-01-01)")
            date = input()
            try:
                date_in = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("The date format was incorrectly entered")
                continue

            print("Specify the check-out date in the format YYYY-MM-DD (e.g 2021-01-01)")
            date = input()
            try:
                date_out = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("The date format was incorrectly entered.")
                continue
            if date_in > date_out:
                print("The check-out date should be after check-in")
                continue

            print("Enter the guest first name")
            f_n = input()
            print("Enter the guest last name")
            l_n = input()
            if Guest.checkIfGuestAlreadyCreated(f_n, l_n):
                guest = getGuestByNames(f_n, l_n)
                Booking(date_in, date_out, guest, room_number)
                print("New booking was added")
            else:
                print("There is no such guest")
                print("Would you like to create this guest? (yes/no)")
                answ = input()
                if answ == "yes":
                    print("Enter first name")
                    first_n = input()
                    print("Enter last name")
                    last_n = input()
                    if Guest.checkIfGuestAlreadyCreated(first_n, last_n):
                        guest = getGuestByNames(first_n, last_n)
                        print("Guest with such first and last names was already created on " + str(guest.registered_on))
                        continue
                    Guest(first_n, last_n)
                    print("The guest " + first_n + " " + last_n + " was created")
                else:
                    continue
        else:
            wrongCommand()

    elif command == "remove":
        print("Available commands:")
        print("guest, room, booking")
        command = input()

        if command == "guest":
            print("Enter the guest first name")
            f_n = input()
            print("Enter the guest last name")
            l_n = input()
            if Guest.checkIfGuestAlreadyCreated(f_n, l_n):
                guest = getGuestByNames(f_n, l_n)
                guests.remove(guest)
                print("The guest was removed")
            else:
                print("Such guest does not exist")

        elif command == "room":
            print("Enter the room number")
            try:
                room_number = int(input())
            except ValueError:
                print("The room number should be a positive integer")
                continue
            if not Room.checkIfRoomCreated(room_number):
                print("The room with this number does not exist")
                continue
            rooms.remove(getRoomByNumber(room_number))
            print("The room was removed")

        elif command == "booking":
            print("Enter room number:")
            try:
                room_number = int(input())
            except ValueError:
                print("The room number should be a positive integer")
                continue
            if not Room.checkIfRoomCreated(room_number):
                print("The room with this number does not exist")
                continue

            print("Specify the check-in date in the format YYYY-MM-DD (e.g 2021-01-01)")
            date = input()
            try:
                date_in = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("The date format was incorrectly entered")
                continue

            print("Specify the check-out date in the format YYYY-MM-DD (e.g 2021-01-01)")
            date = input()
            try:
                date_out = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print("The date format was incorrectly entered.")
                continue

            print("Enter the guest first name")
            f_n = input()
            print("Enter the guest last name")
            l_n = input()
            if Guest.checkIfGuestAlreadyCreated(f_n, l_n):
                guest = getGuestByNames(f_n, l_n)
            else:
                print("Such guest does not exist")
                continue
            try:
                b = getBookingByGuestDateRoom(guest, date_in, date_out, room_number)
            except NoBooking:
                print("Such booking does not exist")
                continue
            bookings.remove(b)
            print("The booking was removed")

        else:
            wrongCommand()

    elif command == "show list":
        print("Available commands:")
        print("guests, rooms, bookings")
        command = input()

        if command == "guests":
            if len(guests) == 0:
                print("There are no guests")
                continue
            for guest in guests:
                print(guest)

        elif command == "rooms":
            if len(rooms) == 0:
                print("There are no rooms")
                continue
            for room in rooms:
                print(room)

        elif command == "bookings":
            if len(bookings) == 0:
                print("There are no bookings")
                continue
            for booking in bookings:
                print(booking)

        else:
            wrongCommand()

    elif command == "exit":
        running = False

    else:
        print("Wrong command. Please repeat.")

print("Thank you for using our software.")
print("Have a nice day!")
