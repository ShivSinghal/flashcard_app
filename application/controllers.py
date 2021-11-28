from flask import request
from flask import render_template
from flask import current_app as app
from application.models import *
from sqlalchemy.orm import Session
from .database import engine
from flask import redirect, url_for, flash
import random
import time

#Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        message1 = "Please enter your username to login"
        an_message1 = "Become a user, if not already registered"
        app.logger.info("Login page entered for user")
        return render_template("login.html", message = message1, an_message = an_message1)
    elif request.method == "POST":
        form = request.form
        with Session(engine) as session:       
            u_name1 = form["u_name1"]
            if "@" in u_name1:
                find_user = session.query(User).filter(User.username == u_name1).first()
                if not find_user:
                    app.logger.info("Login not successful. Routing back to Login Page")
                    message2 = "Username not found. Please enter a valid username, else register as a user below."
                    an_message1 = "Become a user, if not already registered"
                    return render_template("login.html", message = message2, an_message = an_message1)
                else:
                    u_id = find_user.user_id
                    app.logger.info("Login successful. Routing to Dashboard")
                    return redirect(url_for("dashboard", user_id = u_id))     
            else:
                message1 = "Please enter a valid email to be a username to login"
                an_message1 = "Become a user, if not already registered"
                app.logger.info("Username entered not an email. Login page again entered for user")
                return render_template("login.html", message = message1, an_message = an_message1)
            

#Add user for login
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        message1 = "Please suggest your username to the App"
        app.logger.info("add_user page entered")
        return render_template("add_user.html", message = message1)
    elif request.method == "POST":
        form = request.form
        u_name = form["u_name"]
        if "@" in u_name:
            with Session(engine) as session:
                session.begin()
                find_user = session.query(User).filter(User.username == u_name).first()
                session.commit()
                if not find_user:
                    session.begin()
                    try:
                        insert_user = User(username = u_name)
                        session.add(insert_user)             
                    except:
                        app.logger.info("Exception, rolling back")
                        session.rollback()
                        raise
                    else:
                        app.logger.info("No exception, hence commit")
                        session.commit()
                    app.logger.info("Creation of user profile successful. Routing to Dashboard")
                    message2 = "Username created. Please login"
                    return render_template("login.html", message = message2)
                else:
                    app.logger.info("Duplicate username. Routing back to add_user Page")
                    message2 = "Username already taken. Please suggest a different username."
                    return render_template("add_user.html", message = message2 )   
        else:
            app.logger.info("Username creation not successful. Routing back to add_user page.")
            return redirect(url_for("add_user"))   

#Dashboard Page        
@app.route("/dashboard/<int:user_id>", methods=["GET"])
def dashboard(user_id):
    u_id = user_id
    with Session(engine) as session:         
        find_deck = session.query(User_Deck).filter(User_Deck.user_id == u_id).all()
        deck_list = []
        if len(find_deck) != 0: 
            for a in find_deck:
                found = session.query(Deck, Review).filter((Deck.deck_id == a.deck_id) & (Deck.review_id == Review.review_id)).one()
                deck_list = deck_list + [found]
            app.logger.info("Routed to Dashboard successful.")
            return render_template("dashboard.html", deck_list = deck_list, user_id = u_id)
        else:
            app.logger.info("Routed to Dashboard successful.")
            return render_template("dashboard.html", deck_list = deck_list, user_id = u_id)

#Creating a Deck Page
@app.route("/create_deck/<int:user_id>", methods=["GET", "POST"])
def create_deck(user_id):
    u_id = user_id
    if request.method == "GET":
        app.logger.info("Routed to Create Deck page successful.")
        message1 = "Choose an appropriate name for creating a deck, which has not already been used by you"
        return render_template ("create_deck.html", user_id = user_id, message = message1)
    elif request.method == "POST":
        form = request.form
        d_name = form["d_name"]
        with Session(engine) as session:
            session.begin()
            find_deck = session.query(User_Deck).filter(User_Deck.user_id == u_id).all()
            for a in find_deck:
                found = session.query(Deck).filter(Deck.deck_id == a.deck_id).one()
                if d_name == found.deck_name:
                    app.logger.info("Duplicate deck name. Routing back to create_deck Page")
                    return redirect(url_for("create_deck", user_id = u_id))  
            
            #Inserting in Review Table
            try:
                insert_score = Review(review_time = None, score = None)
                session.add(insert_score)             
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()
            
            #Inserting in Deck Table
            try:
                insert_deck = Deck(deck_name = d_name, review_id = insert_score.review_id)
                session.add(insert_deck)             
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()
        
            #Inserting in User_Deck table
            try:
                d_id = insert_deck.deck_id
                insert_user_deck = User_Deck(user_id = u_id, deck_id = d_id)
                session.add(insert_user_deck)             
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()

            app.logger.info("Creation of deck successful. Routing to Dashboard")
            message2 = "Deck successfully created"
            return redirect(url_for("dashboard", user_id = u_id))  


#Deleting a Deck
@app.route("/delete_deck/<int:user_id>/<int:deck_id>", methods = ["GET", "POST"])
def delete_deck(user_id, deck_id):
    u_id = user_id
    d_id = deck_id
    with Session (engine) as session:
        session.begin()
        try:
            find_user_deck = session.query(User_Deck).filter((User_Deck.user_id == u_id)&(User_Deck.deck_id == d_id)).one()
            find_deck = session.query(Deck).filter(Deck.deck_id == d_id).one()
            session.delete(find_user_deck)
            session.delete(find_deck)       
        except:
            print("Excpetion, rolling back")
            session.rollback()
            raise
        else:
            app.logger.info("No exception, hence commit")
            session.commit()
    app.logger.info("Deletion of deck successful. Routing to Dashboard")
    return redirect(url_for("dashboard", user_id = u_id))  

#Editing a Deck
@app.route("/edit_deck/<int:user_id>/<int:deck_id>", methods = ["GET"])
def edit_deck(user_id, deck_id):
    u_id = user_id
    d_id = deck_id
    with Session(engine) as session: 
        find_card = session.query(Deck_Card).filter(Deck_Card.deck_id == d_id).all() 
        card_list = []
        for a in find_card:
            found = session.query(Card).filter(Card.card_id == a.card_id).all()
            card_list = card_list + found   
    message1 = "Current cards in the deck"
    app.logger.info("Routed to Edit Deck page successful.")
    return render_template ("edit_deck.html",  message = message1, card_list = card_list, deck_id = d_id, user_id = u_id)

#Creating a Card
@app.route("/create_card/<int:user_id>/<int:deck_id>", methods=["GET", "POST"])
def create_card(user_id, deck_id):
    u_id = user_id
    d_id = deck_id
    if request.method == "GET":
        app.logger.info("Routed to Create Card page successful.")
        return render_template ("create_card.html", user_id = u_id, deck_id = d_id)
    elif request.method == "POST":
        form = request.form
        front_text = form["front_text"]
        back_text = form["back_text"]
        with Session(engine) as session:
            #Inserting in Card Table
            try:
                insert_card = Card(front = front_text, back = back_text, card_score = 0, times_review = 0)
                session.add(insert_card)             
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()
            
            #Inserting in Deck_Card Table
            try:
                c_id = insert_card.card_id
                insert_deck_card = Deck_Card(deck_id = d_id, card_id = c_id)
                session.add(insert_deck_card)             
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()

            app.logger.info("Creation of card successful. Routing to Edit Deck")
            return redirect(url_for("edit_deck", user_id = u_id, deck_id = d_id)) 

#Deleting a Card
@app.route("/delete_card/<int:user_id>/<int:deck_id>/<int:card_id>", methods = ["GET", "POST"])
def delete_card(user_id, deck_id,card_id):
    u_id = user_id
    d_id = deck_id
    c_id = card_id
    with Session (engine) as session:
        session.begin()
        try:
            find_card_deck = session.query(Deck_Card).filter((Deck_Card.deck_id == d_id)&(Deck_Card.card_id == c_id)).one()
            find_card = session.query(Card).filter(Card.card_id == c_id).one()
            session.delete(find_card_deck)
            session.delete(find_card)       
        except:
            print("Excpetion, rolling back")
            session.rollback()
            raise
        else:
            app.logger.info("No exception, hence commit")
            session.commit()
    app.logger.info("Deletioon of card successful.")
    return redirect(url_for("edit_deck", user_id = u_id, deck_id = d_id))  

#Editing a Card
@app.route("/edit_card/<int:user_id>/<int:deck_id>/<int:card_id>", methods = ["GET", "POST"])
def edit_card(user_id, deck_id, card_id):
    u_id = user_id
    d_id = deck_id
    c_id = card_id
    if request.method == "GET":
        with Session (engine) as session:
            card = session.query(Card).filter(Card.card_id == c_id).one()
        app.logger.info("Routed to Edit card page successful.")
        return render_template ("edit_card.html",  card = card, deck_id = d_id, user_id = u_id)
    elif request.method == "POST":
        form = request.form
        front_text = form["front_text"]
        back_text = form["back_text"]
        with Session (engine) as session:
            session.begin()
            try:
                update_card = session.execute(Card.query.filter(Card.card_id == c_id)).scalar_one()
                update_card.front = front_text
                update_card.back = back_text
            except:
                print("Excpetion, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()

        app.logger.info("Updation of card successful. Routing to Edit Deck")
        return redirect(url_for("edit_deck", user_id = u_id, deck_id = d_id)) 

#Reviewing a Deck
@app.route("/review_deck/<int:user_id>/<int:deck_id>", methods = ["GET"])
@app.route("/review_deck/<int:user_id>/<int:deck_id>/<int:card_id>", methods = ["POST"])
def review_deck(user_id, deck_id, card_id = None):
    u_id = user_id
    d_id = deck_id
    c_id = card_id
    scores = {'easy': 3, 'medium':2, 'difficult':1}
    with Session (engine) as session:
        find_card = session.query(Deck_Card).filter(Deck_Card.deck_id == d_id ).all()
        card_list = []
        for a in find_card:
            found = session.query(Card).filter(Card.card_id == a.card_id).all()
            card_list = card_list + found
    if request.method == "GET":
        if len(find_card) != 0:
            select_card = random.choice(card_list)
            app.logger.info("Routed to Review page successful.")            
            return render_template("review.html", card = select_card, user_id = u_id, deck_id = d_id)
        else:
            flash("No cards in the Deck")
            app.logger.info("Routed to Review page successful.")
            return redirect(url_for("dashboard", user_id = u_id))       
    elif request.method == "POST":
        form = request.form
        score_value = form["difficulty"]
        with Session(engine) as session:
            #Upating Score in the Card
            try:
                update_card = session.execute(Card.query.filter(Card.card_id == c_id)).scalar_one()
                update_card.card_score =  update_card.card_score + scores[score_value]
                update_card.times_review = update_card.times_review + 1
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()
            app.logger.info("Updating of score to Card successful. Moving to update Review")

            #Finding average score of the deck post the updation of score in the card
            find_deck = session.query(Deck_Card).filter(Deck_Card.deck_id == d_id).all()
            card_list = []
            for a in find_deck:
                found = session.query(Card).filter(Card.card_id == a.card_id).all()
                card_list = card_list + found
            total_score = 0
            for b in card_list:
                if b.times_review != 0:
                    card_score = b.card_score/b.times_review
                    total_score = total_score + card_score
            avg_score = total_score/len(card_list)
            avg_score_string = str(round(avg_score,2))
            app.logger.info("Average score calculated successfully.")

            #Finding time to update
            result = time.localtime()  
            time_string = time.strftime("%d/%m/%Y, %H:%M:%S", result)
            app.logger.info("Time stored for updation.")

            #Updating the average score in review table
            try:
                insert_score = Review(review_time = time_string, score = avg_score_string)
                session.add(insert_score)             
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()
            app.logger.info("Updating of score and review to Review successful. Moving to update Deck")
            
            #Deleting old review_id in Review Table
            try:
                find_deck = session.query(Deck).filter(Deck.deck_id == d_id).one()
                find_review = session.query(Review).filter(Review.review_id == find_deck.review_id).one()
                session.delete(find_review)    
            except:
                print("Excpetion, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()
            app.logger.info("Old review_id row in Review table deleted successfully.")
            
            #Updating the deck table with review_id
            try:
                r_id = insert_score.review_id
                update_deck = session.execute(Deck.query.filter(Deck.deck_id == d_id)).scalar_one()
                update_deck.review_id = r_id            
            except:
                app.logger.info("Exception, rolling back")
                session.rollback()
                raise
            else:
                app.logger.info("No exception, hence commit")
                session.commit()  
            app.logger.info("Updating of review_id to Deck successful. Routing to Review Page")
            
            return redirect(url_for("review_deck", user_id = u_id, deck_id = d_id)) 
