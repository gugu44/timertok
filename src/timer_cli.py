import time
import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'routine_history.json')

DEFAULT_TIMERS = [3, 5, 10]


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def show_history(history):
    if not history:
        print('기록이 없습니다.')
        return
    print('\n최근 루틴 기록:')
    for item in history[-5:]:
        ts = item['timestamp']
        dur = item['duration']
        result = '성공' if item['success'] else '포기'
        print(f"- {ts} | {dur}분 | {result}")


def countdown(minutes):
    total_seconds = minutes * 60
    try:
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            print(f"\r남은 시간: {mins:02d}:{secs:02d}", end='')
            time.sleep(1)
            total_seconds -= 1
        print()  # new line after countdown
        return True
    except KeyboardInterrupt:
        print('\n타이머가 중단되었습니다.')
        return False


def main():
    history = load_history()
    show_history(history)

    print('\n추천 타이머 선택:')
    for idx, minute in enumerate(DEFAULT_TIMERS, start=1):
        print(f"{idx}. {minute}분")
    choice = input('번호 선택 (기타 키 입력 시 종료): ')

    if not choice.isdigit() or not (1 <= int(choice) <= len(DEFAULT_TIMERS)):
        print('종료합니다.')
        return

    minutes = DEFAULT_TIMERS[int(choice) - 1]
    print(f"{minutes}분 타이머 시작!")
    success = countdown(minutes)

    if success:
        print('타이머 완료! 코인 +1')
    else:
        print('포기하셨습니다. 다음에 다시 도전해보세요!')

    save = input('기록을 저장할까요? (y/N): ').strip().lower() == 'y'
    if save:
        history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'duration': minutes,
            'success': success
        })
        save_history(history)
        print('기록이 저장되었습니다.')


if __name__ == '__main__':
    main()
