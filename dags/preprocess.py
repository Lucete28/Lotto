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

# if df.shape[0] == recent_round: # 최신회차번호까지는 들어왔는데 예측 row가 없을때
#     # 예측을 위한 row 만들기
#     last_six_nums = df.iloc[-1, -6:].values
#     ap_list = df.iloc[-1, :-6].values.copy()
#     for i in last_six_nums:
#         ap_list[i-1] += 1
#     ap_list = np.concatenate([ap_list, np.full(6, np.nan)])
#     df.loc[df.shape[0]] = ap_list
# elif df.iloc[-1,-1] == np.nan: # 

#     print("good")


# 최신회차까지의 정보 받기
n_list = list(cumulative_list)  # 이전 누적 리스트의 복사본 사용
url = f'http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={recent_round}'
response = requests.get(url)
output = response.json()

num_list = [output.get(f'drwtNo{i}') for i in range(1, 7)]  # 당첨번호들을 받아옴

for i in num_list:
    n_list[i-1] += 1  # 해당하는 인덱스 값에 1 추가

cumulative_list = list(n_list)  # 현재 회차의 누적 리스트를 다음 회차에 사용
n_list.extend(num_list)  # 6개의 당첨번호를 추가
lotto_list.append(n_list)

origin_Data = pd.DataFrame(lotto_list)
# csv 파일로 저장
origin_Data.to_csv('/home/jhy/code/Lotto/dags/lotto.csv', index=False)


# 최솟값 0으로 정제
min_value = origin_Data.iloc[:, :45].min(axis=1)
for i, row in origin_Data.iterrows():
    origin_Data.loc[i, :'44'] -= min_value[i]
origin_Data.to_csv('C:\PlayData\lotto_data\lotto\lotto1.csv', index=False)



