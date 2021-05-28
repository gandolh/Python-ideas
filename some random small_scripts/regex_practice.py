import re
x = '''Ore bune: 13:02 , 23:45 , 02:23 
ore rele: 33:02 , 13:62 , 29:33 , 312:25
Data buna: 16/12/1989, 02/03/95 , 30/11/2015 , 18/02/1943 30/02/2005 
Data rea:	32/05/2020 12/15/2020
numere: 22 111 123.30 12.3 1,1 5 
nenumere: a e3 +-
'''
sentence='Ana are Mere.Ea pleaca la Mare distanta De casa'
# hh:mm
rexp = '((?:(?:[^0-9][0-1]?[0-9])|[2][0-3]):[0-5][0-9])'
# zz/ll/aaaa sau zz/ll/aa
rexp1 = '((?:(?:[0-2][0-9])|(?:3[01]))\/(?:(?:0[0-9])|(?:1[012]))\/[0-9][0-9](?:[0-9][0-9])?)'
#numere care sa nu fie date sau ore 
rexp2 = '[,. ][0-9]+[.,]?[0-9]*(?![\/:0-9])'
rexp3 = '([^.][A-Z]\w+)'
if __name__ == '__main__':
	y = re.findall(rexp, x)
	print('ore: ', y, sep='')
	y1 = re.findall(rexp1, x)
	print('date: ', y1, sep='')
	y2 = re.findall(rexp2, x)
	print('numere:',y2,sep='')
	y3=re.search(rexp3,sentence)
	print(y3.groups())