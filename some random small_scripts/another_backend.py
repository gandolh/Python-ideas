import hashlib
import json
import re

from flask import Flask, request
from datetime import datetime

# We create a Flask object and store some global variables
app = Flask(__name__)
users_filename = "users.txt"
articles_filename = "articles.txt"
ID = 0


def is_valid_username(username):
    """
    Checks if a username is valid. Usernames should be at most 10 characters long and should not start with a digit.
    :param username: string
    :return:    True if the username is valid.
                False if the username is not valid.
    """
    regex = "^\D.{0,9}$"
    result = re.findall(regex, username)
    return bool(result)


def check_username_exists(username):
    """
    Reads the users file and checks if the user already exists in that file. It is not enough to check if the username
    is in the file, since it can appear in the password hash. Thus, it is important that we check if the username equals
    the first element of a line after it has been split by the ";" character.
    :param username: string
    :return:    True if the user already exists.
                False if the user does not exist.
    """
    with open(users_filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if username == line[0]:
            return True
    return False


def is_valid_password(password):
    """
    Checks if a password is valid. Passwords should contain at least one uppercase letter, one lowercase letter, one
    digit and one special character.
    :param password:    string
    :return:    True if the password is valid.
                False if the password is not valid.
    """
    regex = "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&]).*"
    result = re.findall(regex, password)
    return bool(result)


def encrypt_password(password):
    """
    Encrypts a password using SHA256 format.
    :param password: string
    :return:    The encrypted password.
    """
    enc_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return enc_pass


def write_user(username, password, user_type):
    """
    Writes a user's info in the users file. It also adds the date and time.
    :param username: string
    :param password: string
    :param user_type: string
    :return:
    """
    createdOn = datetime.now().strftime("%H:%M:%S-%d/%m/%Y")
    to_write = username + ";" + password + ";" + user_type + ";" + createdOn + "\n"
    with open(users_filename, "a+") as f:
        f.write(to_write)


def add_new_user(username, password, user_type):
    """
    Checks if a user has valid username, password and type. Also, it checks if the user already exists. Afterwards, if
    everything is in order, it encrypts the password and saves the user by calling the "write_user" function.
    :param username:    string
    :param password:    string
    :param user_type:   int
    :return:    string, message containing information regarding the success of the operation.
    """
    if not is_valid_username(username):
        return "Invalid username. Please make sure it does not start with a digit and has at most 10 characters."
    if check_username_exists(username):
        return "Username %s already exists!" % username
    if not is_valid_password(password):
        return "Invalid password. The password must contain at least one uppercase letter, one lowercase letter, " \
               "one digit and one special character!"
    if user_type not in [0, 1]:
        raise Exception("Invalid type. Type must be 0 or 1. 0=Administrator, 1=User")
    enc_password = encrypt_password(password)
    user_type = str(user_type)
    write_user(username, enc_password, user_type)
    return "User added to the file successfully!"


def is_valid_title(title):
    """
    Checks if the title is valid. Titles should not be longer than 50 characters.
    :param title: string
    :return:    True if the title is valid.
                False if the title is not valid.
    """
    regex = "^.{1,50}$"
    result = re.findall(regex, title)
    return bool(result)


def get_writer_info(writer):
    """
    Given a username it retrieves the user's information, if the username is found in the users file.
    :param writer:  string
    :return:    dictionary containing the user's information
    """
    with open(users_filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if writer == line[0]:
            return {
                "password": line[1],
                "user_type": line[2],
                "createdOn": line[3]
            }
    return None


def generate_id():
    """
    Generates unique ids starting from 1, using the global variable ID.
    :return: int, the id value.
    """
    global ID
    ID += 1
    return ID


def write_article(title, content, writer):
    """
    Writes an in the articles file. It also adds and id and the date and time.
    :param title:   string
    :param content: string
    :param writer:  string
    :return:    None
    """
    id = str(generate_id())
    createdOn = datetime.now().strftime("%H:%M:%S-%d/%m/%Y")
    to_write = id + ";" + title + ";" + content + ";" + writer + ";" + createdOn + "\n"
    with open(articles_filename, "a+") as f:
        f.write(to_write)


def add_article(title, content, writer, password):
    """
    Checks if a article has a valid title, if the writer exists, if his password matches and if he has the rights to
    publish and article. Afterwards, if everything is in order, it saves the article by calling the "write_article"
    function.
    :param title:   string
    :param content: string
    :param writer:  string
    :param password:    string
    :return:    string, message containing information regarding the success of the operation.
    """
    if not is_valid_title(title):
        return "Invalid title. The title must have at most 50 characters."
    if not check_username_exists(writer):
        return "Writer %s does not exist!" % writer
    info = get_writer_info(writer)
    if encrypt_password(password) != info["password"]:
        raise Exception("Incorrect password")
    if info["user_type"] != "0":
        return "User not in rights to publish articles!"
    write_article(title, content, writer)
    return "Article added to the file successfully!"


def get_article(id):
    """
    Searches in the articles file for an article by an id. If the article is found, it is returned, otherwise a
    message is returned.
    :param id: int
    :return:    dictionary, containing the article's info, if the id is found
                string, message telling that the id was not found
    """
    with open(articles_filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if str(id) == line[0]:
            result = {
                "title": line[1],
                "content": line[2],
                "writer": line[3],
                "createdOn": line[4]
            }
            return json.dumps(result)
    return "Article with id %d does not exist!" % id


@app.route('/user/add', methods=["POST"])
def addUser():
    """
    Endpoint which accepts POST HTTP requests made for adding a new user. It extracts the data from the request and
    calls the "add_new_user" function.
    :return:    What the "add_new_user" function returns
    """
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user_type = data["user_type"]
        return add_new_user(username, password, user_type)
    else:
        return "Only the POST methods are allowed on this resource"


@app.route('/article/add', methods=["POST"])
def addArticle():
    """
    Endpoint which accepts POST HTTP requests made for adding a new article. It extracts the data from the request and
    calls the "add_article" functgeion.
    :return:    What the "add_article" function returns.
    """
    if request.method == "POST":
        data = request.get_json()
        title = data["title"]
        content = data["content"]
        writer = data["writer"]
        password = data["password"]
        return add_article(title, content, writer, password)
    else:
        return "Only the POST method is allowed on this resource"


@app.route('/article/get')
def getArticle():
    """
    Endpoint which accepts GET HTTP requests made for retrieving and article by using its id. Using the id parameter
    in the dynamic path, it calls the "get_article" function.
    :param id:  int
    :return:    What the "get_article" function returns.
    """
    if request.method == "GET":
        data = request.args
        id = data["id"]
        return get_article(id)
    else:
        return "Only the GET method is allowed on this resource"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # print(add_new_user("iedi", "aA1!", 0))
    # print(add_new_user("marius", "Blabla21@#", 1))
    # print(add_new_user("gigelus", "ds1A#adasda", 1))
    # print(add_article("Turbion", "Seria Turbion e cea mai bine scrisa poveste SF din ultimii 30 de ani", "iedi",
    #                   "aA1!"))
    # print(add_article("Dune", "Seria Dune e cea mai bine scrisa poveste SF din ultimii 60 de ani", "marius",
    #                   "Blabla21@#"))
    # print(add_article("Fundatia", "Seria Fundatia e cea mai bine scrisa poveste SF din toate timpurile", "iedi",
    #                   "aA1!"))
    # print(get_article(1))
    # print(get_article(2))
    # print(get_article(3))
    # print(get_article(4))
    # print(get_article(0))
