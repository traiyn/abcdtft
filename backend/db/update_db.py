import logging
import pandas as pd
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Champion
from sqlalchemy.exc import IntegrityError

logging.basicConfig(filename='abcdtft.log', level=logging.ERROR, format='%(asctime)s %(message)s')

current_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = target_dir = os.path.sep.join(current_dir.split(os.path.sep)[:-2])

champion_filepath = os.path.join(target_dir, 'data', 'champion.json')

df = pd.read_json(champion_filepath)
champ_info_rows = []
for champ in df['data']:
    champ_info = {}
    champ_info['id'] = champ['id']
    champ_info['key'] = champ['key']
    champ_info['name'] = champ['name']
    champ_info_rows.append(champ_info)

champs_df = pd.DataFrame(champ_info_rows)
# champs_df.set_index('key', inplace=True)

engine = create_engine('sqlite:///abcdtft.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
champ_count = 0
for champ in champs_df.iterrows():
    new_champion = Champion(id=champ[1]['key'], name=champ[1]['name'])
    session.add(new_champion)
    champ_count += 1
try:
    session.commit()
    logging.info(f'Inserted {champ_count} new champions.')
except IntegrityError as e:
    session.rollback()
    logging.error(f'Integrity error: {e}')

# result = session.query(Champion).all()