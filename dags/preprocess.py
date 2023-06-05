import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
# import numpy as np

def get_recent_lotto_round():
    url = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    recent_round_str = soup.select_one('.win_result strong').text
    recent_round = re.search(r'\d+', recent_round_str).group()
    return int(recent_round)

recent_round = get_recent_lotto_round()

lotto_list = []
cumulative_list = [0] * 45  # 초기 누적 리스트 생성

df = pd.read_csv('/home/jhy/code/Lotto/dags/lotto.csv')


if df.shape[0] == recent_round:
    url = f'http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={recent_round}'
    response = requests.get(url)
    output = response.json()

    num_list = [output.get(f'drwtNo{i}') for i in range(1, 7)]  # 당첨번호들을 받아옴
    df.iloc[-1, -6:] = num_list
    for i in num_list:
        n_list = df.iloc[-1,:45].copy()
        n_list[i-1] += 1  # 해당하는 인덱스 값에 1 추가
        df.loc[recent_round] = n_list

df.to_csv('/home/jhy/code/Lotto/dags/lotto.csv',index=False)



# 최솟값 0으로 정제
min_value = df.iloc[:, :45].min(axis=1)
for i, row in df.iterrows():
    df.loc[i, :'44'] -= min_value[i]
df.to_csv('C:\PlayData\lotto_data\lotto\lotto1.csv', index=False)



