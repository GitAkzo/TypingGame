import requests
import random
import time
import customtkinter as ctk

class JogoDigitacao(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da Janela
        self.title("Typing Game")
        self.geometry("500x450")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variáveis de Estado
        self.words = []
        self.random_words = []
        self.current_word_index = 0
        self.pontos = 0
        self.caracteres_corretos = 0
        self.tic = 0
        
        # Atalho global para encerrar a aplicação
        self.bind("<Escape>", lambda event: self.destroy())
        
        self.tela_carregamento()
        self.after(100, self.carregar_palavras)

    def tela_carregamento(self):
        self.limpar_tela()
        self.lbl_titulo = ctk.CTkLabel(self, text="Baixando dicionário...", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(expand=True)

    def carregar_palavras(self):
        try:
            url = 'https://www.mit.edu/~ecprice/wordlist.10000'
            resposta = requests.get(url)
            self.words = [word.decode('utf-8') for word in resposta.content.splitlines()]
            self.tela_inicial()
        except Exception:
            self.lbl_titulo.configure(text="Erro de conexão. Verifique sua internet.")

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def tela_inicial(self, event=None):
        # Remove atalhos globais da tela anterior para evitar conflitos
        self.unbind("<Return>")
        self.limpar_tela()
        
        lbl_titulo = ctk.CTkLabel(self, text="Jogo de Digitação", font=("Arial", 24, "bold"))
        lbl_titulo.pack(pady=(50, 15))
        
        # Rótulo de instrução fixo acima do campo
        lbl_instrucao = ctk.CTkLabel(self, text="Quantas palavras deseja?", font=("Arial", 14))
        lbl_instrucao.pack(pady=(10, 0))
        
        # Campo de entrada focado automaticamente
        self.entry_qtd = ctk.CTkEntry(self, width=250)
        self.entry_qtd.pack(pady=(5, 10))
        self.entry_qtd.focus() 
        self.entry_qtd.bind("<Return>", lambda event: self.iniciar_jogo())
        
        btn_iniciar = ctk.CTkButton(self, text="Iniciar Jogo", command=self.iniciar_jogo)
        btn_iniciar.pack(pady=20)
        
        lbl_dica = ctk.CTkLabel(self, text="Pressione 'Esc' a qualquer momento para sair", font=("Arial", 11), text_color="gray")
        lbl_dica.pack(side="bottom", pady=20)
        
        self.lbl_erro = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_erro.pack()

    def iniciar_jogo(self):
        entrada_qtd = self.entry_qtd.get()
        
        try:
            qtd = int(entrada_qtd)
            if qtd <= 0 or qtd > len(self.words):
                raise ValueError
        except ValueError:
            self.lbl_erro.configure(text="Por favor, insira um número inteiro válido.")
            return
            
        self.random_words = random.sample(self.words, qtd)
        self.current_word_index = 0
        self.pontos = 0
        self.caracteres_corretos = 0
        self.tic = time.perf_counter()
        
        self.tela_jogo()

    def tela_jogo(self):
        self.limpar_tela()
        
        lbl_progresso = ctk.CTkLabel(self, text=f"Palavra {self.current_word_index + 1} de {len(self.random_words)}", text_color="gray")
        lbl_progresso.pack(pady=(30, 0))
        
        palavra_atual = self.random_words[self.current_word_index]
        self.lbl_palavra = ctk.CTkLabel(self, text=palavra_atual, font=("Courier New", 32, "bold"))
        self.lbl_palavra.pack(pady=20)
        
        self.entry_digitacao = ctk.CTkEntry(self, width=250, font=("Courier New", 18))
        self.entry_digitacao.pack(pady=10)
        self.entry_digitacao.focus() 
        self.entry_digitacao.bind("<KeyRelease>", self.feedback_digitacao)
        self.entry_digitacao.bind("<Return>", self.verificar_palavra)
        
        btn_confirmar = ctk.CTkButton(self, text="Confirmar", command=lambda: self.verificar_palavra(None))
        btn_confirmar.pack(pady=10)

    def verificar_palavra(self, event):
        entrada = self.entry_digitacao.get().strip()
        palavra_correta = self.random_words[self.current_word_index]
        
        # Validação de acerto e pontuação
        if entrada == palavra_correta:
            self.pontos += 1
            self.caracteres_corretos += len(palavra_correta)
            
        self.current_word_index += 1
        
        if self.current_word_index < len(self.random_words):
            self.tela_jogo()
        else:
            self.tela_resultados()

    def tela_resultados(self):
        self.limpar_tela()
        toc = time.perf_counter()
        tempo_total_segundos = abs(self.tic - toc)
        
        # Cálculo de Velocidade (WPM)
        minutos = tempo_total_segundos / 60
        wpm = round((self.caracteres_corretos / 5) / minutos) if minutos > 0 else 0
        tempo_formatado = round(tempo_total_segundos, 2)
        
        lbl_fim = ctk.CTkLabel(self, text="Fim de Jogo!", font=("Arial", 28, "bold"))
        lbl_fim.pack(pady=(40, 20))
        
        lbl_wpm = ctk.CTkLabel(self, text=f"Velocidade: {wpm} WPM", font=("Arial", 22, "bold"), text_color="#2ecc71")
        lbl_wpm.pack(pady=10)
        
        lbl_pontos = ctk.CTkLabel(self, text=f"Acertos: {self.pontos} / {len(self.random_words)}", font=("Arial", 18))
        lbl_pontos.pack(pady=5)
        
        lbl_tempo = ctk.CTkLabel(self, text=f"Tempo Total: {tempo_formatado} segundos", font=("Arial", 18))
        lbl_tempo.pack(pady=5)
        
        btn_reiniciar = ctk.CTkButton(self, text="Jogar Novamente (Enter)", command=self.tela_inicial)
        btn_reiniciar.pack(pady=30)
        
        # Permite reiniciar o jogo pressionando Enter
        self.bind("<Return>", self.tela_inicial)

    def feedback_digitacao(self, event):
        entrada = self.entry_digitacao.get().strip()
        palavra_atual = self.random_words[self.current_word_index]
        
        # 1. Se o campo estiver vazio, mantém a cor neutra
        if not entrada:
            self.entry_digitacao.configure(text_color="white")
            
        # 2. Se as letras digitadas até agora estão CORRETAS (ficando verde em tempo real)
        elif palavra_atual.startswith(entrada):
            self.entry_digitacao.configure(text_color="#2ecc71")
            
        # 3. Se a pessoa errou alguma letra no meio do caminho
        else:
            self.entry_digitacao.configure(text_color="red")

if __name__ == "__main__":
    app = JogoDigitacao()
    app.mainloop()
