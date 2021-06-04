import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
import seaborn as sns
import squarify
import pycountry
import geopandas
import plotly.graph_objects as go
from PIL import Image
from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator



st.title("Nobelevo4ka")



st.image('1.jpg')
"В этой проге я постараюсь визаулизировать данные по Нобелевской премии 1901-2019. " \
"Данные взяты с Kagle (https://www.kaggle.com/imdevskp/nobel-prize)"
"В датасете содержится информация о литературе/медицине/премии мира/физике/химии и экономике (основана в 1969)"
"Стоит также упомянуть, что в период 1940-1942 Нобелевская премия не вручалась(("




with st.echo(code_location='below'):
    data = pd.read_csv('complete.csv', delimiter=',').sort_values("awardYear").reset_index()
    del data["index"]


with st.echo(code_location='below'):
    data["gender"] = data["gender"].fillna("Organization")
    data_year = pd.DataFrame({"Year": range(1901, 1940), "male": 0, "female": 0, "Organization": 0})
    data_year2 = pd.DataFrame({"Year": range(1943, 2020), "male": 0, "female": 0, "Organization": 0})
    data_year = pd.concat([data_year, data_year2], ignore_index=True)
    for j in ["male", "female", "Organization"]:
        for i in range(1901, 1939):
            data_year.loc[i - 1901][j] = int(data[data["awardYear"] == int(i)]["gender"].to_list().count(j))
        for i in range(1943, 2020):
            data_year.loc[i - 1904][j] = int(data[data["awardYear"] == int(i)]["gender"].to_list().count(j))


with st.echo(code_location='below'):
    number = data_year.sum()[1:4].to_list()
    genders = ["male", "female", "Organization"]
    a, b = plt.subplots()

    ### FROM https://stackoverflow.com/questions/6170246/how-do-i-use-matplotlib-autopct"
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.1f}%  ({v:d})'.format(p=pct, v=val)

        return my_autopct
    ### END FROM https://stackoverflow.com/questions/6170246/how-do-i-use-matplotlib-autopct

    b.pie(number, (0, 0, 0.1), genders, ['#60b3ff', '#ff9999', '#99ff99'], autopct=make_autopct(number),
          shadow=True, startangle=11)
    b.axis('equal')
    plt.tight_layout()
    plt.legend(title='Гендерное равенство?! Ну типа', bbox_to_anchor=(1, 1), loc='upper center')

''''Получился нелепый мужской пакмэн, проглотивший остальных. Действительно, пока что нет никаких новостей,
    с куммулятивным гендерным распределением всё и так был понятно.'''

st.pyplot(plt)

with st.echo(code_location='below'):
    b = ["Chemistry", "Literature", "Physiology or Medicine", "Peace", "Physics", "Economic Sciences"]
    subj = pd.DataFrame({"Category": b, "Total": 0, "Female": 0})
    for j in b:
        data_year[j] = 0
        for i in data_year["Year"]:
            data_year.loc[i - 1901 - 3 * int(i / 1943)][j] = int(
                data[data["awardYear"] == int(i)]["category"].to_list().count(j))
        subj.iloc[b.index(j), 1] = data_year[j].sum()
        subj.iloc[b.index(j), 2] = data[data["category"] == j]["gender"].to_list().count("female")

"Стой!!! Совсем забыл сказать, ты можешь воспользоваться уникальной поисковой системой!  Она бесполезная, но вдруг тебе пригодится..." \
"Код я спрятал, потому что он большой и некрасивый"

cat = st.selectbox('Выберите интересующую вас область:',
                   ["Literature", "Chemistry", "Physiology or Medicine", "Physics", "Economic Sciences"])
year = st.selectbox('Выберите интересующий вас год:', range(1901, 2020))


if year > 1939 and year < 1943:
    "В этом году нобелевскую премию по данному предмету никто не получал. Да и по другим претметам тоже. " \
    "Война всё-так дело серьезное"

else:

    if len(data.loc[data["awardYear"] == year].loc[data["category"] == cat]) == 0:
        "В этом году по Экономике никто не получал премию. Знаете почему? Её тогда ещё не было)) " \
        "Она появилась в 1969."
    elif len(data.loc[data["awardYear"] == year].loc[data["category"] == cat]) == 1:
        "В этом году Нобелевскую премию по " + str(cat) + " была вручена " + \
        data.loc[data["awardYear"] == year].loc[data["category"] == cat]["name"].iloc[0]

        "За что получил? Тут всё очев: " + str(data.loc[data["awardYear"] == year].loc[data["category"] == cat]["motivation"].iloc[0])
        if data.loc[data["awardYear"] == year].loc[data["category"] == cat]["birth_date"].iloc[0] == "":
            st.write("Датафрейм не знает, когда этот человек родился, значит и нам не положено")
        else:
            st.write("Дата рождения " + str(data.loc[data["awardYear"] == year].loc[data["category"] == cat]["name"].iloc[0])
                     + " - " + \
                     data[data["awardYear"] == year].loc[data["category"] == cat]["birth_date"].iloc[0])
        if data.loc[data["awardYear"] == year].loc[data["category"] == cat]["birth_countryNow"].iloc[0] == "":
            st.write("Датафрейм не знает, где она родилась, значит и нам не положено")
        else:
            st.write("Место рождения " + str(data.loc[data["awardYear"] == year].loc[data["category"] == cat]["name"].iloc[0])
                     + " - " + \
                     data.loc[data["awardYear"] == year].loc[data["category"] == cat]["birth_countryNow"].iloc[0])
    else:
        st.write("В "+str(year)+" году нобелевской премией по "+str(cat)+ " было награждено сразу несколько человек!!")

        chel = st.selectbox(
            "Выберите, кто именно вас интересует: ", data[data["awardYear"] == year][data["category"] == cat]["name"].to_list())

        "За что получил? Тут всё очев: " + str(
            data[data["awardYear"] == year][data["category"] == cat][data["name"] == chel]["motivation"].iloc[0])
        if data[data["awardYear"] == year][data["category"] == cat][data["name"] == chel]["birth_date"].iloc[0] == "":
            st.write("Датафрейм не знает, когда этот человек родился, значит и нам не положено")
        else:
            st.write("Дата рождения " + str(data[data["awardYear"] == year][data["category"] == cat][data["name"] == chel]["name"].iloc[0])
                     + " - " + \
                     data[data["awardYear"] == year][data["category"] == cat][data["name"] == chel]["birth_date"].iloc[0])
        if data[data["awardYear"] == year][data["category"] == cat][data["name"] == chel]["birth_countryNow"].iloc[0] == "":
            st.write("Датафрейм не знает, где она родилась, значит и нам не положено")
        else:
            st.write("Место рождения " + str(data[data["awardYear"] == year][data["category"] == cat][data["name"] == chel]["name"].iloc[0])
                     + " - " + \
                     data[data["awardYear"] == year][data["category"] == cat]["birth_countryNow"][data["name"] == chel].iloc[0])






with st.echo(code_location='below'):
    sns.set_theme(style="whitegrid")
    f, ax = plt.subplots(figsize=(4, 4))
    subjects = subj.sort_values("Total", ascending=False)
    sns.barplot(x="Total", y="Category", data=subjects, label="Total", color="#60b3ff")
    sns.set_color_codes("muted")
    sns.barplot(x="Female", y="Category", data=subjects, label="Female", color="#ff9999")
    ax.legend(ncol=1, loc="lower right", frameon=True)
    ax.set(xlim=(0, 250), ylabel="", xlabel="Number of prizes")
    plt.title("Female distribution per categories")

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(sns.despine(left=True, bottom=True))
"Как мы видим, процентные соотношения женщин в каждой из категорий очень разнятся. Наибольшую долю они составляют " \
    "в премии Мира и премии по литературе, откуда можно сделать вывод о том, что женщины лучше преуспевают в гуманитарных науках (литература)" \
    "и в социальной активности/иницитивности (премия Мира), нежели в естественных науках ('преуспевают' в данном контексте относится именно" \
    "к Нобелевской премии)"

"Хмммммм. А вы заметили, что во всех категориях количество врученных премий значительно превышает временной промежуток, на протяжении " \
"которого эти премии присуждались (раз в год)??? Омагадддд, получается, одну премию могут получать сразу несколько человек!!!"

with st.echo(code_location='below'):
    y = data[["awardYear", "category"]].copy()
    y["1"] = 1
    y = y.groupby(["awardYear", "category"]).sum("1")
    x = data_year[["Year", "Chemistry", "Literature", "Physiology or Medicine", "Peace",
                   "Physics", "Economic Sciences"]].pivot_table(["Chemistry", "Literature",
                                                                 "Physiology or Medicine", "Peace", "Physics",
                                                                 "Economic Sciences"], "Year")
    x = pd.pivot_table(x, values=["Chemistry", "Literature", "Physiology or Medicine", "Peace",
                                  "Physics", "Economic Sciences"], columns="Year")
    sns.set_theme()
    f, ax = plt.subplots(figsize=(10, 3))
    sns.heatmap(x, annot=False, fmt="d", linewidths=0.05, ax=ax)
"""Цветовая палитра показывает, сколько человек в конкретный год взяли Нобеля в конкретной категории. По литературе, 
например, почти во все года был награждён один человек, что достаточно логично. Действительно интересный момент, 
который мы видим - в естественных науках с момента появления премии количество дуэтов/трио постепенно росло  и в 
последние десятителия стало модно брать нобеля не одному, а со своими корешами."""

st.pyplot()

with st.echo(code_location='below'):
    quant = subj[["Category", "Total"]]
    colors = [plt.cm.Spectral(i / float(len(quant["Category"]))) for i in range(len(quant["Category"]))]
    plt.figure(figsize=(15, 8), dpi=80)
    squarify.plot(sizes=quant["Total"], label=quant["Category"], color=colors, alpha=0.8, value=quant["Total"])
    plt.title('Treemap of the number of the Nobel prizes per category')
    plt.axis('off')
st.pyplot()

with st.echo(code_location='below'):
    x = data_year[["Chemistry", "Literature", "Physiology or Medicine", "Peace", "Physics", "Economic Sciences"]].copy()
    x.index = data_year["Year"]
    x.plot.area(color=colors)
st.pyplot()
"А вот тут можно сломать мозг, но всё на самом деле проще. По оси Y отложено количество человек, которые взяли нобеля " \
"в каждый год. Верхняя огибающая - тотал, а если мы рассмотрим закрашенные зоны, то поймём, разбиение на предметы внутри " \
"этого тотала. В отличии от прошлого графика, этот ещё выресовываает общую тенденцию в виде роста количества премий с теч времени"




with st.echo(code_location='below'):
    strany = data_year[["Year", "male"]].copy()
    data["birth_countryNow"] = data["birth_countryNow"].fillna(data["org_founded_countryNow"])
    for i in set(data["birth_countryNow"].to_list()):
        strany[i] = 0
    strany = strany.drop(strany.columns[1], axis=1)
    for j in strany.columns.to_list()[1:-1]:
        for i in data_year["Year"]:
            strany.loc[i - 1901 - 3 * int(i / 1943)][j] = int(
                data[data["awardYear"] == int(i)]["birth_countryNow"].to_list().count(j))

    po_strane = pd.DataFrame(strany[strany.columns[1:]].sum().sort_values(ascending=False))

    po_strane = po_strane.iloc[0:25, :]
    plt.figure(figsize=(9, 9))
    ax = plt.subplot(111, polar=True)
    plt.axis('off')
    lowerLimit = 30
    labelPadding = 4
    max = int(po_strane.max())

    # Idea taken FROM https://www.python-graph-gallery.com/circular-barplot-basic
    slope = (max - lowerLimit) / max
    heights = slope * po_strane.iloc[:, 0] + lowerLimit
    width = 2 * np.pi / len(po_strane.index)
    indexes = list(range(1, len(po_strane.index) + 1))
    angles = [element * width for element in indexes]
    bars = ax.bar(angles, height=heights, width=width, bottom=lowerLimit, linewidth=2, edgecolor="white", color=colors)
    for bar, angle, height, label in zip(bars, angles, heights, po_strane.index.to_list()):
        rotation = np.rad2deg(angle)
        alignment = ""
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "right"
            rotation = rotation + 180
        else:
            alignment = "left"
        ax.text(x=angle, y=lowerLimit + bar.get_height() + labelPadding, s=str(label) + " " +
                                                                           str(int(
                                                                               po_strane[po_strane.index == label].iloc[
                                                                               :, 0])), ha=alignment, va='center',
                rotation=rotation, rotation_mode="anchor")
    # END FROM https://www.python-graph-gallery.com/circular-barplot-basic
"тут и так всё понятно"
"Btw, я бы на вашем месте не проверял числа, потому что они не сойдутся, во всём виноват датафрейм((( Я честно пытался ручками сделать его лучше, но он всё ещё дефектный парень"
st.pyplot()



with st.echo(code_location='below'):
    country = pd.DataFrame(strany[strany.columns[2:]].sum())
    country = country.reset_index(level=0, drop=False)

    # FROM https://melaniesoek0120.medium.com/data-visualization-how-to-plot-a-map-with-geopandas-in-python-73b10dcd4b4b
    # Аббревиатура страны по названию
    def alpha3code(column):
        CODE = []
        for country in column:
            try:
                code = pycountry.countries.get(name=country).alpha_3
                # .alpha_3 means 3-letter country code
                # .alpha_2 means 2-letter country code
                CODE.append(code)
            except:
                CODE.append('None')
        return CODE

    # END FROM https://melaniesoek0120.medium.com/data-visualization-how-to-plot-a-map-with-geopandas-in-python-73b10dcd4b4b

    # Плохой датасет, некоторое пришлось прописывать ручками
    country['CODE'] = alpha3code(country["index"])
    country.loc[country['index'] == "Czech Republic", 'CODE'] = "CZE"
    country.loc[country['index'] == "United Kingdom", 0] = 105
    country.loc[country['index'] == "Vietnam", 'CODE'] = "VNM"
    country.loc[country['index'] == "Iran", 'CODE'] = "IRN"
    country.loc[country['index'] == "Venezuela", 'CODE'] = "VEN"
    country.loc[country['index'] == "South Korea", 'CODE'] = "KOR"
    country.loc[country['index'] == "Russia", 'CODE'] = "RUS"
    country.loc[country['index'] == "the Netherlands", 'CODE'] = "NLD"
    country.loc[country['index'] == "USA", 'CODE'] = "USA"

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    country = country.drop(country[country["CODE"] == "None"].index)
    ppp = world.merge(country[["CODE", 0]], left_on='iso_a3', right_on='CODE')

    # Using the example (close to documentation) from https://medium.com/using-specialist-business-databases/creating-a-choropleth-map-using-geopandas-and-financial-data-c76419258746
    plt.figure(figsize=(9, 9))
    ax = ppp.dropna().plot(column=0, cmap="OrRd", figsize=(20, 20), scheme='quantiles', k=5, legend=True)
    ax.set_axis_off()
    ax.get_legend().set_bbox_to_anchor((.12, .12))
    ax.get_figure()

"Карта номер рас:"
st.pyplot()



with st.echo(code_location='below'):
    # idea from https://plotly.com/python/choropleth-maps/
    fig = go.Figure(data=go.Choropleth(locations = country['CODE'],z = country[0],text = country['index'],colorscale = "spectral",
        autocolorscale=False,reversescale=False,
        marker_line_color='darkgray',marker_line_width=0.5,colorbar_title = 'No.'))

    fig.update_layout(
        title_text='Nobel prizes per country',geo=dict(showframe=False,showcoastlines=False,
            projection_type='equirectangular'),annotations = [dict(x=0.55, y=0.1, xref='paper',yref='paper', text="Можно туда сюда поводить потыкать",showarrow = False)])
"Карта номер два:"
st.write(fig)


with st.echo(code_location='below'):
    s = st.selectbox("Chose your fighter:", b)
    text = ""
    for i in data[data["category"]==s]["motivation"]:
        text+= " "+i
    mask = np.array(Image.open("Literature.png"))
    #FROM https://towardsdatascience.com/create-word-cloud-into-any-shape-you-want-using-python-d0b88834bc32
    mask_colors = ImageColorGenerator(mask)
    wc = WordCloud(stopwords=STOPWORDS, mask=mask, background_color="white", max_words=2000, max_font_size=256,
    random_state=42, width=mask.shape[1],height=mask.shape[0],color_func=mask_colors)
    #END FROM https://towardsdatascience.com/create-word-cloud-into-any-shape-you-want-using-python-d0b88834bc32
    wc.generate(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')
"Интересно, а о чём же вообще все эти научные работы? Наверняка у них очень заумные названия..." \
"Но должны же слова иногда повторяться?"
st.pyplot()

yes  = st.checkbox("Хочу посмотреть сразу на все предметы")
if yes == True:
    with st.echo(code_location='below'):
        for j in b:
            text = ""
            for i in data[data["category"] == j]["motivation"]:
                text += " " + i
            wordcloud = WordCloud(width=400, height=400, margin=0, background_color="white").generate(text)
            plt.subplot(2, 3, b.index(j) + 1)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title(str(j))
            plt.margins(x=0, y=0)
    st.pyplot()




with st.echo(code_location='below'):
    univ = data_year[["Year", "male"]].copy()

    for i in set(data["category"].to_list()):
        univ[i] = 0

    for j in ["Literature","Chemistry", "Physiology or Medicine", "Peace", "Physics", "Economic Sciences"]:
        for i in data_year["Year"]:
            if i == 1901:
                univ.loc[i - 1901 - 3 * int(i / 1943)][j] = int(
                    data[data["awardYear"] == int(i)]["category"].to_list().count(j))
            else:
                univ.loc[i - 1901 - 3 * int(i / 1943)][j] = int(
                    data[data["awardYear"] == int(i)]["category"].to_list().count(j))+int(univ.loc[i - 1902 - 3 * int(i / 1943)][j])
    univ = univ.set_index("Year").drop(columns="male")
    univ = univ.sort_values(univ.iloc[115].name,axis=1)
    # USED several comments from https://discuss.streamlit.io/t/how-to-animate-a-line-chart/164/2

    #the_plot = st.pyplot(plt)
    #def animate(i, x, y, colors):
        #ax.barh(x, width=y, color=colors)
        #ax.set_title(i, )
        #the_plot.pyplot(plt)
    #fig, ax = plt.subplots()
    #for i in range(110):
        #width = univ.iloc[i].values
        #animate(i, univ.iloc[i].index, width, colors)
        #time.sleep(0.1)


"Код можно посмотреть в файле, ровно то что закомменчено, но из-за функции код не хочет работать внутри st.echo. Вообще " \
    "для таких штук есть крутой пакет - celluloid, там есть camera которая позволяет делать красоту, но стрмлит ее поддерживает((("

"Придётся подождать... Это не конец, загрузится - появится продолжение"

the_plot = st.pyplot(plt)
def animate(i, x, y, colors):
    ax.barh(x, width=y, color=colors)
    ax.set_title(1901+i+ 3 * int(i / 39,)-3 * int(i / 78,))
    the_plot.pyplot(plt)

fig, ax = plt.subplots()
for i in range(0,116):
    width = univ.iloc[i].values
    animate(i, univ.iloc[i].index, width, colors)
    time.sleep(0.001)



aue  = st.checkbox("Пропустил всю анимацию? Ну ладноооо, специально для тебя могу повторить, поставь галочку и наберись терпения")

if aue == "Yes":
    fig, ax = plt.subplots()
    for i in range(110):
        width = univ.iloc[i].values
        animate(i, univ.iloc[i].index, width, colors)
        time.sleep(0.001)
