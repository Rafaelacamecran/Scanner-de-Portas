import socket
import threading
import os
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Classe Principal da Aplicação ---
class PortScannerApp:
    """
    Classe que encapsula toda a lógica da aplicação de scanner de portas com GUI.
    """
    def __init__(self, master):
        self.master = master
        master.title("Scanner de Portas TCP")
        master.geometry("550x450")

        # --- Elementos da Interface Gráfica ---
        # Frame para agrupar os campos de entrada
        input_frame = tk.Frame(master, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        # Rótulo e campo de entrada para o IP do Alvo
        self.label_ip = tk.Label(input_frame, text="Alvo (IP):")
        self.label_ip.pack(side=tk.LEFT, padx=(0, 5))
        self.entry_ip = tk.Entry(input_frame, width=20)
        self.entry_ip.pack(side=tk.LEFT)
        self.entry_ip.insert(0, "127.0.0.1")  # IP de exemplo (localhost)

        # Rótulo e campo de entrada para a Faixa de Portas
        self.label_ports = tk.Label(input_frame, text="Portas (ex: 1-1024):")
        self.label_ports.pack(side=tk.LEFT, padx=(15, 5))
        self.entry_ports = tk.Entry(input_frame, width=15)
        self.entry_ports.pack(side=tk.LEFT)
        self.entry_ports.insert(0, "1-1024")  # Faixa de exemplo

        # Botão para iniciar o escaneamento
        self.scan_button = tk.Button(master, text="Escanear", command=self.iniciar_scan_thread)
        self.scan_button.pack(pady=5)

        # Área de texto com rolagem para exibir os resultados
        self.results_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=18)
        self.results_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.results_text.configure(state='disabled')  # Torna o campo somente leitura

    def adicionar_log_gui(self, mensagem):
        """Adiciona uma mensagem à área de texto da interface de forma segura."""
        self.results_text.configure(state='normal')
        self.results_text.insert(tk.END, mensagem + "\n")
        self.results_text.configure(state='disabled')
        self.results_text.see(tk.END)  # Garante que a última linha seja visível

    def iniciar_scan_thread(self):
        """
        Inicia o escaneamento em uma nova thread para não bloquear a GUI.
        """
        self.scan_button.config(state=tk.DISABLED)
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.configure(state='disabled')

        # Cria e inicia a thread do scanner
        scan_thread = threading.Thread(target=self.executar_scan)
        scan_thread.daemon = True  # Permite que a janela principal feche a thread
        scan_thread.start()

    def executar_scan(self):
        """
        Contém a lógica principal do scanner de portas.
        """
        alvo_ip = self.entry_ip.get()
        faixa_portas_str = self.entry_ports.get()

        # --- Validação das Entradas do Usuário ---
        try:
            socket.inet_aton(alvo_ip)
        except socket.error:
            messagebox.showerror("Erro de Entrada", f"O endereço IP '{alvo_ip}' não é válido.")
            self.scan_button.config(state=tk.NORMAL)
            return

        try:
            porta_inicio, porta_fim = map(int, faixa_portas_str.split('-'))
            if not (0 < porta_inicio <= porta_fim <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O formato da faixa de portas é inválido.\nUse um formato como '1-1024'.")
            self.scan_button.config(state=tk.NORMAL)
            return

        self.adicionar_log_gui(f"Iniciando escaneamento em {alvo_ip}...")
        self.adicionar_log_gui(f"Verificando portas de {porta_inicio} a {porta_fim}")
        self.adicionar_log_gui("-" * 40)

        portas_abertas = []

        # --- Lógica do Scanner (Loop de verificação) ---
        for porta in range(porta_inicio, porta_fim + 1):
            try:
                # Usar 'with' garante que o socket seja fechado automaticamente
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.5)  # Timeout de 0.5 segundos por porta
                    resultado = sock.connect_ex((alvo_ip, porta))
                    if resultado == 0:
                        self.adicionar_log_gui(f"Porta {porta} [ABERTA]")
                        portas_abertas.append(porta)
            except socket.error as e:
                self.adicionar_log_gui(f"Erro de socket ao escanear porta {porta}: {e}")
                break  # Interrompe se houver um erro geral de conexão

        self.adicionar_log_gui("-" * 40)
        self.adicionar_log_gui("Escaneamento concluído.")

        # --- Armazenamento do Log em Arquivo ---
        self.salvar_log_em_arquivo(alvo_ip, f"{porta_inicio}-{porta_fim}", portas_abertas)

        # Reabilita o botão ao final do processo
        self.scan_button.config(state=tk.NORMAL)

    def salvar_log_em_arquivo(self, ip_alvo, faixa_portas, portas_abertas):
        """
        Cria o diretório C:\\Logs (se não existir) e salva o resultado do scan.
        """
        caminho_log = r"C:\Logs"
        try:
            os.makedirs(caminho_log, exist_ok=True) # Cria o diretório se não existir
            
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            nome_arquivo = os.path.join(caminho_log, f"scan_log_{timestamp}.txt")

            with open(nome_arquivo, 'w') as f:
                f.write("--- Relatório de Escaneamento de Portas ---\n")
                f.write(f"Data/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Alvo: {ip_alvo}\n")
                f.write(f"Faixa de Portas Verificada: {faixa_portas}\n")
                f.write("-" * 40 + "\n\n")

                if portas_abertas:
                    f.write("Portas Abertas Encontradas:\n")
                    for porta in portas_abertas:
                        f.write(f"  - Porta {porta}\n")
                else:
                    f.write("Nenhuma porta aberta foi encontrada na faixa especificada.\n")

            self.adicionar_log_gui(f"Relatório salvo em: {nome_arquivo}")

        except PermissionError:
            erro_msg = (f"Permissão negada para criar o diretório ou arquivo em '{caminho_log}'.\n"
                        "Tente executar o script como administrador.")
            self.adicionar_log_gui(f"ERRO: {erro_msg}")
            messagebox.showerror("Erro de Permissão", erro_msg)
        except Exception as e:
            erro_msg = f"Ocorreu um erro inesperado ao salvar o log: {e}"
            self.adicionar_log_gui(f"ERRO: {erro_msg}")
            messagebox.showerror("Erro ao Salvar Log", erro_msg)


# --- Bloco Principal para Iniciar a Aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()