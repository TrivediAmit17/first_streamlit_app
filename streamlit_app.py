import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#create the repetable code block (Function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())    
  return fruityvice_normalized  

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruite to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLErrror as e:
  streamlit.error()
  
streamlit.write('The user entered ', fruit_choice)

#streamlit.text(fruityvice_response.json())

streamlit.header("Fruite load list contains:")
#snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("use warehouse pc_rivery_wh")
    my_cur.execute("SELECT Fruit_name from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

 # add a button to load the fruit
if streamlit.button('Get Fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("use warehouse pc_rivery_wh")
    stremlit.text("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit +"')")
    #my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)


# don't run the code after this
streamlit.stop()
