# 🎯💨 Panasonic Fart System

**The world's most sophisticated remote-controlled fart button!**

Transform your Panasonic TV remote into the ultimate prank device. Press button "1" to trigger hilarious fart sounds through your Raspberry Pi. Features custom fart recording, pattern learning, and authentic Panasonic IR protocol detection.

![Fart Button Demo](https://github.com/ChrisFryer/panasonic_fart_system/blob/main/CLI_Screenshot.png)

## 🚀 Features

### 🎙️ **Custom Fart Recording Studio**
- Record your own authentic fart sounds (5 seconds each)
- Build a personal fart sound collection
- Name your masterpieces ("The Thunderclap", "Silent But Deadly", etc.)
- Test playback before adding to collection
- Manage and delete recordings

### 📡 **Smart IR Detection**
- Learns Panasonic remote button patterns with 60%+ accuracy
- Handles Panasonic's unique 3-packet IR protocol
- Filters noise and focuses on actual IR signals
- Debouncing prevents multiple triggers

### 🎵 **Advanced Fart Playback**
- Randomly selects from your custom recordings
- Fallback to 5 different animated text fart types
- Personalized stinky messages using your fart names
- Visual effects and dramatic timing

### 🎛️ **Interactive Menu System**
- Learn button patterns
- Start/stop detection
- Access Fart Sound Studio
- View fart collection statistics

## 🛠️ Hardware Requirements

### Essential Components
- **Raspberry Pi** (any model with GPIO)
- **VS1838B IR Receiver** (38kHz)
![IR Sensor Image](<img src="https://github.com/ChrisFryer/panasonic_fart_system/blob/main/VS1838B%20IR%20Receiver.jpg" alt="Description" width="50%">)
- **Panasonic Remote Control**
- **Jumper wires**
- **Breadboard** (optional)

### IR Sensor Wiring
```
VS1838B → Raspberry Pi
S (Signal) → GPIO 4 (Pin 7)
+ (VCC)    → 3.3V (Pin 1 or 17)  
- (GND)    → Ground (Pin 6, 9, 14, 20, 25, 30, 34, or 39)
```

### Optional for Audio Recording
- **USB Microphone** or Pi microphone module
- **Speakers** or headphones for playback

## 📦 Installation

### 1. System Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python GPIO library
sudo apt install python3-rpi.gpio

# Install audio tools (optional - for custom recordings)
sudo apt install alsa-utils

# Install audio players (for fart playback)
sudo apt install alsa-utils pulseaudio-utils
```

### 2. Download and Setup
```bash
# Clone the repository
git clone https://github.com/ChrisFryer/panasonic_fart_system.git
cd panasonic_fart_system

# Or download directly
wget https://raw.githubusercontent.com/ChrisFryer/panasonic_fart_system/main/panasonic_fart_system.py

# Make executable
chmod +x panasonic_fart_system.py

# Create fart sounds directory (automatic on first run)
mkdir -p fart_sounds
```

## 🎯 Quick Start Guide

### 1. Run the System
```bash
sudo python3 panasonic_fart_system.py
```

### 2. Learn Your Remote
1. Choose option **1** (Learn Button 1 pattern)
2. Press button "1" on your Panasonic remote **3 times** when prompted
3. Wait for "Successfully learned!" message

### 3. Record Custom Farts (Optional)
1. Choose option **3** (Fart Sound Studio)
2. Choose option **1** (Record new fart sound)
3. Enter a name for your fart
4. Get into position 🍑
5. Press ENTER and let it rip during the 5-second recording!

### 4. Start Farting!
1. Choose option **2** (Start fart button detection)
2. Press button "1" on your remote
3. Enjoy the stinky chaos! 💨

## 🎙️ Fart Sound Studio

### Recording Your Masterpieces
- **Duration**: 5 seconds per recording
- **Format**: 44.1kHz, 16-bit, mono WAV files
- **Storage**: `fart_sounds/` directory
- **Naming**: Use descriptive names like "The Destroyer" or "Squeaky Pete"

### Managing Your Collection
- **List**: View all recorded fart sounds with file sizes
- **Test Play**: Preview any fart before using
- **Delete**: Remove unwanted recordings
- **Auto-load**: System automatically loads existing recordings on startup

## 🔧 Troubleshooting

### IR Detection Issues
**Low detection rate (<50%)**
- Move remote closer to sensor (5-15cm)
- Point remote directly at IR receiver
- Press button "1" quickly and consistently
- Check wiring connections

**No detection at all**
- Verify wiring with multimeter
- Test with different Panasonic remote
- Check GPIO 4 isn't used by other processes
- Run with `sudo` for GPIO access

### Audio Recording Issues
**"arecord not found"**
```bash
sudo apt install alsa-utils
```

**"No recording device"**
```bash
# Check available audio devices
arecord -l

# Test basic recording
arecord -f S16_LE -c 1 -r 44100 -d 3 test.wav
```

**Permission denied**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Logout and login again
```

### Audio Playback Issues
**"No audio player found"**
```bash
# Install multiple audio options
sudo apt install alsa-utils pulseaudio-utils sox
```

**No sound output**
```bash
# Check audio output
alsamixer

# Test playback
aplay /usr/share/sounds/alsa/Front_Left.wav
```

## 📊 Performance Stats

- **Detection Accuracy**: 60-80% (varies by remote and conditions)
- **Response Time**: <500ms from button press to fart
- **Audio Quality**: CD-quality recordings (44.1kHz/16-bit)
- **Storage**: ~440KB per 5-second fart recording
- **Supported Remotes**: Panasonic TV/AC remotes (38kHz IR)

## 🎨 Customization

### Adding More Buttons
Modify the code to learn additional remote buttons:
```python
# In learn_button_1_simple(), change to:
def learn_button_X_simple(button_name):
    # Learn any button pattern
```

### Custom Text Farts
Add new fart animations in `make_fart_noise()`:
```python
fart_types.append({
    'name': 'Your Custom Fart',
    'animation': ['💨 your', '💨 custom', '💨 sequence'],
    'final': '💨 YOUR FINAL FART!'
})
```

### Audio Effects
Enhance fart playback with audio filters:
```bash
# Install sox for audio effects
sudo apt install sox

# Add reverb to farts
play input.wav reverb
```

## 🤝 Contributing

Found a bug? Want to add features? Contributions welcome!

**Ideas for improvements:**
- Support for other remote brands (NEC, Sony, RC5)
- Multiple button assignments
- Web interface for remote fart triggering
- Bluetooth fart broadcasting
- Fart sound sharing network

## ⚠️ Disclaimer

This project is for **educational and entertainment purposes only**. Use responsibly:

- Don't use in professional/serious environments
- Respect others' comfort levels with humor
- Clean up your fart sound files periodically
- The author is not responsible for relationship damage caused by excessive farting
- May cause uncontrollable laughter and social awkwardness

## 📜 License

**MIT License** - Feel free to fork, modify, and share your fart innovations!

Use this code to spread joy, laughter, and occasional disgust around the world. 🌍💨

## 🏆 Hall of Fame

**Most Creative Fart Names:**
- "The Thunderclap" 
- "Silent But Deadly"
- "Toot Suite"
- "The Brown Note"
- "Atomic Blast"

**Achievement Unlocked:** You've successfully turned a Raspberry Pi into a fart machine. Your parents would be so proud! 😂

---

## 🎯 Quick Reference

| Command | Action |
|---------|---------|
| `sudo python3 panasonic_fart_system.py` | Start the system |
| Option 1 | Learn button pattern |
| Option 2 | Start fart detection |
| Option 3 | Enter Fart Sound Studio |
| Ctrl+C | Stop/Exit |

---

*Made with 💨 and Python on Raspberry Pi*

**Version 1.0** - The Original Fart Button  
**Status**: Ready to unleash chaos! 🎯💨😂
