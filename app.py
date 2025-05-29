
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="기말고사 목표 점수 계산기", page_icon="🎯", layout="centered")

col1, col2 = st.columns([1, 5])
with col1:
    logo = Image.open("오현중학교_교표B.png")
    st.image(logo, width=80)
with col2:
    st.markdown("### 오현중학교 2학년\n## 기말고사 목표 점수 계산기")

st.markdown("---")

subject_items = {
    "국어": [("수행평가1", 0.1), ("수행평가2", 0.1), ("중간고사", 0.4)],
    "영어": [("수행평가", 0.2), ("중간고사", 0.4)],
    "수학": [("수행평가", 0.2), ("중간고사", 0.4)],
    "과학": [("수행평가", 0.2), ("중간고사", 0.4)],
    "도덕": [("수행평가", 0.2)],
    "역사": [("수행평가", 0.2), ("중간고사", 0.4)],
    "기술가정": [("수행평가", 0.2), ("중간고사", 0.4)],
    "컴퓨팅과 융합": [("수행평가", 0.2)]
}

grade_cutoffs = {"A": 89.5, "B": 79.5, "C": 69.5, "D": 59.5, "E": 0}

subject = st.selectbox("과목을 선택하세요:", list(subject_items.keys()))

scores = []
st.markdown("#### 세부 평가 점수 입력")
for label, weight in subject_items[subject]:
    score = st.number_input(f"{label} 점수 (0~100)", min_value=0.0, max_value=100.0, step=0.5)
    scores.append((score, weight))

target_grade = st.radio("목표 등급을 선택하세요:", list(grade_cutoffs.keys())[:-1], horizontal=True)

if st.button("🎯 기말고사 목표 점수 계산"):
    current_score = sum(score * weight for score, weight in scores)
    remaining_weight = 1.0 - sum(weight for _, weight in subject_items[subject])

    if remaining_weight <= 0:
        st.error("기말고사 반영 비율이 없습니다. 이미 모든 평가 요소가 입력되어 있습니다.")
    else:
        needed_score = (grade_cutoffs[target_grade] - current_score) / remaining_weight
        needed_score = max(0, min(needed_score, 100))
        st.markdown(f"🎯 필요한 기말 점수는 **{needed_score:.2f}점** 입니다.", unsafe_allow_html=True)

        if st.button("📤 결과 엑셀로 다운로드"):
            data = {
                "과목": subject,
                "목표 등급": target_grade,
                "현재 반영 점수": round(current_score, 2),
                "필요한 기말 점수": round(needed_score, 2)
            }
            df = pd.DataFrame([data])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="결과")
            st.download_button(
                label="📥 엑셀 다운로드",
                data=output.getvalue(),
                file_name=f"{subject}_기말_목표점수.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
