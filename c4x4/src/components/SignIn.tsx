import * as React from 'react';
import { useEffect } from "react";
import { AppProvider } from '@toolpad/core/AppProvider';
import { SignInPage, type AuthProvider } from '@toolpad/core/SignInPage';
import { useTheme } from '@mui/material/styles';
import { getUserToken } from "../functions/responses.ts";
import { useNavigate } from "react-router";
import TextField from "@mui/material/TextField";

const providers = [{ id: 'credentials', name: 'Email and Password' }];

interface AuthResponse {
  error?: string
  type?: string
}

const signIn: (provider: AuthProvider, formData: FormData) => void = async (
  provider,
  formData,
) => {
  const promise = new Promise<void>((resolve) => {
    setTimeout(() => {
      resolve(getUserToken(formData.get('username-or-email'), formData.get('password')));
    }, 30);
  });
  const response = await promise
  if (response !== undefined) {
    const error: AuthResponse = {
      error: response['non_field_errors'],
      type: "InvalidCreds"
    }
    return error
  }
  return promise;
};

function UsernNameOrEmailField() {
  return (
    <TextField
      id="username-or-email"
      label="Username/Email"
      name="username-or-email"
      type="text"
      required
      fullWidth
      variant="outlined"
      size="small"
      slotProps={{
        inputLabel: {
          style: { fontSize: '0.9rem'}
        }
      }}
    />
  )
}

export default function CredentialsSignInPage() {
  const theme = useTheme();
  const navigate = useNavigate()
  useEffect(() =>{
    if (document.cookie.includes('token=Bearer')) {
      navigate('app');
    }
  }, [])
  const handleSignIn: (provider: AuthProvider, formData: FormData) => void = async (
    provider,
    formData,
  ) => {
    const loginResponse = await signIn(provider, formData);
    if (loginResponse === undefined && document.cookie.includes('token=Bearer')) {
      navigate('app')
    }
    return loginResponse
  }
  return (
    <AppProvider theme={theme}>
      <SignInPage
        signIn={handleSignIn}
        providers={providers}
        slots={{
          emailField: UsernNameOrEmailField
        }}
      />
    </AppProvider>
  );
}