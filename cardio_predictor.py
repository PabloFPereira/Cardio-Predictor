import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import tkinter as tk
from tkinter import messagebox, ttk


data_frame_cardio = pd.read_csv("cardio_train.csv", sep=";", index_col=0)

Y = data_frame_cardio["cardio"]
X = data_frame_cardio.loc[:, data_frame_cardio.columns != 'cardio']


x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)


ml_model = RandomForestClassifier()
ml_model.fit(x_train, y_train)


def prever_doenca_cardiaca():
    try:
        id_paciente = int(entry_id.get())
        if id_paciente in data_frame_cardio.index:
            dados_paciente = data_frame_cardio.loc[id_paciente].drop('cardio').values.reshape(1, -1)
            predicao = ml_model.predict(dados_paciente)
            resultado = "Tem doença cardíaca" if predicao[0] == 1 else "Não tem doença cardíaca"
            

            messagebox.showinfo("Resultado", resultado)
            
            info_window = tk.Toplevel(root)
            info_window.title("Informações do Paciente")
            
            tree = ttk.Treeview(info_window, columns=("Característica", "Valor"), show="headings")
            tree.heading("Característica", text="Característica")
            tree.heading("Valor", text="Valor")
            
            paciente_info = data_frame_cardio.loc[id_paciente].drop('cardio')
            for caracteristica, valor in paciente_info.items():
                tree.insert("", "end", values=(caracteristica, valor))
            
            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
        else:
            messagebox.showerror("Erro", "ID do paciente não encontrado.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")

root = tk.Tk()
root.title("Previsor de Doença Cardíaca")

tk.Label(root, text="Insira o ID do Paciente:").pack(pady=10)
entry_id = tk.Entry(root)
entry_id.pack(pady=5)

btn_prever = tk.Button(root, text="Prever", command=prever_doenca_cardiaca)
btn_prever.pack(pady=20)

root.mainloop()
