# Greeting Injector

The Greeting Injector is a Python utility designed to overlay pre-recorded greetings or sounds into live audio streams on virtual audio devices.

## Features

- **Audio Mirroring**: The greeting can be played through the output device to allow for real-time monitoring.
- **Device Monitoring**: Default audio devices are automatically detected and selected for playback and recording.

## Installation

```bash
git clone https://github.com/dansam8/greeting_injector.git
cd greeting_injector
pip install .
```

## Setting up the virtual audio device

### MacOS

`brew install blackhole-2ch`

Navigate to `Audio MIDI Setup` and create a new aggregate device called `mycrophone` with the following inputs:
- Built-in Microphone
- BlackHole 2ch

## Usage

### Recording a Greeting
To record audio, run:

```bash Copy code
greeting_injector record
```

Follow the prompts to start and stop recording.

### Playing a Greeting
To play the greeting:

```bash Copy code
greeting_injector greet --mirror-audio=[true|false]
```
- --mirror-audio: Set too false to disable playback through the feedback device. Default is true.
Press Enter to play the greeting. Use Ctrl+C to exit.
