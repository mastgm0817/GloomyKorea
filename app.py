import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff


# 텍스트 모음
title = "한국의 미래"
text = "(2011년 - 2022년)"
year_text = "연도 선택"
chart_text = "차트 선택"

st.markdown(f"<div style='font-weight:bold; font-size:40px; text-align:center'>{title}</div>", unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center; font-size:24px'>{text}</div>", unsafe_allow_html=True)
st.markdown("---")

years = np.arange(2011,2023)
chart = ['학생','폐교','출생 및 결혼','폐교(파이)']


st.sidebar.markdown(f"<div style='text-align:center; font-weight:bold; font-size:18px'>{year_text}</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
year = st.sidebar.selectbox(
    "",
    years)
st.sidebar.markdown(f"<div style='text-align:center; font-weight:bold; font-size:18px;'>{chart_text}</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
with st.sidebar:
    option = st.radio(
        "",
        chart)


def display_student_data(year):
    students_df = pd.read_csv("학생수.csv", index_col=0)
    area_number = len(students_df['지역'].unique()[1:])
    not_all_area = students_df[students_df['지역'] != '전국']
    sorted_area = not_all_area[['지역','학생(명)']]
    all_area = students_df[students_df['지역'] == '전국']
    sorted_area['전체평균'] = round(all_area['학생(명)'] / area_number).astype(int)
    set_index_area = sorted_area.reset_index()
    set_index_area.set_index('지역', inplace=True)
    data_year = set_index_area[set_index_area['연도'] == year]
    fig = ff.create_table(data_year, height_constant=60)

    # Add graph data
    team = data_year.index
    each_area_count = data_year['학생(명)']
    average_count = data_year['전체평균']
    trace1 = go.Bar(x=team, y=each_area_count, xaxis='x2', yaxis='y2',
                    marker=dict(color='#FF8000'),
                    name='학생(명)')
    trace2 = go.Bar(x=team, y=average_count, xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099FF'),
                    name='평균 학생 (명)')

    # Add trace data to figure
    fig.add_traces([trace1, trace2])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})

    fig.layout.yaxis2.update({'title': '학생수'})
    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t':75, 'l':50})
    fig.layout.update({'title': f'                                                                        {year}년 지역당 전체 학생 수'})
    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'width':800, 'height':800, 'yaxis':dict(dtick=100000)})

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

def display_closed_school_data(year):
    close_school_df = pd.read_csv("학교.csv", index_col=0)
    area_number = len(close_school_df['지역'].unique()[1:])
    not_all_area = close_school_df[close_school_df['지역'] != '전국']
    sorted_area = not_all_area[['지역','당년(개)']]
    all_area = close_school_df[close_school_df['지역'] == '전국']
    sorted_area['전체평균'] = round(all_area['당년(개)'] / area_number).astype(int)
    set_index_area = sorted_area.reset_index()
    set_index_area.set_index('지역', inplace=True)
    data_year = set_index_area[set_index_area['날짜'] == year]

    # 차트 만들기
    fig = ff.create_table(data_year, height_constant=60)

    # Add graph data
    team = data_year.index
    each_area_count = data_year['당년(개)']
    average_count = data_year['전체평균']
    trace1 = go.Bar(x=team, y=each_area_count, xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099FF'),
                    name='지역별')
    trace2 = go.Bar(x=team, y=average_count, xaxis='x2', yaxis='y2',
                    marker=dict(color='#404040'),

                    name='평균')

    # Add trace data to figure
    fig.add_traces([trace1, trace2])

    # initialize xaxis2 and yaxis2
    fig['layout']['xaxis2'] = {}
    fig['layout']['yaxis2'] = {}

    # Edit layout for subplots
    fig.layout.yaxis.update({'domain': [0, .45]})
    fig.layout.yaxis2.update({'domain': [.6, 1]})

    # The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
    fig.layout.yaxis2.update({'anchor': 'x2'})
    fig.layout.xaxis2.update({'anchor': 'y2'})
    fig.layout.yaxis2.update({'title': '폐교 학교 수'})

    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t':75, 'l':50})

    fig.layout.update({'title': f'                                                                                  {year}년 학교 폐교율'})
    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.update_layout(width=800, height=600)
    fig.update_layout(yaxis=dict(tickmode='linear', dtick=2))

    # Plot!
    st.plotly_chart(fig, use_container_width=True)
    
def draw_pie_year(year):
    close_school_df = pd.read_csv("학교.csv", index_col=0)
    sorted_school_df = close_school_df.rename(columns={'당년(개)': '값'})
    sorted_school_df = sorted_school_df[sorted_school_df['지역'] != '전국']

    sorted_school_df = sorted_school_df[['지역','학교상태','값','누적 총(개)']]
    sorted_school_df.rename_axis("연도", axis='index', inplace=True) # 인덱스의 이름을 바꾸는것

    set_index_area = sorted_school_df.reset_index()
    data_year = set_index_area[set_index_area['연도'] == year]
    data_year.sort_values('값',ascending=False)

    labels =  list(data_year['지역'].unique())
    values = data_year['값']
    values = values.sort_values(ascending=False)
    pull = np.zeros(len(values))
    pull[0] = 0.2
    pull[1] = 0.15

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull, textinfo='label+percent',
                                 insidetextorientation='radial')])
    fig.update_layout(width=800, height=600)

    tab1, tab2 = st.tabs(["일반 색상", "다른 색상"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)

def statistics_year(year):
    marriage_df = pd.read_csv("출생,결혼.csv", index_col=0)
    marriage_df.rename_axis("연도", axis='index', inplace=True)
    marriage_df = marriage_df.reset_index()
    df_month = marriage_df.copy()
    df_month['월'] = df_month['월'].str.replace('월', '').astype(int)
    df_month = df_month.sort_values('월',ascending=True)
    df_month = df_month.set_index('월')


    b_df = df_month[df_month['항목'] == '출생(명)']
    m_df = df_month[df_month['항목'] == '결혼(건)']

    b_df = b_df[['연도','항목','값']]
    m_df = m_df[['연도','항목','값']]


    a = m_df[m_df['연도'] == year]
    a = a.reset_index()
    b = b_df[b_df['연도'] == year]
    b = b.reset_index()

    month = a['월']
    listed_month = [ str(i) + '월' for i in month]
    marriage = a['값']
    birth = b['값']

    fig = go.Figure()
    # Create and style traces

    fig.add_trace(go.Scatter(x=listed_month, y=birth, name = '출생자수',
                            line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=listed_month, y=marriage, name='결혼건수',
                            line = dict(color='firebrick', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title=f'                                                                               {year}년 월별 출생 및 결혼 건수 통계',
                    xaxis_title='월',
                    yaxis_title='건수')
    fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
    fig.update_layout(yaxis=dict(tickmode='linear', dtick=2000))
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)



if option == "학생":
    display_student_data(year)
elif option == "폐교(파이)":
    draw_pie_year(year)
elif option == "출생 및 결혼":
    statistics_year(year)
else:
    display_closed_school_data(year)
