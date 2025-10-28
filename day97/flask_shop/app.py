import os
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import stripe

# Load env
load_dotenv(r"Python-udemy\day97\flask_shop\shop.env")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "devsecret")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///shop.db")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
DOMAIN = os.getenv("DOMAIN", "http://localhost:5000")

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

if not STRIPE_SECRET_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY environment variable not set. See .env.example")
stripe.api_key = STRIPE_SECRET_KEY

### Models ###
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    orders = db.relationship("Order", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_cents = db.Column(db.Integer, nullable=False)  # store price in cents
    image = db.Column(db.String(300), nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_session_id = db.Column(db.String(200), nullable=True)
    paid = db.Column(db.Boolean, default=False)
    total_cents = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    items = db.relationship("OrderItem", backref="order", lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.String(200))
    unit_price_cents = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

### Login loader ###
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

### Helpers ###
def cart_get():
    return session.get("cart", {})

def cart_set(cart):
    session["cart"] = cart
    session.modified = True

def cart_total_cents():
    cart = cart_get()
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            total += p.price_cents * qty
    return total

### Routes ###
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products, publishable_key=STRIPE_PUBLISHABLE_KEY)

@app.route("/product/<int:product_id>")
def product_page(product_id):
    p = Product.query.get_or_404(product_id)
    return render_template("product.html", product=p)

@app.route("/cart")
def cart():
    cart = cart_get()
    items = []
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            items.append({"product": p, "qty": qty, "subtotal_cents": p.price_cents * qty})
    total_cents = cart_total_cents()
    return render_template("cart.html", items=items, total_cents=total_cents, publishable_key=STRIPE_PUBLISHABLE_KEY)

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    qty = int(request.form.get("quantity", 1))
    cart = cart_get()
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    cart_set(cart)
    flash("Added to cart", "success")
    return redirect(request.referrer or url_for("index"))

@app.route("/cart/update", methods=["POST"])
def update_cart():
    # expects form like qty-<product_id>
    cart = {}
    for key, val in request.form.items():
        if key.startswith("qty-"):
            pid = key.split("-", 1)[1]
            try:
                qty = max(0, int(val))
            except:
                qty = 0
            if qty > 0:
                cart[pid] = qty
    cart_set(cart)
    flash("Cart updated", "success")
    return redirect(url_for("cart"))

@app.route("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    flash("Cart cleared", "info")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].lower()
        name = request.form.get("name","")
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))
        u = User(email=email, name=name)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        flash("Welcome! Account created.", "success")
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]
        u = User.query.filter_by(email=email).first()
        if u and u.check_password(password):
            login_user(u)
            flash("Logged in", "success")
            return redirect(url_for("index"))
        flash("Invalid credentials", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("index"))

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    cart = cart_get()
    if not cart:
        flash("Cart is empty", "warning")
        return redirect(url_for("cart"))

    line_items = []
    # Build line_items for Stripe
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if not p:
            continue
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": p.title},
                "unit_amount": p.price_cents,
            },
            "quantity": qty,
        })

    # Create an Order record (pending)
    order = Order(total_cents=cart_total_cents(), paid=False, user_id=current_user.id if current_user.is_authenticated else None)
    db.session.add(order)
    db.session.commit()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=DOMAIN + url_for("checkout_success") + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=DOMAIN + url_for("cart"),
            metadata={"order_id": str(order.id)}
        )
    except Exception as e:
        app.logger.exception("Stripe Checkout Session creation failed")
        flash("Payment initialization failed. Try again.", "danger")
        return redirect(url_for("cart"))

    # Save session id to order (optional)
    order.stripe_session_id = checkout_session.id
    db.session.commit()

    # Redirect to Stripe Checkout
    return redirect(checkout_session.url, code=303)

@app.route("/checkout-success")
def checkout_success():
    session_id = request.args.get("session_id")
    if not session_id:
        flash("No session specified", "warning")
        return redirect(url_for("index"))
    # Optionally, lookup order and show success
    order = None
    # find order by session id
    order = Order.query.filter_by(stripe_session_id=session_id).first()
    # Clear cart
    session.pop("cart", None)
    return render_template("checkout_success.html", order=order)

### Webhook to listen for checkout.session.completed ###
from flask import Response

@app.route("/stripe/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", None)
    event = None

    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
        except Exception as e:
            app.logger.exception("Webhook signature verification failed.")
            return Response(status=400)
    else:
        # If no webhook secret, parse directly (less secure, for quick testing)
        try:
            event = stripe.Event.construct_from(request.get_json(), stripe.api_key)
        except Exception as e:
            app.logger.exception("Failed to construct event")
            return Response(status=400)

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session_obj = event["data"]["object"]
        order_id = session_obj.get("metadata", {}).get("order_id")
        if order_id:
            order = Order.query.get(int(order_id))
            if order:
                order.paid = True
                order.stripe_session_id = session_obj.get("id")
                db.session.commit()
                # create order items copy from cart? For demo, create items from session line_items isn't available here easily,
                # so we can store a basic record. In production, maintain full cart snapshot on Order creation.
                app.logger.info(f"Order {order.id} marked paid.")
    # Return 200 to Stripe
    return Response(status=200)

### Admin-ish route to seed some products (for demo) ###
@app.route("/seed")
def seed():
    if Product.query.count() == 0:
        sample = [
            {"title":"Cozy Hoodie", "description":"Warm & comfy hoodie", "price_cents":3500, "image":"https://picsum.photos/seed/hoodie/600/400"},
            {"title":"Minimalist Mug", "description":"Ceramic mug for your coffee", "price_cents":1200, "image":"https://picsum.photos/seed/mug/600/400"},
            {"title":"Notebook Set", "description":"Pack of 3 lined notebooks", "price_cents":1800, "image":"https://picsum.photos/seed/notebooks/600/400"},
            {"title":"Sticker Pack", "description":"Fun laptop stickers", "price_cents":500, "image":"https://picsum.photos/seed/stickers/600/400"},
        ]
        for s in sample:
            p = Product(title=s["title"], description=s["description"], price_cents=s["price_cents"], image=s["image"])
            db.session.add(p)
        db.session.commit()
        return "Seeded products!"
    return "Already seeded."

### Simple dashboard for user orders ###
@app.route("/dashboard")
@login_required
def dashboard():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template("dashboard.html", orders=orders)

if __name__ == "__main__":
    # create db
    with app.app_context():
        db.create_all()
    app.run(debug=True)
