import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import JsApp from './jsapp';  // Update this line to import `jsapp.js`
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <JsApp />  {/* Update this to render `JsApp` */}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
