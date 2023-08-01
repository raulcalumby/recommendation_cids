from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

app = Flask(__name__)

df_categorias = pd.read_csv('./CID-10-CATEGORIAS.CSV - CID-10-CATEGORIAS.CSV.csv', encoding='utf-8')
df_grupos = pd.read_csv('./CID-10-GRUPOS.CSV - CID-10-GRUPOS.CSV.csv', encoding='utf-8')

def encontrar_grupo(categoria):
    grupo = df_grupos[(df_grupos['CATINIC'] <= categoria) & (df_grupos['CATFIM'] >= categoria)]
    if not grupo.empty:
        return grupo['DESCRICAO'].values[0], grupo['CATFIM'].values[0]
    else:
        return None, None

tabela_relacao = df_categorias[['CAT', 'DESCRICAO']].copy()
tabela_relacao['DESCRICAO_GRUPO'], tabela_relacao['CAT_FIM'] = zip(*tabela_relacao['CAT'].apply(encontrar_grupo))


label_encoder = LabelEncoder()
tabela_train = tabela_relacao.copy()
tabela_train['CAT'] = label_encoder.fit_transform(tabela_train['CAT'])


X = tabela_train[['CAT']]  
y = tabela_train['DESCRICAO_GRUPO'] 


model = RandomForestClassifier()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model.fit(X_train, y_train)

def recomendar_cids(categoria_input):

    categoria_input_encoded = label_encoder.transform([categoria_input])[0]
   

    grupo_predito = model.predict([[categoria_input_encoded]])[0]
    

    categorias_recomendadas = tabela_train[tabela_train['DESCRICAO_GRUPO'] == grupo_predito]
    

    cid_procurado = categorias_recomendadas['CAT'].values[0]
    
    
    cids_recomendados = categorias_recomendadas[categorias_recomendadas['CAT'] != cid_procurado]['CAT'].values
    

    cid_procurado_original = label_encoder.inverse_transform([cid_procurado])[0]
    cids_recomendados_originais = label_encoder.inverse_transform(cids_recomendados)
    
    return cid_procurado_original, cids_recomendados_originais


@app.route('/')
def index():
	return 'Hello, Flask!'

@app.route('/recommend_cids')
def recommend_cids_route():
    categoria_input = request.args.get('categoria_input')
    if categoria_input is None:
        return jsonify({"error": "categoria_input parameter is missing."}), 400

    cid_procurado, cids_recomendados = recomendar_cids(categoria_input)
    response = {
        "cid_procurado": cid_procurado,
        "cids_recomendados": list(cids_recomendados)
    }
    return jsonify(response)

if __name__ == '__main__':
	app.run(debug=True)