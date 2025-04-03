# Multilingual AI Chatbot with Speech Recognition

A sophisticated AI chatbot that supports both text and voice interactions in English and Hindi, featuring real-time speech recognition and a modern web interface.

## Features

- 🤖 **Dual-Mode Interface**
  - Web-based interface with modern UI
  - Terminal-based interface for quick interactions
- 🎤 **Advanced Speech Recognition**
  - Real-time voice input processing
  - Support for both English and Hindi
  - Automatic language detection
  - Noise reduction and audio preprocessing
- 💬 **Multilingual Support**
  - English and Hindi language support
  - Automatic language detection
  - Seamless language switching
- 🎨 **Modern UI/UX**
  - Responsive design
  - Dark/Light mode support
  - Real-time message updates
  - Voice input status indicators
- 🔒 **Security Features**
  - Environment variable configuration
  - Secure API key handling
  - Rate limiting
  - Error handling

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- A working microphone
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chat-bot.git
cd chat-bot
```

2. Set up the Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

5. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Web Interface

1. Start the backend server:
```bash
python run.py --mode web
```

2. In a new terminal, start the frontend development server:
```bash
cd frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

### Terminal Interface

Run the chatbot in terminal mode:
```bash
python run.py --mode terminal
```

## Project Structure

```
chat-bot/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   └── speech_service.py
│   │   ├── terminal_chat.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.js
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT API
- Hugging Face for the wav2vec2 model
- React and Material-UI for the frontend components
- Tailwind CSS for styling

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add support for more languages
- [ ] Implement user authentication
- [ ] Add conversation history
- [ ] Improve speech recognition accuracy
- [ ] Add custom voice models
- [ ] Implement offline mode

## Screenshots

[Add screenshots of your application here]

## Contact

Piyush Mangalam Bajaj - pmbajaj999@gmail.com

Project Link: https://github.com/pmbajaj/nlp_chatbot_with_speech_recognition.git