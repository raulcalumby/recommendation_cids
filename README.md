# Projeto de Aprendizado de Máquina

## Descrição
Este é um projeto de aprendizado de máquina que implementa um sistema de recomendação de códigos de diagnóstico médico (CID) com base em categorias de entrada. Ele utiliza um Classificador Random Forest para prever o grupo de códigos CID que são relevantes para a categoria de entrada. O modelo é treinado em um conjunto de dados de códigos de diagnóstico médico e seus grupos correspondentes. Dada uma categoria de diagnóstico médico, o sistema sugere CIDs relevantes que pertencem ao mesmo grupo.

## Dependências
- Python 3.x
- Flask: Um microframework web para Python que permite criar uma API web para o sistema de recomendação.
- scikit-learn: Uma biblioteca de aprendizado de máquina para Python que fornece ferramentas para tarefas de classificação e pré-processamento.
- pandas: Uma poderosa biblioteca de manipulação de dados para Python, usada para ler e processar o conjunto de dados.
- numpy: Uma biblioteca para computação numérica em Python, frequentemente usada em conjunto com o scikit-learn para manipulação de dados.
- fuzzywuzzy: Uma biblioteca para comparação de strings em Python, usada para encontrar correspondências aproximadas para códigos CID.

## Configuração e Execução do Projeto
1. Verifique se você tem o Python 3.x instalado no seu sistema.
2. Instale as dependências necessárias utilizando o gerenciador de pacotes do Python (pip).
3. Clone este repositório para a sua máquina local.
4. Navegue até o diretório do projeto e execute o aplicativo Flask com: 
5. O aplicativo Flask deve estar sendo executado em `http://127.0.0.1:5000/`.
6. Para fazer uma recomendação, envie uma solicitação GET para `http://127.0.0.1:5000/recommend_cids?categoria_input=SUA_CATEGORIA_DE_ENTRADA` usando o Postman ou um navegador da web.

## Exemplo de Resposta JSON
Aqui está um exemplo de resposta do sistema após enviar uma solicitação para recomendação de CIDs:
Busca:
`http://127.0.0.1:5000/recommend_cids?categoria_input=A00` ou
`http://127.0.0.1:5000/recommend_cids?categoria_input=Cólera`
```json
{
 "searched_cid": "A00",
 "recommended_cids": [
     "A01",
     "A02",
     "A03",
     "A04",
     "A05",
     "A06",
     "A07",
     "A08",
     "A09"
 ]
}
```

## Idéias 
Retornar grupo de cids que geralemente acompanha o cid procurado, exemplo:
Pesquisa: Gripe
Retorno, Gripe, Bronquite, Asma...


