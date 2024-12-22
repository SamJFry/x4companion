import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import X4Base from "./components/Sidebar.tsx";
import CredentialsSignInPage from "./components/SignIn.tsx";
import './x4.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <CredentialsSignInPage />
    <X4Base />
  </StrictMode>,
)
