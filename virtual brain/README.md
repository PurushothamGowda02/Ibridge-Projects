# St.Philomenaa - Intelligent Virtual Assistant

A sophisticated AI-powered assistant combining natural language processing, system control, file management, and advanced task execution capabilities.

## 🤖 Features

### 🧠 AI Core
- **HuggingFace Integration**: Free, powerful language models (google/flan-t5-base)
- **Intelligent Command Processing**: Natural language understanding with St.Philomenaa personality
- **Context-Aware Conversations**: Maintains conversation history and learns from interactions

### 🖥️ System Control
- **Real-time Monitoring**: CPU, RAM, disk usage, and network statistics
- **Process Management**: View and terminate system processes
- **System Information**: Detailed hardware and software information
- **Performance Optimization**: Monitor and optimize system resources

### 📁 File Management
- **Desktop Organization**: Automatically sort files by type
- **Duplicate Detection**: Find and manage duplicate files
- **Large File Finder**: Locate files consuming disk space
- **Temporary File Cleanup**: Clean system temporary files
- **Smart File Operations**: Organize downloads, documents, and media

### 💾 Memory System
- **Vector-Based Storage**: FAISS for semantic search and memory retrieval
- **Conversation History**: Persistent storage of all interactions
- **Contextual Responses**: Remember past conversations and preferences
- **Intelligent Retrieval**: Find relevant information from previous sessions

### 🎤 Voice Interface
- **Speech Recognition**: Advanced voice command processing
- **Text-to-Speech**: St.Philomenaa-style voice responses
- **Voice Announcements**: Audio feedback for all interactions
- **Hands-free Operation**: Complete voice control capability

### 🎯 Task Execution
- **Application Launcher**: Open any system application
- **Mathematical Calculations**: Perform complex calculations
- **Time & Date Information**: Real-time system information
- **System Commands**: Execute various system operations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11
- Internet connection (for initial model download)

### Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run St.Philomenaa**:
   ```bash
   python main.py
   ```

The St.Philomenaa interface will open at `http://localhost:8501`

## 🎮 Usage

### St.Philomenaa Commands

#### System Control
- "system status" - Get comprehensive system information
- "kill process chrome" - Terminate specific processes
- "network info" - View network statistics
- "disk usage" - Check disk space information

#### File Management
- "organize desktop" - Sort desktop files by type
- "find large files" - Locate files larger than 100MB
- "find duplicates" - Detect duplicate files
- "clean temp files" - Remove temporary files

#### Applications
- "open word" - Launch Microsoft Word
- "open chrome" - Launch Google Chrome
- "open calculator" - Launch Calculator
- "open notepad" - Launch Notepad

#### Information
- "what time is it?" - Current time
- "what's the date?" - Current date
- "calculate 15 * 23 + 7" - Mathematical calculations

### Voice Commands
1. Click the 🎤 **Voice Command** button
2. Wait for "Listening... Speak now!" prompt
3. Speak your command clearly
4. St.Philomenaa will process and respond with voice feedback

## ⚙️ Configuration

The system uses `config.yaml` for configuration:

```yaml
# AI Configuration
llm:
  provider: huggingface
  model: google/flan-t5-base
  temperature: 0.7

# Memory System
memory:
  vector_store: faiss
  embedding_model: sentence-transformers/all-MiniLM-L6-v2

# Voice Settings
voice:
  input_enabled: true
  output_enabled: true
  language: en-US
```

## 🏗️ Architecture

```
st-philomenaa-system/
├── src/
│   ├── jarvis/           # St.Philomenaa core intelligence
│   │   ├── jarvis_core.py      # Main St.Philomenaa processing
│   │   ├── system_control.py   # System monitoring & control
│   │   └── file_manager.py     # File operations
│   ├── ai_core/          # AI language processing
│   ├── memory/           # Vector storage & retrieval
│   ├── tasks/            # Task execution engine
│   ├── input/            # Voice & text input
│   ├── output/           # Voice & text output
│   └── ui/               # Web interface
├── config.yaml           # System configuration
├── requirements.txt      # Dependencies
└── main.py              # Application launcher
```

## 🔧 Troubleshooting

### Microphone Issues
If voice input isn't working:
1. Check Windows microphone permissions
2. Set microphone volume to 100%
3. Add +30dB boost in Windows sound settings
4. See `MICROPHONE_QUICK_FIX.md` for detailed steps

### System Performance
- St.Philomenaa monitors system resources automatically
- Use "system status" command to check performance
- Large file operations may take time depending on disk size

## 🎯 Key Features

✅ **Real-time System Monitoring**  
✅ **Intelligent File Management**  
✅ **Voice Command Processing**  
✅ **Natural Language Understanding**  
✅ **Memory & Context Awareness**  
✅ **Application Integration**  
✅ **St.Philomenaa Personality & Responses**  

## 📚 Documentation

- `ST_PHILOMENAA_COMMANDS.md` - Complete command reference
- `QUICK_START.md` - Getting started guide
- `MICROPHONE_QUICK_FIX.md` - Voice setup instructions
- `TROUBLESHOOTING.md` - Common issues and solutions

## 🤝 Contributing

This is a complete St.Philomenaa-like AI assistant system. Feel free to extend functionality by:
- Adding new St.Philomenaa commands
- Enhancing system monitoring capabilities
- Improving file management features
- Expanding voice recognition patterns

## 📄 License

MIT License - Feel free to use and modify for your projects.

---

**"Your intelligent virtual assistant St.Philomenaa, ready for your desktop!"** 🤖✨