import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { PersistGate } from "redux-persist/integration/react";
// import store from './components/redux/store';
import { store, persistor } from './components/redux/store';
import { Provider } from 'react-redux';
ReactDOM.createRoot(document.getElementById('root')).render(
  // <BrowserRouter>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <App />
      </PersistGate>
    </Provider>

  // </BrowserRouter>
);
