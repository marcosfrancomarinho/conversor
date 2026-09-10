<h1 align="center">📄 Conversor de Arquivos</h1>

<p align="center">
  Aplicação desktop para converter imagens e combinar imagens + PDFs em um único PDF.
</p>

## Sobre o projeto

O **Conversor de Arquivos** é uma aplicação desktop em Python/Tkinter para conversão em lote de imagens e geração de PDF.

O fluxo foi pensado para reduzir cliques: ao selecionar os arquivos, a aplicação já sugere e mostra o destino. Ao clicar em **Converter**, o arquivo é salvo diretamente nesse local. O botão **Alterar...** fica disponível apenas quando você realmente quiser escolher outro destino.

## Funcionalidades

- seleção múltipla de imagens e PDFs;
- remoção e limpeza da lista;
- prevenção de arquivos duplicados na seleção;
- alteração da ordem dos arquivos com **↑** e **↓**;
- conversão de imagens para PNG ou JPEG;
- geração de **um único PDF** misturando imagens e PDFs;
- preservação de todas as páginas dos PDFs existentes;
- suporte a imagens com múltiplos frames, como TIFF;
- destino automático exibido antes da conversão;
- alteração opcional do destino;
- nomes de saída previsíveis, sem números aleatórios;
- prevenção de sobrescrita nos arquivos PNG/JPEG;
- botão para abrir rapidamente a pasta de destino;
- barra de progresso e mensagens de erro mais claras.

## Como funciona o destino automático

Depois que os arquivos são selecionados:

- para **PDF**, o resultado é salvo na mesma pasta do primeiro arquivo, com o nome `<primeiro-arquivo>_convertido.pdf`;
- para **PNG/JPEG**, os resultados vão para uma pasta `convertidos` ao lado do primeiro arquivo.

O destino aparece na interface e pode ser alterado com o botão **Alterar...**.

## PDF com imagens e PDFs misturados

Ao escolher **PDF único**, a ordem mostrada na lista é a ordem usada no documento final.

Exemplo:

```text
1. capa.jpg
2. contrato.pdf
3. comprovante.png
4. anexos.pdf
```

O resultado será um único PDF contendo a imagem `capa.jpg`, todas as páginas de `contrato.pdf`, a imagem `comprovante.png` e todas as páginas de `anexos.pdf`, nessa ordem.

## Tecnologias

- **Python 3.11+**
- **Tkinter/ttk** — interface gráfica;
- **Pillow** — processamento de imagens;
- **pypdf** — leitura, união e escrita de PDFs;
- **PyInstaller** — geração de executável.

## Arquitetura

```text
conversor/
├── main.py                     # composition root
├── requirements.txt
└── src/
    ├── application/
    │   ├── dto/
    │   └── usecase/
    ├── domain/
    │   ├── entities/
    │   ├── gateway/
    │   └── valuesobject/
    ├── infrastructure/
    │   ├── pillow_image_converter.py
    │   ├── pypdf_converter.py
    │   ├── tk_file_selector.py
    │   └── tk_file_save_location_selector.py
    └── presentation/
        └── tk_app.py
```

A interface ficou em `presentation`, os adaptadores externos em `infrastructure`, as regras de aplicação em `application` e os contratos/regras centrais em `domain`.

## Instalação

```bash
git clone https://github.com/marcosfrancomarinho/conversor.git
cd conversor

python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

No Ubuntu/Lubuntu, caso necessário:

```bash
sudo apt update
sudo apt install python3-tk
```

## Execução

```bash
python main.py
```

## Gerando executável

```bash
pyinstaller --onefile --windowed --icon=icone.ico main.py
```

O executável é criado em `dist/`.

## Licença

MIT. Consulte [LICENSE](./LICENSE).

## Autor

Desenvolvido por [Marcos Marinho](https://github.com/marcosfrancomarinho).
