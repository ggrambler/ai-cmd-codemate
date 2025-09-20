# AI Command Terminal — Python Backend + React Chatbot UI

A self-contained virtual terminal that mimics a Unix-like shell over a **tree-based, in-memory filesystem**.
Safe by design (no real disk access). React “chat” UI with history and TAB autocompletion.

---

## Features

* **Virtual FS** (per session, in memory): `ls`, `cd`, `pwd`, `mkdir -p`, `rm -r`, `touch`, `cat`, `echo > / >>`, `mv`, `cp`
* **System info** (host read-only): `ps`, `top`, `sys`
* **Command chaining**: `cmd1 && cmd2` (up to 2 commands per line)
* **Helpful errors**: invalid command/path errors shown as text
* **Frontend UX**: chatbot-style UI, ↑/↓ history, **TAB** autocomplete (`/complete`)
* **Session support**: resume by passing a `session_id` (URL, localStorage, or manual paste)

> The filesystem is purely virtual; **no writes to your real disk**.

---

## Project Structure

```
ai-cmd-terminal/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ README.md   (optional)
└─ frontend/
├─ src/
│  ├─ App.jsx
│  ├─ TerminalChat.jsx
│  ├─ api.js
│  └─ styles.css
├─ index.html
├─ package.json
└─ README.md    (optional)
```

---

## Requirements

* Python **3.10+**
* Node **18+** (or recent LTS)
* Windows **cmd** (or PowerShell/Git Bash) — examples below use **cmd** with a `.venv`

---

## Backend Setup (FastAPI)

### 1) Create & activate venv (Windows cmd)

```
cd backend
python -m venv .venv
..venv\Scripts\activate
```

### 2) Install dependencies

If you have a `requirements.txt`:
```
pip install -r requirements.txt
```

Suggested `requirements.txt`:

```
fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.9.2
psutil==6.0.0
python-multipart==0.0.9
```

### 3) Run the API

```
python -m uvicorn app\:app --reload --host 127.0.0.1 --port 8000
```

Open:

* Swagger docs: `http://127.0.0.1:8000/docs`
* Health (if you added `/`): `http://127.0.0.1:8000/`

> If you see “uvicorn is not recognized”, the `python -m uvicorn ...` form above **always** works inside the venv.

---

## Frontend Setup (React + Vite)

### 1) Install

```
cd frontend
npm i
```

### 2) Run dev server

If your backend runs at `http://127.0.0.1:8000`, either set an env var or rely on the default in `src/api.js`.

* Simple (uses default `http://localhost:8000`):

```
npm run dev
```

* Explicit base (macOS/Linux/Git Bash):

```
VITE\_API\_BASE=[http://127.0.0.1:8000](http://127.0.0.1:8000) npm run dev
```
Open: `http://127.0.0.1:5173`

---

## Using the App (Sample Commands)

```
pwd
ls
mkdir -p home/user/projects/demo
cd /home/user/projects/demo
touch hello.txt
echo "Hello, World!" > hello.txt
cat hello.txt
cp hello.txt hello.copy
ls
mv hello.copy notes.txt
rm notes.txt
history
ps
top
sys
```

**Redirection**

* Overwrite: `echo "text" > file.txt`
* Append: `echo "more" >> file.txt`

**Chaining**

* `mkdir test && cd test`

---

## Commands Supported

| Command            | Description                                       |
| ------------------ | ------------------------------------------------- |
| `pwd`              | Print current directory                           |
| `ls [path]`        | List contents                                     |
| `cd [path]`        | Change directory (`/`, relative, `.`, `..`)       |
| `mkdir [-p] <dir>` | Create directory (`-p` to create parents)         |
| `rm [-r] <path>`   | Remove file; remove directory tree with `-r`      |
| `touch <file...>`  | Create empty file(s) if missing                   |
| `cat <file...>`    | Output file contents                              |
| `echo <text>`      | Print text (combine with `>`/`>>` to write files) |
| `mv <src> <dst>`   | Move/rename                                       |
| `cp <src> <dst>`   | Copy to dir or new name                           |
| `history`          | Show per-session command history                  |
| `ps`               | List processes (limited view)                     |
| `top`              | One-shot CPU/memory snapshot                      |
| `sys`              | Uptime, CPU count, disk usage                     |

---

## API Reference

### Create Session

**POST** `/session` → returns:
```
{ "session\_id": "UUID" }
```

### Get State

**GET** `/state?session_id=<SID>` → returns:
```
{ "ok": true, "output": "", "cwd": "/...", "session\_id": "<SID>" }
```

### Execute Command

**POST** `/execute`
Body:
```
{ "session\_id": "<SID>", "command": "ls /home" }
```

Response:
```
{ "ok": true, "output": "user  tmp  var", "cwd": "/home", "session\_id": "<SID>" }
```

### Autocomplete

**GET** `/complete?prefix=<TYPED>&session_id=<SID>` → returns:
```
{ "items": \["ls", "ls /home", ...] }
```

---

## Resuming a Session

Pass `session_id` with every request.

* **State**:
  `GET /state?session_id=<SID>`
* **Execute**:
  `POST /execute` with body containing `session_id`

Frontend tips:

* Store `session_id` in `localStorage`
* Accept `?sid=<SID>` in the URL to auto-resume
* Optional small UI to paste a previous `session_id`

> Note: Sessions are in-memory. After a server restart, old sessions are gone unless you add persistence (e.g., Redis). You can either recreate on missing ID (current behavior) or return `404` (strict mode).

---

## Troubleshooting

* **“uvicorn is not recognized”**
  Use: `python -m uvicorn app:app --reload --port 8000`

* **Port already in use**
  Change port: `--port 8010` and set `VITE_API_BASE=http://127.0.0.1:8010`.

* **CORS blocked**
  Dev CORS is open (`*`). In prod, restrict `allow_origins` to your frontend origin.

* **Module not found**
  Ensure venv is activated and `pip install -r requirements.txt` ran without errors.

* **Session not resuming**
  Verify you’re sending the same `session_id`. If the server restarted, the session was lost (unless persisted).

---

## Security Notes

* Only the **virtual FS** is mutated; **no real filesystem** access.
* No shelling out; commands are interpreted and executed by the Python VFS.
* CORS is wide open in dev; **lock it down for production**.

---

## Roadmap (optional)

* Persistent sessions (Redis/SQLite) + cleanup/TTL
* Rich `ls -l`, `tree`, file sizes/quotas
* WebSocket streaming for long outputs
* Auth/session ownership controls
