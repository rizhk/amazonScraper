# Following pip packages need to be installed:
# !pip install git+https://github.com/huggingface/transformers sentencepiece datasets

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset
import loadText


processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

inputs = processor(text=loadText.TEXT, return_tensors="pt")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

max_length = 500
input_parts = []
audio_parts = []
input_torch = inputs["input_ids"]

print('input_torch.size():', input_torch.size())
input_torch_shape = inputs["input_ids"].shape[1]

if(inputs["input_ids"].shape[1] > max_length):
    input_parts = torch.split(inputs["input_ids"], max_length, dim=1)
    for part in input_parts:
        audio = model.generate_speech(part, speaker_embeddings, vocoder=vocoder)
        print('audio.size():', audio.size())
        audio_parts.append(audio)
    audio = torch.cat(audio_parts, dim=0)
else:
    audio = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)


sf.write("speech.wav", audio.numpy(), samplerate=16000)
