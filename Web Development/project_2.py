import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
import uuid 
from flask import request, jsonify
import datetime
from datetime import datetime
import bcrypt  # For password hashing
# Configure the Flask app
app = Flask(__name__)

# Configure session secret (replace with a secure random string)
app.config['SECRET_KEY'] = 'your_secret_key'

# Specify the session type
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize session
Session(app)

HOST = '127.0.0.1'
USER = 'root'  # Assuming 'root' is your username
DATABASE = 'hotelmanagement3'

# Function to connect to database
def get_db():
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        database=DATABASE,
    )
    return connection

# Route to handle user login
# Route to handle user login
# Route to handle user login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Display login form
    else:
        username = request.form['username']
        password = request.form['password']

        # Database query to check user credentials and admin status
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            if user[0] == 1:  # Check if the user is an admin (1 represents admin status)
                # Admin login successful, set session variable
                session['admin_logged_in'] = True
                session['username'] = username
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
            else:
                flash('You are not authorized to access the admin dashboard.', 'error')
                return redirect(url_for('admin_dashboard'))  # Redirect to homepage
        else:
            flash('User does not exist.', 'error')
            return render_template('login.html')  # Display login form again


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/bookings')
def bookings():
    return render_template('submitbooking.html')


@app.route('/contact_form')
def contact_form():
    print("Hello")

#@app.route('/bookingsubmit')
#def bookingsubmit():
 #   print("Submit Bookings")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('registration.html')


#@app.route('/admin')
#def admin():
#    return render_template('admin.html')
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'GET':
        return render_template('admin-login.html')  # Display login form
    else:
        username = request.form['username']
        password = request.form['password']

        # Database query to check user credentials
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Login successful, set session variable
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to homepage
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html')  # Display login form again

# Registration route
@app.route('/adminregistration', methods=['GET', 'POST'])
def adminregistration():
    if request.method == 'POST':
        # Form submission logic
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('registration.html'))  # Redirect to registration page

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert data into the database
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO adminregistration (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        connection.commit()  # Commit changes to the database
        cursor.close()
        connection.close()

        flash('Admin Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page

@app.route('/verify-login', methods = ['POST', 'GET'])
def verify_login():
    msg = ""
    print("verify-login")
    if request.method == 'POST':
        try:
            Username = request.form['Username']
            Password = request.form['Password']
            print(Username)
            print(Password)
            conn = get_db()

            if conn != None:
                dbcursor = conn.cursor()
                SQL_statement = 'SELECT * FROM hotelmanagement3.user where Username = %s and Password = %s'
                args = (Username,Password,)
                dbcursor.execute(SQL_statement,args)
                rows = dbcursor.fetchall()

                if len(rows) > 0:
                    print("Authenticated")
                    return render_template('index.html')
                else:
                    return render_template("login.html")

                dbcursor.close()
                conn.close()

        except Exception as e:
            print(e)
    return render_template('index.html')

#loginverifyv2
# Authenticate a user

#@app.route('/favicon.ico')
#def favicon():
    #return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Route to handle user logout
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))  # Redirect to homepage

# Registration route
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Form submission logic
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('registration.html'))  # Redirect to registration page

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert data into the database
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        connection.commit()  # Commit changes to the database
        cursor.close()
        connection.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page

# Route to display booking form (login required)
@app.route('/make-booking')
def make_booking():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Redirect if not logged in
    return render_template('bookings.html')  # Display booking form

# Route to handle booking submission3old


    # Form submission logic
 #Insert data into the database
#main booking route
#@app.route('/submitbooking', methods=['GET', 'POST'])
#def submitbooking():
#    if request.method == 'POST':
#        # Form submission logic
#        hotel = request.form['hotel']
#        check_in_date = request.form['check_in_date']
#        check_out_date = request.form['check_out_date']
#        room_type = request.form['room_type']
#        email = request.form['email']
#        card_number = request.form['card_number']
#        expiration_date = request.form['expiration_date']
#        cvv = request.form['cvv']
#        card_holder_name = request.form['card_holder_name']
       

        # Insert data into the database
#        connection = get_db()
#        cursor = connection.cursor()
#        cursor.execute("INSERT INTO bookings (hotel, check_in_date, check_out_date, room_type, email, card_number, expiration_date, cvv, card_holder_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#               (hotel, check_in_date, check_out_date, room_type, email, card_number, expiration_date, cvv, card_holder_name))

#        connection.commit()  # Commit changes to the database-
#        cursor.close()
#        connection.close()
#
#        flash('Booking successful! You have now Booked.', 'success')
#        return redirect(url_for('bookings'))  # Redirect to login page
#    #cpass  # Replace this with your booking submission logic



@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')




def calculate_price(check_in_date, check_out_date, room_type, advance_booking_days):
    # Sample room prices (you can replace this with data from your database)
    room_prices = {
        "standard_room": {
            "peak_season": 200,
            "off_peak_season": 100
        },
        "double_room": {
            "peak_season": 250,
            "off_peak_season": 150
        },
        "family_room": {
            "peak_season": 300,
            "off_peak_season": 200
        }
    }
   
    # Sample discount information
    discount_info = {
        "80-90": 30,
        "60-79": 20,
        "45-59": 10,
        "under_45": 0
    }

    # Calculate duration of stay in days
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    duration_of_stay = (check_out - check_in).days

    # Determine season
    if check_in.month in [4, 5, 6, 7, 8, 11, 12]:  # Peak Season
        season = "peak_season"
    else:
        season = "off_peak_season"

    # Fetch room price from room_prices dictionary
    room_price = room_prices.get(room_type, {}).get(season)

    # Calculate total price
    if room_price is not None:
        total_price = room_price * duration_of_stay

        # Apply discount based on advance booking days
        if advance_booking_days >= 80:
            discount = discount_info["80-90"]
        elif 60 <= advance_booking_days <= 79:
            discount = discount_info["60-79"]
        elif 45 <= advance_booking_days <= 59:
            discount = discount_info["45-59"]
        else:
            discount = discount_info["under_45"]

        total_price -= (total_price * discount) / 100

        return total_price
    else:
        return None

# Example usage
check_in_date = "2024-06-15"
check_out_date = "2024-06-20"
room_type = "double_room"
advance_booking_days = 70

print(calculate_price(check_in_date, check_out_date, room_type, advance_booking_days))

# Route for the booking form page
# Function to generate a unique booking ID
def generate_booking_id():
    return str(uuid.uuid4())

# Route for submitting a booking
@app.route('/submitbooking', methods=['POST'])
def submitbooking():
    if request.method == 'POST':
        # Form submission logic
        hotel = request.form['hotel']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_type = request.form['room_type']
        email = request.form['email']
        card_number = request.form['card_number']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']
        card_holder_name = request.form['card_holder_name']
        total_price=request.form['total_price']
        
        # Generate a unique booking ID
        booking_id = generate_booking_id()

        # Hash sensitive information
        hashed_card_number = bcrypt.hashpw(card_number.encode('utf-8'), bcrypt.gensalt())
        hashed_expiration_date = bcrypt.hashpw(expiration_date.encode('utf-8'), bcrypt.gensalt())
        hashed_cvv = bcrypt.hashpw(cvv.encode('utf-8'), bcrypt.gensalt())

        # Convert bytes to string for database insertion
        hashed_card_number_str = hashed_card_number.decode('utf-8')
        hashed_expiration_date_str = hashed_expiration_date.decode('utf-8')
        hashed_cvv_str = hashed_cvv.decode('utf-8')

        # Insert data into the database
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO bookings ( hotel, check_in_date, check_out_date, room_type, email, card_number, expiration_date, cvv, card_holder_name,total_price,booking_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
               ( hotel, check_in_date, check_out_date, room_type, email, hashed_card_number_str, hashed_expiration_date_str, hashed_cvv_str, card_holder_name,total_price,booking_id))


        connection.commit()  # Commit changes to the database-
        cursor.close()
        connection.close()
        
        # Redirect to receipt page with booking information as URL parameters
        return redirect(url_for('receipt', 
                                hotel=hotel, 
                                check_in_date=check_in_date, 
                                check_out_date=check_out_date, 
                                room_type=room_type, 
                                email=email, 
                                card_number=card_number, 
                                expiration_date=expiration_date, 
                                cvv=cvv, 
                                card_holder_name=card_holder_name,
                                total_price=total_price,
                                booking_id=booking_id))
    else:
        return render_template('bookings.html')

# Route for the receipt page
@app.route('/receipt')
def receipt():
    # Retrieve booking information from URL parameters
    hotel = request.args.get('hotel')
    check_in_date = request.args.get('check_in_date')
    check_out_date = request.args.get('check_out_date')
    room_type = request.args.get('room_type')
    email = request.args.get('email')
    card_number = request.args.get('card_number')
    expiration_date = request.args.get('expiration_date')
    cvv = request.args.get('cvv')
    card_holder_name = request.args.get('card_holder_name')
    total_price = request.args.get('total_price')
    booking_id = request.args.get('booking_id')
    
    # Render the receipt template with the booking information
    return render_template('receipt.html', 
                           hotel=hotel, 
                           check_in_date=check_in_date, 
                           check_out_date=check_out_date, 
                           room_type=room_type, 
                           email=email, 
                           card_number=card_number, 
                           expiration_date=expiration_date, 
                           cvv=cvv, 
                           card_holder_name=card_holder_name,
                           total_price=total_price,
                           booking_id=booking_id)

# Admin dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Route for adding a hotel
@app.route('/add_hotel_admin', methods=['GET', 'POST'])
def add_hotel_admin():
        if request.method == 'POST':
            # Get data from the form
            hotel_name = request.form['hotel_name']
            
            # Insert the hotel into the database
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO hotels (hotel_name) VALUES (%s)", (hotel_name,))
            connection.commit()
            connection.close()
            
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('add_hotel_admin.html')

#route for setting status of hotel

@app.route('/delete_hotel_admin', methods=['POST'])
def delete_hotel_admin(hotel_name):
    if request.method == 'POST':
        # Remove the hotel from the database
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM hotels WHERE name = %s", (hotel_name,))
        connection.commit()
        connection.close()
        
        return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard

   

    



@app.route('/monthlysalesreport_admin', methods=['GET', 'POST'])
def monthlysalesreport_admin():
    if request.method == 'GET':
        # Handle GET request to display form
        return render_template('monthlysalesreport_admin.html')
    elif request.method == 'POST':
        # Handle POST request to generate the monthly sales report
        month = request.form.get('month')
        year = request.form.get('year')
        # Call the function to generate the monthly sales report
        total_sales = monthlysalesreport_admin(month, year)
        return render_template('monthly_sales_report.html', total_sales=total_sales)


        


if __name__ == '__main__':
    app.run(debug=True)



# Route for booking 2 old
