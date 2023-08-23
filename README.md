# Zsaszk! - A forum page web application

## Short introduction

This is the third and last sprint of our team project named "Zsaszk!" at our programming school Codecool, it's about creating a web app where anyone can ask anything. You can visit the page as a guest and view questions and answers. If you'd like to, you can create a new user to be able to ask and answer questions, as well as to tag, upvote or downvote them. There are also a number of little inside jokes and easter eggs we've hidden inside the webpage or the code.

## Technologies

- backend, server: Python Flask
- template design: HTML, CSS, SCSS (grid, flex)
- template engine: Jinja2
- database: PostgreSQL
- encryption, password hashing: Bcrypt
- Gitflow workflow
- Javascript basic DOM manipulation

## Installation guide

1. You'll need at least Python 3.8 to be able to run the server. Please install Python 3.8 and a compatible version of pip package manager.
2. Install the necessary requirements with pip included in the "requirements.txt" file.
3. Install PostgreSQL (and optionally PgAdmin) and create a new database for this app (database name "zsaszk-3" by default), run "ask_mate_sprint_3.sql" code to set up a database schema.
4. Modify the ".env" file using your own environment variable for the project
5. (Optional) Install a Python IDE to be able to open and execute the project files more easily. Jetbrains Pycharm or VS Code is recommended.
6. Execute the "server.py" file, run as an administrator if necessary.
7. If the server runs flawlessly, you'll see it responding in the console log.
8. Navigate to "localhost:5000" in a web browser of your choice.
9. If everything is working as intended, you'll see the homepage of our website. Press Ctrl+F5 to reload the page, if necessary.
10. Have fun!

If you'd like to ask any questions or you have trouble setting up the work environment or the server please contact me, SzimBensze. The project is considered finished and is not going to recieve any updates soon. Contributors: Deezyeke, MiMi0001, ahpmh, WonkeTomi, SzimBensze. Please look for the contributors sidebar for more contact information.

## Task description and backstory

"Last week you made great progress improving your web application.
We need some more features to make it more usable and more appealing to users.

The users requested new features, such as the ability to register and login.
There are a few other feature requests which you can find in the user stories.

The management wants you to separate the already working features from
the upcoming ones, so your development team need to **start using branching
workflow and open new branches for the features you start in this sprint**.
Just like last week, the ownership is in your hands. There are no compulsory stories,
but of course, management would prefer if all stories were implemented.
So first, choose the stories, then ask a mentor to validate your choice.

Just like last week, you have a **prioritized list** of new user stories that you should
add to the unfinished stories from last week on your product backlog. Try to
estimate these new stories as well, and, based on the estimations, decide how many
your team can finish until the demo. As the order is important, you choose
from the beginning of the list as much as you can."

### This week's goals

1. Since you work in a new repository, but also need the code from the previous sprint, add the `ask-mate-3` repository as a new remote to the repository of the previous sprint, then pull (merge) and push your changes into it.
    - There is a merge commit in the project repository that contains code from the previous sprint.

2. As a user, I would like to be able to register a new account in the system.
    - There is a `/registration` page.
    - The page is linked from the front page.
    - There is a form on the `/registration` page when a request is issued with the `GET` method.
    - The form ask for a username (or email address) and a password, then issues a `POST` request to `/registration` on submitting.
    - After submitting, the page redirects to the main page and the new user account is saved in the database.
    - A user account consists of an email address stored as a username, a password stored as a password hash, and a registration date.

3. As a registered user, I would like to be able to log in to the system with my previously saved username and password.
    - There is a `/login` page.
    - The page is linked from the front page.
    - Theres is a form on the `/login` page when a request is issued with `GET` method.
    - The form asks for the username (email address) and password, then issues a `POST` request to `/login` on submit.
    - After submitting the page redirects to the main page and the user is logged in.
    - It is only possible to ask or answer a question when logged in.

4. There should be a page where I can list all the registered users with all their attributes.
    - There is a `/users` page.
    - The page is linked from the front page when logged in.
    - The page is not accessible without logging in.
    - Theres is a `<table>` with user data in it. The table contains the following details of a user.
  - Username (with a link to the user page if implemented)
  - Registration date
  - Number of asked questions (if binding is implemented)
  - Number of answers (if binding is implemented)
  - Number of comments (if binding is implemented)
  - Reputation (if implemented)

5. As a user, when I add a new question, I would like to be saved as the user who created the new question.
    - The user ID of the logged in user is saved when a new question is added.

6. As a user, when I add a new answer, I would like to be saved as the user who created the new answer.
    - The user ID of the logged in user is saved when a new answer is added.

7. As a user, when I add a new comment, I would like to be saved as the user who created the new comment.
    - The user ID of the logged in user is saved when a new comment is added.

8. There should be a page where we can see all details and activities of a user.
    - There is a `/user/<user_id>` page.
    - The user page of a logged in user is linked from the front page.
    - The page of every user is linked from the users list page.
    - Theres is a list with the following deatils about the user.
  - User ID
  - Username (link to user page if implemented)
  - Registration date
  - Number of asked questions (if binding is implemented)
  - Number of answers (if binding is implemented)
  - Number of comments (if binding is implemented)
  - Reputation (if implemented)
    - There is a separate table where every **question** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **answer** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **comment** is listed that the user created. The related question is linked in every line.

9. As a user, I would like to have the possibility to mark an answer as accepted.
    - There is a clickable element for every answer on the question page, that can be used for marking an answer as accepted.
    - There is an option to remove the accepted state from an answer.
    - Only the user who asked the question can change the accepted state of answers.
    - An accepted answer has some visual distinction from other answers.

10. As a user, I would like to see a reputation system to strengthen the community. Reputation is a rough measurement of how much the community trusts a user.
    - **A user gains reputation when:**
- their question is voted up: +5
- their answer is voted up: +10
- their answer is marked "accepted": +15

11. As a user, I would like to see a small drop in reputation when a user's question or answer is voted down.
    - **A user loses reputation when:**
- their question is voted down: −2
- their answer is voted down: −2

12. As a user, I would like to see a page that lists all existing tags and the number of questions marked with those tags.
    - There is a `/tags` page.
    - The page is linked from the front page and a question page.
    - The page is accessible whithout logging in.

13. When the user navigates to the `bonus-questions` route and types in the input box, the displayed questions are filtered to match the criteria. This must be done without page reload.
    - When typing `life`, the only question displayed is the one titled `What is the meaning of life ?`.
    - When typing `!life`, questions are filtered to the ones that do NOT include the word `life`. (That is nine questions in this scenario.)
    - When typing `Description:life`, questions are filtered to those that include the word `life` in the `Description` column. (No question is displayed in this scenario.)
    - When typing `!Description:life`, questions are filtered to those that do NOT include the word `life` in the `Description column. (All ten questions are displayed in this scenario)

14. When the user navigates to the `bonus-questions` route and clicks on any table header, the items are sorted based on the column. This must be done without page reload.
    - When clicking the `Description` column, the questions are sorted in alphabetical order, based on the values from the `Description` column.
    - When clicking the `Description` column a second time, the questions are sorted in reverse alphabetical order, based on the values from the `Description` column.

15. [OPTIONAL] When the user navigates to the `bonus-questions` and clicks the `Decrease page font` or `Increase page font` button, the font size is decreased or increased in the page, respectively. This must be done without page reload.
    - Clicking the `Increase page font` button increases the font in the page.
    - Clicking the `Increase page font` button multiple times increases the font size to a maximum of 15. Further clicks do not result in an increase.
    - Clicking the `Decrease page font` button decreases the font the page.
    - Clicking the `Decrease page font` button multiple times decreases the font size to a minimum of 3. Further clicks do not result in an decrease.

## End note

The project is public, but please do not copy and reshare the source without permission! Only use for personal or educational purposes. Thank you for checking out our repo!
