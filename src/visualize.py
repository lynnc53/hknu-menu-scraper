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
    plt.show()
    plt.savefig('data/visualization/top10_menus_.png')

# 2. 식단구분별 식수 인원 비교: 강수량(유-최대/ 최소, 무-최대/최소), 시험기간(유-최대/ 최소, 무-최대/최소)
# two separate bar charts for 강수량 and 시험기간