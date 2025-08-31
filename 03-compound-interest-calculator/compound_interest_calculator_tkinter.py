from datetime import date, datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar 
from pathlib import Path
import os
from dotenv import load_dotenv

from engine import calculator_complete


if __name__ == "__main__":
    
    # Main window
    root = tk.Tk()
    root.title("Calculadora de Juros Compostos")
    root.geometry("490x410") # Width vs Height

    # Frame principal
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    #################
    ### Variables ###
    #################

    env_path = Path(__file__).parent / ".env.tkinter"
    load_dotenv(dotenv_path=env_path, override=True)
    env_invest_inicial = os.getenv("INVEST_INICIAL")
    env_aporte_mensal = os.getenv("APORTE_MENSAL")
    env_plr_anual = os.getenv("PLR_ANUAL")
    env_bonus_anual = os.getenv("BONUS_ANUAL")
    env_interest_anual = os.getenv("INTEREST_ANUAL")
    env_inflation_anual = os.getenv("INFLATION_ANUAL")
    env_list_tempo = os.getenv("LIST_TEMPO")
    env_qtd_tempo = os.getenv("QTD_TEMPO")
    env_granul_tempo = os.getenv("GRANUL_TEMPO")
    env_nasc_dia = os.getenv("NASC_DIA")
    env_nasc_mes = os.getenv("NASC_MES")
    env_nasc_ano = os.getenv("NASC_ANO")

    default_width = 14
    dropdown_width = default_width - 3

    # Investimento Inicial
    ttk.Label(frame, text="Investimento Inicial (R$):").grid(row=0, column=0, sticky=tk.W, pady=5)
    entry_invest_inicial = ttk.Entry(frame, width=default_width)
    entry_invest_inicial.grid(row=0, column=1, pady=5)
    entry_invest_inicial.insert(0, env_invest_inicial)

    # Aporte Mensal
    ttk.Label(frame, text="Aporte Mensal (R$):").grid(row=1, column=0, sticky=tk.W, pady=5)
    entry_aporte_mensal = ttk.Entry(frame, width=default_width)
    entry_aporte_mensal.grid(row=1, column=1, pady=5)
    entry_aporte_mensal.insert(0, env_aporte_mensal)

    # PLR Anual
    ttk.Label(frame, text="PLR Anual (R$):").grid(row=2, column=0, sticky=tk.W, pady=5)
    entry_plr_anual = ttk.Entry(frame, width=default_width)
    entry_plr_anual.grid(row=2, column=1, pady=5)
    entry_plr_anual.insert(0, env_plr_anual)

    # Bonus Anual
    ttk.Label(frame, text="Bônus Anual (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
    entry_bonus_anual = ttk.Entry(frame, width=default_width)
    entry_bonus_anual.grid(row=3, column=1, pady=5)
    entry_bonus_anual.insert(0, env_bonus_anual)
    
    # Juros anual
    ttk.Label(frame, text="Taxa de Juros Anual:").grid(row=4, column=0, sticky=tk.W, pady=5)
    entry_interest_anual = ttk.Entry(frame, width=default_width)
    entry_interest_anual.grid(row=4, column=1, pady=5)
    entry_interest_anual.insert(0, env_interest_anual)

    # Inflacao anual
    ttk.Label(frame, text="Inflação Anual:").grid(row=5, column=0, sticky=tk.W, pady=5)
    entry_inflation_anual = ttk.Entry(frame, width=default_width)
    entry_inflation_anual.grid(row=5, column=1, pady=5)
    entry_inflation_anual.insert(0, env_inflation_anual)

    # Unidade de tempo
    ttk.Label(frame, text="Período (Mês/Ano):").grid(row=6, column=0, sticky=tk.W, pady=5)
    entry_list_tempo = ttk.Combobox(frame, values=["Mês", "Ano"], state="readonly", width=dropdown_width)
    entry_list_tempo.grid(row=6, column=1, pady=5)
    entry_list_tempo.set(env_list_tempo)

    # Quantidade de tempo
    ttk.Label(frame, text="Qtd. Período:").grid(row=7, column=0, sticky=tk.W, pady=5)
    entry_qtd_tempo = ttk.Entry(frame, width=default_width)
    entry_qtd_tempo.grid(row=7, column=1, pady=5)
    entry_qtd_tempo.insert(0, env_qtd_tempo)

    # Granularidade de tempo
    ttk.Label(frame, text="Granularidade de tempo:").grid(row=8, column=0, sticky=tk.W, pady=5)
    entry_granul_tempo = ttk.Combobox(frame, values=["Num. Anos", "Data", "Idade"], state="readonly", width=dropdown_width)
    entry_granul_tempo.grid(row=8, column=1, pady=5)
    entry_granul_tempo.set(env_granul_tempo)

    # Data de Nascimento
    ttk.Label(frame, text="Data de Nascimento:").grid(row=9, column=0, sticky=tk.W, pady=5)
    entry_nasc_dia = ttk.Combobox(frame, values=[str(i).zfill(2) for i in range(1, 32)], width=dropdown_width)
    entry_nasc_dia.grid(row=9, column=1, padx=(0, 5), pady=5)
    entry_nasc_dia.set(env_nasc_dia)

    ttk.Label(frame, text="/").grid(row=9, column=2)
    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    entry_nasc_mes = ttk.Combobox(frame, values=meses, width=dropdown_width)
    entry_nasc_mes.grid(row=9, column=3, padx=5)
    entry_nasc_mes.set(env_nasc_mes)

    ttk.Label(frame, text="/").grid(row=9, column=4)
    ano_atual = datetime.now().year
    anos = [str(i) for i in range(1950, ano_atual + 1)]
    entry_nasc_ano = ttk.Combobox(frame, values=anos, width=dropdown_width)
    entry_nasc_ano.grid(row=9, column=5, padx=(5, 0))
    entry_nasc_ano.set(env_nasc_ano)
    
    # Botão Calcular
    btn_calcular = ttk.Button(
        frame, text="Calcular",
        command=lambda: calculator_complete(
            entry_invest_inicial.get(),
            entry_aporte_mensal.get(),
            entry_plr_anual.get(),
            entry_bonus_anual.get(),
            entry_interest_anual.get(),
            entry_inflation_anual.get(),
            entry_list_tempo.get(),
            entry_qtd_tempo.get(),
            entry_granul_tempo.get(),
            entry_nasc_ano.get(),
            entry_nasc_mes.get(),
            entry_nasc_dia.get()
            )
        )
    btn_calcular.grid(row=20, column=0, columnspan=2, pady=20)

    # Configurar expansão
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
        
    # Iniciar interface
    root.mainloop()

    # Fechar a janela de input
    # root.destroy()

