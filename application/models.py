from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    decks_to_learn = db.relationship("Deck", secondary="user_deck")

class Deck(db.Model):
    __tablename__ = 'deck'
    deck_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    deck_name = db.Column(db.String, nullable = False)
    review_id = db.Column(db.Integer)
    cards_to_deck = db.relationship("Card", secondary="deck_card")

class User_Deck(db.Model):
    __tablename__ = 'user_deck'
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key = True, nullable = False)
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.deck_id"), primary_key = True, nullable = False)

class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    front = db.Column(db.String, nullable = False)
    back = db.Column(db.String, nullable = False)
    card_score = db.Column(db.Integer)
    times_review = db.Column(db.Integer)

class Deck_Card(db.Model):
    __tablename__ = 'deck_card'
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.deck_id"), primary_key = True, nullable = False)
    card_id = db.Column(db.Integer, db.ForeignKey("card.card_id"), primary_key = True, nullable = False)
   
class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    review_time = db.Column(db.String)
    score = db.Column(db.String)