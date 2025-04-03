import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, TextField, IconButton, Typography, CircularProgress, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { Send as SendIcon, Mic as MicIcon, Stop as StopIcon } from '@mui/icons-material';
import axios from 'axios';

interface Message {
  text: string;
  isUser: boolean;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        await processAudioInput(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const processAudioInput = async (audioBlob: Blob) => {
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob);
      formData.append('language', selectedLanguage);

      const response = await axios.post('http://localhost:8000/api/chat/voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { text } = response.data;
      addMessage(text, false);
    } catch (error) {
      console.error('Error processing audio:', error);
      addMessage('Sorry, I could not process your voice input.', false);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = inputText;
    setInputText('');
    addMessage(userMessage, true);

    setIsProcessing(true);
    try {
      const response = await axios.post('http://localhost:8000/api/chat/text', {
        text: userMessage,
        language: selectedLanguage,
      });

      const { text } = response.data;
      addMessage(text, false);
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage('Sorry, I encountered an error processing your message.', false);
    } finally {
      setIsProcessing(false);
    }
  };

  const addMessage = (text: string, isUser: boolean) => {
    setMessages(prev => [...prev, { text, isUser, timestamp: new Date() }]);
  };

  return (
    <Box className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <Paper className="flex-1 overflow-hidden mb-4">
        <Box className="h-full flex flex-col">
          <Box className="flex-1 overflow-y-auto p-4">
            {messages.map((message, index) => (
              <Box
                key={index}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'} mb-4`}
              >
                <Paper
                  className={`max-w-[70%] p-3 ${
                    message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-100'
                  }`}
                >
                  <Typography>{message.text}</Typography>
                  <Typography variant="caption" className="opacity-70">
                    {message.timestamp.toLocaleTimeString()}
                  </Typography>
                </Paper>
              </Box>
            ))}
            <div ref={messagesEndRef} />
          </Box>
        </Box>
      </Paper>

      <Box className="flex items-center gap-2">
        <FormControl size="small" className="w-32">
          <InputLabel>Language</InputLabel>
          <Select
            value={selectedLanguage}
            label="Language"
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            <MenuItem value="en">English</MenuItem>
            <MenuItem value="hi">Hindi</MenuItem>
          </Select>
        </FormControl>

        <IconButton
          color={isRecording ? 'error' : 'primary'}
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
        >
          {isRecording ? <StopIcon /> : <MicIcon />}
        </IconButton>

        <form onSubmit={handleTextSubmit} className="flex-1 flex gap-2">
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isProcessing}
          />
          <IconButton
            color="primary"
            type="submit"
            disabled={!inputText.trim() || isProcessing}
          >
            <SendIcon />
          </IconButton>
        </form>

        {isProcessing && (
          <CircularProgress size={24} className="ml-2" />
        )}
      </Box>
    </Box>
  );
};

export default ChatInterface; 