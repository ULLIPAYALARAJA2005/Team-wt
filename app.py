from flask import Flask, render_template, request, redirect, url_for, session, send_file,flash
from pymongo import MongoClient
import gridfs
import bcrypt
import io
from bson import ObjectId
import smtplib
import secrets
app = Flask(__name__, template_folder="templates")
app.secret_key = "secret"

# Connect to MongoDB
MONGO_URL = "mongodb+srv://raja:rajaRAJA1234@users.7psqc.mongodb.net/?retryWrites=true&w=majority&appName=users"
client = MongoClient(MONGO_URL)
print("Mongo connected")
db = client["mydatabase"]  # Database name
users_collection = db["userdetails"]  # Collection name
fs = gridfs.GridFS(db)  # GridFS for storing images

feedbacks_collection1 = db["feedback"]  # Obesity feedback
depression_collection = db["depression"]  # Depression feedback
migraine_collection = db["migraine"]  # Migraine feedback
dengue_collection = db["dengue"]  # Dengue feedback



# Store tokens temporarily for password reset
reset_tokens = {}

# SMTP Configuration
EMAIL_ADDRESS = "r210264@rguktrkv.ac.in"
EMAIL_PASSWORD = "cdmz ttzb lxmi vdkz"

# Route to display registration page
@app.route("/")
def signup():
    return render_template("forms/signup.html")


# Route to handle registration form submission
@app.route("/signup_action", methods=["POST"])
def signup_action():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    photo = request.files["photo"]
    # Hash Password

    # Store Image in GridFS
    if photo:
        photo_id = fs.put(photo.read(), filename=photo.filename)
    else:
        photo_id = None


    # Check if email already exists
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        flash("Email already registered. Please log in.", "danger")
        return redirect(url_for("signup"))

    # Insert new user if email does not exist
        # Store User Data in MongoDB
    user_data = {"name": name, "email": email, "password":password, "photo_id": photo_id}
    users_collection.insert_one(user_data)    
    flash("Registration successful!", "success")
    return redirect(url_for("login"))

# Route to display login page
@app.route("/login")
def login():
    return render_template("forms/login.html")

# Route to handle login form submission
@app.route("/login", methods=["POST"])
def login_user():
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if email exists
    user = users_collection.find_one({"email": email})
    if not user:
        flash("Email is not registered. Please sign up.", "danger")
        return redirect(url_for("login"))

    # Check if password matches
    if user["password"] != password:
        flash("Incorrect password. Please try again.", "danger")
        return redirect(url_for("login"))

    # Store user session
    session["user"] = email
    flash("Login successful!", "success")
    return redirect(url_for("index"))  # Redirect to menu page after login


@app.route("/index")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/index.html",user=user)
@app.route("/obesity")
def obesity():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    session["name"] = "obesity1"
    return render_template("forms/obesity.html",user=user)
@app.route("/depression")
def depression():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    session["name"] = "depression1"
    return render_template("forms/depression.html",user=user)
@app.route("/migraine")
def migraine():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    session["name"] = "migraine1"
    return render_template("forms/migraine.html",user=user)
@app.route("/dengue")
def dengue():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    session["name"] = "dengue1"
    return render_template("forms/dengue.html",user=user)
@app.route("/About_obesity")
def About_obesity():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/About_Obesity.html",user=user)
@app.route("/About_depression")
def About_depression():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/About_depression.html",user=user)
@app.route("/About_migraint")
def About_migraint():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/About_migraint.html",user=user)
@app.route("/About_dengue")
def About_dengue():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/About_dengue.html",user=user)

@app.route("/contact")
def contact():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/contact_Obesity.html",user=user)

@app.route("/contact_obesity")
def contact_obesity():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/contact_Obesity1.html",user=user)
@app.route("/contact_depression")
def contact_depression():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/contact_depression.html",user=user)
@app.route("/contact_dengue")
def contact_dengue():
    if "user" not in session:
        return redirect(url_for("login"))
    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/contact_dengue.html",user=user)

# Forgot Password Route
@app.route("/forgot")
def forgot():
    return render_template("forms/forgot.html")

@app.route("/forgot", methods=["POST"])
def forgot_user():
    email = request.form.get("email")

    # Check if email exists
    user = users_collection.find_one({"email": email})
    if not user:
        flash("Email is not registered. Please sign up.", "danger")
        return redirect(url_for("forgot"))

    # Generate a reset token
    reset_token = secrets.token_urlsafe(16)

    # Store token in the database with expiration time (optional)
    users_collection.update_one({"email": email}, {"$set": {"reset_token": reset_token}})

    # Send email with reset link
    reset_link = f"http://127.0.0.1:5001/reset/{reset_token}"
    send_reset_email(email, reset_link)

    flash("Password reset link has been sent to your email.", "success")
    return redirect(url_for("forgot"))


# Function to send reset email
def send_reset_email(email, reset_link):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f"Subject: Password Reset\n\nClick the link to reset your password: {reset_link}"
            print("sent")
            server.sendmail(EMAIL_ADDRESS, email, message)
    except Exception as e:
        print("Error sending email:", e)

# Route to display reset password page
@app.route("/reset/<token>")
def reset_password(token):
    user = users_collection.find_one({"reset_token": token})

    if not user:
        flash("Invalid or expired reset token.", "danger")
        return redirect(url_for("forgot"))

    session["reset_email"] = user["email"]
    return render_template("forms/reset.html")


# Route to handle password reset submission
@app.route("/reset", methods=["POST"])
def reset_password_submit():
    new_password = request.form.get("password")

    email = session.get("reset_email")
    if not email:
        flash("Session expired. Please try again.", "danger")
        return redirect(url_for("forgot"))

    # Update password and remove reset token
    users_collection.update_one({"email": email}, {"$set": {"password": new_password}, "$unset": {"reset_token": ""}})
    
    flash("Password successfully reset! You can now log in.", "success")

    session.pop("reset_email", None)
    return redirect(url_for("login"))







@app.route("/userfeedback", methods=["GET", "POST"])
def userfeedback():   
    return render_template("forms/feed.html")
@app.route("/feedback", methods=["GET"])
def feedback():
    return render_template("forms/feedback.html")

# Route to handle feedback submission
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    
    email = session["user"]  # Get logged-in user's email
    feedback_text = request.form.get("feedback")
    print("...bbbbbbbbbbbbbbbbbbbbbbbbbbbb..........aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa........................")
    if  not feedback_text:
        flash("Please fill in all field!", "danger")
        return redirect(url_for("feedback"))
    
    
    userpage = session["name"]

    # Default to None (or a safe fallback collection)
    feedbacks_collection = None  

    if userpage == "obesity1":
        feedbacks_collection = feedbacks_collection1
    elif userpage == "depression1":
        feedbacks_collection = depression_collection
    elif userpage == "migraine1":
        feedbacks_collection = migraine_collection
    elif userpage == "dengue1":
        feedbacks_collection = dengue_collection
 # Check if feedbacks_collection is correctly assigned
    if feedbacks_collection is None:
        print("Error: feedbacks_collection is not assigned properly!")
        raise ValueError("Invalid userpage session value: " + str(userpage))

    # Check if feedback already exists for this email
    existing_feedback = feedbacks_collection.find_one({"email": email})
    if existing_feedback:
        flash("You have already submitted feedback!", "danger")
        return redirect(url_for("feedback"))
    useremail = users_collection.find_one({"email": session["user"]})
    username = useremail["name"]
    # Insert feedback if not already given
    feedbacks_collection.insert_one({"email": email, "name":username, "feedback": feedback_text})
    flash("Feedback submitted successfully!", "success")
    return redirect(url_for("feedback"))

# Route to display all feedback
@app.route("/all_feedback")
def all_feedback():
    user_email = session["user"]
    userpage = session["name"]
    if(userpage == "obesity1"):
        feedbacks_collection = feedbacks_collection1;
    elif(userpage == "depression1"):
        feedbacks_collection =depression_collection;
    elif(userpage == "migraine1"):
        feedbacks_collection =migraine_collection;    
    elif(userpage == "dengue1"):
        feedbacks_collection =dengue_collection; 
     
    feedbacks = list(feedbacks_collection.find())  # Fetch all feedbacks
    return render_template("forms/all_feedback.html", feedbacks=feedbacks, user_email=user_email)

# Route to delete feedback
@app.route("/delete_feedback/<feedback_id>", methods=["POST"])
def delete_feedback(feedback_id):
    if "user" not in session:
        flash("You must be logged in to delete feedback.", "danger")
        return redirect(url_for("login"))
    userpage = session["name"]
    if(userpage == "obesity1"):
        feedbacks_collection = feedbacks_collection1;
    elif(userpage == "depression1"):
        feedbacks_collection =depression_collection;
    elif(userpage == "migraine1"):
        feedbacks_collection =migraine_collection;    
    elif(userpage == "dengue1"):
        feedbacks_collection =dengue_collection; 
     
    
    feedback = feedbacks_collection.find_one({"_id": ObjectId(feedback_id)})
    if feedback and feedback["email"] == session["user"]:  
        feedbacks_collection.delete_one({"_id": ObjectId(feedback_id)})
        flash("Feedback deleted successfully!", "success")
    else:
        flash("You are not authorized to delete this feedback.", "danger")

    return redirect(url_for("all_feedback"))

# Route to edit feedback
@app.route("/edit_feedback/<feedback_id>", methods=["POST"])
def edit_feedback(feedback_id):
    if "user" not in session:
        flash("You must be logged in to edit feedback.", "danger")
        return redirect(url_for("login"))
    userpage = session["name"]
    if(userpage == "obesity1"):
        feedbacks_collection = feedbacks_collection1;
    elif(userpage == "depression1"):
        feedbacks_collection =depression_collection;
    elif(userpage == "migraine1"):
        feedbacks_collection =migraine_collection;    
    elif(userpage == "dengue1"):
        feedbacks_collection =dengue_collection; 
     
    
    new_feedback_text = request.form.get("edited_feedback")
    feedback = feedbacks_collection.find_one({"_id": ObjectId(feedback_id)})

    if feedback and feedback["email"] == session["user"]:  
        feedbacks_collection.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$set": {"feedback": new_feedback_text}}
        )
        flash("Feedback updated successfully!", "success")
    else:
        flash("You are not authorized to edit this feedback.", "danger")

    return redirect(url_for("all_feedback"))




# Route to Profile Page
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    user = users_collection.find_one({"email": session["user"]})
    return render_template("forms/profile.html", user=user)

# Route to Fetch User Image
@app.route("/photo/<photo_id>")
def get_photo(photo_id):
    try:
        photo = fs.get(ObjectId(photo_id))  # Convert to ObjectId
        return send_file(io.BytesIO(photo.read()), mimetype="image/jpeg")
    except Exception as e:
        return f"Error: {str(e)}"

# **New Route: Update Name and Profile Picture**
@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "user" not in session:
        return redirect(url_for("login"))

    user = users_collection.find_one({"email": session["user"]})

    if not user:
        return "User not found!"

    new_name = request.form["new_name"]
    new_photo = request.files.get("new_photo")

    update_data = {"name": new_name}  # Update name

    if new_photo:
        # Delete old photo if exists
        if user.get("photo_id"):
            fs.delete(ObjectId(user["photo_id"]))

        # Store new photo in GridFS
        new_photo_id = fs.put(new_photo.read(), filename=new_photo.filename)
        update_data["photo_id"] = new_photo_id  # Update photo_id

    # Update user's name and/or photo_id in the database
    users_collection.update_one({"email": session["user"]}, {"$set": update_data})

    return redirect(url_for("profile"))

@app.route('/logout')
def logout():
    if "user" in session:
        user_email = session["user"]  # Get logged-in user's email

        # Delete user details from the database
        users_collection.delete_one({"email": user_email})

        # Remove user session
        session.pop("user", None)  
        flash("Your account has been deleted and you have been logged out.", "danger")

    return redirect(url_for('login'))
@app.route('/back_to_login')
def back_to_login():
    return redirect(url_for('login'))

@app.route('/back_to_menu')
def back_to_menu():
    userpage = session["name"]
    if(userpage == "obesity1"):
        return redirect(url_for('obesity'))
    elif(userpage == "depression1"):
        return redirect(url_for('depression'))
    elif(userpage == "migraine1"):
        return redirect(url_for('migraine'))   
    elif(userpage == "dengue1"):
        return redirect(url_for('dengue'))
    
if __name__ == "__main__":
    app.run(debug=True, port=5002)