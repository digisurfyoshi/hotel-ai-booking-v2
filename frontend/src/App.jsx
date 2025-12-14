import { useState } from 'react'

function App() {
    const [count, setCount] = useState(0)

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
            <h1>Antigravity Hotel AI</h1>
            <p>Welcome to the Antigravity Hotel AI management system.</p>
            <div className="card">
                <button onClick={() => setCount((count) => count + 1)}>
                    count is {count}
                </button>
            </div>
        </div>
    )
}

export default App
