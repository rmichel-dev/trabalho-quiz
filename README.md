# 📘 Trabalho Quiz - Django (SENAC 2026)

Repositório da **Aula 09** da disciplina no SENAC - Programação com Python (2026), com foco em introdução ao desenvolvimento web utilizando **Django**.

```bash
git clone git@github.com:rmichel-dev/aula-09.git
```

---

## 🚀 Objetivo

Este projeto foi desenvolvido em aula com o objetivo de apresentar os fundamentos do ecossistema Django, incluindo:

- Criação de ambiente virtual
- Estrutura de projetos Django
- Criação de apps
- Execução do servidor local

---

## 💻 Sistema Operacional

Este guia foi preparado para **Windows (PowerShell)**.

---

## ⚙️ Pré-requisitos

Antes de iniciar, verifique se o Python está instalado:

```powershell
python --version
```

Caso encontre restrições no PowerShell, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

> ⚠️ O Windows Defender pode bloquear scripts dependendo da configuração de segurança ("Controle Inteligente de Aplicativos").

---

## 🧪 1. Criar Ambiente Virtual

```powershell
python -m venv venv
```

Será criada a pasta `venv`, isolando as dependências do projeto.

---

## ▶️ 2. Ativar Ambiente Virtual

No **PowerShell**:

```powershell
.\venv\Scripts\activate
```

Se ativado corretamente, aparecerá:

```
(venv)
```

### ❗ Possíveis problemas

Se houver erro de execução de script:

- Use o **Prompt de Comando (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
- Ou ajuste a política de execução (passo anterior)

---

## 📦 3. Instalar pacotes

```powershell
pip install django
pip install reportlab
```
---

## 🔄 Gerar Migrações

```powershell
python manage.py makemigrations
```

## 🧱 Aplicar Migrações

```powershell
python manage.py migrate
```

## Aplicar dados
```
python manage.py loaddata questoes_exemplo questoes_prova
```