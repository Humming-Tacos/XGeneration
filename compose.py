import torch
print(torch.cuda.is_available())
from .task1_explicit.inference import inference
from .task2_explicit.harmonizer import generate_chord
from .task3_explicit.AccoMontage_inference import generate_acc


def compose(midi_path):
    print(torch.cuda.is_available())

    # task1
    task1_output = inference(midi_path)
    print(task1_output)

    # task2
    task2_output = generate_chord(task1_output)
    print(task2_output)

    # task3
    task3_output = generate_acc(task2_output)
    print(task3_output)

    return task3_output
