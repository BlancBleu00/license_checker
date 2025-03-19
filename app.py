import streamlit as st
import pandas as pd
import json  # JSON 파일 로드
import datetime  # 날짜 처리를 위해 추가
from fuzzywuzzy import process  # 유사한 자격증 찾기
import time  # 애니메이션 효과 추가

# ✅ JSON 파일 불러오기
with open("certifications.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    national_licenses = data["국가기술자격"]  # JSON 키에 맞게 불러오기

# ✅ 국가기술자격 목록 출력 (디버깅용)
print("📌 로드된 국가기술자격 목록 개수:", len(national_licenses))
print("✅ 자격증 목록 샘플:", national_licenses[:10])  # 앞 10개만 출력

# 🌟 Streamlit 스타일 조정 (버튼 & 입력창 UI 개선)
st.markdown("""
    <style>
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 24px;
        }
        .stTextInput>div>div>input {
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ 연령 확인 함수 (생년월 기준)
def is_valid_age(birth_year, birth_month):
    """ 생년월을 기준으로 지원 가능 여부 확인 """
    today = datetime.date.today()  # 오늘 날짜 가져오기
    current_year = today.year
    current_month = today.month

    min_year, min_month = current_year - 40, 3  # 최소 연도(1985년 3월 포함)
    max_year, max_month = current_year - 19, 3  # 최대 연도(2006년 3월 포함)

    # ✅ 연도 기준 판별 (1985년 3월 ~ 2006년 3월까지 가능)
    if birth_year < min_year or birth_year > max_year:
        return False  # 연도가 범위에서 벗어나면 불가

    # ✅ 1985년 출생자는 3월 이상부터 가능
    if birth_year == min_year and birth_month < min_month:
        return False  # 1985년 3월 이전 출생자는 불가

    # ✅ 2006년 출생자는 3월 이하까지만 가능
    if birth_year == max_year and birth_month > max_month:
        return False  # 2006년 3월 이후 출생자는 불가

    return True  # ✅ 지원 가능

# ✅ 유사한 자격증 찾기 (Fuzzy Matching 활용)
def find_similar_cert(input_cert):
    match, score = process.extractOne(input_cert, national_licenses)
    return match if score >= 70 else None  # 유사도가 70% 이상이면 추천

# ✅ Streamlit UI 구성
st.title("국가기술자격 응시료 지원 여부 판별기")

# 📌 사용자 입력 받기 (출생 연도 + 출생 월 추가)
birth_year = st.number_input("출생 연도 입력 (1985~2006)", min_value=1985, max_value=2006, step=1)
birth_month = st.number_input("출생 월 입력 (1~12)", min_value=1, max_value=12, step=1)
residence = st.radio("현재 대구 거주 여부", ["예", "아니오"])
employment = st.radio("취업 상태 선택", ["미취업", "고용보험 가입 3개월 이하", "주 30시간 이하 근로"])

# 📌 시험명 자동완성 기능 추가 (text_input → selectbox 변경)
exam_name = st.selectbox("응시한 시험명을 선택하세요", options=national_licenses, index=None)

# ✅ 판별 로직 실행 (애니메이션 추가)
if st.button("지원 가능 여부 확인"):
    with st.spinner("검토 중..."):  # 로딩 애니메이션
        time.sleep(1)  # 1초 대기 후 결과 출력

    # ✅ 판별 로직 실행 (생년월 기준)
    if not is_valid_age(birth_year, birth_month):
        st.error("❌ 지원 불가: 연령 기준(1985년 3월 ~ 2006년 3월) 미충족")

    elif residence != "예":
        st.error("❌ 지원 불가: 대구 거주자만 신청 가능")

    elif employment not in ["미취업", "고용보험 가입 3개월 이하", "주 30시간 이하 근로"]:
        st.error("❌ 지원 불가: 취업 상태 조건 미충족")

    elif exam_name:
        st.success(f"✅ '{exam_name}' 자격증은 지원 가능합니다! 🎉")

    else:
        similar_cert = find_similar_cert(exam_name.strip()) if exam_name else None
        if similar_cert:
            st.warning(f"❓ '{exam_name}'은(는) 국가기술자격이 아닙니다. 혹시 '{similar_cert}'를 뜻하셨나요?")
        else:
            st.error(f"❌ 지원 불가: '{exam_name}'은(는) 국가기술자격이 아님")
