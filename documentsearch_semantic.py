from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
#import openai
#from openai import util
from openai import AzureOpenAI
# インデックス名の指定
index_name = "index-semantic"
# Cognitive SearchのエンドポイントとAPIキーを指定
endpoint = "AZURE_OPEN_AI_SEARCH_ENDPOINT"
key = "AZURE_OPEN_AI_SEARCH_KEY"
model_name = "test-model-text-embedding-ada-002"

# 検索ワードの指定
#search_word = "4年目の年収はどれくらいになりますか"
search_word = '私は在籍2年目で月額単価は80万円です。5年目の年収はどれくらい上がる可能性がありますか？'

# 検索クライアントの作成　　
search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))
client = AzureOpenAI(
    api_key="AZURE_OPEN_AI_SEARCH_API_KEY",
    azure_endpoint="AZURE_ENDPOINT",
    api_version="2023-05-15"
    )
search_word_embedding = client.embeddings.create(input=search_word,model=model_name).data[0].embedding

# 検索クエリの実行
results = search_client.search(
    search_text=search_word,
    vectors=[Vector(
        value=search_word_embedding, 
        k=3, 
        fields='description_vector'
    )],
    select=["description"],
    top=3
)

#検索結果の表示
for result in results:
    #print(result)
    #print("title: " + result["title"])
    print("description: " + result["description"])

    # 根拠となる文書の表示
    captions = result['@search.captions']
    if captions:
        caption = captions[0]
        print(f"Caption: {caption.text}\n")