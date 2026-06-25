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

    const res = await fetch("http://127.0.0.1:8000/query" , { 
      method: "POST", 
      headers: { "content-type": "application/json" }, 
      body: JSON.stringify({ user_query: text }) });
    const data = await res.json();
    
    console.log("data: ", data);

    setLLMThoughts(data.LLM_thinking);
    setLLMResponse(data.LLM_response);
  };
  
  const handleIngest = async () => {
    const res = await fetch("http://127.0.0.1:8000/ingest" , { "method": "GET" })
    const data = await res.json();
  
    console.log("data: ", data);
    console.log("data.message: ", data.message);
    setIngestMessage(data.message);
  };

    return (
      <div>
        {/* LLM Thoughts */}
        <div>
          <h3>LLM Thoughts will appear here</h3>
          <p>{llmThoughts}</p>
        </div>
        
        {/* LLM Response */}
        <div>
          <h3>LLM Responses will appear here</h3>
          <p>{llmResponse}</p>
        </div>

        {/* Input and buttons */}
        <input onInput={e => setText(e.currentTarget.value)}></input>
        <button onClick={() => handleChat(text)}>Send</button>
        <button onClick={() => handleIngest()}>Re-Ingest</button>
        <p>{ingestMessage}</p>
      </div>
    )
}

export function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <p>HR Onboarding Chatbot</p>
      <TextInput/>
    </>


    // <>
    //   <section id="center">
    //     <div class="hero">
    //       <img src={heroImg} class="base" width="170" height="179" alt="" />
    //       <img src={preactLogo} class="framework" alt="Preact logo" />
    //       <img src={viteLogo} class="vite" alt="Vite logo" />
    //     </div>
    //     <div>
    //       <h1>Get started</h1>
    //       <p>
    //         Edit <code>src/app.tsx</code> and save to test <code>HMR</code>
    //       </p>
    //     </div>
    //     <button
    //       type="button"
    //       class="counter"
    //       onClick={() => setCount((count) => count + 1)}
    //     >
    //       Count is {count}
    //     </button>
    //   </section>

    //   <div class="ticks"></div>

    //   <section id="next-steps">
    //     <div id="docs">
    //       <svg class="icon" role="presentation" aria-hidden="true">
    //         <use href="/icons.svg#documentation-icon"></use>
    //       </svg>
    //       <h2>Documentation</h2>
    //       <p>Your questions, answered</p>
    //       <ul>
    //         <li>
    //           <a href="https://vite.dev/" target="_blank">
    //             <img class="logo" src={viteLogo} alt="" />
    //             Explore Vite
    //           </a>
    //         </li>
    //         <li>
    //           <a href="https://preactjs.com/" target="_blank">
    //             <img class="button-icon" src={preactLogo} alt="" />
    //             Learn more
    //           </a>
    //         </li>
    //       </ul>
    //     </div>
    //     <div id="social">
    //       <svg class="icon" role="presentation" aria-hidden="true">
    //         <use href="/icons.svg#social-icon"></use>
    //       </svg>
    //       <h2>Connect with us</h2>
    //       <p>Join the Vite community</p>
    //       <ul>
    //         <li>
    //           <a href="https://github.com/vitejs/vite" target="_blank">
    //             <svg class="button-icon" role="presentation" aria-hidden="true">
    //               <use href="/icons.svg#github-icon"></use>
    //             </svg>
    //             GitHub
    //           </a>
    //         </li>
    //         <li>
    //           <a href="https://chat.vite.dev/" target="_blank">
    //             <svg class="button-icon" role="presentation" aria-hidden="true">
    //               <use href="/icons.svg#discord-icon"></use>
    //             </svg>
    //             Discord
    //           </a>
    //         </li>
    //         <li>
    //           <a href="https://x.com/vite_js" target="_blank">
    //             <svg class="button-icon" role="presentation" aria-hidden="true">
    //               <use href="/icons.svg#x-icon"></use>
    //             </svg>
    //             X.com
    //           </a>
    //         </li>
    //         <li>
    //           <a href="https://bsky.app/profile/vite.dev" target="_blank">
    //             <svg class="button-icon" role="presentation" aria-hidden="true">
    //               <use href="/icons.svg#bluesky-icon"></use>
    //             </svg>
    //             Bluesky
    //           </a>
    //         </li>
    //       </ul>
    //     </div>
    //   </section>

    //   <div class="ticks"></div>
    //   <section id="spacer"></section>
    // </>
  )
}
