import React from 'react';

const Sidebar = () => {
  return (
    <>
      <aside className='sidebar'>
        <div className='sidebar-logo'>
          <div className='logo-icon'>🛡</div>
          <h2>Insurance AI</h2>
          <span>Intelligence Assistant</span>
        </div>

        <div className='sidebar-section'>
          <p className='section-title'>Main Menu</p>
          <nav className='sidebar-nav'>
            <button className='nav-item'>
              <span>⌂</span>
              Dashboard
            </button>
            <button className='nav-item active'>
              <span>✦</span>AI Assistant
            </button>
            <button className='nav-item'>
              <span>▣</span>
              Claims
            </button>
            <button className='nav-item'>
              <span>📄</span>
              Policies
            </button>
            <button className='nav-item'>
              <span>📑</span>
              Documents
            </button>
            <button className='nav-item'>
              <span>🏥</span>
              Hospitals
            </button>
          </nav>
        </div>
        <div className='sidebar-bottom'>
          <button className='nav-item'>
            <span>⚙️</span>
            Settings
          </button>
          <div className='user-profile'>
            <span>👤</span>
          </div>

          <div>
            <strong>Insurance User</strong>
            <small>Administrator</small>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
