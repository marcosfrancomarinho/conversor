<h1 align="center">📄 Conversor PDF & Imagens</h1>

<p align="center">
  Aplicação desktop em Python para converter imagens e combinar imagens + PDFs em um único documento.
</p>

## Sobre o projeto

O **Conversor PDF & Imagens** foi pensado para deixar conversões do dia a dia rápidas, principalmente quando vários documentos precisam virar um único PDF.

O fluxo evita etapas desnecessárias: você adiciona os documentos, confere a ordem e o local de saída e clica em **Converter**. O destino é sugerido automaticamente e só precisa ser alterado quando você quiser.

## Funcionalidades

- seleção múltipla de imagens e PDFs;
- suporte a imagens com extensões não convencionais, como `.001`, `.002`, `.010` etc., desde que o conteúdo seja uma imagem válida reconhecida pelo Pillow;
- janela aberta maximizada para manter as ações principais visíveis;
- tabela com ordem, nome, tipo e tamanho dos arquivos;
- prevenção de arquivos duplicados;
- reordenação com **Subir** e **Descer**;
- remoção individual/múltipla e limpeza da lista;
- conversão de imagens para PNG ou JPEG;
- geração de **um único PDF** misturando imagens e PDFs;
- preservação de todas as páginas dos PDFs existentes;
- suporte a imagens multipágina, como TIFF, quando a saída é PDF;
- correção automática da orientação EXIF de imagens;
- destino automático exibido antes da conversão;
- botão **Alterar...** para escolher outro destino;
- botão **Usar automático** para voltar ao caminho sugerido;
- prevenção de sobrescrita acidental;
- proteção para impedir que o PDF final substitua um PDF usado como entrada;
- botão para abrir a pasta de destino;
- botão para abrir o resultado após a conversão;
- barra de progresso e status da operação;
- bloqueio dos controles durante a conversão para evitar clique duplo;
- validação visual quando PDFs são usados com saída PNG/JPEG;
- nomes previsíveis para arquivos convertidos;
- JPEG salvo com qualidade alta e PNG otimizado.

## Arquivos com extensão numérica

Alguns sistemas salvam imagens com nomes como:

```text
foto.001
foto.002
pagina.010
```

O conversor não depende da extensão para abrir esses arquivos como imagem. Eles podem ser selecionados normalmente e o Pillow identifica o formato pelo conteúdo real do arquivo.

Assim, uma imagem JPEG chamada `foto.002`, por exemplo, pode ser convertida para PNG, JPEG ou incluída em um PDF normalmente.

## Fluxo de uso

1. Clique em **Adicionar arquivos**.
2. Confira a ordem dos documentos.
3. Escolha **PDF único**, **PNG** ou **JPEG**.
4. Confira o destino mostrado na interface.
5. Clique em **Converter**.

Para PDF, não é necessário escolher pasta e nome a cada conversão.

### Destino automático

Para **PDF**, o resultado é sugerido na mesma pasta do primeiro documento:

```text
contrato.pdf
→ contrato_convertido.pdf
```

Se o arquivo já existir:

```text
contrato_convertido_2.pdf
contrato_convertido_3.pdf
...
```

Para **PNG/JPEG**, os resultados são enviados para uma pasta:

```text
convertidos/
```

## PDF com imagens e PDFs misturados

A ordem exibida na tabela é a ordem usada no documento final.

```text
1. capa.jpg
2. contrato.pdf
3. comprovante.001
4. anexos.pdf
```

O PDF final terá:

```text
capa.jpg
+ todas as páginas de contrato.pdf
+ comprovante.001 (se o conteúdo for uma imagem válida)
+ todas as páginas de anexos.pdf
```

Os PDFs existentes são combinados com `pypdf`, sem transformar suas páginas em imagens.

## Atalhos

| Atalho | Ação |
|---|---|
| `Ctrl + O` | Adicionar arquivos |
| `Delete` | Remover selecionados |
| `Ctrl + ↑` | Subir selecionados |
| `Ctrl + ↓` | Descer selecionados |
| `Ctrl + Enter` | Converter |

## Tecnologias

- **Python 3.11+**
- **Tkinter/ttk** — interface gráfica
- **Pillow** — processamento e identificação de imagens
- **pypdf** — leitura, união e escrita de PDFs
- **PyInstaller** — geração de executável
- **unittest** — testes automatizados
- **GitHub Actions** — execução automática dos testes

## Arquitetura

```text
conversor/
├── main.py
├── requirements.txt
├── tests/
│   ├── test_file.py
│   ├── test_image_converter.py
│   └── test_pdf_converter.py
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
        ├── theme.py
        └── tk_app.py
```

Responsabilidades:

- `domain`: regras e contratos centrais;
- `application`: casos de uso e DTOs;
- `infrastructure`: Pillow, pypdf, sistema de arquivos e diálogos Tkinter;
- `presentation`: interface e tema visual;
- `main.py`: composition root e inicialização da aplicação.

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

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes também são executados automaticamente no GitHub Actions para Python 3.11, 3.12 e 3.13.

## Gerando executável

```bash
pyinstaller --onefile --windowed --icon=icone.ico main.py
```

O executável é criado em `dist/`.

## Licença

MIT. Consulte [LICENSE](./LICENSE).

## Autor

Desenvolvido por [Marcos Marinho](https://github.com/marcosfrancomarinho).
