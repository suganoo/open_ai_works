#import openai
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.models import Vector
import anthropic

gpt_model_name = 'test-model-gpt-35-turbo-16k'
embedding_model_name = "test-model-text-embedding-ada-002"

# Cognitive SearchのAPIキー／エンドポイント等を設定する
search_service_endpoint = "AZURE_OPEN_AI_SEARCH_ENDPOINT"
search_service_api_key = "AZURE_OPEN_AI_SEARCH_KEY"
index_name = "index-semantic"
credential = AzureKeyCredential(search_service_api_key)

# ユーザーの質問文を設定する
question = '妻が妊娠しました。会社手続きになにかやることはありますか？'
#question = '私は在籍2年目で月額単価は80万円です。5年目の年収はどれくらい上がる可能性がありますか？'
print(f"question: {question}")

client = AzureOpenAI(
    api_key="AZURE_OPEN_AI_SEARCH_API_KEY",
    azure_endpoint="AZURE_ENDPOINT",
    api_version="2023-05-15"
    )

anthropic_client = anthropic.Anthropic(
    api_key="ANTHROPIC_API_KEY"
)
# 質問文をAzure OpenAIに送信して、ベクトル化する
question_word_embedding = client.embeddings.create(input=question,model=embedding_model_name).data[0].embedding

# Cognitive Searchのクライアントオブジェクトを作成する
search_client = SearchClient(search_service_endpoint, index_name, credential)  

# ハイブリッド検索を行う（テキスト検索とベクトル検索のハイブリッド検索）
results = search_client.search(  
    search_text=question,  
    vectors=[Vector(
        value=question_word_embedding, 
        k=3, 
        fields='description_vector'
    )],
    select=["description"],
    top=5
)

# Cognitive Searchの検索結果を変数に格納します
search_result = ''
for result in results:  
    search_result += result['description']

system_prompt = f'''
あなたは優秀なサポートAIです。ユーザーから提供される情報をベースにあなたが学習している情報を付加して回答してください。
'''

user_prompt = f'''
{ question }\n参考情報：
{ search_result }
'''
#print(f"user_prompt: {user_prompt}")
# ChatCompletion経由でAzure OpenAIにリクエストする
# APIのパラメータとして、システムプロンプトとユーザーのプロンプトを設定する
'''
response = client.chat.completions.create(
  model=gpt_model_name, 
  messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
'''
message = anthropic_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0.0,
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_prompt}
    ]
)

print()
# 結果を画面上で出力する
#print(text)
print(message.content[0].text)