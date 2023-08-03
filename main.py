from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import re

app = Flask(__name__)

df_categories = pd.read_csv('./data/CID-10-CATEGORIAS.CSV - CID-10-CATEGORIAS.CSV.csv', encoding='utf-8')
df_groups = pd.read_csv('./data/CID-10-GRUPOS.CSV - CID-10-GRUPOS.CSV.csv', encoding='utf-8')

def find_group(category):
    group = df_groups[(df_groups['CATINIC'] <= category) & (df_groups['CATFIM'] >= category)]
    if not group.empty:
        return group['DESCRICAO'].values[0], group['CATFIM'].values[0]
    else:
        return None, None

table_relation = df_categories[['CAT', 'DESCRICAO']].copy()
table_relation['GROUP_DESCRIPTION'], table_relation['CAT_END'] = zip(*table_relation['CAT'].apply(find_group))

label_encoder = LabelEncoder()
table_train = table_relation.copy()
table_train['CAT'] = label_encoder.fit_transform(table_train['CAT'])

X = table_train[['CAT']]
y = table_train['GROUP_DESCRIPTION']

model = RandomForestClassifier()
model.fit(X, y)

name_cat_to_cid = table_relation.set_index('DESCRICAO')['CAT'].to_dict()

def recommend_cids(input_category):
    if isinstance(input_category, str):
        if not is_valid_cid(input_category):
            closest_match, confidence = process.extractOne(input_category, name_cat_to_cid.keys())
            if confidence >= 80:
                input_category = name_cat_to_cid[closest_match]
            else:
                return "Category not found", []

    input_category_encoded = label_encoder.transform([input_category])[0]
    predicted_group = model.predict([[input_category_encoded]])[0]
    recommended_categories = table_train[table_train['GROUP_DESCRIPTION'] == predicted_group]
    searched_cid = input_category_encoded
    recommended_cids = recommended_categories[recommended_categories['CAT'] != searched_cid]['CAT'].values
    searched_cid_original = label_encoder.inverse_transform([searched_cid])[0]
    recommended_cids_original = label_encoder.inverse_transform(recommended_cids)

    return searched_cid_original, recommended_cids_original

def is_valid_cid(code):
    pattern = r'^[A-Z]\d{2}$'
    return re.match(pattern, code) is not None

@app.route('/')
def index():
    return 'Hello, Flask!'

@app.route('/recommend_cids')
def recommend_cids_route():
    input_category = request.args.get('input_category')
    if input_category is None:
        return jsonify({"error": "input_category parameter is missing."}), 400

    searched_cid, recommended_cids = recommend_cids(input_category)
    response = {
        "searched_cid": searched_cid,
        "recommended_cids": list(recommended_cids)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
