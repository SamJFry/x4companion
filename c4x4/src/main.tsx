import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router';
import X4Base from "./components/Sidebar.tsx";
import CredentialsSignInPage from "./components/SignIn.tsx";
import './x4.css'

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <StrictMode>
      <Routes>
        <Route path="/" element={<CredentialsSignInPage />} />
        <Route path="app" element={<X4Base />} />
      </Routes>
    </StrictMode>
  </BrowserRouter>
)
