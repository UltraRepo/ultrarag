<p align="center">
  <a href="https://librechat.ai">
    <img src="client/public/assets/logo.svg" height="256">
  </a>
  <h1 align="center">
    <a href="https://librechat.ai">LibreChat Cloned</a>
  </h1>
</p>

<p align="center">
  <a href="https://docs.librechat.ai"> 
    <img
      src="https://img.shields.io/badge/DOCS-blue.svg?style=for-the-badge&logo=read-the-docs&logoColor=white&labelColor=000000&logoWidth=20">
  </a>
  <a aria-label="Sponsors" href="https://github.com/sponsors/danny-avila">
    <img
      src="https://img.shields.io/badge/SPONSORS-brightgreen.svg?style=for-the-badge&logo=github-sponsors&logoColor=white&labelColor=000000&logoWidth=20">
  </a>

## ✨ Get original here: [LibreChat](https://github.com/danny-avila/LibreChat/releases)

# Getting Started

## 🚀 Quick Start Guide for MacOS

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.ai)
- [Git](https://git-scm.com/download/mac)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/danny-avila/LibreChat.git
   cd LibreChat
   ```

2. **Create Configuration Files**
   - Create `librechat.yaml` in the root directory:
   ```yaml
   endpoints:
     ollama:
       baseURL: http://host.docker.internal:11434
       models:
         - llama2
         - codellama
         - mistral
         - mixtral
         # Add other models you've pulled in Ollama
         # IMPORTANT: The model names here must match the tags used when pulling models in Ollama
         # For example: if you run 'ollama pull llama2:13b', use 'llama2:13b' here
         # See your available models with 'ollama list'
   ```

   - Create `docker-compose.override.yml`:
   ```yaml
   services:
     api:
       environment:
         - OLLAMA_PROXY=true
   ```

   > 📚 **Documentation Links**
   > - [Detailed Ollama Setup Guide](https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/ollama)
   > - [Docker Configuration Guide](https://www.librechat.ai/docs/installation/docker)
   > - [LibreChat YAML Configuration](https://www.librechat.ai/docs/configuration/librechat_yaml)

3. **Start Docker Services**
   ```bash
   docker compose up --build
   ```

4. **Access LibreChat**
   - Open [http://localhost:3080](http://localhost:3080) in your browser
   - Create an account and log in
   - Select "Ollama" from the model dropdown
   - Start chatting with your local LLMs!

### Troubleshooting
- If models aren't visible in LibreChat, ensure Ollama is running and models are pulled:
  ```bash
  ollama list
  ollama pull mistral  # or any other model you want to use
  ```
- Check Docker logs if you encounter issues:
  ```bash
  docker compose logs -f
  ```

## ✨ Features of this clone

## Project Structure

> 📁 `.cursor/rules/` - AI Coding Rules
> ```
> .cursor/rules/
> ├── frontend.mdc .............. Frontend development rules and patterns
> └── backend.mdc ............... Backend development and API guidelines
> ```

```
📁 LibreChat
├── 📁 [API] api/ ........................... Backend API and server-side code
├── 📁 [Frontend] client/ ................... Frontend React application
│   ├── 📁 public/ ......................... Static assets and files
│   └── 📁 src/ ............................ Source code for the React app
├── 📁 [Config] config/ .................... Configuration files and settings
├── 📁 [Modules] packages/ ................. Shared packages and modules
├── 📁 [Testing] e2e/ ...................... End-to-end testing files
├── 📁 [Helpers] utils/ .................... Utility functions and helper code
├── 📁 [IDE] .cursor/ ...................... Cursor IDE configuration
│   └── 📁 rules/ .......................... AI coding rules and settings
├── 📁 [Python] .venv/ ..................... Python virtual environment
└── 📁 [K8s] charts/ ...................... Kubernetes Helm charts
```

- 🖥️ Modified logo and UI for use in LibreDash project

- 🤖 **AI Model Selection**:  
  - Anthropic (Claude), AWS Bedrock, OpenAI, Azure OpenAI, Google, Vertex AI, OpenAI Assistants API (incl. Azure)
  - [Custom Endpoints](https://www.librechat.ai/docs/quick_start/custom_endpoints): Use any OpenAI-compatible API with LibreChat, no proxy required
  - Compatible with [Local & Remote AI Providers](https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints):
    - Ollama, groq, Cohere, Mistral AI, Apple MLX, koboldcpp, together.ai,
    - OpenRouter, Perplexity, ShuttleAI, Deepseek, Qwen, and more

- 🔧 **[Code Interpreter API](https://www.librechat.ai/docs/features/code_interpreter)**: 
  - Secure, Sandboxed Execution in Python, Node.js (JS/TS), Go, C/C++, Java, PHP, Rust, and Fortran
  - Seamless File Handling: Upload, process, and download files directly
  - No Privacy Concerns: Fully isolated and secure execution

- 🔦 **Agents & Tools Integration**:  
  - **[LibreChat Agents](https://www.librechat.ai/docs/features/agents)**:
    - No-Code Custom Assistants: Build specialized, AI-driven helpers without coding  
    - Flexible & Extensible: Attach tools like DALL-E-3, file search, code execution, and more  
    - Compatible with Custom Endpoints, OpenAI, Azure, Anthropic, AWS Bedrock, and more
    - [Model Context Protocol (MCP) Support](https://modelcontextprotocol.io/clients#librechat) for Tools
  - Use LibreChat Agents and OpenAI Assistants with Files, Code Interpreter, Tools, and API Actions

- 🪄 **Generative UI with Code Artifacts**:  
  - [Code Artifacts](https://youtu.be/GfTj7O4gmd0?si=WJbdnemZpJzBrJo3) allow creation of React, HTML, and Mermaid diagrams directly in chat

- 💾 **Presets & Context Management**:  
  - Create, Save, & Share Custom Presets  
  - Switch between AI Endpoints and Presets mid-chat
  - Edit, Resubmit, and Continue Messages with Conversation branching  
  - [Fork Messages & Conversations](https://www.librechat.ai/docs/features/fork) for Advanced Context control

- 💬 **Multimodal & File Interactions**:  
  - Upload and analyze images with Claude 3, GPT-4.5, GPT-4o, o1, Llama-Vision, and Gemini 📸  
  - Chat with Files using Custom Endpoints, OpenAI, Azure, Anthropic, AWS Bedrock, & Google 🗃️

- 🌎 **Multilingual UI**:  
  - English, 中文, Deutsch, Español, Français, Italiano, Polski, Português Brasileiro
  - Русский, 日本語, Svenska, 한국어, Tiếng Việt, 繁體中文, العربية, Türkçe, Nederlands, עברית

- 🧠 **Reasoning UI**:  
  - Dynamic Reasoning UI for Chain-of-Thought/Reasoning AI models like DeepSeek-R1

- 🎨 **Customizable Interface**:  
  - Customizable Dropdown & Interface that adapts to both power users and newcomers

- 🗣️ **Speech & Audio**:  
  - Chat hands-free with Speech-to-Text and Text-to-Speech  
  - Automatically send and play Audio  
  - Supports OpenAI, Azure OpenAI, and Elevenlabs

- 📥 **Import & Export Conversations**:  
  - Import Conversations from LibreChat, ChatGPT, Chatbot UI  
  - Export conversations as screenshots, markdown, text, json

- 🔍 **Search & Discovery**:  
  - Search all messages/conversations

- 👥 **Multi-User & Secure Access**:
  - Multi-User, Secure Authentication with OAuth2, LDAP, & Email Login Support
  - Built-in Moderation, and Token spend tools

- ⚙️ **Configuration & Deployment**:  
  - Configure Proxy, Reverse Proxy, Docker, & many Deployment options  
  - Use completely local or deploy on the cloud

- 📖 **Open-Source & Community**:  
  - Completely Open-Source & Built in Public  
  - Community-driven development, support, and feedback

[For a thorough review of our features, see our docs here](https://docs.librechat.ai/) 📚

## 🪶 All-In-One AI Conversations with LibreChat

LibreChat brings together the future of assistant AIs with the revolutionary technology of OpenAI's ChatGPT. Celebrating the original styling, LibreChat gives you the ability to integrate multiple AI models. It also integrates and enhances original client features such as conversation and message search, prompt templates and plugins.

With LibreChat, you no longer need to opt for ChatGPT Plus and can instead use free or pay-per-call APIs. We welcome contributions, cloning, and forking to enhance the capabilities of this advanced chatbot platform.

[![Watch the video](https://raw.githubusercontent.com/LibreChat-AI/librechat.ai/main/public/images/changelog/v0.7.6.gif)](https://www.youtube.com/watch?v=ilfwGQtJNlI)

Click on the thumbnail to open the video☝️

---

## 🌐 Resources

**GitHub Repo:**
  - **RAG API:** [github.com/danny-avila/rag_api](https://github.com/danny-avila/rag_api)
  - **Website:** [github.com/LibreChat-AI/librechat.ai](https://github.com/LibreChat-AI/librechat.ai)

**Other:**
  - **Website:** [librechat.ai](https://librechat.ai)
  - **Documentation:** [docs.librechat.ai](https://docs.librechat.ai)
  - **Blog:** [blog.librechat.ai](https://blog.librechat.ai)

---

## 📝 Changelog

Keep up with the latest updates by visiting the releases page and notes:
- [Releases](https://github.com/danny-avila/LibreChat/releases)
- [Changelog](https://www.librechat.ai/changelog) 

**⚠️ Please consult the [changelog](https://www.librechat.ai/changelog) for breaking changes before updating.**

---

## ⭐ Star History

<p align="center">
  <a href="https://star-history.com/#danny-avila/LibreChat&Date">
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=danny-avila/LibreChat&type=Date&theme=dark" onerror="this.src='https://api.star-history.com/svg?repos=danny-avila/LibreChat&type=Date'" />
  </a>
</p>
<p align="center">
  <a href="https://trendshift.io/repositories/4685" target="_blank" style="padding: 10px;">
    <img src="https://trendshift.io/api/badge/repositories/4685" alt="danny-avila%2FLibreChat | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>
  <a href="https://runacap.com/ross-index/q1-24/" target="_blank" rel="noopener" style="margin-left: 20px;">
    <img style="width: 260px; height: 56px" src="https://runacap.com/wp-content/uploads/2024/04/ROSS_badge_white_Q1_2024.svg" alt="ROSS Index - Fastest Growing Open-Source Startups in Q1 2024 | Runa Capital" width="260" height="56"/>
  </a>
</p>

---

## ✨ Contributions

Contributions, suggestions, bug reports and fixes are welcome!

For new features, components, or extensions, please open an issue and discuss before sending a PR.

If you'd like to help translate LibreChat into your language, we'd love your contribution! Improving our translations not only makes LibreChat more accessible to users around the world but also enhances the overall user experience. Please check out our [Translation Guide](https://www.librechat.ai/docs/translation).

---

## 💖 This project exists in its current state thanks to all the people who contribute

<a href="https://github.com/danny-avila/LibreChat/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=danny-avila/LibreChat" />
</a>

---

## 🎉 Special Thanks

We thank LibreChat team.  Also [Locize](https://locize.com) for their translation management tools that support multiple languages in LibreChat.

<p align="center">
  <a href="https://locize.com" target="_blank" rel="noopener noreferrer">
    <img src="https://github.com/user-attachments/assets/d6b70894-6064-475e-bb65-92a9e23e0077" alt="Locize Logo" height="50">
  </a>
</p>
