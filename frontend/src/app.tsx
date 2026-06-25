import { useState } from 'preact/hooks'
// import preactLogo from './assets/preact.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
import './app.css'

const TextInput = () => {
  const [ingestMessage, setIngestMessage] = useState("");
  const [llmThoughts, setLLMThoughts] = useState("");
  const [llmResponse, setLLMResponse] = useState("");
  const [text, setText] = useState("");

  const handleChat = async (text: string) => {
    setText("");

    const res = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ user_query: text })
    });
    const data = await res.json();

    console.log("data: ", data);

    setLLMThoughts(data.LLM_thinking);
    setLLMResponse(data.LLM_response);
  };

  const handleIngest = async () => {
    const res = await fetch("http://127.0.0.1:8000/ingest", { "method": "GET" })
    const data = await res.json();

    console.log("data: ", data);
    console.log("data.message: ", data.message);
    setIngestMessage(data.message);
  };

  return (
    <div>
      {/* Input and buttons */}
      <input onInput={e => setText(e.currentTarget.value)}></input>
      <button onClick={() => handleChat(text)}>Send</button>
      <button onClick={() => handleIngest()}>Re-Ingest</button>
      <p>{ingestMessage}</p>

      {/* LLM Response */}
      <div>
        <h3>LLM Responses will appear here</h3>
        <p>{llmResponse}</p>
      </div>

      {/* LLM Thoughts */}
      <div>
        <h3>LLM Thoughts will appear here</h3>
        <p>{llmThoughts}</p>
      </div>

    </div>
  )
}

export function App() {
  return (
    <>
      <p>HR Onboarding Chatbot</p>
      <TextInput />
    </>
  )
}
