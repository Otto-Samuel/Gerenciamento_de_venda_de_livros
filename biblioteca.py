import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Conectar ao banco de dados
conn = sqlite3.connect('biblioteca.db')
c = conn.cursor()

# Criar a janela principal
root = tk.Tk()
root.title("Gerenciamento de Vendas de Livros")
root.configure(bg='#092d5d')  # Define a cor de fundo como azul claro

# Carregar a imagem do logotipo e redimensioná-la
image = Image.open("./imgs/livraria1.png")
image = image.resize((180, 180))
photo = ImageTk.PhotoImage(image)

# Exibir o logotipo como um label
label_logo = tk.Label(root, image=photo, bg="#092d5d")
label_logo.pack(pady=(20, 10))

# Título
lbl_titulo = tk.Label(root, text="Gerenciamento de Vendas de Livros 🪶", font=("Arial", 30), fg="white", bg="#092d5d")
lbl_titulo.pack(pady=(10, 20))

# Função para exibir estatísticas
def exibir_estatisticas():
    # Abrir uma nova janela para exibir estatísticas
    estatisticas_window = tk.Toplevel(root)
    estatisticas_window.title("Estatísticas")

    # Exibir estatísticas de vendas
    total_vendas = c.execute("SELECT SUM(preco * quantidade) FROM livros").fetchone()[0]
    livro_mais_vendido = c.execute("SELECT titulo FROM livros ORDER BY quantidade DESC LIMIT 1").fetchone()[0]
    media_preco = c.execute("SELECT AVG(preco) FROM livros").fetchone()[0]

    # Texto para exibir estatísticas
    lbl_total_vendas = tk.Label(estatisticas_window, text=f"Total de vendas: R${total_vendas if total_vendas else 0}")
    lbl_total_vendas.pack()

    lbl_livro_mais_vendido = tk.Label(estatisticas_window, text=f"Livro mais vendido: {livro_mais_vendido}")
    lbl_livro_mais_vendido.pack()

    lbl_media_preco = tk.Label(estatisticas_window, text=f"Média de preço dos livros: R${media_preco if media_preco else 0}")
    lbl_media_preco.pack()

    # Gráfico de dispersão com linha tracejada para mostrar a relação entre preço e quantidade
    fig, ax = plt.subplots()
    livros = c.execute("SELECT preco, quantidade FROM livros").fetchall()
    precos = [livro[0] for livro in livros]
    quantidades = [livro[1] for livro in livros]
    ax.scatter(precos, quantidades, label='Vendas de Livros')
    ax.axhline(np.mean(quantidades), color='gray', linestyle='--', label='Média de Quantidades Vendidas')
    ax.set_xlabel('Preço')
    ax.set_ylabel('Quantidade Vendida')
    ax.set_title('Relação entre Preço e Quantidade Vendida')
    ax.legend()

    # Incorporar o gráfico ao tkinter
    canvas = FigureCanvasTkAgg(fig, master=estatisticas_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Função para adicionar livro
def adicionar_livro():
    add_window = tk.Toplevel(root)
    add_window.title("Adicionar Livro")

    # Campos de entrada para adicionar livro
    lbl_titulo = tk.Label(add_window, text="Título:")
    lbl_titulo.grid(row=0, column=0, padx=5, pady=5)
    entry_titulo = tk.Entry(add_window)
    entry_titulo.grid(row=0, column=1, padx=5, pady=5)

    lbl_autor = tk.Label(add_window, text="Autor:")
    lbl_autor.grid(row=1, column=0, padx=5, pady=5)
    entry_autor = tk.Entry(add_window)
    entry_autor.grid(row=1, column=1, padx=5, pady=5)

    lbl_preco = tk.Label(add_window, text="Preço:")
    lbl_preco.grid(row=2, column=0, padx=5, pady=5)
    entry_preco = tk.Entry(add_window)
    entry_preco.grid(row=2, column=1, padx=5, pady=5)

    lbl_quantidade = tk.Label(add_window, text="Quantidade:")
    lbl_quantidade.grid(row=3, column=0, padx=5, pady=5)
    entry_quantidade = tk.Entry(add_window)
    entry_quantidade.grid(row=3, column=1, padx=5, pady=5)

    # Função para adicionar livro ao banco de dados
    def adicionar():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        preco = float(entry_preco.get())
        quantidade = int(entry_quantidade.get())

        c.execute("INSERT INTO livros (titulo, autor, preco, quantidade) VALUES (?, ?, ?, ?)",
                  (titulo, autor, preco, quantidade))
        conn.commit()
        print("Livro adicionado com sucesso!")

        add_window.destroy()

    # Botão para adicionar livro
    icon_add = Image.open("./imgs/botao-adicionar.png")  # Substitua "add_icon.png" pelo caminho da imagem do ícone de adicionar
    icon_add = icon_add.resize((20, 20))
    icon_add = ImageTk.PhotoImage(icon_add)
    btn_adicionar = tk.Button(add_window, text="Adicionar", image=icon_add, compound=tk.LEFT, command=adicionar)
    btn_adicionar.grid(row=4, columnspan=2, padx=5, pady=5)

# Função para excluir livro
def excluir_livro():
    delete_window = tk.Toplevel(root)
    delete_window.title("Excluir Livro")

    # Campo de entrada para ID do livro a ser excluído
    lbl_id = tk.Label(delete_window, text="ID do Livro:")
    lbl_id.grid(row=0, column=0, padx=5, pady=5)
    entry_id = tk.Entry(delete_window)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    # Função para excluir livro do banco de dados
    def excluir():
        id_livro = int(entry_id.get())
        c.execute("DELETE FROM livros WHERE id=?", (id_livro,))
        conn.commit()
        print("Livro excluído com sucesso!")

        delete_window.destroy()

    # Botão para excluir livro
    icon_delete = Image.open("./imgs/excluir.png")  # Substitua "delete_icon.png" pelo caminho da imagem do ícone de excluir
    icon_delete = icon_delete.resize((20, 20))
    icon_delete = ImageTk.PhotoImage(icon_delete)
    btn_excluir = tk.Button(delete_window, text="Excluir", image=icon_delete, compound=tk.LEFT, command=excluir)
    btn_excluir.grid(row=1, columnspan=2, padx=5, pady=5)

# Função para editar livro
def editar_livro():
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Livro")

    # Campos de entrada para editar livro
    lbl_id = tk.Label(edit_window, text="ID do Livro:")
    lbl_id.grid(row=0, column=0, padx=5, pady=5)
    entry_id = tk.Entry(edit_window)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    lbl_titulo = tk.Label(edit_window, text="Novo Título:")
    lbl_titulo.grid(row=1, column=0, padx=5, pady=5)
    entry_titulo = tk.Entry(edit_window)
    entry_titulo.grid(row=1, column=1, padx=5, pady=5)

    lbl_autor = tk.Label(edit_window, text="Novo Autor:")
    lbl_autor.grid(row=2, column=0, padx=5, pady=5)
    entry_autor = tk.Entry(edit_window)
    entry_autor.grid(row=2, column=1, padx=5, pady=5)

    lbl_preco = tk.Label(edit_window, text="Novo Preço:")
    lbl_preco.grid(row=3, column=0, padx=5, pady=5)
    entry_preco = tk.Entry(edit_window)
    entry_preco.grid(row=3, column=1, padx=5, pady=5)

    lbl_quantidade = tk.Label(edit_window, text="Nova Quantidade:")
    lbl_quantidade.grid(row=4, column=0, padx=5, pady=5)
    entry_quantidade = tk.Entry(edit_window)
    entry_quantidade.grid(row=4, column=1, padx=5, pady=5)

    # Função para editar livro no banco de dados
    def editar():
        id_livro = int(entry_id.get())
        novo_titulo = entry_titulo.get()
        novo_autor = entry_autor.get()
        novo_preco = float(entry_preco.get())
        nova_quantidade = int(entry_quantidade.get())

        c.execute("UPDATE livros SET titulo=?, autor=?, preco=?, quantidade=? WHERE id=?",
                  (novo_titulo, novo_autor, novo_preco, nova_quantidade, id_livro))
        conn.commit()
        print("Livro editado com sucesso!")

        edit_window.destroy()

    # Botão para editar livro
    icon_edit = Image.open("./imgs/botao-editar.png")  # Substitua "edit_icon.png" pelo caminho da imagem do ícone de editar
    icon_edit = icon_edit.resize((20, 20))
    icon_edit = ImageTk.PhotoImage(icon_edit)
    btn_editar = tk.Button(edit_window, text="Editar", image=icon_edit, compound=tk.LEFT, command=editar)
    btn_editar.grid(row=5, columnspan=2, padx=5, pady=5)

# Função para realizar venda
def realizar_venda():
    venda_window = tk.Toplevel(root)
    venda_window.title("Realizar Venda")

    # Campos de entrada para realizar venda
    lbl_id = tk.Label(venda_window, text="ID do Livro:")
    lbl_id.grid(row=0, column=0, padx=5, pady=5)
    entry_id = tk.Entry(venda_window)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    lbl_quantidade = tk.Label(venda_window, text="Quantidade Vendida:")
    lbl_quantidade.grid(row=1, column=0, padx=5, pady=5)
    entry_quantidade = tk.Entry(venda_window)
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

    # Função para realizar venda do livro
    def vender():
        id_livro = int(entry_id.get())
        quantidade_vendida = int(entry_quantidade.get())

        livro = c.execute("SELECT * FROM livros WHERE id=?", (id_livro,)).fetchone()
        if livro:
            if livro[4] >= quantidade_vendida:
                novo_estoque = livro[4] - quantidade_vendida
                c.execute("UPDATE livros SET quantidade=? WHERE id=?", (novo_estoque, id_livro))
                conn.commit()
                valor_total = quantidade_vendida * livro[3]
                print(f"Venda realizada! Valor total: R${valor_total}")
            else:
                print("Quantidade insuficiente em estoque.")
        else:
            print("Livro não encontrado.")

        venda_window.destroy()

    # Botão para realizar venda
    icon_sell = Image.open("./imgs/dinheiro.png")  # Substitua "sell_icon.png" pelo caminho da imagem do ícone de realizar venda
    icon_sell = icon_sell.resize((20, 20))
    icon_sell = ImageTk.PhotoImage(icon_sell)
    btn_vender = tk.Button(venda_window, text="Realizar Venda", image=icon_sell, compound=tk.LEFT, command=vender)
    btn_vender.grid(row=2, columnspan=2, padx=5, pady=5)

# Função para exibir livros
def exibir_livros():
    exibir_window = tk.Toplevel(root)
    exibir_window.title("Livros Disponíveis")

    # Texto para exibir livros
    text = tk.Text(exibir_window, height=10, width=50)
    text.pack(padx=10, pady=10)

    # Função para exibir livros na janela
    def exibir():
        livros = c.execute("SELECT * FROM livros").fetchall()
        if livros:
            text.delete("1.0", tk.END)
            for livro in livros:
                text.insert(tk.END, f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Preço: R${livro[3]}, Quantidade em estoque: {livro[4]}\n\n")
        else:
            text.insert(tk.END, "Nenhum livro disponível.")

    exibir()

# Botões para cada funcionalidade

btn_estatisticas = tk.Button(root, text="Exibir Estatísticas", command=exibir_estatisticas)
icon_estatisticas = Image.open("./imgs/estatisticas.png")  # Substitua "estatisticas_icon.png" pelo caminho da imagem do ícone de estatísticas
icon_estatisticas = icon_estatisticas.resize((20, 20))
icon_estatisticas = ImageTk.PhotoImage(icon_estatisticas)
btn_estatisticas.config(image=icon_estatisticas, compound=tk.LEFT)
btn_estatisticas.pack(padx=10, pady=10)

btn_adicionar = tk.Button(root, text="Adicionar Livro", command=adicionar_livro)
icon_add = Image.open("./imgs/botao-adicionar.png")  # Substitua "add_icon.png" pelo caminho da imagem do ícone de adicionar
icon_add = icon_add.resize((20, 20))
icon_add = ImageTk.PhotoImage(icon_add)
btn_adicionar.config(image=icon_add, compound=tk.LEFT)
btn_adicionar.pack(padx=10, pady=10)

btn_excluir = tk.Button(root, text="Excluir Livro", command=excluir_livro)
icon_delete = Image.open("./imgs/excluir.png")  # Substitua "delete_icon.png" pelo caminho da imagem do ícone de excluir
icon_delete = icon_delete.resize((20, 20))
icon_delete = ImageTk.PhotoImage(icon_delete)
btn_excluir.config(image=icon_delete, compound=tk.LEFT)
btn_excluir.pack(padx=10, pady=10)

btn_editar = tk.Button(root, text="Editar Livro", command=editar_livro)
icon_edit = Image.open("./imgs/botao-editar.png")  # Substitua "edit_icon.png" pelo caminho da imagem do ícone de editar
icon_edit = icon_edit.resize((20, 20))
icon_edit = ImageTk.PhotoImage(icon_edit)
btn_editar.config(image=icon_edit, compound=tk.LEFT)
btn_editar.pack(padx=10, pady=10)

btn_vender = tk.Button(root, text="Realizar Venda", command=realizar_venda)
icon_sell = Image.open("./imgs/dinheiro.png")  # Substitua "sell_icon.png" pelo caminho da imagem do ícone de realizar venda
icon_sell = icon_sell.resize((20, 20))
icon_sell = ImageTk.PhotoImage(icon_sell)
btn_vender.config(image=icon_sell, compound=tk.LEFT)
btn_vender.pack(padx=10, pady=10)

btn_exibir = tk.Button(root, text="Exibir Livros", command=exibir_livros)
icon_books = Image.open("./imgs/livro.png")  # Substitua "books_icon.png" pelo caminho da imagem do ícone de exibir livros
icon_books = icon_books.resize((20, 20))
icon_books = ImageTk.PhotoImage(icon_books)
btn_exibir.config(image=icon_books, compound=tk.LEFT)
btn_exibir.pack(padx=173, pady=10)

root.mainloop()
