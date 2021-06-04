
from operator import itemgetter

import datetime
import plotly.graph_objects as go
import plotly.express as px

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=False)


def main():
    df = pd.read_csv('./country_vaccinations.csv')
    datum = df.groupby('date')['daily_vaccinations'].sum()
    df_vacc_distr = df.groupby(['vaccines', 'date'])['daily_vaccinations'].sum()
    df_nan_distr = pd.read_csv('./country_vaccinations.csv',
                               usecols=['country', 'total_vaccinations', 'daily_vaccinations'])

    # список стран
    countries = sorted(list(set(df['country'].tolist())))
    # список вакцин
    vaccines = set()
    for i in df['vaccines']:
        sp = i.split(', ')
        for vaci in sp:
            vaccines.add(vaci)
    vaccines = list(sorted(vaccines))
    # список дат
    date = set()
    for i in df['date']:
        date.add(i.replace('-', ''))
    date = sorted(list(date))
    vaccinations = {}
    for i in range(len(date)):
        vaccinations[date[i]] = datum[i]

    page = st.sidebar.selectbox("Выберите страницу",
                                ['Основные данные', 'Анализ кол-ва вакцинировавшихся', 'Список доступных вакцин',
                                 'Вакцинация конкретной вакциной по дням', 'Наименее открытые по данным страны'])

    if page == 'Основные данные':
        with st.echo(code_location='below'):
            # подгружаем датасеты
            df = pd.read_csv('./country_vaccinations.csv')
            datum = df.groupby('date')['daily_vaccinations'].sum()
            df_vacc_distr = df.groupby(['vaccines', 'date'])['daily_vaccinations'].sum()
            df_nan_distr = pd.read_csv('./country_vaccinations.csv',
                                       usecols=['country', 'total_vaccinations', 'daily_vaccinations'])

            st.title('Анализ вакцинации от Covid-19')
            st.text('Выберите страницу')
            st.dataframe(df)

            # список стран
            countries = sorted(list(set(df['country'].tolist())))
            # список вакцин
            vaccines = set()
            for i in df['vaccines']:
                sp = i.split(', ')
                for vaci in sp:
                    vaccines.add(vaci)
            vaccines = list(sorted(vaccines))
            # список дат
            date = set()
            for i in df['date']:
                date.add(i.replace('-', ''))
            date = sorted(list(date))
            vaccinations = {}
            for i in range(len(date)):
                vaccinations[date[i]] = datum[i]

    elif page == 'Анализ кол-ва вакцинировавшихся':
        with st.echo(code_location='below'):
            st.title('Анализ кол-ва вакцинировавшихся')
            st.text('Обратите внимание, что перемещаться может как левый, так и правый ползунок')
            st.dataframe(datum)
            a = st.slider('Дата', 5, 15, (0, 115), 5)

            start_date = datetime.datetime.strptime(date[a[0]], '%Y%m%d').strftime("%d. %B %Y")
            end_date = datetime.datetime.strptime(date[a[1] - 1], '%Y%m%d').strftime("%d. %B %Y")

            st.info('Начало: **%s** Конец: **%s**' % (start_date, end_date))
            x = list(dict(sorted(vaccinations.items(), key=itemgetter(1))[a[0]:a[1]:5]).keys())
            y = list(dict(sorted(vaccinations.items(), key=itemgetter(1))[a[0]:a[1]:5]).values())

            fig_daily_vacc = go.Figure(data=[go.Bar(x=x, y=y)])
            fig_daily_vacc.update_layout(title='Рост количества вакцинировавшихся', autosize=False,
                                         width=800, height=800)
            st.plotly_chart(fig_daily_vacc)
            st.write(
                'Мы можем заметить что в декабре рост был линейным.(просто разместите ползунок так,чтобы показывался только месяц декабрь). В январе произошел резкий рост(почти квадратичный). В феврале же кол-во вакцинировшихся осталось постоянным. В марте-апреле кол-во вакцинировшихся снова начало экспоненциально расти')

    elif page == 'Список доступных вакцин':
        with st.echo(code_location='below'):
            st.title('Список доступных вакцин')
            st.text('В последнее время появилолсь множество вакцин, в этой работе я хочу рассмотреть их популярность')
            for i in vaccines:
                st.markdown(i)

    elif page == 'Вакцинация конкретной вакциной по дням':
        with st.echo(code_location='below'):
            st.title('Вакцинация конкретной вакциной по дням')
            aaa = df.groupby(['vaccines', 'date'])['daily_vaccinations'].sum().to_dict()
            vaccines_distr = {}
            for i in vaccines:
                vaccines_distr[i] = {}
                for k in date:
                    vaccines_distr[i][k] = 0
            aaa1 = {}
            for i in aaa:
                temp = i[0].split(', ')
                temp = tuple(temp)
                i1 = (temp, i[1].replace('-', ''))
                aaa1[i1] = aaa[i] / len(i[0].split(', '))
            for i in aaa1:
                for k in i[0]:
                    vaccines_distr[k][i[1]] += aaa1[i]

            vaccines_distr_pie = {}
            for i in vaccines_distr:
                vaccines_distr_pie[i] = vaccines_distr[i][list(vaccines_distr[i].keys())[-1]]

            st.dataframe(df_vacc_distr)

            x1_pie = vaccines
            y1_pie = list(vaccines_distr_pie.values())
            num = len(x1_pie)
            theta = [(i + 1.5) * 360 / num for i in range(num)]
            width = [360 / num for _ in range(num)]
            color_seq = px.colors.qualitative.Pastel
            color_ind = range(0, len(color_seq), len(color_seq) // num)
            colors = [color_seq[i] for i in color_ind]

            a_ticks = [(i + 1) * 360 / num for i in range(num)]

            plotss = [go.Barpolar(r=[r], theta=[t], width=[w], name=n, marker_color=[c])
                      for r, t, w, n, c in zip(y1_pie, theta, width, x1_pie, colors)]

            fig_vacc_distr_pie = go.Figure(plotss)
            fig_vacc_distr_pie.update_layout(polar_angularaxis_tickvals=a_ticks, title='Общая популярность вакцин',
                                             autosize=False, width=800, height=800,
                                             polar=dict(angularaxis=dict(showticklabels=False, ticks='')))

            st.plotly_chart(fig_vacc_distr_pie)

            option_1 = st.selectbox(
                'Выберите вакцину №1',
                vaccines, key='1')
            'Вы выбрали: ', option_1

            option_2 = st.selectbox(
                'Выберите вакцину №2',
                vaccines, key='2')
            'Вы выбрали: ', option_2

            x1_1 = list(vaccines_distr[option_1].keys())[::5]
            y1_1 = list(vaccines_distr[option_1].values())[::5]

            y1_2 = list(vaccines_distr[option_2].values())[::5]

            fig_vacc_distr = go.Figure()
            fig_vacc_distr.add_trace(go.Bar(name=option_1, x=x1_1, y=y1_1))
            fig_vacc_distr.add_trace(go.Bar(name=option_2, x=x1_1, y=y1_2))
            fig_vacc_distr.update_layout(title='Популярность вакцин ' + option_1 + ' и ' + option_2 + ' со временем',
                                         autosize=False,
                                         width=800, height=800)
            st.plotly_chart(fig_vacc_distr)
            st.text(
                'Сейчас самой популярной вакциной является Оксфорд.Затем идет Синовак, который почти в 2 раза менее популярный. Вместе они покрывают более 1/4 рынка. Затем все идет согласно диаграмме о вакцинах')



    else:
        with st.echo(code_location='below'):
            st.title('Наименее открытые по данным страны')
            st.dataframe(df_nan_distr)

            all_nans = 0
            for i in df_nan_distr.isna().sum():
                all_nans += i
            nan_distr = {}
            for i in countries:
                nan_distr[i] = 0
            for i in range(len(df_nan_distr)):
                nan_distr[df_nan_distr.iloc[i, 0]] += df_nan_distr.iloc[i].isna().sum()
            for i in nan_distr:
                nan_distr[i] = nan_distr[i] * 100 / all_nans

            x2 = list(dict(sorted(nan_distr.items(), key=itemgetter(1), reverse=True)[:10]).keys())
            y2 = list(dict(sorted(nan_distr.items(), key=itemgetter(1), reverse=True)[:10]).values())

            help_dict = {"countries": list(range(len(x2))), "perc": y2}
            help_fig = px.scatter(help_dict, x="countries", y="perc", trendline="ols")
            x_trend = help_fig["data"][1]['x']
            y_trend = help_fig["data"][1]['y']

            fig_nan = go.Figure()

            fig_nan.add_trace(go.Bar(x=x2, y=y2, name="Распределение закрытости данных"))
            fig_nan.add_trace(go.Line(x=x2, y=y_trend, name="Линия тренда"))
            # fig_nan.add_trace(go.Scatter(name = 'Линия тренда', x = x2, y = y_pred, mode = 'lines'))
            fig_nan.update_layout(title='Топ 10 стран по закрытости данных, %', autosize=False,
                                  width=800, height=800)
            fig_nan.update_layout(xaxis_title='countries', yaxis_title='%')

            st.plotly_chart(fig_nan)


if __name__ == '__main__':
    main()
