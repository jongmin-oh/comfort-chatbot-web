import sqlite3
from datetime import date


def record_visitor():
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect('visitor.db')
    cursor = conn.cursor()

    # visitor 테이블이 없으면 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            daily_count INTEGER,
            total_count INTEGER
        )
    ''')
    conn.commit()

    # 현재 날짜 가져오기
    today = date.today().strftime("%Y-%m-%d")

    # 오늘 방문자 수 조회
    cursor.execute("SELECT daily_count FROM visitor WHERE date=?", (today,))
    result = cursor.fetchone()

    if result:
        daily_count = result[0]
    else:
        daily_count = 0

    # 총 방문자 수 조회
    cursor.execute("SELECT total_count FROM visitor WHERE date IS NULL")
    result = cursor.fetchone()

    if result:
        total_count = result[0]
    else:
        total_count = 0

    # 방문자 수 증가
    daily_count += 1
    total_count += 1

    # 오늘 방문자 수 업데이트
    cursor.execute("INSERT OR REPLACE INTO visitor (date, daily_count) VALUES (?, ?)", (today, daily_count))

    # 총 방문자 수 업데이트
    cursor.execute("INSERT OR REPLACE INTO visitor (date, total_count) VALUES (NULL, ?)", (total_count,))

    conn.commit()

    return daily_count, total_count