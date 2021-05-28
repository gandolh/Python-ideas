from flask import Flask
import c7e1
import c7e2
import re
import json
app= Flask(__name__)

@app.route('/')
def hello():
	return '<h1>hello!</h1>'
@app.route('/c7e1')
def solving1():
	result=''
	# result+='<style> .cards{display:inline-block;margin-right:5px}</style>'
	#for displaying cards on one line, personally i think it looks better cascading
	result+='<title> Sa ma bata mamaita</title>'
	deck = c7e1.Deck()
	for i in range(10):
		deck.add(c7e1.Card(c7e1.posible_values[i], c7e1.symbols[0]))
	result+= '<h1>deck before shuffle</h1>'
	for card in deck.cards:
		result+='<p class="cards">  {} {} </p>'.format(card.value,card.symbol)
	deck.shuffle()
	error=deck.add(2)
	if error==-1:
		# print('Duplicate')
		result+='<p>Duplicate</p>'
	elif error==-2:
		# print('invalid type')
		result+='<p>Trying to add 2</p>'
		result+='<p>invalid type</p>'
	error=deck.delete(2)
	if error==-1:
		result+='<p>Trying to remove 2</p>'
		result+='<p>Cannot remove this Card.</p>'
	result+='<h1> After shuffle</h1>'
	for card in deck.cards:
		result+='<p class="cards"> {} {} </p>'.format(card.value,card.symbol)
	result+='<h1> Full Deck</h1>'
	deck1=c7e1.CreateFullDeck()

	for card in deck1.cards:
		result+='<p class="cards"> {} {} </p>'.format(card.value,card.symbol)
	return result
@app.route('/c7e2')
#using the plural of regex
def regrets():
	result=''
	result+='<title> regrets.py</title>'
	result+='<style> .elem{display:inline-block;margin-right:20px}</style>'
	result+='<h2>text-ul 1</h2>'
	lx=c7e2.x.split('\n')
	for sentence in lx:
		result+='<p>{}</p>'.format(sentence)
	result+='<h2>text-ul 2</h2>'
	result+='<p>{}</p>'.format(c7e2.sentence)
	result+='<h2>Regex Results</h2>'
	my_dict={}
	y = re.findall(c7e2.rexp, c7e2.x)
	my_dict['ore']=y
	y1 = re.findall(c7e2.rexp1, c7e2.x)
	my_dict['date']=y1
	y2 = re.findall(c7e2.rexp2, c7e2.x)
	my_dict['numere']=y2
	y3=re.search(c7e2.rexp3,c7e2.sentence)
	#FBL= First big letter
	my_dict['FBL']=y3.groups()

	# z=json.dumps(my_dict,indent=4)
	#good displaying
	for key in my_dict.keys():
		result+='<p class="elem">{}:'.format(key)
		for value in my_dict[key]:
			result+='<p class="elem">{}</p>'.format(value)
		result+='</p>'

	return result;

	return result
if __name__ == '__main__':
	app.run(debug="True",port=5001)
