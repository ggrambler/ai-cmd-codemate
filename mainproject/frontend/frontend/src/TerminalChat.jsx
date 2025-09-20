import { useEffect, useRef, useState } from "react";
import { createSession, execCommand, complete } from "./api";
import "./styles.css";

const SUPPORTED = [
  "help","pwd","ls","cd","mkdir","rm","touch","cat","echo","mv","cp","history","ps","top","sys"
];

function isValidCommandLocal(input) {
  const trimmed = (input || "").trim();
  if (!trimmed) return false;
  const first = trimmed.split(/\s+/)[0];
  return SUPPORTED.includes(first);
}

export default function TerminalChat() {
  const [sessionId, setSessionId] = useState(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [hIdx, setHIdx] = useState(-1);
  const logRef = useRef(null);

  useEffect(() => {
    (async () => {
      const s = await createSession();
      setSessionId(s.session_id);
      setMessages(m => [
        ...m,
        { role: "bot", text: `Session: ${s.session_id}\nType 'help' to get started.` }
      ]);
    })();
  }, []);

  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [messages]);

  async function send() {
    const text = input.trim();
    if (!text) return;
    if (!isValidCommandLocal(text)) {
      setMessages(m => [
        ...m,
        { role: "user", text },
        { role: "bot", text: "(local) invalid command — try 'help'" }
      ]);
      setInput("");
      return;
    }
    setMessages(m => [...m, { role: "user", text }]);
    setHistory(h => [...h, text]);
    setHIdx(-1);
    setInput("");
    const res = await execCommand(sessionId, text);
    const out = res.output || "";
    if (out) setMessages(m => [...m, { role: "bot", text: out }]);
  }

  async function handleKey(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      await send();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (!history.length) return;
      const i = hIdx < 0 ? history.length - 1 : Math.max(0, hIdx - 1);
      setHIdx(i);
      setInput(history[i]);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (!history.length) return;
      const i = hIdx < 0 ? history.length - 1 : Math.min(history.length - 1, hIdx + 1);
      setHIdx(i);
      setInput(history[i]);
    } else if (e.key === "Tab") {
      e.preventDefault();
      const r = await complete(sessionId, input);
      const first = (r.items || [])[0];
      if (first) setInput(first);
    }
  }

  return (
    <div className="container">
      <div className="header">
        <div className="dot" />
        <strong>AI Command Terminal</strong>
        <span className="hint">— React chatbot UI</span>
      </div>

      <div className="chat">
        <div ref={logRef} className="log">
          {messages.map((m, i) => (
            <div key={i} className={"msg " + (m.role === "user" ? "user" : "bot")}>
              {m.text}
            </div>
          ))}
        </div>

        <div className="prompt">
          <input
            placeholder='Type a command (try: ls, mkdir demo, echo "hi" > a.txt)'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            spellCheck={false}
          />
          <button onClick={send}>Run</button>
        </div>

        <div className="hint">
          Press <kbd>↑/↓</kbd> for history, <kbd>TAB</kbd> for autocomplete.
        </div>
        <div className="suggestion">Supported: {SUPPORTED.join(", ")}</div>
      </div>
    </div>
  );
}
