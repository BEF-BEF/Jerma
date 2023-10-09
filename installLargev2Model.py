# this code can be ran to automatically install large-v2 model so we can transcribe with maximum quality

from faster_whisper import WhisperModel

  

model_size = "large-v2"

model = WhisperModel(model_size, device="cuda", compute_type="float16")

model_size = "medium"

model = WhisperModel(model_size, device="cuda", compute_type="float16")