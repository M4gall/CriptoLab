# CriptoLab

Aplicação didática em Python + Streamlit sobre matrizes inversíveis,
aritmética modular e a Cifra de Hill.

## Requisitos
- Python 3.10 ou superior
- VS Code
- Extensão Python no VS Code (recomendado)

## Como executar no terminal do VS Code

1. Abra a pasta `criptolab` no VS Code.
2. Crie um ambiente virtual:

   Windows:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale a dependência:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Inicie o site:

   ```bash
   streamlit run app.py
   ```

5. O Streamlit abrirá o CriptoLab no navegador. Se não abrir automaticamente,
   copie o endereço local mostrado no terminal (normalmente http://localhost:8501).

## Observação acadêmica
A Cifra de Hill é uma demonstração didática de álgebra linear e aritmética
modular. Ela não deve ser usada para proteger dados reais.
