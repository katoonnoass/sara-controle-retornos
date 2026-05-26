# Como Instalar o SARA como Serviço do Windows

Siga estes passos para o SARA rodar em segundo plano **mesmo após desconectar do Remote Desktop**.

---

## Opção 1: Usando NSSM (Recomendado)

NSSM transforma qualquer script em um serviço do Windows que:
- Inicia automaticamente com o Windows
- Continua rodando após desconectar RDP
- Reinicia automaticamente se cair

### Passo 1: Baixar NSSM

1. Acesse: https://nssm.cc/download
2. Baixe a versão **Win64** (ou Win32 se for Windows 32 bits)
3. Extraia o `nssm.exe` para `C:\Windows\System32\` (assim fica disponível no PATH)

### Passo 2: Instalar o Serviço

Abra o **PowerShell como Administrador** e execute:

```powershell
# Crie o serviço
nssm install SARA
```

Uma janela vai abrir. Preencha:

| Campo | Valor |
|-------|-------|
| **Application Path** | `CAMINHO_DO_SEU_PYTHON\python.exe` _(ex: C:\Python312\python.exe)_ |
| **Startup Directory** | `CAMINHO_DO_PROJETO` _(ex: C:\SARA)_ |
| **Arguments** | `-m waitress --host=0.0.0.0 --port=5000 --threads=8 "app:create_app()"` |

Na aba **Details**:
- Display Name: `SARA - Sistema de Retornos`

Na aba **Log On**:
- Marque "Allow service to interact with desktop" (opcional)

Clique em **Install Service**.

### Passo 3: Iniciar o Serviço

```powershell
nssm start SARA
```

### Passo 4: Verificar se está rodando

```powershell
nssm status SARA
```

Ou acesse: http://localhost:5000

### Comandos úteis do NSSM

```powershell
nssm start SARA       # Iniciar
nssm stop SARA        # Parar
nssm restart SARA     # Reiniciar
nssm status SARA      # Ver status
nssm edit SARA        # Editar configurações
nssm remove SARA      # Remover serviço (confirmar)
```

---

## Opção 2: Usando o Agendador de Tarefas (mais simples)

1. Abra o **Agendador de Tarefas** (Taskschd.msc)
2. Clique em **"Criar Tarefa..."** no menu direito
3. **Geral**:
   - Nome: `SARA Web`
   - Marque **"Executar esteja o usuário logado ou não"**
   - Marque **"Executar com privilégios mais altos"**
4. **Gatilhos** → Novo:
   - Iniciar tarefa: **"Ao iniciar"**
5. **Ações** → Novo:
   - Programa: `CAMINHO_DO_SEU_PYTHON\python.exe`
   - Argumentos: `-m waitress --host=0.0.0.0 --port=5000 --threads=8 "app:create_app()"`
   - Iniciar em: `CAMINHO_DO_PROJETO`
6. OK → OK

Para testar:
1. Clique com botão direito na tarefa → **Executar**
2. Acesse http://localhost:5000

---

## Ver logs (para debug)

Se o serviço não iniciar, veja os logs:

```powershell
nssm log SARA
```

Ou redirecione a saída para um arquivo:

```powershell
python -m waitress --host=0.0.0.0 --port=5000 --threads=8 app:create_app() > sara.log 2>&1
```
