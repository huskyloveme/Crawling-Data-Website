import sqlalchemy as db
import pandas as pd
import re
import json

#Create engine MYsql
engine = db.create_engine("mysql+pymysql://root:@localhost:3306/data_craw")
connection = engine.connect()

# Handle dataframe before write to SQL
df = pd.read_csv("data_craw_one_thread.csv")

# Convert current_price to float
df['current_price'] = df['current_price'].str.replace(',','').astype(float)

# Make the shipping from string to float
df['int_shipping'] = df['shipping'].apply(lambda x: x.split(' ')[0])
def convert_shipping(value):
    rs = re.findall(r"(\d+\.\d+)", value)
    if len(rs) > 0:
        return rs[0]
    return 0
df['int_shipping'] = df['int_shipping'].apply(convert_shipping)
df['int_shipping'] = df['int_shipping'].astype(float)

# Make the total price column
df['total_price'] = df['current_price'] + df['int_shipping']

def convert_product(row):
    values = row[['max_resolution', 'displayport', 'hdmi', 'directx','model']].to_dict()
    json_str = json.dumps(values)
    return json_str


df['detail_product'] = df.apply(convert_product,axis=1)

#Write to SQL
df.to_sql('final_data', con=engine, if_exists='replace', index=False)
