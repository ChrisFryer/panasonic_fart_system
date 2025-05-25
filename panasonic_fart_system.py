#!/usr/bin/env python3
"""
Simple IR Signal Detector
Just captures the first part of the signal and ignores the rest
"""

from gpiozero import Button
import time
import os
import random
import subprocess

# Setup IR sensor
ir_sensor = Button(4, pull_up=True)

# Storage for button 1 pattern and fart recordings
button_1_pattern = None
fart_recordings = []
FART_DIR = "fart_sounds"

print("🎯 SIMPLE IR SIGNAL DETECTOR")
print("📱 Captures just the first part of IR signals")
print("💨 Makes fart noises when button 1 is pressed!")
print("🎙️  Can record your own custom fart sounds!")
print("=" * 50)

def setup_fart_directory():
    """Create directory for fart sound recordings"""
    if not os.path.exists(FART_DIR):
        os.makedirs(FART_DIR)
        print(f"📁 Created {FART_DIR} directory for your fart collection!")

def record_fart_sound():
    """Record a custom fart sound"""
    print("\n🎙️  FART SOUND RECORDING STUDIO")
    print("=" * 40)
    
    # Check if arecord is available
    try:
        subprocess.run(["which", "arecord"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ Audio recording not available (arecord not found)")
        print("💡 Install with: sudo apt install alsa-utils")
        return False
    
    fart_name = input("🎭 Enter a name for your fart sound: ").strip()
    if not fart_name:
        fart_name = f"fart_{len(fart_recordings) + 1}"
    
    # Clean filename
    safe_name = "".join(c for c in fart_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{FART_DIR}/{safe_name}.wav"
    
    print(f"\n🎙️  Get ready to record '{fart_name}'!")
    print("📋 Instructions:")
    print("   1. Get into position 🍑")
    print("   2. Press ENTER when ready")
    print("   3. You'll have 5 seconds to make your fart")
    print("   4. Recording will stop automatically")
    
    input("Press ENTER when ready to record...")
    
    print("\n🔴 RECORDING in 3...")
    time.sleep(1)
    print("🔴 RECORDING in 2...")
    time.sleep(1)  
    print("🔴 RECORDING in 1...")
    time.sleep(1)
    print("🎙️  RECORDING NOW! Let it rip! 💨")
    
    try:
        # Record 5 seconds of audio with correct parameters
        subprocess.run([
            "arecord", 
            "-f", "S16_LE",       # 16-bit signed little endian format
            "-c", "1",            # Mono (1 channel)
            "-r", "44100",        # Sample rate 44.1kHz
            "-d", "5",            # Duration: 5 seconds
            filename
        ], check=True)
        
        print("✅ Recording complete!")
        print(f"💾 Saved as: {filename}")
        
        # Test playback
        play_choice = input("🔊 Want to test your fart? (y/n): ").lower()
        if play_choice == 'y':
            play_fart_sound(filename)
        
        # Add to collection
        fart_recordings.append({
            'name': fart_name,
            'filename': filename,
            'size': os.path.getsize(filename) if os.path.exists(filename) else 0
        })
        
        print(f"🎉 '{fart_name}' added to your fart collection!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Recording failed: {e}")
        print("💡 Try checking your microphone settings with: arecord -l")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  Recording cancelled")
        return False

def play_fart_sound(filename):
    """Play a fart sound file"""
    try:
        # Try different audio players
        players = ["aplay", "paplay", "play"]
        
        for player in players:
            try:
                subprocess.run(["which", player], check=True, capture_output=True)
                print(f"🔊 Playing fart with {player}...")
                subprocess.run([player, filename], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                continue
        
        print("❌ No audio player found")
        return False
        
    except Exception as e:
        print(f"❌ Playback failed: {e}")
        return False

def load_existing_fart_sounds():
    """Load any existing fart recordings"""
    global fart_recordings
    
    if not os.path.exists(FART_DIR):
        return
    
    for filename in os.listdir(FART_DIR):
        if filename.endswith('.wav'):
            filepath = os.path.join(FART_DIR, filename)
            name = filename.replace('.wav', '')
            fart_recordings.append({
                'name': name,
                'filename': filepath,
                'size': os.path.getsize(filepath)
            })
    
    if fart_recordings:
        print(f"🎵 Loaded {len(fart_recordings)} existing fart sounds!")

def list_fart_collection():
    """Show all recorded fart sounds"""
    if not fart_recordings:
        print("📂 No fart sounds recorded yet!")
        return
    
    print(f"\n🎵 YOUR FART SOUND COLLECTION ({len(fart_recordings)} sounds):")
    print("-" * 50)
    
    for i, fart in enumerate(fart_recordings, 1):
        size_kb = fart['size'] / 1024
        print(f"   {i:2d}. {fart['name']} ({size_kb:.1f}KB)")
    
    print("-" * 50)

def fart_sound_menu():
    """Interactive menu for fart sound management"""
    while True:
        print(f"\n🎙️  FART SOUND STUDIO")
        print("=" * 30)
        print("1. 🎙️  Record new fart sound")
        print("2. 🎵 List fart collection")
        print("3. 🔊 Test play a fart sound")
        print("4. 🗑️  Delete a fart sound")
        print("5. ⬅️  Back to main menu")
        
        choice = input("\nChoose option (1-5): ").strip()
        
        if choice == '1':
            record_fart_sound()
        elif choice == '2':
            list_fart_collection()
        elif choice == '3':
            if fart_recordings:
                list_fart_collection()
                try:
                    idx = int(input("Enter number to play: ")) - 1
                    if 0 <= idx < len(fart_recordings):
                        play_fart_sound(fart_recordings[idx]['filename'])
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Please enter a number")
            else:
                print("📂 No fart sounds to play!")
        elif choice == '4':
            if fart_recordings:
                list_fart_collection()
                try:
                    idx = int(input("Enter number to delete: ")) - 1
                    if 0 <= idx < len(fart_recordings):
                        fart = fart_recordings[idx]
                        confirm = input(f"Delete '{fart['name']}'? (y/n): ").lower()
                        if confirm == 'y':
                            os.remove(fart['filename'])
                            fart_recordings.pop(idx)
                            print(f"🗑️  Deleted '{fart['name']}'!")
                    else:
                        print("❌ Invalid number")
                except ValueError:
                    print("❌ Please enter a number")
            else:
                print("📂 No fart sounds to delete!")
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice!")

def make_fart_noise():
    """Play custom recorded fart sounds or fallback to text effects"""
    
    # First try to play a custom recorded fart sound
    if fart_recordings:
        chosen_fart = random.choice(fart_recordings)
        print(f"🎵 Playing recorded fart: '{chosen_fart['name']}'")
        
        if play_fart_sound(chosen_fart['filename']):
            # Successfully played custom fart
            stinky_messages = [
                f"🤢 Ewww! That '{chosen_fart['name']}' was rank!",
                f"🤮 That '{chosen_fart['name']}' is disgusting!",
                f"😷 Quick! '{chosen_fart['name']}' cleared the room!",
                f"🌪️ '{chosen_fart['name']}' - TOXIC GAS ALERT! 🚨",
                f"💀 That '{chosen_fart['name']}' is lethal!",
                f"🦨 '{chosen_fart['name']}' - skunk-level stench!",
                f"🔥 '{chosen_fart['name']}' burned my nostrils!"
            ]
            print(random.choice(stinky_messages))
            return
    
    # Fallback to text-based farts if no recordings or playback failed
    print("💨 No custom farts available - using classic text farts!")
    
    # Different fart types with their own animations
    fart_types = [
        {
            'name': 'Classic Long Fart',
            'animation': [
                "💨 p...",
                "💨 pf...", 
                "💨 pff...",
                "💨 pfff...",
                "💨 pfffr...",
                "💨 pfffrr...",
                "💨 pfffrrr...",
                "💨 pfffrrrr...",
                "💨 PFFFRRRRT!",
                "💨 PFFFRRRRTTT!",
                "💨 💨 💨"
            ],
            'final': "💨 PPPFFFFRRRRRTTTTTT!"
        },
        {
            'name': 'Squeaky Fart',
            'animation': [
                "💨 *squeak*",
                "💨 *SQUEAK*",
                "💨 *squeeeeak*",
                "💨 pf-SQUEAK!",
                "💨 PFFFFFT!"
            ],
            'final': "💨 *squeak* PFFFFFT!"
        },
        {
            'name': 'Bubbly Fart',
            'animation': [
                "💨 blub...",
                "💨 blub blub...",
                "💨 BLUB BLUB...",
                "💨 BLUB-PFFFT!",
                "💨 PFFFT-BLUB-PFFFT!"
            ],
            'final': "💨 BLUB-BLUB-PFFFFFFFFT!"
        },
        {
            'name': 'Machine Gun Fart',
            'animation': [
                "💨 pft",
                "💨 pft-pft",
                "💨 pft-pft-pft",
                "💨 PFT-PFT-PFT",
                "💨 PFT-PFT-PFT-PFT",
                "💨 PFTPFTPFTPFT!"
            ],
            'final': "💨 PFFT-PFFT-PFFFFFFFFT!"
        },
        {
            'name': 'Wet Fart',
            'animation': [
                "💨 splt...",
                "💨 splrt...",
                "💨 SPLRT...",
                "💨 SPLRRRT...",
                "💨 SPLLLURT!"
            ],
            'final': "💨 *wet fart* SPLLLLLURT!"
        }
    ]
    
    # Pick a random fart type
    chosen_fart = random.choice(fart_types)
    
    print(f"🎬 {chosen_fart['name']} incoming...")
    time.sleep(0.3)
    
    # Play the animation
    for frame in chosen_fart['animation']:
        print(f"\r{frame:<30}", end="", flush=True)
        time.sleep(0.15)
    
    print()  # New line
    
    # Final dramatic fart sound
    print("🔊 " + chosen_fart['final'])
    
    # Add some visual effects
    effects = [
        "💨💨💨 *STINK CLOUD* 💨💨💨",
        "🌪️ *TOXIC WIND* 🌪️",
        "☁️💨 *FART FOG* 💨☁️",
        "💨🌊 *GAS WAVE* 🌊💨"
    ]
    
    print(random.choice(effects))
    
    # Stinky aftermath messages
    stinky_messages = [
        "🤢 Ewww! That's rank!",
        "🤮 That's absolutely disgusting!",
        "😷 Quick! Open all the windows!",
        "🌪️ TOXIC GAS ALERT! 🚨",
        "🧄 Smells like rotten eggs and sulfur!",
        "💀 That's lethal! Call hazmat!",
        "🚨 EVACUATE THE AREA! 🚨",
        "🤧 *cough cough* Can't breathe!",
        "🦨 That's skunk-level stench!",
        "🔥 My nostrils are on fire!",
        "🧪 That violated the Geneva Convention!",
        "👻 Something died in here!"
    ]
    
    time.sleep(0.5)
    print(random.choice(stinky_messages))
    
    # Final dramatic pause
    print("...")
    time.sleep(0.5)
    print("💨 *lingering stench* 💨")
    time.sleep(0.3)

def record_first_signal_only():
    """Record only the first part of the IR signal"""
    # Wait for signal to start
    timeout = time.time() + 5.0
    while ir_sensor.is_pressed and time.time() < timeout:
        time.sleep(0.01)
    
    if time.time() >= timeout:
        return None
    
    print("🔴 Signal started, recording first 200ms only...")
    
    packets = []
    start_time = time.time()
    last_state = ir_sensor.is_pressed
    last_change = start_time
    
    # Only record for 200ms - this captures the actual IR data
    while time.time() - start_time < 0.2:  # Just 200ms!
        current_state = ir_sensor.is_pressed
        current_time = time.time()
        
        if current_state != last_state:
            duration = (current_time - last_change) * 1000
            if duration > 0.1:
                packets.append((0 if last_state else 1, duration))
                last_change = current_time
                last_state = current_state
        
        time.sleep(0.0001)
    
    # Add final pulse
    if packets:
        final_duration = (time.time() - last_change) * 1000
        if final_duration > 0.1:
            packets.append((0 if last_state else 1, final_duration))
    
    total_duration = sum(d for _, d in packets)
    print(f"🔴 Captured {len(packets)} pulses in {total_duration:.0f}ms")
    return packets

def create_simple_fingerprint(packets):
    """Create very simple fingerprint"""
    if not packets or len(packets) < 5:
        return None
    
    total_duration = sum(duration for _, duration in packets)
    
    # Accept any reasonable signal
    if total_duration < 10:
        return None
    
    # Just use the first few pulses as the pattern
    key_pulses = []
    for i, (state, duration) in enumerate(packets[:20]):  # First 20 pulses only
        # Round duration to 5ms buckets for tolerance
        rounded_duration = round(duration / 5) * 5
        key_pulses.append((state, rounded_duration))
    
    return {
        'total_duration': round(total_duration / 10) * 10,  # 10ms buckets
        'total_pulses': round(len(packets) / 5) * 5,        # 5-pulse buckets
        'key_pulses': key_pulses
    }

def simple_match(pattern1, pattern2):
    """Very simple pattern matching"""
    if not pattern1 or not pattern2:
        return False
    
    # Very loose duration check (±100ms)
    dur_diff = abs(pattern1['total_duration'] - pattern2['total_duration'])
    if dur_diff > 100:
        return False
    
    # Very loose pulse count check (±50 pulses)
    pulse_diff = abs(pattern1['total_pulses'] - pattern2['total_pulses'])
    if pulse_diff > 50:
        return False
    
    # Compare first few key pulses
    pulses1 = pattern1['key_pulses']
    pulses2 = pattern2['key_pulses']
    
    min_len = min(len(pulses1), len(pulses2), 10)  # Only compare first 10
    matches = 0
    
    for i in range(min_len):
        state1, dur1 = pulses1[i]
        state2, dur2 = pulses2[i]
        
        # Match if same state and duration within 20ms
        if state1 == state2 and abs(dur1 - dur2) <= 20:
            matches += 1
    
    # Need at least 50% match on first pulses
    similarity = matches / min_len if min_len > 0 else 0
    return similarity >= 0.5

def learn_button_1_simple():
    """Learn button 1 with simple approach"""
    print("\n🎓 Learning Button 1 (Simple Mode)...")
    print("📋 Press button '1' quickly 3 times")
    print("📋 Only the first 200ms of each press will be used\n")
    
    samples = []
    
    for attempt in range(3):
        print(f"⏳ Attempt {attempt + 1}/3 - Press button '1'...")
        
        packets = record_first_signal_only()
        if packets:
            fingerprint = create_simple_fingerprint(packets)
            
            if fingerprint:
                samples.append(fingerprint)
                print(f"✅ Sample {attempt + 1}: {fingerprint['total_pulses']} pulses, {fingerprint['total_duration']}ms")
            else:
                total_duration = sum(d for _, d in packets) if packets else 0
                print(f"❌ Invalid: {len(packets)} pulses, {total_duration:.0f}ms")
        else:
            print(f"❌ No signal")
        
        if attempt < 2:
            time.sleep(2)
    
    # Use any valid sample as the pattern
    global button_1_pattern
    
    if samples:
        button_1_pattern = samples[0]  # Just use the first valid sample
        print(f"\n🎉 Button 1 learned!")
        print(f"📊 Using pattern: {button_1_pattern['total_pulses']} pulses, {button_1_pattern['total_duration']}ms")
        print(f"📊 Key pulses: {len(button_1_pattern['key_pulses'])}")
        return True
    else:
        print(f"\n❌ No valid samples captured")
        return False

def start_simple_detection():
    """Start simple detection"""
    print("\n🔍 Simple Detection Started!")
    print("📱 Press button '1' to trigger detection")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 40)
    
    detection_count = 0
    signal_count = 0
    last_detection = 0
    
    print(f"📝 Learned pattern: {button_1_pattern['total_pulses']} pulses, {button_1_pattern['total_duration']}ms")
    print()
    
    def on_signal():
        nonlocal detection_count, signal_count, last_detection
        
        # Debounce
        current_time = time.time()
        if current_time - last_detection < 0.5:
            return
        
        signal_count += 1
        print(f"\n📡 Signal #{signal_count}...")
        
        packets = record_first_signal_only()
        if packets:
            fingerprint = create_simple_fingerprint(packets)
            
            if fingerprint:
                print(f"   Current: {fingerprint['total_pulses']} pulses, {fingerprint['total_duration']}ms")
                print(f"   Learned: {button_1_pattern['total_pulses']} pulses, {button_1_pattern['total_duration']}ms")
                
                if simple_match(fingerprint, button_1_pattern):
                    detection_count += 1
                    last_detection = current_time
                    print(f"✅ BUTTON 1 MATCH! (#{detection_count})")
                    print("🎯 Button 1 is being pressed!")
                    
                    # Make a fart noise! 💨
                    make_fart_noise()
                    
                else:
                    print(f"❓ No match")
                    
                    # Show detailed comparison for debugging
                    dur_diff = abs(fingerprint['total_duration'] - button_1_pattern['total_duration'])
                    pulse_diff = abs(fingerprint['total_pulses'] - button_1_pattern['total_pulses'])
                    print(f"   Duration diff: {dur_diff}ms (limit: 100ms)")
                    print(f"   Pulse diff: {pulse_diff} (limit: 50)")
                    
            else:
                total_duration = sum(d for _, d in packets) if packets else 0
                print(f"   Invalid: {len(packets)} pulses, {total_duration:.0f}ms")
        else:
            print(f"   No signal captured")
    
    ir_sensor.when_pressed = on_signal
    
    try:
        while True:
            print(f"⏳ Listening... (Matches: {detection_count}, Total: {signal_count})", end='\r')
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n\n🛑 Detection stopped")
        print(f"📊 Results:")
        print(f"   🎯 Button 1 matches: {detection_count}")
        print(f"   📡 Total signals: {signal_count}")
        if signal_count > 0:
            print(f"   📈 Success rate: {detection_count/signal_count*100:.1f}%")

def main():
    try:
        # Setup
        setup_fart_directory()
        load_existing_fart_sounds()
        
        # Main menu
        while True:
            print(f"\n🎯 PANASONIC FART BUTTON SYSTEM")
            print("=" * 40)
            print("1. 🎓 Learn Button 1 pattern")
            print("2. 🔍 Start fart button detection")
            print("3. 🎙️  Fart Sound Studio")
            print("4. 👋 Exit")
            
            choice = input("\nChoose option (1-4): ").strip()
            
            if choice == '1':
                learn_button_1_simple()
            elif choice == '2':
                if button_1_pattern:
                    print("\n" + "="*50)
                    start_simple_detection()
                else:
                    print("❌ Please learn button 1 pattern first!")
            elif choice == '3':
                fart_sound_menu()
            elif choice == '4':
                print("👋 Thanks for using the Fart Button System!")
                break
            else:
                print("❌ Invalid choice!")
                
    except KeyboardInterrupt:
        print(f"\n\n👋 Goodbye!")

if __name__ == "__main__":
    main()