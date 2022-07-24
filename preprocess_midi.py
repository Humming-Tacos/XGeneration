import pretty_midi
import math


def clamp_midi_data(input_midi_data: pretty_midi.PrettyMIDI):
    tempo = input_midi_data.get_tempo_changes()[1][0]

    original_end_time = input_midi_data.instruments[0].notes[-1].end
    # end_time -> beats
    original_end_beat = (original_end_time/60)*tempo

    end_time = math.ceil((60/tempo)*original_end_beat/2)*2
    # extends first and last note to the end
    input_midi_data.instruments[0].notes[0].start = 0
    input_midi_data.instruments[0].notes[-1].end = end_time
    
def quantize_midi_data(input_midi_data: pretty_midi.PrettyMIDI):
    tempo = input_midi_data.get_tempo_changes()[1][0]

    def quantize(time):
        beat = round((time / 60) * tempo * 8) / 8
        new_time = ((beat/tempo) * 60)
        return new_time

    delete_notes_index = []

    for i, note in enumerate(input_midi_data.instruments[0].notes):
        note.start = quantize(note.start)
        note.end = quantize(note.end)
        if i != 0:
            if note.start == input_midi_data.instruments[0].notes[i-1].start:
                # choose longest => choose last end
                if note.end > input_midi_data.instruments[0].notes[i-1].end:
                    delete_notes_index.append(i-1)
                else:
                    delete_notes_index.append(i)
            elif note.start >= input_midi_data.instruments[0].notes[i-1].start and note.start < input_midi_data.instruments[0].notes[i-1].end:
                input_midi_data.instruments[0].notes[i-1].end = note.start

    input_midi_data.instruments[0].notes = [
        note for i, note in enumerate(input_midi_data.instruments[0].notes) if i not in delete_notes_index
    ]

def _print_notes(input_midi_data: pretty_midi.PrettyMIDI):
    for note in input_midi_data.instruments[0].notes:
        print(note)

def preprocess(input_midi_path):
    input_midi_data = pretty_midi.PrettyMIDI(input_midi_path)

    _print_notes(input_midi_data)

    clamp_midi_data(input_midi_data)

    quantize_midi_data(input_midi_data)

    _print_notes(input_midi_data)

    # write midi data
    output_midi_path = ''.join(input_midi_path.split('.')[:-1])+'_preprocessed.mid'
    print(output_midi_path)
    input_midi_data.write(output_midi_path)

    return output_midi_path 