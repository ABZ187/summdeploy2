import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)


def get_response(input_text, num_return_sequences):
    batch = tokenizer.prepare_seq2seq_batch([input_text], truncation='only_first', padding='longest', max_length=60,
                                            return_tensors="pt").to(torch_device)
    translated = model.generate(**batch, max_length=120, num_beams=20, num_return_sequences=num_return_sequences,
                                temperature=1.5)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text


text = input("Paste your text: ")

get_response(text, 1)
