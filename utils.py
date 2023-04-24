import pdfplumber as pp
import mindsdb_sdk as mdb
import pandas as pd
import docx2txt
import os


MDB_EMAIL=os.getenv('mdb')
MDB_PWD=os.getenv('mdb-pass')
MODEL_NAME=os.getenv('mdb-model')


correct_schema = {
  "hex": "#000000",
  "rgb": [0, 0, 0],
  "hsl": [0, 0, 0]
}

def verifyResponse(response):
    result = True
    if response is None:
        return False
    for key, value in correct_schema.items():
        if key not in response:
            result = False
        if type(value) != type(response[key]):
            result = False
    return result

def color_pick(text):
    server=mdb.connect(login=MDB_EMAIL,password=MDB_PWD)
    model=server.get_project('mindsdb')
    query = model.query(f'select * from color_test_3 WHERE colorname = \'{text}\'')
    response = query.fetch()
    return response['color'][0]

# def _from_mindsdb(df: pd.DataFrame):
#     server=mdb.connect(login=MDB_EMAIL,password=MDB_PWD)
#     model=server.get_project('mindsdb').get_model(MODEL_NAME)

#     databases = server.list_databases()

#     database = databases[0] # Database type object
#     query = database.query(f'select * from color_test_3 WHERE colorname = {text}')
#     print(query.fetch())

#     print("got model")
#     entity_df=model.predict(df)
#     print("got prediction", entity_df)
    # json_df = pd.DataFrame(entity_df['json'].tolist())
    # entity_df = pd.concat([entity_df, json_df], axis=1)
    # entity_df = entity_df.drop('json', axis=1)
#     return entity_df 