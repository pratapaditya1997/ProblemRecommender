from bs4 import BeautifulSoup as bs
import requests

url = 'https://a2oj.com/categories'
response=requests.get(url)

soup = bs(response.text,'html.parser')

category_codes = {'Dynamic Programming':'0',
                  'implementation':'0',
                  'math':'0',
                  'Greedy':'0',
                  'Graph Theory':'category?ID=13',
                  'data structures':'0',
                  'Binary Search & Ternary Search':'0',
                  'constructive algorithms':'0',
                  'Geometry':'0',
                  'strings':'0'}

#parsing for getting the links of respective categories
for categories in soup.findAll('a'):
    if categories.parent.name == 'td':
        category_name = categories.text
        category_code = categories['href']
        if category_name in category_codes:
            category_codes[category_name]=category_code

#mapping the category names with an integer
mapping_categories={}
counter=0
for cat_name,cat_code in category_codes.items():
    mapping_categories[counter]=cat_name
    counter+=1

print('\nType the number of category you want to practice')
print('example - Type 0 if you want to practice DP')
print()

for i,j in mapping_categories.items():
    print(str(i)+' '+j)

choosen_cat = int(input())

print('\nYou chose '+str(choosen_cat)+': '+mapping_categories[choosen_cat])

base = 'https://a2oj.com/'
choosen_cat_code = mapping_categories[choosen_cat]
req_url = base+category_codes[choosen_cat_code]

res = requests.get(req_url)
soup = bs(res.text,'html.parser')

problems = {}
distinct_levels = set()

#parsing the problems page for getting links and difficulty level of each problem
tabulka = soup.find('table',{'class':'tablesorter'})
for row in tabulka.findAll('tr')[1:]:
    level = 0
    counter=0
    for i in row.findAll('td'):
        if counter==6:
            level=int(i.text)
            distinct_levels.add(level)
        counter+=1
    for links in row.findAll('a',target='_blank'):
        if links.parent.name == 'td':
            problems[links['href']]=level

print('choose a difficulty level of problem for practice')
for i in distinct_levels:
    print(i)

choosen_level = int(input())

print('\nYou have chosen difficulty level = '+ str(choosen_level))

#making a list of problems of same difficulty as choosen by the user
req_probs = []
for i,j in problems.items():
    if j==choosen_level:
        req_probs.append(i)

total = len(req_probs)

from random import randint
random_number = randint(0,total )

print('\nRandomly generated problem for your practice is -\n')
print(req_probs[random_number])
print()

print('Do you want us to open the problem for you in the browser (too lazy to copy and paste :P)')
print('type [y]/[n]')

#checking the python version for taking the text input
import sys
if sys.version_info[0]<3:
    ans=raw_input()
else:
    ans=input()


if ans == 'y' or ans == 'Y':
    import webbrowser
    webbrowser.open(req_probs[random_number],new=0,autoraise=True)

print('\n THANK YOU FOR USING!\n')
