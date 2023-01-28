import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

# Consts
df_2020 = pd.read_csv("assets/cv_2020.csv", sep=";")
df_2021 = pd.read_csv("assets/cv_2021.csv", sep=";")
df_2022 = pd.read_csv("assets/cv_2022.csv", sep=";")

df = pd.concat([df_2020, df_2021, df_2022], ignore_index=True)
db_by_year = pd.read_csv("assets/data_by_year.csv", sep=";")
css = "assets/styles.css"
main_card_color = "#f0f5fa"
# app start
app = Dash(__name__, external_stylesheets=[css, dbc.themes.MORPH])
server = app.server

# layout
app.layout = html.Div([
    # NavBAr
    dbc.NavbarSimple(
        [
            dcc.DatePickerRange(
                id='data-filtro',
                min_date_allowed=df.dt_notificacao.min(),
                max_date_allowed=df.dt_notificacao.max(),
                initial_visible_month=df.dt_notificacao.min(),
                end_date=df.dt_notificacao.max(),
                start_date=df.dt_notificacao.min(),
                style={"text-color": "midnightblue"}
            )], brand="EstatisticasCovidPE",
        className="sidebar_style"),

    # DIV TELA PRICIPAL
    html.Div([
        # Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Recuperados", className="card-title", style={"padding-top": "2%"}),
                        html.P(df.query("evolucao == 'RECUPERADO'").__len__(), id="card_cured",
                               className="card-text")
                    ])
                ], outline=True, style={"margin": "10px", "text-align": "center"},
                    className="card text-white bg-primary mb-3")
            ], md=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Confirmados", className="card-title", style={"padding-top": "2%"}),
                        html.P(df.__len__(), id="card_confirm", className="card-text")
                    ], style={})
                ], outline=True, style={"margin": "10px", "text-align": "center"},
                    className="card text-white bg-danger mb-3")
            ], md=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Óbitos", className="card-title", style={"padding-top": "2%"}),
                        html.P(df.query("evolucao == 'OBITO'").__len__(), id="card_dead", className="card-text")
                    ], )
                ], outline=True, style={"margin": "10px", "text-align": "center"},
                    className="card text-white bg-dark mb-3")
            ], md=4)

        ], style={"display": "flex"}),

        # Graficos
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5("Recuperados x Faixa etária"),
                    dcc.Graph(id="bar_cured", config=dict(displayModeBar=False))
                ], className="graf_card", md=4),
                dbc.Col([
                    html.H5("Confirmados x Faixa etária"),
                    dcc.Graph(id="bar_confirm", config=dict(displayModeBar=False))
                ], className="graf_card", md=4),
                dbc.Col([
                    html.H5("Óbitos x Faixa etária"),
                    dcc.Graph(id="bar_dead", config=dict(displayModeBar=False))
                ], className="graf_card", md=4),
            ], style={"display": "flex"}),
            # graficos botoom
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H5("Casos por Ano"),
                        dcc.Graph(id="data_year", config=dict(displayModeBar=False))
                    ], className="graf_card", md=6),
                    dbc.Col([
                        html.H5("Confirmados x Óbitos"),
                        dcc.Graph(id="pie_sex", config=dict(displayModeBar=False))
                    ], className="graf_card", md=6),
                ])
            ], className="bottom-div"),
        ])], className="div-direita"),


], className="div-tela")


@app.callback(
    Output('card_cured', 'children'),
    Output('card_confirm', 'children'),
    Output("card_dead", "children"),
    Output("bar_cured", "figure"),
    Output("bar_confirm", "figure"),
    Output("bar_dead", "figure"),
    Output("data_year", "figure"),
    Output("pie_sex", "figure"),
    [Input('data-filtro', 'start_date'),
     Input('data-filtro', 'end_date')]
)
def update_cards(start_date, end_date):
    db = df.query("dt_notificacao >= '{}' & dt_notificacao <= '{}'".format(start_date, end_date))
    card_confirmados = "{}".format(db.index.__len__())
    card_recuperados = "{}".format(db.query("evolucao == 'RECUPERADO'").index.__len__())
    card_obitos = "{}".format(db.query("evolucao == 'OBITO' ").index.__len__())

    # cured cases
    fig_cured = px.histogram(db.query("evolucao == 'RECUPERADO'"), x="faixa_etaria", color="Sexo", text_auto=True)
    fig_cured.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=11,
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        plot_bgcolor=main_card_color,
        paper_bgcolor=main_card_color,
    )
    # confirm cases
    fig_confirm = px.histogram(db, x="faixa_etaria", color="Sexo", text_auto=True)
    fig_confirm.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=11,
                color="black"
            ),
            bgcolor='rgba(0,0,0,0)',
        ),
        plot_bgcolor=main_card_color,
        paper_bgcolor=main_card_color,
    )
    #

    # dead cases
    fig_dead = px.histogram(db.query("evolucao == 'OBITO'"), x="faixa_etaria", color="Sexo", text_auto=True)
    fig_dead.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=11,
                color="black"
            ),
            bgcolor='rgba(0,0,0,0)',
        ),
        plot_bgcolor=main_card_color,
        paper_bgcolor=main_card_color,
    )

    # data year
    fig_year = px.line(db_by_year, x="Ano", y=["Confirmados", "Recuperados", "Óbitos"])
    fig_year.update_layout(legend=dict(
        orientation="h",
        entrywidth=70,
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ), plot_bgcolor=main_card_color,
        paper_bgcolor=main_card_color, )
    # Pie
    fig_pie = go.Figure(data=[go.Pie(labels=['Confirmados', 'Óbitos'], values=[card_confirmados, card_obitos],
                                     textinfo='value+percent', pull=[0, 0.2])])
    fig_pie.update_layout(plot_bgcolor=main_card_color,
                          paper_bgcolor=main_card_color, )
    return (
        card_recuperados,
        card_confirmados,
        card_obitos,
        fig_cured,
        fig_confirm,
        fig_dead,
        fig_year,
        fig_pie
    )


if __name__ == '__main__':
    app.run_server(debug=True)
