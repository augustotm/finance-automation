from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def format_number_matplotlib(x, pos):
    if abs(x) >= 1e9:
        return f'{x/1e9:.1f} B'
    elif abs(x) >= 1e6:
        return f'{x/1e6:.1f} M'
    elif abs(x) >= 1e3:
        return f'{x/1e3:.1f} K'
    else:
        return f'{x:.0f}'

def format_percent_matplotlib(x, pos):
    return f'{x:.1%}'

############################
###
############################

def format_number(x):
    if abs(x) >= 1e9:
        return f'{x/1e9:.1f} B'
    elif abs(x) >= 1e6:
        return f'{x/1e6:.1f} M'
    elif abs(x) >= 1e3:
        return f'{x/1e3:.1f} K'
    else:
        return f'{x:.0f}'

def format_percent(x):
    return f'{x:.1%}'

############################
### Dataframe Calculator ###
############################

def dataframe_calculator(init_invest, mo_interest, mo_inflation, mo_invest, months, current_month, current_age):
     
    df = pd.DataFrame({
        'year' : [(i+1)/12 for i in range(months)],
        'date' : [current_month + relativedelta(months=i) for i in range(months)],
        'age' : [current_age + (i+1)/12 for i in range(months)],
        'init_invest_acumm': [init_invest] * months,
        'mo_invest_acumm': [i * mo_invest for i in range(months)]
    })

    df['init_nominal_acumm'] = df.apply(
        lambda row:
        row['init_invest_acumm'] * pow(1+mo_interest, row.name + 1),
        axis=1
    )

    df['init_inflation_acumm'] = df.apply(
        lambda row:
        row['init_invest_acumm'] * pow(1+mo_inflation, row.name + 1),
        axis=1
    )

    df['mo_nominal_acumm'] = 0.0
    df['mo_inflation_acumm'] = 0.0

    for i in range(months):
        if i == 0:
            df.loc[i, 'mo_nominal_acumm'] = 0
            df.loc[i, 'mo_inflation_acumm'] = 0
        else:
            value_nom = (mo_invest + df.loc[i-1, 'mo_nominal_acumm']) * (1+mo_interest)
            df.loc[i, 'mo_nominal_acumm'] = value_nom
            value_real = (mo_invest + df.loc[i-1, 'mo_inflation_acumm']) * (1+mo_inflation)
            df.loc[i, 'mo_inflation_acumm'] = value_real

    df['total_invested'] = df['init_invest_acumm'] + df['mo_invest_acumm']
    df['total_nominal'] = df['init_nominal_acumm'] + df['mo_nominal_acumm']
    df['total_inflation'] = df['init_inflation_acumm'] + df['mo_inflation_acumm']
    df['total_real'] = df['total_nominal'] - df['total_inflation'] + df['total_invested']
    df['mo_divid_nominal'] = df['total_nominal'] * (mo_interest)
    df['mo_divid_real'] = df['total_nominal'] * (mo_interest- mo_inflation)

    return df

#####################################
### Calculator - Complete Version ###
#####################################

def calculator_complete(init_invest,
                        mo_default_invest,
                        annual_plr,
                        annual_bonus,
                        annual_interest,
                        annual_inflation,
                        unit_time,
                        qtd_time,
                        time_granum_text,
                        birth_year,
                        birth_month,
                        birth_day):
    
    init_invest = float(init_invest)
    mo_default_invest = float(mo_default_invest)
    annual_plr = float(annual_plr)
    annual_bonus = float(annual_bonus)
    annual_interest = float(annual_interest)
    annual_inflation = float(annual_inflation)

    match unit_time:
        case "Mês":
            months = int(qtd_time)
        case "Ano":
            months = 12*int(qtd_time)
    
    match time_granum_text:
        case "Num. Anos":
            time_granum = 'year'
        case "Data":
            time_granum = 'date'
        case "Idade":
            time_granum = 'age'
    
    birthday = date(int(birth_year), int(birth_month), int(birth_day))

    mo_invest = mo_default_invest + (annual_plr + annual_bonus)/12

    current_month = date.today()

    current_age = relativedelta(current_month, birthday).years + relativedelta(current_month, birthday).months/12

    mo_interest = pow(1+annual_interest, 1/12) - 1
    mo_inflation = pow(1+annual_inflation, 1/12) - 1

    df = dataframe_calculator(init_invest, mo_interest, mo_inflation, mo_invest, months, current_month, current_age)

    font_size = 8
    title_font_size = 9

    colors = {
        'investido': '#d62728',      # Vermelho
        'nominal': '#1f77b4',        # Azul
        'real': '#2ca02c'            # Verde
    }

    fig, axes = plt.subplots(3, 1, figsize=(8, 7)) # Width vs Height

    ### Figure title

    fig.suptitle('Gráficos dos Investimentos pelo Tempo', 
             fontsize=12, 
             fontweight='normal',
             y=0.98, # Ajusta a posição vertical
             ha='center')

    ### Parameters block

    param_text = (
        f"- Investimento inicial: R$ {format_number(init_invest)}\n"
        f"- Aporte mensal: R$ {format_number(mo_default_invest)}\n"
        f"- PLR anual: R$ {format_number(annual_plr)}\n"
        f"- Bônus anual: R$ {format_number(annual_bonus)}\n"
        f"- Total mensal: R$ {format_number(mo_invest)}\n"
        f"- Taxa de juros anual: R$ {format_percent(annual_interest)}\n"
        f"- Inflação anual: R$ {format_percent(annual_inflation)}\n"
        f"- Data de nascimento: {birth_day}/{birth_month}/{birth_year}"
    )

    fig.text(
        0.05, 0.93,   # posição X, Y (coordenadas relativas à figura)
        param_text,
        ha='left', va='top',
        fontsize=title_font_size,
        fontweight='normal'
    )

    # Ajuste para evitar sobreposição entre axes e fig.text
    fig.tight_layout(rect=[0.06, 0.05, 0.98, 0.80], h_pad=3.0) # [left, bottom, right, top]

    # plt.subplots_adjust(hspace=0.6)

    nb_chart = 0
    axis_y_margin_chart = 1.20

    axes[nb_chart].plot(df[time_granum], df['total_invested'],
                 label='Investido',
                 linewidth=1.5,
                 color=colors['investido'],
                 marker='o',
                 markersize=2)
    axes[nb_chart].plot(df[time_granum], df['total_nominal'],
                 label='Nominal',
                 linewidth=1.5,
                 color=colors['nominal'],
                 marker='o',
                 markersize=2)
    axes[nb_chart].plot(df[time_granum], df['total_real'], label='Real', linewidth=1.5, color=colors['real'], marker='o', markersize=2)
    axes[nb_chart].grid(True)
    axes[nb_chart].legend(loc="upper left", fontsize=font_size)
    axes[nb_chart].set_xlabel('{}'.format(time_granum_text), fontsize=font_size)
    axes[nb_chart].set_ylabel('Valor (R$)', fontsize=font_size)
    axes[nb_chart].set_ylim(bottom=0, top = df[['total_invested', 'total_nominal', 'total_real']].max().max() * axis_y_margin_chart)
    axes[nb_chart].yaxis.set_major_formatter(mticker.FuncFormatter(format_number_matplotlib))
    axes[nb_chart].set_title('Total Investido vs Total Acumulado', fontsize=title_font_size, fontweight='normal')
    nb_chart+=1

    axes[nb_chart].plot(df[time_granum], df['total_nominal']/df['total_invested']-1, label='Rend. Nominal (%)', linewidth=1.5, color=colors['nominal'], marker='o', markersize=2)
    axes[nb_chart].plot(df[time_granum], df['total_real']/df['total_invested']-1, label='Rend. Real (%)', linewidth=1.5, color=colors['real'], marker='o', markersize=2)
    axes[nb_chart].grid(True)
    axes[nb_chart].legend(loc="upper left", fontsize=font_size)
    axes[nb_chart].set_xlabel('{}'.format(time_granum_text), fontsize=font_size)
    axes[nb_chart].set_ylabel('Rendimento (%)', fontsize=font_size)
    axes[nb_chart].set_ylim(bottom=0, top = max( (df['total_nominal']/df['total_invested']-1).max(), (df['total_real']/df['total_invested']-1).max() ) * axis_y_margin_chart)
    axes[nb_chart].yaxis.set_major_formatter(mticker.FuncFormatter(format_percent_matplotlib))
    axes[nb_chart].set_title('Rendimento Nominal vs Real (Valor percentual)', fontsize=title_font_size, fontweight='normal')
    nb_chart+=1

    axes[nb_chart].plot(df[time_granum], df['mo_divid_nominal'], label='Prov. Nominal (R$)', linewidth=1.5, color=colors['nominal'], marker='o', markersize=2)
    axes[nb_chart].plot(df[time_granum], df['mo_divid_real'], label='Prov. Real (R$)', linewidth=1.5, color=colors['real'], marker='o', markersize=2)
    axes[nb_chart].grid(True)
    axes[nb_chart].legend(loc="upper left", fontsize=font_size)
    axes[nb_chart].set_xlabel('{}'.format(time_granum_text), fontsize=font_size)
    axes[nb_chart].set_ylabel('Valor (R$)', fontsize=font_size)
    axes[nb_chart].set_ylim(bottom=0, top = df[['mo_divid_nominal', 'mo_divid_real']].max().max() * axis_y_margin_chart)
    axes[nb_chart].yaxis.set_major_formatter(mticker.FuncFormatter(format_number_matplotlib))
    axes[nb_chart].set_title('Provento Nominal vs Real', fontsize=title_font_size, fontweight='normal')
    nb_chart+=1

    for ax in axes:
        ax.tick_params(axis='x', which='major', labelsize=font_size)
        ax.tick_params(axis='y', which='major', labelsize=font_size)

    # Adjust layout and spacing
    # plt.tight_layout()

    # Show chart
    plt.show()

