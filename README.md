# 📚 Sistema de Ponto Acadêmico

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Sistema web desenvolvido em **Django** para controle de entrada e saída de alunos dentro da instituição de ensino.

## 🎯 Visão Geral

O sistema permite que cada aluno registre seus horários de presença por meio de um mecanismo simples e confiável de **batida de ponto**. Funciona exclusivamente em **rede local (LAN)**, garantindo que os registros só possam ser feitos dentro da faculdade.

## 🛠️ Tecnologias

- **Backend**: Django (Python)
- **Autenticação**: Django Authentication System
- **Rede**: LAN (Local Area Network)

## 📋 Funcionalidades

### Para Alunos
- ✅ Registro de entrada
- ✅ Registro de saída  
- 📈 Visualização do histórico pessoal de registros

### Para Professores e Administradores
- 📊 Visualização de registros de todos os alunos
- 👨‍🎓 Consulta do histórico geral

## 🏗️ Estrutura Técnica

### Modelo de Dados - `RegistroPonto`
- **Aluno** (`ForeignKey` para User) → Usuário responsável pelo registro
- **Data e Hora** (`DateTimeField`) → Momento exato, preenchido automaticamente com `timezone.now`
- **Tipo de Registro** (`CharField`) → "Entrada" ou "Saída"

**Ordenação**: Mais recentes primeiro (`ordering = ["-data_hora"]`)

### Funcionamento dos Registros
- Cada marcação cria um **novo registro** imutável
- Horário baseado no servidor (não no dispositivo do aluno)
- Formato de exibição: `dd/mm/yyyy hh:mm`

Exemplo:
```
João da Silva – Entrada em 21/08/2025 08:02
João da Silva – Saída em 21/08/2025 11:37
```

## 📊 Regras de Negócio

- ✅ Somente alunos autenticados podem registrar ponto
- ⏰ Ponto registrado com horário oficial do servidor
- 🔄 Cálculo de horas baseado em pares Entrada → Saída consecutivos
- 🚫 Entrada sem saída não permite cálculo de tempo
- 📅 Múltiplos registros no mesmo dia = ciclos independentes
- 👀 Professores e administradores visualizam todos os registros

## 🔐 Segurança

- **Autenticação**: Login obrigatório via Django Auth
- **Timestamp**: Horário do servidor (evita adulteração)
- **Imutabilidade**: Registros não podem ser editados
- **Integridade**: Dados no banco relacional com migrations

## 📱 Interface do Usuário

### Aluno
- Botão para registrar entrada
- Botão para registrar saída
- Histórico dos pontos já batidos

### Professor/Administrador
- Dashboard com visão geral de todos os alunos
- Histórico completo dos registros

## 🚀 Instalação

```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]

# Ambiente virtual
python -m venv venv
source venv/bin/activate

# Dependências
pip install -r requiriments.txt

# Migrações
python manage.py makemigrations
python manage.py migrate

# Superusuário
python manage.py createsuperuser

# Servidor (rede local)
python manage.py runserver 0.0.0.0:8000
```

## 📈 Cálculo de Horas

O sistema calcula automaticamente as horas de permanência baseado em pares de registros:

```
Entrada: 08:02
Saída: 11:37
Tempo: 3h35min
```

- ❌ Entrada sem saída = sem cálculo
- ✅ Múltiplas entradas/saídas = ciclos independentes

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

**Sistema de Ponto Acadêmico** - Controle de presença para instituições de ensino