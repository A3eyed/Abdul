/**
 * Abdul Desktop UI — talks to core API on localhost or remote brain URL.
 * Heavy models stay off the laptop (VPS / API).
 */

const DEFAULT_API = localStorage.getItem("abdul_api") || "http://127.0.0.1:8080";

const messagesEl = document.getElementById("messages") as HTMLElement;
const inputEl = document.getElementById("input") as HTMLTextAreaElement;
const sendBtn = document.getElementById("send") as HTMLButtonElement;
const statusEl = document.getElementById("status") as HTMLElement;

function addBubble(text: string, who: "user" | "abdul") {
  const div = document.createElement("div");
  div.className = `bubble ${who}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function checkHealth() {
  try {
    const r = await fetch(`${DEFAULT_API}/health`);
    if (!r.ok) throw new Error(String(r.status));
    const data = await r.json();
    statusEl.textContent = `online · ${data.routing?.selected || "ok"}`;
    statusEl.className = "status ok";
    return true;
  } catch {
    statusEl.textContent = "core offline — start Abdul core";
    statusEl.className = "status err";
    return false;
  }
}

async function send() {
  const text = inputEl.value.trim();
  if (!text) return;
  inputEl.value = "";
  addBubble(text, "user");
  sendBtn.disabled = true;
  try {
    const r = await fetch(`${DEFAULT_API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await r.json();
    addBubble(data.reply || JSON.stringify(data), "abdul");
  } catch (e) {
    addBubble(`Could not reach Abdul core: ${e}`, "abdul");
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener("click", send);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send();
  }
});

addBubble(
  "Abdul desktop shell ready. Core brain should be on localhost:8080 or your VPS — not a heavy model on this laptop.",
  "abdul"
);
checkHealth();
setInterval(checkHealth, 15000);
