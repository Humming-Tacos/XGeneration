from .preprocess_midi import preprocess
from .task1_explicit.inference import inference
from .task2_explicit.harmonizer import generate_chord

def compose(midi_path):
    preprocess_path = preprocess(midi_path)
    complete_melody_path = inference(preprocess_path)
    melody_cord_path = generate_chord(complete_melody_path)

    return melody_cord_path