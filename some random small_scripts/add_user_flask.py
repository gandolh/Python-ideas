from flask import Flask, request
import datetime
import re
import hashlib
app = Flask(__name__)


def save_user(Username, Password, Type):
    CreatedOn = datetime.datetime.now()
    # print(CreatedOn)
    to_write = "{};{};{};{}\n".format(Username, Password, Type, CreatedOn)
    with open('users.txt', 'a+') as f:
        f.write(to_write)


def valid_user(username):
    rexp = '^[^0-9].{,10}$'
    x = re.match(rexp, username)
    if x:
        return True
    else:
        return False


def already_exist(username):
    with open('users.txt', 'r') as f:
        line = f.readline()
        while line:
            if re.match(username+';', line) == True:
                return True
            line = f.readline()
    return False


def good_password(password):
    rexp = '(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&]).*'
    return bool(re.search(rexp, password))


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


@app.route('/')
def hello():
    return '123'


@app.route('/user/add', methods=['POST'])
def addUser():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user_type = data['user_type']
    if valid_user(username):
        if already_exist(username):
            print('User already exist!')
        else:
            if good_password(password):
                password = encrypt_string(password)
                if user_type in [0, 1]:
                    save_user(username, password, user_type)
                else:
                    return 'invalid Type'
            else:
                return 'Invalid password'
    else:
       return 'Invalid User'
    return 'user added'


if __name__ == '__main__':
    # add_data()
    app.run(debug=True, port=5000)
    pass
