import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind

stud = pd.read_csv('stud_math.xls')

#заменяю пустые в столбцах Fedu и famrel значние на None
stud.Fedu = stud.Fedu.apply(lambda x: None if pd.isnull(x) else None if x == 'nan' else x)
stud.famrel = stud.famrel.apply(lambda x: None if pd.isnull(x) else None if x == 'nan' else x)

#заполняем пустые значения для ранговых показателей (значение = мода столбца)
columns_str = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
               'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
               'nursery', 'higher', 'internet', 'romantic', 'Medu', 'Fedu',
               'traveltime', 'studytime', 'failures', 'studytime, granular', 
               'freetime', 'goout', 'health', 'famrel']

for i in columns_str:
    stud[i].fillna(stud[i].value_counts().index[0], inplace = True)

#пустые значения столбца "score" заполняем медианным значением столбца
stud["score"].fillna(stud["score"].median(), inplace = True)

#удаляем выбросы в стоибцах Fedu и famrel
stud = stud.loc[stud.Fedu.between(0,5)]
stud = stud.loc[stud.famrel.between(1,5)]

#выбросы по полю "absences" удаляем по процентилям
IQR = stud.absences.quantile(0.75) - stud.absences.quantile(0.25)
perc25 = stud.absences.quantile(0.25)
perc75 = stud.absences.quantile(0.75)
stud = stud.loc[stud.absences.between(perc25 - 1.5*IQR, perc75 + 1.5*IQR)]

"""
Выводы по качеству данных датасета:
    1. датасет в целом качественный, основная проблема - это пустые значения. Они
       были заполнены модой (для ранговых показателей) и медианой (для колличественных)
    2. выбросов в данных мало. Наибольший объем выбросов был по столбцу "absences".
       Выбросы были удалены по процентилям.
"""

#корреляционный анализ количественных переменных
stud_corr = stud.corr()
print(stud_corr.loc['score'].sort_values(ascending=False))

"""
Выводы:
    1. Наиболее существенная корреляция наблюдается между оценкой и показателем "Medu".
       Образование матери оказывает наибольшее прямое влияние на результат теста.
    2. Дополнительное наблюдение - наличие обратной связи между оценкой и количеством
       внеучебных неудач. Высокое количество неуспехов влечет низкую оценку
    3. Наименьшее влияние на тестирование влияют свободное время и здоровье школьника
"""

#анализ номинативных переменных

#функция рисования boxplot по каждой номинативной переменной. 
#показывает зависимость score и каждого параметра
def get_boxplot(column):
    fig, ax = plt.subplots(figsize = (7, 10))
    sns.boxplot(x=column, y='score', 
                data=stud.loc[stud.loc[:, column].isin(stud.loc[:, column].value_counts().index[:10])],
                ax=ax)
    plt.xticks(rotation=45)
    ax.set_title('Boxplot for ' + column)

#список номинативных параметров
paramtrs_nom = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 
                'Fjob', 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 
                'activities', 'nursery', 'higher', 'internet', 'romantic']

for col in paramtrs_nom:
    get_boxplot(col)

"""
Выводы:
    1. Среди номинативных показателей наибольшее влияние на оценку оказывает желание
       школьника получить высшее образование, а также - работа матери.
    2. Минимальное влияние оказывают размер семьи (famsize), причины выбора школы
       (reason) и опекунство (guardian)
"""

