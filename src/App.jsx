// import { useState } from 'react';'
import Sidebar from './components/Sidebar';
import { Chat } from './pages/Chat';

import './App.css';

function App() {
  return (
    <div className='app'>
      {/* <h1>Insurance Intelligence Assistant</h1> */}
      <Sidebar />

      <div className='main-content'>
        <Chat />
      </div>
    </div>
  );
}

export default App;
