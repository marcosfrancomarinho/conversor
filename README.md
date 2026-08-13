<h1 align="center">🖼️ Conversor de Imagens</h1>

<p align="center">
  Aplicação desktop para converter imagens e gerar arquivos PDF de forma simples e rápida.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Tkinter-GUI-2C5E8A?style=flat-square" alt="Tkinter">
  <img src="https://img.shields.io/badge/Pillow-12-8A2BE2?style=flat-square" alt="Pillow">
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/licença-MIT-green?style=flat-square" alt="Licença MIT">
  </a>
</p>

## Sobre o projeto

O **Conversor de Imagens** é uma aplicação desktop desenvolvida em Python que permite selecionar vários arquivos e convertê-los para **PNG** ou **JPEG**. Também é possível reunir todas as imagens selecionadas em um único arquivo **PDF**.

A interface foi construída com Tkinter e oferece seleção múltipla, remoção de itens, escolha do destino e acompanhamento do processamento por uma barra de progresso.

## Funcionalidades

- Seleção de múltiplas imagens;
- visualização dos arquivos selecionados;
- remoção individual ou múltipla da lista;
- conversão em lote para PNG;
- conversão em lote para JPEG;
- união das imagens em um único PDF;
- escolha da pasta ou arquivo de destino;
- barra de progresso;
- mensagens de validação, erro e conclusão.

## Tecnologias

- **Python** — linguagem principal;
- **Tkinter/ttk** — interface gráfica;
- **Pillow** — leitura e conversão de imagens;
- **PyInstaller** — geração de executável;
- **Docker** — configuração alternativa do ambiente.

## Arquitetura

O código separa as regras da aplicação dos detalhes da interface e do sistema de arquivos:

```text
conversor/
├── main.py
├── requirements.txt
├── icone.ico
└── src/
    ├── application/      # DTOs e casos de uso
    ├── domain/           # Contratos e regras centrais
    └── infrastrucure/    # Tkinter, seleção e conversão de arquivos
```

Essa divisão facilita manutenção, testes e substituição das implementações externas.

## Pré-requisitos

- Python 3.11 ou superior;
- suporte ao Tkinter no sistema operacional.

No Ubuntu e derivados, instale o Tkinter caso ainda não esteja disponível:

```bash
sudo apt update
sudo apt install python3-tk
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/marcosfrancomarinho/conversor.git
cd conversor
```

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado:

```bash
python main.py
```

Na aplicação:

1. Clique em **Selecionar Arquivos**;
2. escolha uma ou mais imagens;
3. selecione PNG, JPEG ou PDF;
4. clique em **Converter**;
5. escolha o destino dos arquivos.

## Gerando um executável

O projeto inclui PyInstaller nas dependências. Para gerar uma versão distribuível:

```bash
pyinstaller --onefile --windowed --icon=icone.ico main.py
```

O arquivo gerado ficará no diretório `dist/`. O executável deve ser criado no mesmo sistema operacional em que será utilizado.

## Licença

Distribuído sob a licença MIT. Consulte [LICENSE](./LICENSE).

## Autor

Desenvolvido por [Marcos Marinho](https://github.com/marcosfrancomarinho).
