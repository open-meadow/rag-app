import { useRef, useState } from 'preact/hooks'
import './app.css'
import type { JSX } from 'preact/jsx-runtime';

const BACKEND_URL = "http://127.0.0.1:8001"

const Interface = () => {
  const [loadingMessage, setLoadingMessage] = useState("No operation is being conducted");
  const [llmThoughts, setLLMThoughts] = useState("");
  const [llmResponse, setLLMResponse] = useState("");
  const [text, setText] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  // When text is input and "Submit" button is clicked
  const handleChat = async (text: string) => {
    setLoadingMessage("Response is being retrieved from LLM");
    setText("");
    
    const res = await fetch(`${BACKEND_URL}/query`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ user_query: text })
    });
    const data = await res.json();


    setLLMThoughts(data.LLM_thinking);
    setLLMResponse(data.LLM_response);
    setLoadingMessage("Response has been retrieved");
  };

  const handleFileUpload = async (event: JSX.TargetedEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if(!files) return;

    const file = files[0];
    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${BACKEND_URL}/ingest`, { 
      method: "POST", 
      body: formData
    })
  }

  const handleButtonClick = (event: JSX.TargetedMouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    fileInputRef.current?.click();
  }

  return (
    <div>
      {/* Loading Message */}
      <h4>{loadingMessage}</h4>

      {/* Input and buttons */}
      <div>
        <input id="inputBox" value={text} onInput={e => setText(e.currentTarget.value)}></input>
        <div id="buttons">
          <button onClick={() => handleChat(text)}>Send</button>
          {/* <button onClick={() => handleIngest()}>Re-Ingest</button> */}
          <button onClick={handleButtonClick}>Ingest</button>
          <input ref={fileInputRef} type='file' hidden onChange={handleFileUpload}></input>
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
      <Interface />
    </>
  )
}
