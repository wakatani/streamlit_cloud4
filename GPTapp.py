#
#
#
from math import exp
import json
from openai import OpenAI
import os
import random
import copy
import streamlit as st

#load_dotenv()

#
# APIキーは環境変数にセットしておく
#
client = OpenAI()

#

st.title("■ Let's study scikit-learn ■")

lang = st.radio(label='Which lang.?',
                 options=('Japanese', 'English'),
                 index=0,
                 horizontal=True,
)
if lang=="Japanese":
  language="日本語"
else:
  language="英語"

#
# 問題作成の元になる文章群
#
explanationList=[
    "scikit-learnでLasso回帰を使う場合は、Lasso関数を用います。",
    "scikit-learnでRidge回帰を使う場合は、Ridge関数を用います。",
    "scikit-learnで線形回帰を使う場合は、LinearRegression関数を用います。"
]

probtypeList=[
    "関数の名前を問うようにしろ。",
    "オプションの値の大小について問うようにしろ。",
    "オプションについて問うようにしろ。",
    "Numpyと組み合せるようにしろ。",
    "pandasと組み合せるようにしろ。"
]


quiz_response="NONE"
b=["","","",""]
ans=""
expl=""

if 'counter' not in st.session_state:
  st.session_state['counter'] = 0

if st.button('問題 (Quiz)'):
#
# 文章群から文章をランダムに選ぶ
#
  st.session_state['counter'] += 1

  explanation=explanationList[int(random.random()*len(explanationList))]
  probtype   =probtypeList[int(random.random()*len(probtypeList))]

  response1 = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    temperature=0.8,
    messages=[
      {"role": "system",\
               "content":"あなたは機械学習の専門家です。知っている知識を駆使して初心者向けの機械学習の学習のための問題を作ります。"},
      {"role": "user",\
               "content": "「{0}」の文章に関して、Pythonの4択問題を考えます。問題にはPythonコードの一部を穴埋めする問題とします。問題のPythonコードと問題文と、4個の選択肢の文言とその答の番号を示せ。選択肢の文言は選択肢の番号は不要である。また、Pythonコードは改行をつけること。また、Pythonコードではデータの初期化をすること。「{1}」を守ること。正解の選択肢以外の選択肢の文言は間違っているようにすること。{2}で。".format(explanation,probtype,language)}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "quiz_data",
            "schema": {
                "type": "object",
                "properties": {
                    "問題文": {"type": "string"},
                    "Pythonコード": {"type": "string"},
                    "選択肢１": {"type": "string"},
                    "選択肢２": {"type": "string"},
                    "選択肢３": {"type": "string"},
                    "選択肢４": {"type": "string"},
                    "答え": {"type": "number"},
                },
                "required": ["問題文","Pythonコード","選択肢１", "選択肢２", "選択肢３", "選択肢４","答え"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
  )

  quiz_response = json.loads(response1.choices[0].message.content)
  st.session_state['quiz'] = quiz_response
  st.session_state['expl'] = explanation

  msg=quiz_response
  prob=quiz_response["問題文"]
  code="{0}".format(quiz_response["Pythonコード"])
  b[0]="１：{0}".format(quiz_response["選択肢１"])
  b[1]="２：{0}".format(quiz_response["選択肢２"])
  b[2]="３：{0}".format(quiz_response["選択肢３"])
  b[3]="４：{0}".format(quiz_response["選択肢４"])
  ans ="答えは{0}です。".format(quiz_response["答え"])
  expl="  [ {0} ]".format(explanation)

  counter=st.session_state['counter']
  msg="-----------------------------------------------------{0}".format(counter)
  st.write(msg)
  msg=prob
  st.write(msg)
  msg=code
  st.code(msg)
  msg="次の選択肢から正しいものを選べ (Choose the correct one)"
  st.write(msg)
  for i in range(4):
    st.write(b[i])
  msg="-----------------------------------------------------"
  st.write(msg)

  
if st.button('答え (Answer)'):
  try:
    quiz_response=st.session_state['quiz']
    explanation=st.session_state['expl']
  
    prob=quiz_response["問題文"]
    code="{0}".format(quiz_response["Pythonコード"])
    b[0]="１：{0}".format(quiz_response["選択肢１"])
    b[1]="２：{0}".format(quiz_response["選択肢２"])
    b[2]="３：{0}".format(quiz_response["選択肢３"])
    b[3]="４：{0}".format(quiz_response["選択肢４"])
    ans ="答えは{0}です。(The answer is {0}.)".format(quiz_response["答え"])
    expl="  [ {0} ]".format(explanation)
  
    st.write(ans)
    st.write(expl)
    counter=st.session_state['counter']
    msg="-----------------------------------------------------{0}".format(counter)
    st.write(msg)
    msg=prob
    st.write(msg)
    msg=code
    st.code(msg)
    for i in range(4):
      st.write(b[i])
    msg="-----------------------------------------------------"
    st.write(msg)
    msg="◇◇◇ 次の問題は「問題」を押してください (click Quiz, again.)"
    st.write(msg)

  except:
      st.write('まず「問題」を押してください (click Quiz, first.)')

