import streamlit
import pandas

streamlit.title('My Moms healthy Diner')
streamlit.header('🥭Breakfast Menu')
streamlit.text('🍌Omega 3 & Blueberry Oatmeal')
streamlit.text('🥝Kale, Spinach & Rocket Smoothie')
streamlit.text('🍇Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

# nornalisation of output
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# show the normalised output
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("use warehouse pc_rivery_wh")
my_cur.execute("SELECT *  as Fruit from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruite load list contains:")
streamlit.dataframe(my_data_rows)

my_fruit_list1 = my_fruit_list1.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
add_my_fruit = streamlit.multiselect("What fruite you would like to add:", list(my_fruit_list1.index))
#fruits_to_show = my_data_rows[add_my_fruit]
#streamlit.write('Thanks for adding ', fruits_to_show)
