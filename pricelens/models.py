from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    history_entries = db.relationship("UserHistory", back_populates="user", lazy="dynamic")


class Grocery(db.Model):
    __tablename__ = "groceries"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_image = db.Column(db.String(255))
    blinkit_price = db.Column(db.Integer)
    zepto_price = db.Column(db.Integer)
    instamart_price = db.Column(db.Integer)

    @property
    def id(self):
        return self.product_id

    @property
    def name(self):
        return self.product_name

    @property
    def image_url(self):
        return self.product_image

    @property
    def category(self):
        return "Grocery"

    @property
    def brand(self):
        return ""


class Clothing(db.Model):
    __tablename__ = "clothing"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_image = db.Column(db.String(255))
    ajio_price = db.Column(db.Integer)
    myntra_price = db.Column(db.Integer)

    @property
    def id(self):
        return self.product_id

    @property
    def name(self):
        return self.product_name

    @property
    def image_url(self):
        return self.product_image

    @property
    def category(self):
        return "Clothing"

    @property
    def brand(self):
        return ""


class Gadgets(db.Model):
    __tablename__ = "gadgets"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_image = db.Column(db.String(255))
    amazon_price = db.Column(db.Integer)
    flipkart_price = db.Column(db.Integer)

    @property
    def id(self):
        return self.product_id

    @property
    def name(self):
        return self.product_name

    @property
    def image_url(self):
        return self.product_image

    @property
    def category(self):
        return "Gadgets"

    @property
    def brand(self):
        return ""


class UserHistory(db.Model):
    __tablename__ = "user_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False, index=True)
    product_id = db.Column(db.Integer, nullable=False, index=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    user = db.relationship("User", back_populates="history_entries")
