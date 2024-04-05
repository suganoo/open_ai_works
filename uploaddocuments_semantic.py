from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
#import openai
#from openai import util
from openai import AzureOpenAI
import time
import json

# インデックス名の指定
index_name = "index-semantic"
# Cognitive SearchのエンドポイントとAPIキーを指定
endpoint = "AZURE_OPEN_AI_SEARCH_ENDPOINT"
key = "AZURE_OPEN_AI_SEARCH_KEY"
model_name = "test-model-text-embedding-ada-002"

client = AzureOpenAI(
    api_key="AZURE_OPEN_AI_SEARCH_API_KEY",
    azure_endpoint="AZURE_ENDPOINT",
    api_version="2023-05-15"
    )

# アップロードするドキュメントの指定
DOCUMENT = None
with open('docs_rules.json', encoding="utf-8") as f:
    DOCUMENT = json.load(f)

for doc in DOCUMENT:
    # タイトルをベクトル化
    print("vectorizing title ...")
    doc['title_vector'] = client.embeddings.create(input=doc['title'],model=model_name).data[0].embedding
    print("waiting...")
    time.sleep(15)
    # 説明をベクトル化
    print("vectorizing description ...")
    doc['description_vector'] = client.embeddings.create(input=doc['description'],model=model_name).data[0].embedding
    print("waiting...")
    time.sleep(15)

# インデックスの内容を格納
search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))
# ドキュメントのアップロード
print("uploading documents")
result = search_client.upload_documents(documents=DOCUMENT)
# アップロードの結果を表示
print("ドキュメントの登録に成功しました: {}".format(result[0].succeeded))