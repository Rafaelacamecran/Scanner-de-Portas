# Nome do projeto:
Scanner de Portas simples

# Descrição:
O scanner de portas é uma ferramenta de software projetada para identificar o estado das portas em um computador ou dispositivo de rede.
As portas TCP (Transmission Control Protocol) são canais de comunicação virtual que permitem que diferentes aplicações e serviços em um dispositivo se comuniquem através de uma rede.
Ao verificar quais portas estão abertas ou fechadas, um scanner de portas oferece um panorama detalhado dos serviços ativos em um sistema, servindo como um instrumento crucial tanto para a segurança da informação quanto para o gerenciamento de redes.

# Instalação
O código é um script Python que cria uma aplicação de scanner de portas com uma interface gráfica.
Para instalar, você basicamente precisa ter o Python no seu sistema e executar o arquivo.

Aqui está um passo a passo detalhado para colocar o scanner em funcionamento.
Pré-requisitos: Ter o Python Instalado
O script é escrito em Python e usa a biblioteca tkinter, que já vem inclusa na maioria das instalações do Python, especialmente para Windows.
Verifique se você tem o Python: Abra o seu terminal (Prompt de Comando ou PowerShell no Windows, Terminal no macOS ou Linux) e digite um dos comandos abaixo:

Bash
python --version
Bash
python3 --version
Se você receber uma resposta com a versão (ex: Python 3.13.3), ótimo!
Se não, você precisa instalar o Python primeiro.
Recomendo a versão mais recente.

(Apenas para alguns sistemas Linux) Verifique o Tkinter: Em algumas distribuições Linux, o tkinter precisa ser instalado separadamente.
Se você encontrar um erro como ModuleNotFoundError: No module named '_tkinter', instale-o com o gerenciador de pacotes do seu sistema.
Por exemplo, em sistemas baseados em Debian/Ubuntu:

Bash
sudo apt-get update
sudo apt-get install python3-tk

Passo 1: Salvar o Código
Copie todo o código fornecido.
Abra um editor de texto simples como o Bloco de Notas no Windows, TextEdit no Mac, ou um editor de código como VS Code e etc...
Cole o código no editor.
Salve o arquivo com a extensão .py.
Passo 2: Executar o Script
Abra o VSCODE e abra a pasta onde você salvou o arquivo e rode o script.
ex: python3 Scanner de portas.py
Se tudo correu bem, a janela do "Scanner de Portas" deverá aparecer na sua tela.

Passo 3: Configuração e Uso
A "configuração" do scan é feita diretamente na interface gráfica:
Alvo (IP): Digite o endereço IP do computador ou servidor que você deseja escanear. O padrão é 127.0.0.1 (localhost), que é o seu próprio computador.
Portas: Defina a faixa de portas que deseja verificar. O formato é inicio-fim (ex: 1-1024, 80-88, etc.).
Escanear: Clique no botão "Escanear" para iniciar o processo. Os resultados aparecerão na caixa de texto abaixo em tempo real.
O script salva automaticamente os relatórios de scan em um diretório fixo no Windows: C:\Logs. Abra o caminho da pasta e abra o arquivo em .txt salvo.

Funcionalidades: 
O scanner de portas serve para dois propósitos principais
1- Gerenciamento e Auditoria de Redes: Administradores de sistemas e redes utilizam scanners de portas para verificar a configuração de seus próprios sistemas.
Isso permite confirmar que apenas as portas necessárias para os serviços essenciais (como servidores web, e-mail ou arquivos) estão abertas, garantindo que a política de segurança da organização está sendo seguida. A verificação regular ajuda a identificar portas abertas por engano ou por softwares não autorizados, que poderiam representar um risco de segurança.
2- Análise de Segurança e Testes de Invasão (Pentest): Profissionais de segurança da informação, conhecidos como pentesters ou hackers éticos, empregam scanners de portas para simular ataques e avaliar a postura de segurança de uma rede. Ao identificar portas abertas, eles podem determinar quais serviços estão em execução e, consequentemente, procurar por vulnerabilidades conhecidas nesses serviços que poderiam ser exploradas por atacantes mal-intencionados.
Como Funciona um Scanner de Portas
Um scanner de portas opera enviando pacotes de dados para uma gama de portas em um endereço IP de destino e analisando as respostas recebidas. A natureza da resposta (ou a falta dela) indica o estado da porta:
Aberta: O dispositivo de destino responde com um pacote que indica que um serviço está ativo e aceitando conexões naquela porta.
Fechada: O dispositivo de destino responde com um pacote que indica que a porta não está sendo usada por nenhuma aplicação. Embora a porta esteja acessível, não há serviço para se conectar.

# Tecnologias usadas:
Linguagem Python

