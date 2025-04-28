# 필요한 라이브러리 임포트
import os
import numpy as np
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm
from datetime import datetime

# 1. Heatmap 그려서 저장하는 함수 정의
def draw_and_save_heatmap(user_id, user_name, comments, save_dir='./heatmaps'):
    """
    주어진 계정(user_id, user_name)의 댓글 리스트(comments)를 바탕으로
    활동 패턴 heatmap을 그려서 save_dir 폴더에 저장하는 함수입니다.
    """

    # 1-1. 시간대별 댓글 수 행렬 초기화 (24시간 x 7일)
    activity_matrix = np.zeros((24, 7), dtype=int)

    # 1-2. 댓글 작성 시간대 분석
    for comment in comments:
        dt = datetime.strptime(comment['created_at'], '%Y-%m-%d %H:%M')
        weekday = dt.weekday()  # 0: 월요일, 6: 일요일
        hour = dt.hour
        activity_matrix[hour, weekday] += 1

    # 1-3. 저장 폴더 생성
    os.makedirs(save_dir, exist_ok=True)

    # 1-4. 그래프 그리기
    plt.figure(figsize=(6, 8))
    plt.rcParams['font.family'] = 'AppleGothic'  # Windows면 'Malgun Gothic'으로 변경
    plt.rcParams['axes.unicode_minus'] = False

    plt.imshow(activity_matrix, cmap='YlOrRd', aspect='auto')
    plt.colorbar(label='활동 횟수')

    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    plt.xticks(range(7), weekdays)

    hours = [f'{i:02d}' for i in range(24)]
    plt.yticks(range(24), hours)

    plt.title(f'User #{user_id}({user_name}) 활동 패턴')
    plt.tight_layout()

    # 1-5. 파일로 저장
    filename = f'{save_dir}/{user_id}({user_name}).png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f'[+] 저장 완료: {filename}')


# 2. 메인 코드 시작
def main():
    # 2-1. 댓글 데이터 수집
    total_comments = []
    num_posts = 100
    print("[+] 댓글 수집 시작...")
    for post_id in tqdm(range(1, num_posts + 1)):
        url = f'http://board.nyan101.com/comments/{post_id}'
        response = requests.get(url)
        comments = response.json()
        total_comments.extend(comments)
    print(f'[+] 총 댓글 수: {len(total_comments)}개 수집 완료')

    # 2-2. 계정별 댓글 정리
    user_comments = {}
    for comment in total_comments:
        author_id = comment['author_id']
        if author_id not in user_comments:
            user_comments[author_id] = []
        user_comments[author_id].append(comment)
    print(f'[+] 총 계정 수: {len(user_comments.keys())}명')

    # 2-3. 모든 계정에 대해 heatmap 생성 및 저장
    print("\n[+] 계정별 Heatmap 생성 시작...")
    for user_id, comments in user_comments.items():
        user_name = comments[0]['author_name']
        draw_and_save_heatmap(user_id, user_name, comments)
    
    print("\n✅ 모든 작업 완료! (heatmaps 폴더에 .png 저장됨)")


# 3. 프로그램 시작
if __name__ == "__main__":
    main()
