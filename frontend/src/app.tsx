import { useRef, useState } from 'preact/hooks'
import './app.css'

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

    const res = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ user_query: text })
    });
    const data = await res.json();

    setLLMThoughts(data.LLM_thinking);
    setLLMResponse(data.LLM_response);
    setLoadingMessage("Response has been retrieved");
  };

  // When "Re-ingest" button is clicked
  const handleIngest = async () => {
    setLoadingMessage("Adding new files for RAG");

    const res = await fetch("http://127.0.0.1:8000/ingest", { "method": "GET" })
    const data = await res.json();

    console.log("data: ", data);
    console.log("data.message: ", data.message);
    setLoadingMessage("Ingestion complete");
  };

  const handleFileUpload = async (event) => {
    const files = event.target.files;
    if(!files) return;

    const file = files[0];

    console.log("filename: ", file.name);
  
    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:8000/ingest", { 
      method: "POST", 
      body: formData
    })
  }

  const handleButtonClick = (event) => {
    event.preventDefault();
    if (!fileInputRef || !fileInputRef.current) return;
    
    fileInputRef.current.click();
  }

  return (
    <div>
      {/* Loading Message */}
      <h4>{loadingMessage}</h4>

      {/* Input and buttons */}
      <div>
        <input id="inputBox" onInput={e => setText(e.currentTarget.value)}></input>
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
