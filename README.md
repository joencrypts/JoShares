# JoShares

**JoShares** is a real-time, multi-channel YouTube listening and chat web app. Built with Flask-SocketIO, it lets users join shared music rooms, synchronize YouTube playback, chat, and manage a collaborative song queue—all with a modern, mobile-friendly, neon/glassmorphism UI.

## Features

- **Multi-Channel Support:** Join one of four channels, each acting as a shared listening room.
- **Synchronized YouTube Playback:** Paste a YouTube link and playback (play, pause, seek, video change) is synchronized in real time for all users in the channel.
- **Real-Time Chat:** Chat with others in the channel, reply to specific messages (WhatsApp/Discord style), and see system messages for join/leave events.
- **User Presence:** See the number of active members in each channel (up to 50 per channel).
- **Picture-in-Picture (PiP):** Pop out the YouTube player into PiP mode with robust error handling.
- **Music-Responsive Animation:** Animated music bars and background particles react to playback.
- **Song Queue:** Add up to 5 YouTube links to a queue via a floating "+" button. The queue is managed client-side and plays automatically.
- **Infinite Scroll Chat:** Chat UI supports infinite scroll (from in-memory history, capped at 100 messages per channel).
- **Modern, Vibrant UI:** Neon/glassmorphism theme, glowing buttons, responsive layout, and a fixed navbar.
- **Mobile-First:** Fully responsive and touch-friendly for all devices and orientations.

## Screenshots

<!-- Add screenshots here if available -->
<!-- ![Screenshot 1](screenshots/screenshot1.png) -->

## Demo

_Deploy your app and add a link here, or run locally as described below._

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/joencrypts/JoShares.git
   cd JoShares
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

### Docker Deployment

1. **Build and run with Docker:**
   ```bash
   docker build -t joshare .
   docker run -p 5000:5000 joshare
   ```

2. **Deploy to Render.com or any cloud provider supporting Docker.**

## Usage

- Open the app in your browser.
- Choose a channel and (optionally) enter a username.
- Paste a YouTube link to start synchronized playback.
- Chat, reply, and manage the song queue with others in real time.

## Project Structure

```
sharepatt/
  ├── app.py                # Flask-SocketIO backend
  ├── requirements.txt      # Python dependencies
  ├── Dockerfile            # For containerized deployment
  └── templates/
        └── index.html      # Main frontend (HTML, CSS, JS)
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE) (add a LICENSE file if you want to specify)

## Author

- [joencrypts](https://github.com/joencrypts)

---

**Repository:** [https://github.com/joencrypts/JoShares](https://github.com/joencrypts/JoShares) 