###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError, RadioField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import json

## App setup code
app = Flask(__name__)
app.debug = True

## All app.config values
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://HarrisonDvoor@localhost/HDvoorSI364F18'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################
def get_or_create_movie(director, year, rated, title):
    unique_movie = MovieInfo.query.filter_by(director=director, title=title).first()
    if unique_movie is None:
        movie = MovieInfo(director=director,year=year,rated=rated,title=title)
        db.session.add(movie)
        db.session.commit()
        return movie
    else:
        return unique_movie

def get_or_create_reviews(movie, rating, review):
    unique_review = Reviews.query.filter_by(movie_id=movie.id,review=review).first()
    if unique_review:
        flash('This movie has already received the same review...leave a different review')
        return redirect(url_for('movie_entry'))
    else:
        review = Reviews(rating=rating, review=review, movie_id=movie.id)
        db.session.add(review)
        db.session.commit()
        return review

def get_omdb(movie_title):
    OMDB_API_KEY = '88dfac0f'
    OMDB_base_url = 'http://www.omdbapi.com/'
    resp1 = requests.get(OMDB_base_url, params={'apikey': OMDB_API_KEY, 't': movie_title})
    obj1 = json.loads(resp1.text)
    return obj1

def get_director(api_dict):
    director = api_dict['Director']
    return director


def get_year(api_dict):
    year = api_dict['Year']
    return year

def get_rated(api_dict):
    rated = api_dict['Rated']
    return rated

def get_title(api_dict):
    title = api_dict['Title']
    return title

def main():
    print (get_omdb('Ted'))
    print (type(get_omdb('Ted')))



##################
##### MODELS #####
##################

class MovieInfo(db.Model):
    __tablename__ = "Movies"
    id = db.Column(db.Integer, primary_key = True)
    director = db.Column(db.String)
    year = db.Column(db.String)
    rated = db.Column(db.String)
    title = db.Column(db.String)
    review = db.relationship('Reviews', backref='Movies')
    def __repr__(self):
        return "{} (ID: {})".format(self.title, self.id)

class Reviews(db.Model):
    __tablename__ = "Reviews"
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.id'))



###################
###### FORMS ######
###################

class MovieForm(FlaskForm):
    movie_name = StringField("Please enter the name of a movie: ",validators=[Required()])
    submit = SubmitField()

class ReviewForm(FlaskForm):
    movie = StringField('Please enter the name of a movie you want to review: ', validators=[Required()])
    rating = IntegerField('Enter a rating from 0-5',validators=[Required()])
    review = StringField('Please enter your review',validators=[Required()])
    submit = SubmitField()

def validate_rating(self, field):
    if self.rating.data > 5 or self.rating.data < 0:
        raise ValidationError('Invalid Rating. Must be between 0 and 5.')


#######################
###### VIEW FXNS ######
#######################


@app.route('/movie_entry', methods=['GET','POST'])
def movie_entry():
    my_form = MovieForm()
    num_movies = MovieInfo.query.count()

    return render_template('movie_entry.html', form = my_form, num_movies=num_movies)

@app.route('/movie_answers')
def answers():
    if request.args:
        movie = request.args.get('movie_name')
        api_dict = get_omdb(movie)
        director = get_director(api_dict)
        year = get_year(api_dict)   
        rated = get_rated(api_dict)
        title =get_title(api_dict)
        print(title)
        print(year)
        print(rated)
        print(director)
        movie = get_or_create_movie(director, year, rated, title)
    
    movie_lst = []
    
    for movies in MovieInfo.query.all():
        director = movies.director
        year = movies.year
        rated = movies.rated
        title = movies.title
        movie_lst.append((director,year,rated,title))
    return render_template('movie_answers.html', movie_lst=movie_lst)


@app.route('/reviews', methods = ["GET", "POST"])
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        movie = form.movie.data
        rating = form.rating.data
        review = form.review.data

        movie1 = MovieInfo.query.filter_by(title=movie).first()

        get_or_create_reviews(movie1,rating,review)

    rev_lst = []
    for rev in Reviews.query.all():
        rating_data = rev.rating
        review_data = rev.review
        movie_data = MovieInfo.query.filter_by(id=rev.movie_id).first()
        rev_lst.append((rating_data,review_data, movie_data))
    return render_template('reviews.html', form=form, rev_lst=rev_lst)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

## Code to run the application...
# Put the code to do so here!
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
