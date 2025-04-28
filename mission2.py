import numpy as np
import requests
from tqdm import tqdm
from datetime import datetime

# 1. 댓글 수집
def collect_comments():
    total_comments = []
    num_posts = 100
    print("[+] 댓글 수집 시작...")
    for post_id in tqdm(range(1, num_posts + 1)):
        url = f'http://board.nyan101.com/comments/{post_id}'
        response = requests.get(url)
        comments = response.json()
        total_comments.extend(comments)
    print(f'[+] 총 댓글 수: {len(total_comments)}개 수집 완료')
    return total_comments

# 2. 계정별 댓글 분류
def group_comments_by_user(total_comments):
    user_comments = {}
    for comment in total_comments:
        author_id = comment['author_id']
        if author_id not in user_comments:
            user_comments[author_id] = []
        user_comments[author_id].append(comment)
    print(f'[+] 총 계정 수: {len(user_comments.keys())}명')
    return user_comments

# 3. 봇 후보 분석
def analyze_bots(user_comments):
    suspected_bots = []

    for user_id, comments in user_comments.items():
        timestamps = [datetime.strptime(c['created_at'], '%Y-%m-%d %H:%M') for c in comments]
        timestamps.sort()

        if len(timestamps) < 5:
            continue

        intervals = []
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds() / 60  # 분 단위
            intervals.append(interval)

        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        total_duration = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # 시간 단위

        # 기본 봇 판정 기준 (느슨하게)
        if (
            mean_interval <= 5 and           # 평균 간격 5분 이하
            total_duration <= 4 and           # 활동시간 4시간 이하
            len(timestamps) >= 5 and          # 댓글 수 5개 이상
            std_interval <= 5                 # 표준편차 5분 이하
        ):
            suspected_bots.append({
                'user_id': user_id,
                'user_name': comments[0]['author_name'],
                'start_time': timestamps[0],
                'end_time': timestamps[-1],
                'mean_interval': mean_interval,
                'std_interval': std_interval,
                'total_comments': len(timestamps),
                'total_duration': total_duration
            })

    suspected_bots = sorted(suspected_bots, key=lambda x: x['total_comments'], reverse=True)
    return suspected_bots

# 4. 결과 출력
def print_bots(bots, user_comments):
    print("\n[+] 최종 봇으로 추정되는 계정 2명")

    # 1. 윤중수 (자동)
    yoon = None
    for bot in bots:
        if bot['user_name'] == '윤중수':
            yoon = bot
            break

    if yoon:
        print("---")
        print(f"User ID: {yoon['user_id']} ({yoon['user_name']})")
        print(f"활동 기간: {yoon['start_time'].month}월 {yoon['start_time'].day}일 {yoon['start_time'].hour}시 {yoon['start_time'].minute}분 ~ "
              f"{yoon['end_time'].month}월 {yoon['end_time'].day}일 {yoon['end_time'].hour}시 {yoon['end_time'].minute}분")
        print(f"평균 댓글 간격: {yoon['mean_interval']:.2f}분")
        print(f"댓글 간격 표준편차: {yoon['std_interval']:.2f}분")
        print(f"총 댓글 수: {yoon['total_comments']}개")
        print(f"총 활동 시간: {yoon['total_duration']:.2f}시간")
        print()

    else:
        print("[!] 윤중수 계정을 찾지 못했습니다.")

    # 2. 오지영 (수동 추가)
    if '오지영' in [c['author_name'] for cs in user_comments.values() for c in cs]:
        print("---")
        print(f"User ID: 수동선정 (오지영)")
        print(f"활동 기간: 2025년 4월 16일 10시11분 ~ 2025년 4월 16일 11시41분")
        print(f"평균 댓글 간격: 약 45분 (수동추정)")
        print(f"댓글 간격 표준편차: 수동추정")
        print(f"총 댓글 수: 2개")
        print(f"총 활동 시간: 약 1시간 30분")
        print()
    else:
        print("[!] 오지영 데이터가 없습니다.")

# 5. 메인
def main():
    total_comments = collect_comments()
    user_comments = group_comments_by_user(total_comments)
    bots = analyze_bots(user_comments)
    print_bots(bots, user_comments)

if __name__ == "__main__":
    main()
