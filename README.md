# Maestro

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0473FF?style=for-the-badge&logo=google&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Programa para a execução de macros no computador através de gestos.

## Descrição

O Maestro é um projeto de visão computacional que utiliza OpenCV e MediaPipe para detectar gestos em tempo real e
executar comandos de terminal personalizados, permitindo que você controle seu ambiente de trabalho sem tocar no
teclado.

https://github.com/user-attachments/assets/8f2fb7ba-5632-4cef-ae02-a44030a15b53

## Sobre

Desenvolvi o Maestro como uma ferramenta pessoal para momentos em que o teclado não é a opção mais prática, seja para
controlar o computador à distância ou apenas para tornar o fluxo de trabalho mais dinâmico e divertido usando gestos
simples ao invés de atalhos complexos de teclado.

O projeto possui uma interface gráfica intuitiva feita em **Tkinter**, permitindo configurar comandos específicos para
os gestos do modelo do MediaPipe e ajustar a sensibilidade do modelo para garantir precisão mesmo em ambientes com
iluminação variável ou com muita informação de fundo.

O projeto também possui suporte para configurações de longo prazo a partir do arquivo config.json e suporte para log,
registrando as saídas dos comandos
para facilitar debug e histórico de comandos.

### ✋ Gestos Suportados

| Gesto                     | Identificador | 
|:--------------------------|:--------------| 
| ✊ **Punho Fechado**       | `Closed_Fist` | 
| ✌️ **"Sinal de V"**       | `Victory`     | 
| 👍 **Polegar para cima**  | `Thumb_Up`    | 
| 👎 **Polegar para baixo** | `Thumb_Down`  | 
| ☝️ **Apontar para cima**  | `Pointing_Up` | 
| 🤟 **"Te amo"**           | `ILoveYou`    | 

## Como funciona e Casos de uso:

O Maestro executa comandos diretamente através do shell do sistema via Python. Ele é focado em **automações estilo "fire
and forget"** , sendo ideal para tarefas que não exigem inputs nem retornar valores após o uso.

**Exemplos do comandos que podem ser executados:**

* **Gestão de Apps:** Abrir, minimizar ou fechar programas rapidamente.
* **Controle de Mídia:** Pausar músicas, pular faixas ou alterar o volume.
* **Navegação Web:** Alternar abas, fechar, e atualizar páginas.
* **Automações Customizadas:** Executar scripts com arquivos como `.sh`, `.py` ou `.bat`.
* **Sistema de Arquivos:** Criar, deletar ou manipular arquivos e diretórios.
* **Hotkeys:** Simular combinações de teclas complexas com um único movimento.

## ⚠️ Atenção:

Como o Maestro tem permissão para executar comandos diretamente no shell, o resultado dos comandos executados é de total
responsabilidade do usuário.
Em caso de mal funcionamento ou erros, consulte o arquivo de log na pasta raiz do programa ou consulte o terminal.

> **Nota:** Evite mapear gestos para comandos destrutivos ou sensíveis para evitar acionamento acidental (nada de usar
`sudo rm -rf /*` no computador do amiguinho).

## Começando:

### Pré-requisitos:

* **Python 3.11+ (recomendado)**
* **Linux (Recomendado):** O programa só foi testado no linux e o mesmo extrai mais utilidade dele pois
  possui uma grande variedade de ações que podem ser executadas por terminal.
* **Webcam:** É recomendado o uso de uma webcam ao invés de softwares que usam seu celular como câmera para evitar
  possível incompatibilidade.

## Instalação:

1. **Clonar o projeto:**

* Abra o terminal, navegue até a pasta desejada e execute:

```bash
git clone https://github.com/nemesis-noctis/maestro.git
```

* *Alternativamente, baixe o projeto como ZIP e descompacte-o.*

2. **Ambiente Virtual e Dependências:**

* Crie o ambiente virtual:

```bash
python -m venv .venv
```

* Ative o ambiente:
* **Windows:** `.venv\Scripts\activate`
* **Linux/Mac:** `source .venv/bin/activate`


* Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

## Execução:

> **Nota:** Verifique se a sua câmera não está sendo utilizada por outro aplicativo antes de rodar o programa.

1. Inicie o arquivo principal no terminal usando o comando:

```bash
python main.py
```

2. Na interface do **Tkinter**, realize sua configuração e salve no botão **"Update Config"** e aperte o botão **"Start"
   ** para iniciar o programa. Para para-lo, aperte o botão **"Stop"**.

## Desafios técnicos:

Quero usar este espaço para compartilhar um pouco das decisões que tomei e os desafios que precisei resolver para a
criação deste projeto nesta fase inicial.

### A escolha da Interface

Utilizei o Tkinter para chegar a um estado funcional sem demandar muito tempo configurando a interface.
O Tkinter é rápido e funcional para o propósito pensado e proporciona suporte para diferentes sistemas operacionais.

### Unir a interface, execução de comandos e a detecção de gestos

O maior desafio foi manter os três processos rodando de forma simultânea: a interface gráfica, o modelo de detecção de
gestos e a execução dos comandos.

Para resolver isso, implementei uma arquitetura baseada em Multi-threading e Subprocess:

1. Isolei o OpenCV e o MediaPipe em uma thread separada para que o mainloop do Tkinter não fosse bloqueado. Sem isso, a
   interface não responderia aos cliques enquanto a câmera estivesse ligada e não seria possível encerrar o programa.


2. Como o usuário pode configurar comandos que abrem aplicativos ou scripts longos, usei a biblioteca subprocess com
   Popen.


3. Descobri que, para capturar o retorno do comando (erros ou logs) sem travar o programa, eu não poderia usar o
   .communicate() de forma simples, pois ele espera o fim do processo para retornar os valores.


4. A solução foi criar uma thread para a execução do comando permitindo que quando ele terminasse, possíveis erros ou
   valores de retorno fossem registrados no arquivo de log.

## Contato:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jorgemedeirosqneto/) [![email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:jorgemedeiros.qneto@gmail.com)

## Licença:

Este projeto está licenciado sob a Licença **MIT** - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.
