import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [count, setCount] = useState(0);
  const [helloMessage, setHelloMessage] = useState<{ Hello: string }>({ Hello: '' });

  useEffect(() => {
    fetch(`${API_BASE_URL}/`)
      .then(response => response.json())
      .then(data => setHelloMessage(data))
      .catch(error => console.error('Error:', error));
    
      fetch(`${API_BASE_URL}/clickcount`)
      .then(response => response.json())
      .then(data => setCount(data.click_count ?? 0))
      .catch(error => console.error('Error:', error));
  }, []);

  const handleIncrementClick = () => {
    fetch(`${API_BASE_URL}/clickcount/increment`)
    .then(response => response.json())
    .then(data => setCount(data.click_count ?? 0))
    .catch(error => console.error('Error:', error));
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => handleIncrementClick()}>
          count is {count}
        </button>
        <p>
          {helloMessage?.Hello}
        </p>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
