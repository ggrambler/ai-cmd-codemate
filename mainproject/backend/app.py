# from __future__ import annotations
# """
# This module imports the 'annotations' feature from Python's __future__ module.

# The __future__ module allows the use of features from future Python versions in the current interpreter.
# By importing 'annotations', this code enables postponed evaluation of type annotations, which means
# annotations are stored as string expressions and evaluated only when needed. This is useful for
# forward references and can improve performance and compatibility with newer Python versions.
# """
# from typing import Dict,List, Optional, Tuple
# """
# The `typing` module provides type hints for Python code. Common generics used here:

# - Dict[K, V]: a mapping from keys of type K to values of type V (e.g., Dict[str, int]).
# - List[T]: a sequence of items of type T (e.g., List[str]).
# - Optional[T]: either a value of type T or None (e.g., Optional[str]).
# - Tuple[T1, T2, ...]: a fixed-length sequence with specified types (e.g., Tuple[int, str]).

# Type hints help with editor autocompletion, static analysis (mypy, Pyright), and
# documentation. They do not change runtime behavior by themselves, but when used
# with tools they make code safer and easier to understand.

# Example:

# 	user: Dict[str, Optional[int]] = {"age": None, "id": 123}

# """
# from fastapi import FastAPI, HTTPException
# """
# FastAPI: this is the application class you instantiate to create your web API server (app = FastAPI()). It wires routing, request parsing, validation (via Pydantic), dependency injection, OpenAPI generation, and the ASGI interface used by servers (uvicorn). Without it you don't have the app object to register routes or run the API.
# HTTPException: a helper exception used to return HTTP error responses from inside path operation functions. Raise HTTPException(status_code=404, detail="Not found") to immediately return a formatted JSON error with the status code and detail. It ensures proper headers and body format and integrates with FastAPI's exception handling.
# When to use each

# Use FastAPI when you need to create the app, define routes with decorators, and access app-level configuration (middleware, startup/shutdown events).
# Use HTTPException inside route handlers when you need to abort processing and send a specific HTTP error to the client (authorization failure, resource not found, validation beyond pydantic, etc.)."""
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# """
# CORSMiddleware:

# Purpose: Enables Cross-Origin Resource Sharing (CORS) rules for your FastAPI app so browser clients from other origins (different domain/port/protocol) can make requests safely.
# Why you need it: Modern browsers block cross-origin requests by default. If your frontend (e.g., running on localhost:5173) calls your backend (e.g., localhost:8000), the browser enforces CORS. CORSMiddleware sets the appropriate Access-Control-Allow-* headers so the browser allows the request.
# Typical usage:
# Configure allowed origins, methods, headers.
# Mount middleware on the FastAPI app before defining routes.
# Example:
# app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=[""], allow_headers=[""])
# Best practice: Be restrictive in production—specify exact origins and only needed methods/headers instead of allowing "*".
# BaseModel (from Pydantic):

# Purpose: Declarative data models used by FastAPI for request parsing, validation, and automatic OpenAPI schema generation.
# Why you need it: When you declare request bodies or response models with Pydantic models, FastAPI automatically:
# Parses JSON into model instances,
# Validates types and required fields,
# Produces clear error responses for invalid input,
# Documents the model in the OpenAPI docs (Swagger UI / ReDoc).
# """

# import psutil
# import httpx
# import shlex
# import time
# import uuid
# """psutil

# Purpose: Cross-platform library for retrieving system and process information (CPU, memory, disk, network, process list, system uptime).
# Common uses: Monitor resource usage, get process CPU/memory, check system load, implement health checks.
# Short example:
# cpu = psutil.cpu_percent(interval=1)
# mem = psutil.virtual_memory().percent
# Cautions: Accessing many metrics frequently can be expensive; avoid tight polling loops. Some calls require elevated permissions to get info about other users' processes.
# httpx

# Purpose: Modern HTTP client for Python with sync and async APIs; alternative to requests, supports HTTP/2, timeouts, streaming, and async.
# Common uses: Call external APIs, perform background requests, fetch resources.
# Short example (async):
# async with httpx.AsyncClient() as client:\n r = await client.get("https://api.example.com\")\n data = r.json()
# Cautions: Use timeouts and exception handling; prefer AsyncClient for async code; close clients or use context managers to avoid connection leaks.
# shlex

# Purpose: Utilities for parsing and joining shell-like syntaxes safely (split a command string into argv list and quote arguments).
# Common uses: Safely split user-provided command strings before passing to subprocess.run when shell=False; escape arguments.
# Short example:
# args = shlex.split("ls -la /some/path")\n subprocess.run(args)
# Cautions: Do not use shlex to sanitize untrusted input for shell=True; prefer passing a list to subprocess with shell=False.

# time

# Purpose: Standard library for time-related functions: sleep, measuring time, formatting timestamps.
# Common uses: Sleep delays (time.sleep), measure duration (time.time or time.perf_counter), timestamps.
# Short example:
# start = time.perf_counter(); ...; elapsed = time.perf_counter() - start
# Cautions: time.sleep blocks the current thread (use asyncio.sleep in async code).
# uuid

# Purpose: Generate UUIDs (unique identifiers) — useful for request IDs, resource IDs, tokens where global uniqueness is desired.
# Common uses: uuid.uuid4() for random UUIDs; uuid.uuid1() includes MAC/time.
# Short example:
# request_id = str(uuid.uuid4())
# Cautions: Don't use uuid1 for privacy-sensitive contexts (it embeds MAC/time); for secure tokens, consider random + signing.
# """

# # for the virtual file system , since i m not gonna allow a random app to play with my system files.
# # i m gonna allow the creation of a file system, mabe a simple tree like data structure. 
# # so this is my  VIRTUAL IN-MEM FILE SYSTEM

# # BTW FOR EVERYONE WHO HATES DOING OOPS IN PYTHON, HERE IS OOPS IN PYTHON: 😊

# class FileNode:
#     def __init__(self,name: str,is_dir: bool):
#         self.name = name
#         self.is_dir = is_dir
#         self.children : Dict [str, FileNode] = {} if is_dir else {}
#         self.content : str = "" if not is_dir else ""

#     def clone(self) -> "FileNode" :
#         node = FileNode(self.name,self.is_dir)
#         node.content = self.content
#         for k,v in self.children.items():
#             node.children[k] = v.clone()
#         return node

# class VFS:
#     def __init__(self):
#         self.root = FileNode("/", True)

#     @staticmethod
#     def _parts(path: str) -> List[str]:
#         if path=="/":
#             return []
#         return [p for p in path.split("/") if p and p!="."]

#     def _resolve(self, cwd:  str, path: str) -> Tuple [FileNode, str, List[str]]:
#         ''' Returns parent node, last_name, walked parts for a path , without creating '''
#         if not path:
#             path = "."
#         abs_parts: List[str] = []
#         if path.startswith('/'):
#             base_parts = []
#         else:
#             base_parts = self._parts(cwd)
        
#         for part in self._parts(path):
#             if part == "..":
#                 if base_parts:
#                     base_parts.pop()
#             else:
#                 base_parts.append(part)
        
#         parent = self.root
#         for p in base_parts[:-1]:
#             if p not in parent.children or not parent.children[p].is_dir:
#                 raise FileNotFoundError(f"No such directory: /{'/'.join(base_parts[:-1])}")
#             parent = parent.children[p]

#         last = base_parts[-1] if base_parts else ""
#         return parent, last, base_parts

#     def pwd_normalize(self, cwd: str, path: Optional[str] = None) -> str :
#         if not path or path == ".":
#             return cwd
#         if path.startswith("/"):
#             parts = []
#         else:
#             parts = self._parts(cwd)
        
#         for part in self._parts(path):
#             if part=="..":
#                 if parts:
#                     part.pop()
#             else:
#                 parts.append(part)
        
#         return "/" + "/".join(parts) if parts else "/"

#     def ls(self, cwd: str, path: Optional[str] = None) -> List[str]:

#         target_path = self.pwd_normalize(cwd, path)
#         node = self.get_node(target_path)
#         if not node.is_dir:
#             return [node.name]
#         return sorted(node.children.keys())

#     def get_node(self, path:str) -> FileNode:
#         if path=="/":
#             return self.root

#         parts = self._parts(path)
#         node = self.root

#         for p in parts:
#             if p not in node.children:
#                 raise FileNotFoundError(f"No such file or directory: {path}")
#             node = node.children[p]
#         return node

#     def mkdir(self, cwd: str, paths: List[str], parents: bool = False) -> None:
#         for raw in paths:
#             norm = self.pwd_normalize(cwd, raw)
#             parent_path = "/"
#             if norm != '/':
#                 parent_path = "/" + "/".join(self._parts(norm)[:-1]) if len(self._parts(norm))>1 else "/"
#             name = self._parts(norm)[:-1] if self._parts(norm) else ""

#             if not name:
#                 raise FileExistsError("cannot create directory '/' ")
#             if parents:
#                 cur = self.root
#                 parts = self._parts(norm)
#                 for i,p in enumerate(parts):
#                     if p not in cur.children:
#                         cur.children[p] = FileNode(p, True)
#                     elif not cur.children[p].is_dir:
#                         raise NotADirectoryError(f"Path component is file : /{'/'.join(parts[:i+1])}")
#                     cur = cur.children[p]
#             else:
#                 par = self.get_node(parent_path)
#                 if not par.is_dir:
#                     raise NotADirectoryError(f"Not a directory: {parent_path}")
#                 if name in par.children:
#                     raise FileExistsError(f"File exists: {norm}")

#                 par.children[name] = FileNode(name, True)
        
#     def rm(self, cwd: str, paths: List[str], recursive: bool = False) -> None:

#         for raw in paths:
#             norm  = self.pwd_normalize(cwd, raw)
#             if norm =="/":
#                 raise PermissionError("Cannot remove '/' ")
#             parts = self._parts(norm)
#             parent_path = "/" if len(parts)==1 else "/" + '/'.join(parts[:-1])
#             name = parts[-1]
#             par = self.get_node(parent_path)
#             if name not in par.children:
#                 raise FileNotFoundError(f"No such File or Directory: {norm}")
#             node = par.children[name]

#             if node.is_dir and not recursive and node.children:
#                 raise IsADirectoryError("Directory not empyty (use rm -r)")

#             del par.children[name]
    
#     def touch(self, cwd:str, paths: List[str])-> None:
#         for raw in paths:
#             norm = self.pwd_normalize(cwd, raw)
#             parts = self._parts(norm)
#             parent_path = "/" if len(parts)==1 else "/"+"/".join(parts[:-1])
#             par = self.get_node(parent_path)
#             if not par.is_dir:
#                 raise NotADirectoryError(f"Not a Directory: {parent_path}")
#             name = parts[-1]
#             if name not in par.children:
#                 par.children[name] = FileNode(name, False)
#     def write(self, cwd:str, path: str, data: str, append_bool : bool= False) -> None:
#         norm = self.pwd_normalize(cwd, path)
#         parts = self._parts(norm)
#         parent_path = "/" if len(parts)==1 else "/"+"/".join(parts[:-1])
#         par = self.get_node(parent_path)
#         if not par.is_dir:
#             raise NotADirectoryError(f"Not a Directory: f{parent_path}")
        
#         name = parts[-1]
#         if name not in par.children:
#             par.children[name] = FileNode(name, False)
#         node = par.children[name]
#         if node.is_dir:
#             raise IsADirectoryError(f"Is a Director: {norm}")
#         node.content = node.content + data if append_bool else data

# # these are the sessiosn i have
# # so these are the sessiosn code to be honest. 
                
# class Session:
#     def __init__(self):
#         self.fs = VFS()
#         self.cwd = "/"
#         self.history : List[str] = {}

# sessions: Dict[str, Session] = {}
# S_CMDS = ["help", "pwd", "ls", "cd", "mkdir", "rm", "touch" ,"echo", "history", "ps", "top", "sys"]

# # cat, mv,cp, aicmd not implemented so .... idk do it urself ig.


# # idk what these rae supposed to be response models for fastAPI

# class ExecuteIn(BaseModel):
#     session_id : Optional[str] = None
#     Command: str

# class ExecuteOut(BaseModel):
#     ok : bool
#     output: str
#     cwd: str
#     session_id: str

# class SessionOut(BaseModel):
#     session_id: str

# #  Ok this part is the command engine. IDK wtf that means . this is AI brain tbh

# def ensure_session(session_id: Optional[str]) -> Tuple[str, Session]:

#     if session_id and session_id in sessions:
#         return session_id, sessions[session_id]

#     sid = session_id or str(uuid.uuid4())
#     sessions[sid] = Session()

#     s = sessions[sid]
#     s.fs.mkdir("/", ["home"], parents=True)
#     s.fs.mkdir("/", ["tmp"], parents=True)
#     s.fs.mkdir("/", ["var"], parents=True)
#     s.fs.mkdir("/", ["usr"], parents=True)
#     s.fs.mkdir("/", ["home/user"], parents=True)
#     s.fs.touch("/", ["home/user/readme.txt"], parents=False)
#     s.fs.write("/", "home/user/readme.txt", "Welcome to the virtual terminal !\n")

#     return sid,s


# def run_command(s: Session, raw: str):
#     raw = raw.strip()
#     if not raw:
#         return ""
    
#     parts = [p.strip() for p in raw.split("&&") if p.strip()]
#     outputs = []

#     for part in parts:
#         outputs.append(run_single(s, part))
#     return "\n".join([o for o in outputs if o])

# def run_single(s: Session, raw: str) -> str:
#     import shlex
#     tokens = shlex.split(raw.strip())
#     if not tokens:
#         return ""

#     cmd = tokens[0]
#     if cmd not in S_CMDS:
#         raise ValueError(f"Unsupported command: {cmd}")

#     # Detect output redirection: '>' or '>>'
#     redirect = None  # (mode, path) where mode in {">", ">>"}
#     if ">>" in tokens:
#         i = tokens.index(">>")
#         redirect = (">>", tokens[i + 1] if i + 1 < len(tokens) else None)
#         tokens = tokens[:i]
#     elif ">" in tokens:
#         i = tokens.index(">")
#         redirect = (">", tokens[i + 1] if i + 1 < len(tokens) else None)
#         tokens = tokens[:i]

#     out = ""

#     try:
#         if cmd == "help":
#             out = (
#                 "Commands: " + ", ".join(S_CMDS) + "\n"
#                 "Usage examples:\n"
#                 "  pwd\n"
#                 "  ls\n"
#                 "  ls /home\n"
#                 "  cd /home/user\n"
#                 "  mkdir -p projects/demo\n"
#                 "  touch notes.txt\n"
#                 "  echo \"hello\" > notes.txt\n"
#                 "  cat notes.txt\n"
#                 "  mv notes.txt notes.old\n"
#                 "  cp notes.old copy.txt\n"
#                 "  rm copy.txt\n"
#                 "  rm -r projects\n"
#                 "  history\n"
#                 "  ps | top | sys (system info)\n"
#             )

#         elif cmd == "pwd":
#             out = s.cwd

#         elif cmd == "ls":
#             path = tokens[1] if len(tokens) > 1 else None
#             out = "  ".join(s.fs.ls(s.cwd, path))

#         elif cmd == "cd":
#             if len(tokens) == 1:
#                 s.cwd = "/"
#             else:
#                 target = s.fs.pwd_normalize(s.cwd, tokens[1])
#                 node = s.fs.get_node(target)
#                 if not node.is_dir:
#                     raise NotADirectoryError(f"Not a directory: {target}")
#                 s.cwd = target
#             out = ""

#         elif cmd == "mkdir":
#             parents = False
#             paths: List[str] = []
#             for t in tokens[1:]:
#                 if t == "-p":
#                     parents = True
#                 else:
#                     paths.append(t)
#             if not paths:
#                 raise ValueError("mkdir: missing operand")
#             s.fs.mkdir(s.cwd, paths, parents=parents)
#             out = ""

#         elif cmd == "rm":
#             recursive = False
#             paths: List[str] = []
#             for t in tokens[1:]:
#                 if t == "-r":
#                     recursive = True
#                 else:
#                     paths.append(t)
#             if not paths:
#                 raise ValueError("rm: missing operand")
#             s.fs.rm(s.cwd, paths, recursive=recursive)
#             out = ""

#         elif cmd == "touch":
#             if len(tokens) < 2:
#                 raise ValueError("touch: missing file operand")
#             s.fs.touch(s.cwd, tokens[1:])
#             out = ""

#         elif cmd == "cat":
#             if len(tokens) < 2:
#                 raise ValueError("cat: missing file operand")
#             out = s.fs.cat(s.cwd, tokens[1:])

#         elif cmd == "echo":
#             # tokens after 'echo' are the text (quotes already handled by shlex)
#             out = " ".join(tokens[1:])

#         elif cmd == "mv":
#             if len(tokens) != 3:
#                 raise ValueError("mv: usage: mv <src> <dst>")
#             s.fs.mv(s.cwd, tokens[1], tokens[2])
#             out = ""

#         elif cmd == "cp":
#             if len(tokens) != 3:
#                 raise ValueError("cp: usage: cp <src> <dst>")
#             s.fs.cp(s.cwd, tokens[1], tokens[2])
#             out = ""

#         elif cmd == "history":
#             out = "\n".join(f"{i+1}  {c}" for i, c in enumerate(s.history))

#         elif cmd == "ps":
#             procs = []
#             for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
#                 try:
#                     procs.append(
#                         f"{p.info['pid']:>6} {p.info['name'][:22]:<22} "
#                         f"{p.info['cpu_percent']:>5.1f}%  {p.info['memory_info'].rss//1024//1024:>4}MB"
#                     )
#                 except Exception:
#                     continue
#             out = "PID    NAME                   CPU%  RSS\n" + "\n".join(procs[:50])

#         elif cmd == "top":
#             out = (
#                 f"CPU: {psutil.cpu_percent(interval=0.1)}%\n"
#                 f"Mem: {psutil.virtual_memory().percent}% used\n"
#                 f"Swap: {psutil.swap_memory().percent}% used\n"
#             )

#         elif cmd == "sys":
#             b = psutil.boot_time()
#             up = time.time() - b
#             out = (
#                 f"Uptime: {int(up)//3600}h {(int(up)%3600)//60}m\n"
#                 f"CPUs: {psutil.cpu_count(logical=True)} (logical)\n"
#                 f"Disk: {psutil.disk_usage('/').percent}% used\n"
#             )

#         else:
#             raise ValueError(f"Unsupported command: {cmd}")

#         if redirect:
#             mode, path = redirect
#             if not path:
#                 raise ValueError("redirection: missing file path")
#             append = (mode == ">>")
#             payload = out + ("\n" if out and not out.endswith("\n") else "")
#             s.fs.write(s.cwd, path, payload, append=append)
#             out = ""

#         return out

#     except FileNotFoundError as e:
#         return f"error: {str(e)}"
#     except NotADirectoryError as e:
#         return f"error: {str(e)}"
#     except IsADirectoryError as e:
#         return f"error: {str(e)}"
#     except PermissionError as e:
#         return f"error: {str(e)}"
#     except ValueError as e:
#         return f"error: {str(e)}"

# # these are the fastAPI part of code:

# app = FastAPI(title="TERMINAL API APP")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["*"],
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )

# @app.post("/session", response_model = SessionOut)
# async def create_session():
#     sid, _ = ensure_session(None)
#     return SessionOut(session_id=sid)

# @app.get("/state", response_model=ExecuteOut)
# async def get_state(session_id: Optional[str] = None):
#     sid,s = ensure_session(session_id)
#     return ExecuteOut(ok = True, output = "", cwd = s.cwd, session_id=sid)

# @app.post("/execute", response_model=ExecuteOut)
# async def execute(cmd: ExecuteIn):
#     sid, s = ensure_session(cmd.session_id)
#     s.history.append(cmd.command)
#     out = run_command(s, cmd.command)
#     return ExecuteOut(ok=True, output=out, cwd=s.cwd, session_id=sid)


# @app.post("/reset", response_model=SessionOut)
# async def reset(session_id: Optional[str] = None):
#     sid = session_id or str(uuid.uuid4())
#     if sid in sessions:
#         del sessions[sid]
#     sessions[sid] = Session()
#     return SessionOut(session_id=sid)


# @app.get("/complete")
# async def complete(prefix: str, session_id: Optional[str] = None):
#     sid, s = ensure_session(session_id)
#     try:
#         tokens = shlex.split(prefix)
#     except Exception:
#         tokens = prefix.split()
#     if not tokens:
#         return {"items": S_CMDS}
#     if len(tokens) == 1:
#         return {"items": [c for c in S_CMDS if c.startswith(tokens[0])]}
#     last = tokens[-1]
#     base_dir = s.fs.pwd_normalize(s.cwd, last if last.endswith("/") else (last + "/.."))
#     try:
#         node = s.fs.get_node(base_dir)
#         if not node.is_dir:
#             return {"items": []}
#         items = []
#         for name in node.children.keys():
#             full = last[:-2] + name if last.endswith("/..") else (base_dir.rstrip("/") + "/" + name)
#             if full.startswith(last):
#                 items.append(full)
#         return {"items": items[:50]}
#     except Exception:
#         return {"items": []}

from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psutil
import shlex
import time
import uuid

# -------------------------------
# In-memory virtual filesystem
# -------------------------------

class FileNode:
    def __init__(self, name: str, is_dir: bool):
        self.name = name
        self.is_dir = is_dir
        self.children: Dict[str, FileNode] = {} if is_dir else {}
        self.content: str = "" if not is_dir else ""

    def clone(self) -> "FileNode":
        node = FileNode(self.name, self.is_dir)
        node.content = self.content
        for k, v in self.children.items():
            node.children[k] = v.clone()
        return node


class VFS:
    def __init__(self):
        self.root = FileNode("/", True)

    @staticmethod
    def _parts(path: str) -> List[str]:
        if path == "/":
            return []
        return [p for p in path.split("/") if p and p != "."]

    def pwd_normalize(self, cwd: str, path: Optional[str] = None) -> str:
        if not path or path == ".":
            return cwd
        parts: List[str] = [] if path.startswith("/") else self._parts(cwd)
        for part in self._parts(path):
            if part == "..":
                if parts:
                    parts.pop()  # <-- bugfix (was part.pop())
            else:
                parts.append(part)
        return "/" + "/".join(parts) if parts else "/"

    def get_node(self, path: str) -> FileNode:
        if path == "/":
            return self.root
        node = self.root
        for p in self._parts(path):
            if p not in node.children:
                raise FileNotFoundError(f"No such file or directory: {path}")
            node = node.children[p]
        return node

    def ls(self, cwd: str, path: Optional[str] = None) -> List[str]:
        target_path = self.pwd_normalize(cwd, path)
        node = self.get_node(target_path)
        if not node.is_dir:
            return [node.name]
        return sorted(node.children.keys())

    def mkdir(self, cwd: str, paths: List[str], parents: bool = False) -> None:
        for raw in paths:
            norm = self.pwd_normalize(cwd, raw)
            parent_path = "/"
            if norm != "/":
                norm_parts = self._parts(norm)
                parent_path = "/" if len(norm_parts) <= 1 else "/" + "/".join(norm_parts[:-1])
            name = self._parts(norm)[-1] if self._parts(norm) else ""
            if not name:
                raise FileExistsError("Cannot create directory '/'")
            if parents:
                cur = self.root
                parts = self._parts(norm)
                for i, p in enumerate(parts):
                    if p not in cur.children:
                        cur.children[p] = FileNode(p, True)
                    elif not cur.children[p].is_dir:
                        raise NotADirectoryError(f"Path component is file: /{'/'.join(parts[:i+1])}")
                    cur = cur.children[p]
            else:
                par = self.get_node(parent_path)
                if not par.is_dir:
                    raise NotADirectoryError(f"Not a directory: {parent_path}")
                if name in par.children:
                    raise FileExistsError(f"File exists: {norm}")
                par.children[name] = FileNode(name, True)

    def touch(self, cwd: str, paths: List[str]) -> None:
        for raw in paths:
            norm = self.pwd_normalize(cwd, raw)
            parts = self._parts(norm)
            parent_path = "/" if len(parts) == 1 else "/" + "/".join(parts[:-1])
            par = self.get_node(parent_path)
            if not par.is_dir:
                raise NotADirectoryError(f"Not a directory: {parent_path}")
            name = parts[-1]
            if name not in par.children:
                par.children[name] = FileNode(name, False)

    def write(self, cwd: str, path: str, data: str, append: bool = False) -> None:
        norm = self.pwd_normalize(cwd, path)
        parts = self._parts(norm)
        parent_path = "/" if len(parts) == 1 else "/" + "/".join(parts[:-1])
        par = self.get_node(parent_path)
        if not par.is_dir:
            raise NotADirectoryError(f"Not a directory: {parent_path}")
        name = parts[-1]
        if name not in par.children:
            par.children[name] = FileNode(name, False)
        node = par.children[name]
        if node.is_dir:
            raise IsADirectoryError(f"Is a directory: {norm}")
        node.content = node.content + data if append else data

    def cat(self, cwd: str, paths: List[str]) -> str:
        outs: List[str] = []
        for raw in paths:
            norm = self.pwd_normalize(cwd, raw)
            node = self.get_node(norm)
            if node.is_dir:
                raise IsADirectoryError(f"Is a directory: {norm}")
            outs.append(node.content)
        return "\n".join(outs)

    def rm(self, cwd: str, paths: List[str], recursive: bool = False) -> None:
        for raw in paths:
            norm = self.pwd_normalize(cwd, raw)
            if norm == "/":
                raise PermissionError("Cannot remove '/'")
            parts = self._parts(norm)
            parent_path = "/" if len(parts) == 1 else "/" + "/".join(parts[:-1])
            name = parts[-1]
            par = self.get_node(parent_path)
            if name not in par.children:
                raise FileNotFoundError(f"No such file or directory: {norm}")
            node = par.children[name]
            if node.is_dir and not recursive and node.children:
                raise IsADirectoryError("Directory not empty (use rm -r)")
            del par.children[name]

    def mv(self, cwd: str, src: str, dst: str) -> None:
        src_norm = self.pwd_normalize(cwd, src)
        dst_norm = self.pwd_normalize(cwd, dst)
        src_parts = self._parts(src_norm)
        sp_parent = "/" if len(src_parts) == 1 else "/" + "/".join(src_parts[:-1])
        src_name = src_parts[-1]
        sparent = self.get_node(sp_parent)
        if src_name not in sparent.children:
            raise FileNotFoundError(f"No such file or directory: {src_norm}")
        node = sparent.children[src_name]
        try:
            dst_node = self.get_node(dst_norm)
            if dst_node.is_dir:
                if node.name in dst_node.children:
                    raise FileExistsError(f"File exists: {dst_norm}/{node.name}")
                dst_node.children[node.name] = node
            else:
                raise NotADirectoryError(f"Destination exists and is a file: {dst_norm}")
        except FileNotFoundError:
            dparts = self._parts(dst_norm)
            dp_parent = "/" if len(dparts) == 1 else "/" + "/".join(dparts[:-1])
            dparent = self.get_node(dp_parent)
            newname = dparts[-1]
            if newname in dparent.children:
                raise FileExistsError(f"File exists: {dst_norm}")
            dparent.children[newname] = node
        del sparent.children[src_name]

    def cp(self, cwd: str, src: str, dst: str) -> None:
        src_norm = self.pwd_normalize(cwd, src)
        dst_norm = self.pwd_normalize(cwd, dst)
        node = self.get_node(src_norm)
        try:
            dst_node = self.get_node(dst_norm)
            if not dst_node.is_dir:
                raise NotADirectoryError(f"Destination is not a directory: {dst_norm}")
            if node.name in dst_node.children:
                raise FileExistsError(f"File exists: {dst_norm}/{node.name}")
            dst_node.children[node.name] = node.clone()
        except FileNotFoundError:
            parts = self._parts(dst_norm)
            dp_parent = "/" if len(parts) == 1 else "/" + "/".join(parts[:-1])
            dparent = self.get_node(dp_parent)
            newname = parts[-1]
            if newname in dparent.children:
                raise FileExistsError(f"File exists: {dst_norm}")
            clone = node.clone()
            clone.name = newname
            dparent.children[newname] = clone

# -------------------------------
# Sessions & models
# -------------------------------

class Session:
    def __init__(self):
        self.fs = VFS()
        self.cwd = "/"
        self.history: List[str] = []  # <-- bugfix (was {})

sessions: Dict[str, Session] = {}
SUPPORTED_CMDS = [
    "help", "pwd", "ls", "cd", "mkdir", "rm", "touch", "cat", "echo",
    "mv", "cp", "history", "ps", "top", "sys"
]

class ExecuteIn(BaseModel):
    session_id: Optional[str] = None
    command: str  # <-- bugfix (was Command)

class ExecuteOut(BaseModel):
    ok: bool
    output: str
    cwd: str
    session_id: str

class SessionOut(BaseModel):
    session_id: str

# -------------------------------
# Command Engine
# -------------------------------

def ensure_session(session_id: Optional[str]) -> Tuple[str, Session]:
    if session_id and session_id in sessions:
        return session_id, sessions[session_id]
    sid = session_id or str(uuid.uuid4())
    sessions[sid] = Session()
    s = sessions[sid]
    s.fs.mkdir("/", ["home"], parents=True)
    s.fs.mkdir("/", ["tmp"], parents=True)
    s.fs.mkdir("/", ["var"], parents=True)
    s.fs.mkdir("/", ["usr"], parents=True)
    s.fs.mkdir("/", ["home/user"], parents=True)
    s.fs.touch("/", ["home/user/readme.txt"])  # <-- bugfix: no parents kw
    s.fs.write("/", "home/user/readme.txt", "Welcome to the virtual terminal!\n")
    return sid, s

def run_command(s: Session, raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    parts = [p.strip() for p in raw.split("&&") if p.strip()]
    outputs = []
    for part in parts:
        outputs.append(run_single(s, part))
    return "\n".join([o for o in outputs if o])

def run_single(s: Session, raw: str) -> str:
    tokens = shlex.split(raw.strip())
    if not tokens:
        return ""

    cmd = tokens[0]
    if cmd not in SUPPORTED_CMDS:
        raise ValueError(f"Unsupported command: {cmd}")

    redirect = None  # (mode, path)
    if ">>" in tokens:
        i = tokens.index(">>")
        redirect = (">>", tokens[i + 1] if i + 1 < len(tokens) else None)
        tokens = tokens[:i]
    elif ">" in tokens:
        i = tokens.index(">")
        redirect = (">", tokens[i + 1] if i + 1 < len(tokens) else None)
        tokens = tokens[:i]

    out = ""
    try:
        if cmd == "help":
            out = (
                "Commands: " + ", ".join(SUPPORTED_CMDS) + "\n"
                "Usage examples:\n"
                "  pwd\n"
                "  ls\n"
                "  ls /home\n"
                "  cd /home/user\n"
                "  mkdir -p projects/demo\n"
                "  touch notes.txt\n"
                "  echo \"hello\" > notes.txt\n"
                "  cat notes.txt\n"
                "  mv notes.txt notes.old\n"
                "  cp notes.old copy.txt\n"
                "  rm copy.txt\n"
                "  rm -r projects\n"
                "  history\n"
                "  ps | top | sys (system info)\n"
            )

        elif cmd == "pwd":
            out = s.cwd

        elif cmd == "ls":
            path = tokens[1] if len(tokens) > 1 else None
            out = "  ".join(s.fs.ls(s.cwd, path))

        elif cmd == "cd":
            if len(tokens) == 1:
                s.cwd = "/"
            else:
                target = s.fs.pwd_normalize(s.cwd, tokens[1])
                node = s.fs.get_node(target)
                if not node.is_dir:
                    raise NotADirectoryError(f"Not a directory: {target}")
                s.cwd = target
            out = ""

        elif cmd == "mkdir":
            parents = False
            paths: List[str] = []
            for t in tokens[1:]:
                if t == "-p":
                    parents = True
                else:
                    paths.append(t)
            if not paths:
                raise ValueError("mkdir: missing operand")
            s.fs.mkdir(s.cwd, paths, parents=parents)
            out = ""

        elif cmd == "rm":
            recursive = False
            paths: List[str] = []
            for t in tokens[1:]:
                if t == "-r":
                    recursive = True
                else:
                    paths.append(t)
            if not paths:
                raise ValueError("rm: missing operand")
            s.fs.rm(s.cwd, paths, recursive=recursive)
            out = ""

        elif cmd == "touch":
            if len(tokens) < 2:
                raise ValueError("touch: missing file operand")
            s.fs.touch(s.cwd, tokens[1:])
            out = ""

        elif cmd == "cat":
            if len(tokens) < 2:
                raise ValueError("cat: missing file operand")
            out = s.fs.cat(s.cwd, tokens[1:])

        elif cmd == "echo":
            out = " ".join(tokens[1:])

        elif cmd == "mv":
            if len(tokens) != 3:
                raise ValueError("mv: usage: mv <src> <dst>")
            s.fs.mv(s.cwd, tokens[1], tokens[2])
            out = ""

        elif cmd == "cp":
            if len(tokens) != 3:
                raise ValueError("cp: usage: cp <src> <dst>")
            s.fs.cp(s.cwd, tokens[1], tokens[2])
            out = ""

        elif cmd == "history":
            out = "\n".join(f"{i+1}  {c}" for i, c in enumerate(s.history))

        elif cmd == "ps":
            procs = []
            for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
                try:
                    procs.append(
                        f"{p.info['pid']:>6} {p.info['name'][:22]:<22} "
                        f"{p.info['cpu_percent']:>5.1f}%  {p.info['memory_info'].rss//1024//1024:>4}MB"
                    )
                except Exception:
                    continue
            out = "PID    NAME                   CPU%  RSS\n" + "\n".join(procs[:50])

        elif cmd == "top":
            out = (
                f"CPU: {psutil.cpu_percent(interval=0.1)}%\n"
                f"Mem: {psutil.virtual_memory().percent}% used\n"
                f"Swap: {psutil.swap_memory().percent}% used\n"
            )

        elif cmd == "sys":
            b = psutil.boot_time()
            up = time.time() - b
            out = (
                f"Uptime: {int(up)//3600}h {(int(up)%3600)//60}m\n"
                f"CPUs: {psutil.cpu_count(logical=True)} (logical)\n"
                f"Disk: {psutil.disk_usage('/').percent}% used\n"
            )

        else:
            raise ValueError(f"Unsupported command: {cmd}")

        if redirect:
            mode, path = redirect
            if not path:
                raise ValueError("redirection: missing file path")
            append = (mode == ">>")
            payload = out + ("\n" if out and not out.endswith("\n") else "")
            s.fs.write(s.cwd, path, payload, append=append)
            out = ""

        return out

    except FileNotFoundError as e:
        return f"error: {str(e)}"
    except NotADirectoryError as e:
        return f"error: {str(e)}"
    except IsADirectoryError as e:
        return f"error: {str(e)}"
    except PermissionError as e:
        return f"error: {str(e)}"
    except ValueError as e:
        return f"error: {str(e)}"

# -------------------------------
# FastAPI app & endpoints
# -------------------------------

app = FastAPI(title="TERMINAL API APP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class _RootOut(BaseModel):
    ok: bool

@app.get("/", response_model=_RootOut)
async def root():
    return _RootOut(ok=True)

@app.post("/session", response_model=SessionOut)
async def create_session():
    sid, _ = ensure_session(None)
    return SessionOut(session_id=sid)

@app.get("/state", response_model=ExecuteOut)
async def get_state(session_id: Optional[str] = None):
    sid, s = ensure_session(session_id)
    return ExecuteOut(ok=True, output="", cwd=s.cwd, session_id=sid)

@app.post("/execute", response_model=ExecuteOut)
async def execute(cmd: ExecuteIn):
    sid, s = ensure_session(cmd.session_id)
    s.history.append(cmd.command)
    out = run_command(s, cmd.command)
    return ExecuteOut(ok=True, output=out, cwd=s.cwd, session_id=sid)

@app.post("/reset", response_model=SessionOut)
async def reset(session_id: Optional[str] = None):
    sid = session_id or str(uuid.uuid4())
    if sid in sessions:
        del sessions[sid]
    sessions[sid] = Session()
    return SessionOut(session_id=sid)

@app.get("/complete")
async def complete(prefix: str, session_id: Optional[str] = None):
    sid, s = ensure_session(session_id)
    try:
        tokens = shlex.split(prefix)
    except Exception:
        tokens = prefix.split()
    if not tokens:
        return {"items": SUPPORTED_CMDS}
    if len(tokens) == 1:
        return {"items": [c for c in SUPPORTED_CMDS if c.startswith(tokens[0])]}
    last = tokens[-1]
    base_dir = s.fs.pwd_normalize(s.cwd, last if last.endswith("/") else (last + "/.."))
    try:
        node = s.fs.get_node(base_dir)
        if not node.is_dir:
            return {"items": []}
        items = []
        for name in node.children.keys():
            full = last[:-2] + name if last.endswith("/..") else (base_dir.rstrip("/") + "/" + name)
            if full.startswith(last):
                items.append(full)
        return {"items": items[:50]}
    except Exception:
        return {"items": []}

