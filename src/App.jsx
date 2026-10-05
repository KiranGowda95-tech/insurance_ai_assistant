// import { useState } from 'react';'
import Sidebar from './components/Sidebar';
import { Chat } from './pages/Chat';

import './App.css';

function App() {
  return (
    <div className='app'>
      {/* <h1>Insurance Intelligence Assistant</h1> */}
      <Sidebar />

      <Chat />
    </div>
  );
}

export default App;
