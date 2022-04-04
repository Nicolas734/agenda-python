from tkinter import *
import tkinter.ttk as tkk
import tkinter as tk
from tkinter import messagebox
import sqlite3


# realiza a conexão com o banco de dados, caso não exista um BD é criado um automaticamente
conn = sqlite3.connect('Agenda.db')
cursor = conn.cursor()

# cria a tabela caso já exista não será criado
cursor.execute('''CREATE TABLE IF NOT EXISTS teste (
                Registro TEXT,
                Descricao TEXT)''')

print('Tabela criada com sucesso.')


# realiza uma consulta em todas as linhas da tabela
def consulta():
     return cursor.execute(" SELECT rowid, * FROM teste; ").fetchall()


# realiza uma consulta no ultimo registro adicionado na tabela
def consultar_ultimo_rowid():
        return cursor.execute('SELECT MAX(rowid) FROM teste').fetchone()


def inserir():
    # recebe os elmentos digitados nas entrys 
    Registro = nome.get()
    descricao = idadedg.get()
    
    # insere os elementos recebidos na tabela
    cursor.execute(
            '''INSERT INTO teste(Registro, Descricao)
            VALUES (?, ?)''', (Registro, descricao))
    conn.commit()

    # Coletando a ultima rowid que foi inserida no banco.
    rowid = consultar_ultimo_rowid()[0]
    
    # Adicionando os novos dados no treeview.
    treeview.insert('', 'end',   values=(rowid,Registro, descricao), tags = ('oddrow',))
    
    # limpa o campo da entry logo após ser adicionado na tabela
    nome.delete(0,END)
    idadedg.delete(0,END)
        


def remover_registro(rowid):
    
    # recebe o item selecionado pelo mouse
    item_selecionado = treeview.focus()
    rowid = treeview.item(item_selecionado)
    rowid = rowid['values']
    rowid1 = rowid[0]
    
    # tenta deletar o elemento selecionado pelo mouse
    try:
        cursor.execute("DELETE FROM teste WHERE rowid=?", (rowid1,))
        
    # em caso de erro não adiciona a tabela e retorna o erro ocorrido
    except Exception as e:
        print('\n[x] Falha ao remover registro [x]\n')
        print('[x] Revertendo operação (rollback) %s [x]\n' % e)
        conn.rollback()
    
    # se não ocorreu nenhum erro é adicionado a tabela e retorna uma mensagem de confirmação no prompt
    else:
        conn.commit()
        print('\n[!] Registro removido com sucesso [!]\n')
    

def excluir_registro():
    # Verificando se algum item está selecionado.
    if not treeview.focus():
        messagebox.showerror('Erro', 'Nenhum item selecionado')
    else:
        # Coletando qual item está selecionado.
        item_selecionado = treeview.focus()

        # Coletando os dados do item selecionado (dicionário).
        rowid = treeview.item(item_selecionado)
            
        # Removendo o item com base no valor do rowid (argumento text do treeview).
        # Removendo valor da tabela.
        remover_registro(rowid['text'])
            
        # Removendo valor do treeview.
        treeview.delete(item_selecionado)



app = Tk()

app.title("Agenda")
app.geometry('600x400')
app.resizable(width=False, height=False)


frame1 = tk.Frame()
frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


frame2 = tk.Frame()
frame2.pack(fill=tk.BOTH, expand=True)


frame3 = tk.Frame()
frame3.pack(side=tk.BOTTOM, padx=5)


nomedg = Label(frame1, width=10, text='Registro', font=('Arial 10'))
nomedg.grid(row=0, column=0)
nome = Entry(frame1, width=20, font=('Arial 10'))
nome.grid(row=1, column=0)


idade = Label(frame1, width=10, text='Descrição', font=('Arial 10'))
idade.grid(row=0, column=1)
idadedg = Entry(frame1, width=20, font=('Arial 10'))
idadedg.grid(row=1, column=1, padx=10)


botao = Button(frame1, command=inserir,bg='white', width=6, height=1, text="Adicionar")
botao.grid(row=0, column=3, rowspan=2, padx=10)


treeview = tkk.Treeview(frame2, columns=('Item', 'Registro', 'Descricao'), show="headings")
treeview.column('Item',minwidth=0,width=60)
treeview.column('Registro',minwidth=0,width=200)
treeview.column('Descricao',minwidth=0,width=200)
# treeview.tag_configure('oddrow', background='green')
treeview.heading('Item', text='Item')
treeview.heading('Registro', text='Registro')
treeview.heading('Descricao', text='Descrição')

for row in consulta():
            treeview.insert('', 'end', values=(row[0], row[1], row[2]))

treeview.pack(fill=tk.BOTH, expand=True)


button_excluir = tk.Button(frame3,command=excluir_registro, text='Excluir', bg='red', fg='white')
button_excluir.pack(pady=10)


app.mainloop()