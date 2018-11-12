My application utilizes the IMDB API to allow users to search for movies while giving them data about the movies they searched. It also provides a place for users to enter a review on a desired movie. 

When you visit http://localhost:5000/movie_entry, you can submit the name of a movie (Ted, Titanic, etc), you will be taken to http://localhost:5000/movie_answers,  which provides you with the respective movie’s director, rating (PG-13, R), and year of release. 

Furthermore, when you visit http://localhost:5000/reviews , you can enter the name of the movie that you’d like to review, along with a 5-star rating and a short description of the review.


!!!ROUTES!!!

The application should have the following routes, each rendering the template listed below:
•	http://localhost:5000/movie_entry -> movie_entry.html
•	http://localhost:5000/movie_answers-> movie_answers.html
•	http://localhost:5000/reviews -> reviews.html

