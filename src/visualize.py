import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib as mpl

'''
이 파일은 데이터 시각화 관련 함수들을 포함합니다.
'''
# Set Korean font globally
mpl.rcParams['font.family'] = 'Malgun Gothic'  # Windows
mpl.rcParams['axes.unicode_minus'] = False     # Fix minus sign issue

# import cleaned dataframes 
healthy = pd.read_csv("data/cleaned/hknu_healthy_menus_cleaned.csv")
yummy = pd.read_csv("data/cleaned/hknu_yummy_menus_cleaned.csv")

# 1. 식수량 기준 Top 10개 메뉴 : 표 형식, 메뉴명, (맛난한끼/ 건강한끼)
# y-axis will be 식수량 
# x-axis will be top 10 메뉴명

healthy_top10 = healthy.nlargest(10, '식수량')
yummy_top10 = yummy.nlargest(10, '식수량')
#print("Healthy Top 10 Menus:\n", healthy_top10[['메뉴', '식수량']])

def plot_top10_menus():
    plt.figure(figsize=(12, 6))

    # Plot for Healthy Menus
    plt.subplot(1, 2, 1)
    plt.bar(healthy_top10['메뉴'], healthy_top10['식수량'], color='green')
    plt.title('Top 10 Healthy Menus by 식수량')
    plt.xlabel('메뉴명')
    plt.ylabel('식수량')
    plt.xticks(rotation=45)
    
    # Plot for Yummy Menus
    plt.subplot(1, 2, 2)
    plt.bar(yummy_top10['메뉴'], yummy_top10['식수량'], color='orange')
    plt.title('Top 10 Yummy Menus by 식수량')
    plt.xlabel('메뉴명')
    plt.ylabel('식수량')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('data/visualization/top10_menus_.png')
    plt.show()

# 2. 식단구분별 식수 인원 비교: 강수량(유-최대/ 최소, 무-최대/최소), 시험기간(유-최대/ 최소, 무-최대/최소)
# two separate bar charts for 강수량 and 시험기간

# 식수량 vs. 시험여부 
# graph average 식수량 monday to friday for 시험기간 유 and 무
def plot_exam_vs_student_count():

    healthy['식수량'] = pd.to_numeric(healthy['식수량'], errors='coerce')

    exam_yes = healthy[healthy['시험기간 여부'] == '예']
    exam_no = healthy[healthy['시험기간 여부'] == '아니오']

    exam_yes_avg = exam_yes.groupby('요일')['식수량'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    exam_no_avg = exam_no.groupby('요일')['식수량'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])


    print("시험기간 유 row 수:", len(exam_yes))
    print("시험기간 무 row 수:", len(exam_no))
    print(exam_yes_avg)
    print(exam_no_avg)


    plt.figure(figsize=(10, 6))
    plt.plot(exam_yes_avg.index, exam_yes_avg.values, marker='o', label='시험기간 유', color='blue')
    plt.plot(exam_no_avg.index, exam_no_avg.values, marker='o', label='시험기간 무', color='red')
    plt.title('건강한끼 평균 식수량: 시험기간 유 vs 무')
    plt.xlabel('요일')
    plt.ylabel('평균 식수량')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('data/visualization/exam_vs_student_count_healthy.png')
    plt.show()

    yummy['식수량'] = pd.to_numeric(yummy['식수량'], errors='coerce')

    exam_yes = yummy[yummy['시험기간 여부'] == '예']
    exam_no = yummy[yummy['시험기간 여부'] == '아니오']

    exam_yes_avg = exam_yes.groupby('요일')['식수량'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    exam_no_avg = exam_no.groupby('요일')['식수량'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])


    print("시험기간 유 row 수:", len(exam_yes))
    print("시험기간 무 row 수:", len(exam_no))
    print(exam_yes_avg)
    print(exam_no_avg)


    plt.figure(figsize=(10, 6))
    plt.plot(exam_yes_avg.index, exam_yes_avg.values, marker='o', label='시험기간 유', color='blue')
    plt.plot(exam_no_avg.index, exam_no_avg.values, marker='o', label='시험기간 무', color='red')
    plt.title('맛난한끼 평균 식수량: 시험기간 유 vs 무')
    plt.xlabel('요일')
    plt.ylabel('평균 식수량')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('data/visualization/exam_vs_student_count_yummy.png')
    plt.show()
# 식수량 vs. 강수량