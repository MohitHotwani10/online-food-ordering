import os
import time
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==================================================
# FLASK APPLICATION
# ==================================================

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)


# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

# Used for sessions and flash messages
app.config["SECRET_KEY"] = "foodexpress-dev-key"

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///foodexpress.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ==================================================
# DATABASE
# ==================================================

db = SQLAlchemy(app)


# ==================================================
# USER MODEL
# ==================================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="customer"
    )

    def __repr__(self):
        return f"<User {self.email}>"

class FoodItem(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(255),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    def __repr__(self):
        return f"<FoodItem {self.name}>"

class Cart(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    food_id = db.Column(
        db.Integer,
        db.ForeignKey("food_item.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="cart_items"
    )

    food = db.relationship(
        "FoodItem",
        backref="cart_entries"
    )

class Order(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Placed"
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    user = db.relationship(
        "User",
        backref="orders"
    )


class OrderItem(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    food_id = db.Column(
        db.Integer,
        db.ForeignKey("food_item.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    order = db.relationship(
        "Order",
        backref="items"
    )

    food = db.relationship(
        "FoodItem"
    )

# ==================================================
# CREATE DATABASE TABLES
# ==================================================

with app.app_context():

    # Try connecting to the database
    # MySQL may take a few seconds to start in Docker Compose
    for attempt in range(10):

        try:
            db.create_all()

            print("Database connection successful!")

            break

        except Exception as error:

            print(
                f"Database not ready. "
                f"Retrying... ({attempt + 1}/10)"
            )

            time.sleep(5)

    else:
        raise RuntimeError(
            "Could not connect to the database."
        )


    # Add sample food only if the table is empty
    if FoodItem.query.count() == 0:

        sample_food = [

            FoodItem(
                name="Margherita Pizza",
                description="Classic pizza with tomato sauce, mozzarella and herbs.",
                price=249,
                category="Pizza",
                image="pizza.jpg"
            ),

            FoodItem(
                name="Veg Burger",
                description="Crispy vegetable patty with cheese and fresh vegetables.",
                price=149,
                category="Burger",
                image="burger.jpg"
            ),

            FoodItem(
                name="Paneer Biryani",
                description="Aromatic basmati rice cooked with paneer and Indian spices.",
                price=229,
                category="Indian",
                image="biryani.jpg"
            ),

            FoodItem(
                name="White Sauce Pasta",
                description="Creamy white sauce pasta with vegetables and herbs.",
                price=199,
                category="Pasta",
                image="pasta.jpg"
            ),

            FoodItem(
                name="Grilled Sandwich",
                description="Grilled vegetable sandwich filled with cheese.",
                price=129,
                category="Sandwich",
                image="sandwich.jpg"
            ),

            FoodItem(
                name="Chocolate Brownie",
                description="Rich chocolate brownie served as the perfect dessert.",
                price=99,
                category="Dessert",
                image="brownie.jpg"
            )
        ]

        db.session.add_all(sample_food)

        db.session.commit()

        print("Sample food items added!")


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "application": "Online Food Ordering System"
    }, 200


# ==================================================
# REGISTER
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    # If user is already logged in,
    # send them back to homepage
    if session.get("user_id"):

        return redirect(
            url_for("home")
        )

    # Registration form submitted
    if request.method == "POST":

        name = request.form["name"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        # ------------------------------------------
        # Validate fields
        # ------------------------------------------

        if not name or not email or not password:

            flash(
                "Please fill in all fields.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        # ------------------------------------------
        # Check whether email already exists
        # ------------------------------------------

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        # ------------------------------------------
        # Hash password
        # ------------------------------------------

        hashed_password = generate_password_hash(
            password
        )

        # ------------------------------------------
        # Create new user
        # ------------------------------------------

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="customer"
        )

        # ------------------------------------------
        # Save user to database
        # ------------------------------------------

        db.session.add(new_user)

        db.session.commit()

        # ------------------------------------------
        # Success message
        # ------------------------------------------

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    # GET request
    return render_template(
        "register.html"
    )


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # If already logged in
    if session.get("user_id"):

        # Admin goes to admin dashboard
        if session.get("role") == "admin":
            return redirect(
                url_for("admin")
            )

        # Customer goes to homepage
        return redirect(
            url_for("home")
        )

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        # Find user
        user = User.query.filter_by(
            email=email
        ).first()

        # Check email and password
        if user and check_password_hash(
            user.password,
            password
        ):

            # Create session
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role

            flash(
                "Login successful!",
                "success"
            )

            # ADMIN LOGIN
            if user.role == "admin":

                return redirect(
                    url_for("admin")
                )

            # CUSTOMER LOGIN
            return redirect(
                url_for("home")
            )

        # Wrong email/password
        flash(
            "Invalid email or password.",
            "danger"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "login.html"
    )

# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    # Remove everything from session
    session.clear()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("home")
    )


@app.route("/menu")
def menu():

    food_items = FoodItem.query.all()

    return render_template(
        "menu.html",
        food_items=food_items
    )

@app.route("/add-to-cart/<int:food_id>", methods=["POST"])
def add_to_cart(food_id):

    if not session.get("user_id"):
        flash("Please login before adding items to your cart.", "warning")
        return redirect(url_for("login"))

    food = db.session.get(FoodItem, food_id)

    if not food:
        flash("Food item not found.", "danger")
        return redirect(url_for("menu"))

    existing_item = Cart.query.filter_by(
        user_id=session["user_id"],
        food_id=food_id
    ).first()

    if existing_item:
        existing_item.quantity += 1

    else:
        cart_item = Cart(
            user_id=session["user_id"],
            food_id=food_id,
            quantity=1
        )

        db.session.add(cart_item)

    db.session.commit()

    flash(
        f"{food.name} added to cart!",
        "success"
    )

    return redirect(url_for("menu"))

@app.route("/cart")
def cart():

    if not session.get("user_id"):

        flash(
            "Please login to view your cart.",
            "warning"
        )

        return redirect(url_for("login"))

    cart_items = Cart.query.filter_by(
        user_id=session["user_id"]
    ).all()

    total = sum(
        item.food.price * item.quantity
        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )

@app.route(
    "/remove-from-cart/<int:cart_id>",
    methods=["POST"]
)
def remove_from_cart(cart_id):

    if not session.get("user_id"):
        return redirect(url_for("login"))

    cart_item = Cart.query.filter_by(
        id=cart_id,
        user_id=session["user_id"]
    ).first()

    if not cart_item:

        flash(
            "Cart item not found.",
            "danger"
        )

        return redirect(url_for("cart"))

    db.session.delete(cart_item)
    db.session.commit()

    flash(
        "Item removed from cart.",
        "success"
    )

    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if not session.get("user_id"):

        flash(
            "Please login to checkout.",
            "warning"
        )

        return redirect(url_for("login"))

    cart_items = Cart.query.filter_by(
        user_id=session["user_id"]
    ).all()

    if not cart_items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(url_for("cart"))

    total = sum(
        item.food.price * item.quantity
        for item in cart_items
    )

    if request.method == "POST":

        # Create order
        new_order = Order(
            user_id=session["user_id"],
            total_amount=total,
            status="Placed"
        )

        db.session.add(new_order)

        # Get the new order ID
        db.session.flush()

        # Copy cart items into order items
        for item in cart_items:

            order_item = OrderItem(
                order_id=new_order.id,
                food_id=item.food_id,
                quantity=item.quantity,
                price=item.food.price
            )

            db.session.add(order_item)

        # Clear cart
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()

        flash(
            f"Order #{new_order.id} placed successfully!",
            "success"
        )

        return redirect(
            url_for("orders")
        )

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )

@app.route("/orders")
def orders():

    if not session.get("user_id"):

        flash(
            "Please login to view your orders.",
            "warning"
        )

        return redirect(url_for("login"))

    user_orders = Order.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders
    )

@app.route("/admin")
def admin():

    if not session.get("user_id"):
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("home"))

    food_items = FoodItem.query.all()

    all_orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "admin.html",
        food_items=food_items,
        orders=all_orders
    )

@app.route("/admin/add-food", methods=["GET", "POST"])
def add_food():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form["name"].strip()

        description = request.form["description"].strip()

        price = request.form["price"]

        category = request.form["category"].strip()

        new_food = FoodItem(
            name=name,
            description=description,
            price=float(price),
            category=category
        )

        db.session.add(new_food)
        db.session.commit()

        flash(
            "Food item added successfully!",
            "success"
        )

        return redirect(url_for("admin"))

    return render_template("add_food.html")

@app.route(
    "/admin/delete-food/<int:food_id>",
    methods=["POST"]
)
def delete_food(food_id):

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("home"))

    food = db.session.get(
        FoodItem,
        food_id
    )

    if not food:

        flash(
            "Food item not found.",
            "danger"
        )

        return redirect(url_for("admin"))

    # Don't delete foods referenced by previous orders.
    order_reference = OrderItem.query.filter_by(
        food_id=food_id
    ).first()

    if order_reference:

        flash(
            "This food item belongs to an existing order and cannot be deleted.",
            "warning"
        )

        return redirect(url_for("admin"))

    # Remove it from any current carts first.
    Cart.query.filter_by(
        food_id=food_id
    ).delete()

    db.session.delete(food)
    db.session.commit()

    flash(
        "Food item deleted successfully.",
        "success"
    )

    return redirect(url_for("admin"))

@app.route(
    "/admin/update-order/<int:order_id>",
    methods=["POST"]
)
def update_order_status(order_id):

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("home"))

    order = db.session.get(
        Order,
        order_id
    )

    if not order:

        flash(
            "Order not found.",
            "danger"
        )

        return redirect(url_for("admin"))

    status = request.form["status"]

    allowed_statuses = [
        "Placed",
        "Preparing",
        "Out for Delivery",
        "Delivered"
    ]

    if status not in allowed_statuses:

        flash(
            "Invalid order status.",
            "danger"
        )

        return redirect(url_for("admin"))

    order.status = status

    db.session.commit()

    flash(
        f"Order #{order.id} updated to {status}.",
        "success"
    )

    return redirect(url_for("admin"))

# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )