import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

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

# 최신회차까지의 정보 받기
for num in range(1, recent_round+1):
    n_list = list(cumulative_list)  # 이전 누적 리스트의 복사본 사용
    url = f'http://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={num}'
    response = requests.get(url)
    output = response.json()

    num_list = [output.get(f'drwtNo{i}') for i in range(1, 7)]  # 당첨번호들을 받아옴

    for i in num_list:
        n_list[i-1] += 1  # 해당하는 인덱스 값에 1 추가

    cumulative_list = list(n_list)  # 현재 회차의 누적 리스트를 다음 회차에 사용
    n_list.extend(num_list)  # 6개의 당첨번호를 추가
    lotto_list.append(n_list)

origin_Data = pd.DataFrame(lotto_list)

# 예측을 위한 row 만들기
last_six_nums = origin_Data.iloc[-1, -6:].values
ap_list = origin_Data.iloc[-1, :-6].values.copy()
for i in last_six_nums:
    ap_list[i-1] += 1
ap_list = np.concatenate([ap_list, np.full(6, np.nan)])
origin_Data.loc[origin_Data.shape[0]] = ap_list


# csv 파일로 저장
origin_Data.to_csv('/home/jhy/code/Lotto/dags/lotto.csv', index=False)