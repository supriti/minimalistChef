#!/usr/bin/python3.4

from bs4 import BeautifulSoup
import requests
import re
import time
import mysql.connector
import time

'''
These are the levels at which we are crawling
Intersection of each level should be empty. 
We can just go in iterative order. So you can reach 
level 2 from 1 or 0. 
level_0 contains all hyperlinks following the main link.
level_1 contains all hyperlinks following level_0
level_2 contais the hyperlink containing single recipe.
'''
level0_links = set()
level1_links = set()
level2_links = set()

'''
DB def
'''
select_recipe = ("SELECT id from recipes "
                 "WHERE name=%s")

insert_recipe = ("INSERT INTO recipes "
              "(name, url, image_url, created_at, updated_at) "
              "VALUES (%s, %s, %s, %s, %s)")

select_ingredient = ("SELECT id from ingredients "
                     "WHERE name=%s")

insert_ingredient = ("INSERT INTO ingredients "
                   "(name, created_at, updated_at) "
                   "VALUES (%s, %s, %s)")

insert_recipe_ingredient = ("INSERT INTO recipe_ingredients "
                         "(recipe_id, ingredient_id, created_at, updated_at) "
                         "VALUES (%s, %s, %s, %s)")

'''
Debug
'''
supu = open("/home/supriti/work/minimalistChef/supu","w")
Ingredients = set()

def new_recipe (name, url, image_url, ingredients):
    mysql_cnx = mysql.connector.connect (user='supriti', password='password', database='chef_development', buffered=True)
    cursor = mysql_cnx.cursor()

    cursor.execute(select_recipe, (name,))
    print (cursor.rowcount)
    if (cursor.rowcount > 0):
        print("Recipe already exists!!")
        exit(1)

    cursor.execute(insert_recipe, (name, url, image_url, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

    cursor.execute(select_recipe, (name,))
    if (cursor.rowcount != 1):
        print("Recipe was not inserted in the table!")
        exit(1)
    else:
        for (id) in cursor:
            recipe_id = "{}".format(id)[1:-2]
            print (recipe_id)

    for ingredient in ingredients:
        cursor.execute(select_ingredient, (ingredient,))
        if (cursor.rowcount <= 0):
            # print("Ingredient was not found! Add Recipe")
            cursor.execute(insert_ingredient, (ingredient, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

        cursor.execute(select_ingredient, (ingredient,))
        if (cursor.rowcount != 1):
            print("Ingredient does not exist in the table!")
            exit(1)

        for (id) in cursor:
            ingredient_id = "{}".format(id)[1:-2]
            cursor.execute(insert_recipe_ingredient, (recipe_id, ingredient_id, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))

    mysql_cnx.commit()

#Extract the ingeridents from the table.
def parse(text):
    str1 = re.split(r'-', text)
    Ingredients.add(str1[0])
    #supu.write(str1[0])
    #supu.write("\n")
    #Add to the database and run query against it if it returns anything
    

def level_2(recipe_url):
    soup = BeautifulSoup(requests.get(recipe_url, verify=False).text, "lxml")
    count = 0

    #supu.write("Recipe URL:: " + str(recipe_url) + "\n")
    recipe_name = recipe_url.rpartition('/')
    #supu.write("Recipe Name:: " + recipe_name[-1] + "\n")
    for td in soup.find_all('td',{"colspan":"2"}):
        if count == 1:
            break
        if("Ingredients" in str(td.text)):
            count = count + 1
            continue

        if "Method" in str(td.text):
            return
        str1 = str(td.text)
        str1 = str1.replace("• ","")
        parse(str1)
        
    #for item in Ingredients:
    #    supu.write("%s\n" % item)
    #supu.write("\n")
    new_recipe (recipe_name[-1], recipe_url, " ", Ingredients)    
    Ingredients.clear()

def level_1(uri):
    soup = BeautifulSoup(requests.get(uri, verify=False).text, "lxml")

    for link in soup.findAll('h2', attrs={'class':'curry_p'}):
        if link in level0_links:
            continue
        level1_links.add(link.find('a')['href'])

    for item in level1_links:
        level_2(item)
    

def level_0(start_address):
    level0_links.add(start_address)

    soup = BeautifulSoup(requests.get(start_address, verify=False).text, "lxml")
    for link in soup.find_all('a', href=re.compile(r'recipe')):
        level0_links.add(link['href'])
    
    for item in level0_links:
        level_1(item)


def main():
    level_0("https://www.vahrehvah.com/")

if __name__ == "__main__": main()