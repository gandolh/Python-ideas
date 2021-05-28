from flask import Flask, request
import re

app = Flask(__name__)
valid_positions = ['GK', 'LB', 'CB', 'RB', 'LM', 'CM', 'RM', 'LW', 'RW', 'ST']
Echipe = {}


def valid_position(position):
    return position in valid_positions


def valid_team_name(name):
    rexp = '^(FC|CS)[\w\d -]+$'
    return bool(re.match(rexp, name))


class Jucator():
    def __init__(self, nume, prenume, varsta, pozitie, salariu):
        self.nume = nume
        self.prenume = prenume
        self.varsta = int(varsta)
        self.pozitie = pozitie
        self.salariu = int(salariu)
        if valid_position(pozitie) == False:
            raise Exception("Pozitie invalida")
        if self.salariu < 0:
            raise Exception('Salariul nu poate fi negativ')
        self.status = 'rezerva'

    def modify_salary(self, bonus):
        new_salary = self.salariu + int(bonus)
        if new_salary < 0:
            raise Exception('Salariul nu poate fi negativ')
        self.salariu = new_salary

    def modify_status(self, status):
        if status not in ['titular', 'rezerva']:
            raise Exception('Status invalid')
        self.status = status


class Echipa():
    def __init__(self, nume):
        if valid_team_name(nume) == False:
            raise Exception('Numele echipei nu coincide cu cerinta')
        self.nume = nume

    def add_player(self, jucator):
        if getattr(self, 'players_list', None) == None:
            self.players_list = [jucator, ]
        else:
            self.players_list.append(jucator)

    def get_all_players(self):
        return self.players_list

    def get_reserves(self):
        reserves_list = []
        for player in self.players_list:
            if player.status == 'rezerva':
                reserves_list.append(player)
        return reserves_list

    def get_youth_players(self):
        youth_players = filter(lambda x: x.varsta <= 21, self.players_list)
        return youth_players
    def __str__():
    	sum=0
    	for player in list_of_players:
    		sum+=player.salariu
    	return '{};{};{}'.format(self.nume,len(self.players_list),sum)

def adding_player_in_database(nume, prenume, varsta, echipa, pozitia, salariu):
	with open('jucatori.txt', 'a+') as f:
		f.write('{};{};{};{};{};rezerva;{}'.format(
		    nume, prenume, varsta, echipa, pozitia, salariu))


@app.route('/')
def hello():
    return 'hi'


@app.route('/add/team', methods=['POST'])
def add_team():
    data = request.get_json()
    nume = data['nume']  # atentie e nume nu name, facui o data greseala asta
    print(nume)
    Echipe[nume] = Echipa(nume)  # adaug in lista globala in constructor
    return 'Team added succesfully'


def save_player(data):
	nume = data['nume']
	prenume = data['prenume']
	varsta = data['varsta']
	pozitie = data['pozitie']
	echipa = data['echipa']
	salariu = data['salariul']
	Echipe[echipa] = Echipa(echipa)
	adding_player_in_database(nume,prenume,varsta,echipa,pozitie,salariu)
	for x in Echipe:
		if x == echipa:
			Echipe[x].add_player(
                Jucator(nume, prenume, varsta, pozitie, salariu))

@app.route('/add/player', methods=['POST'])
def add_player_flask():
    data = request.get_json()
    save_player(data)
    return 'player added succesfully'

@app.route('/add/multiple_players',methods=['POST'])
def add_multiple_players():
	data = request.get_json()
	list_of_players=data['jucatori']
	for data in list_of_players:
		save_player(data)

@app.route('/save/team',methods=['GET'])
def save_team():
	data=request.args
	echipa= data['echipa']
	for x in Echipe:
		if x== echipa:
			with open('echipe.txt') as f:
				f.append(str(Echipe[x]))

	return 'OOpsie,no time'
if __name__ == '__main__':
	app.run(debug=True, port=5000)

    # j1 = Jucator('alex', 'Cri', '18', 'GK', '5000')
    # j2 = Jucator('Gica', 'Hagi', 101, 'ST', '69420')
    # print("{} {} {} {} {}".format(j1.nume, j1.prenume, \
    #                               j1.varsta, j1.pozitie, j1.salariu))
    # j1.modify_salary('300')
    # print(j1.salariu)
    # j2.modify_status('titular')

    # print(j1.status)
    # e1 = Echipa('FC alex')
    # print(e1.nume)
    # e1.add_player(j1)
    # e1.add_player(j2)
    # print(e1.players_list[0].nume)
    # all_players_in_e1 = e1.get_all_players()
    # for x in all_players_in_e1:
    #     print(x.nume)

    # all_reserves_in_e1 = e1.get_reserves()
    # for x in all_reserves_in_e1:
    #     print(x.nume)

    # youth_in_e1 = e1.get_youth_players()
    # for x in youth_in_e1:
    #     print(x.nume)
    # for e in Echipe:
    # 	print(e)
	pass
