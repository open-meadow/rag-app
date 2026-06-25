import { useState } from 'preact/hooks'
// import preactLogo from './assets/preact.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
import './app.css'

const TextInput = () => {
  const [loadingMessage, setLoadingMessage] = useState("No operation is being conducted");
  const [llmThoughts, setLLMThoughts] = useState("");
  const [llmResponse, setLLMResponse] = useState("");
  const [text, setText] = useState("");

  const handleChat = async (text: string) => {
    setLoadingMessage("Response is being retrieved from LLM");
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
    setLoadingMessage("Response has been retrieved");
  };

  const handleIngest = async () => {
    setLoadingMessage("Adding new files for RAG");

    const res = await fetch("http://127.0.0.1:8000/ingest", { "method": "GET" })
    const data = await res.json();

    console.log("data: ", data);
    console.log("data.message: ", data.message);
    setLoadingMessage("Ingestion complete");
  };

  return (
    <div>
      {/* Loading Message */}
      <h4>{loadingMessage}</h4>

      {/* Input and buttons */}
      <div>
        <input id="inputBox" onInput={e => setText(e.currentTarget.value)}></input>
        <div id="buttons">
          <button onClick={() => handleChat(text)}>Send</button>
          <button onClick={() => handleIngest()}>Re-Ingest</button>
        </div>
      </div>

      {/* LLM Response */}
      <div id="llmResponse">
        <h3>LLM Responses will appear here</h3>
        <p>{llmResponse}</p>
      </div>

      {/* LLM Thoughts */}
      <div id="llmThoughts">
        <h3>LLM Thoughts will appear here</h3>
        <p>{llmThoughts}</p>
      </div>

    </div>
  )
}

export function App() {
  return (
    <>
      <h1>U-TO PeopleAssist</h1>
      <TextInput />
    </>
  )
}
