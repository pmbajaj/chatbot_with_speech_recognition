import React from 'react';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import ChatInterface from './components/ChatInterface';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-4xl mx-auto py-4 px-4">
            <h1 className="text-2xl font-bold text-gray-900">AI Chatbot</h1>
          </div>
        </header>
        <main className="container mx-auto py-4">
          <ChatInterface />
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App; 