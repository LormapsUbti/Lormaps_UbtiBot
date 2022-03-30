from transformers import GPT2Tokenizer, GPT2LMHeadModel


def get_model_answer():
    tok = GPT2Tokenizer.from_pretrained("/VVEDI/SVOI/PUT")
    model = GPT2LMHeadModel.from_pretrained("/VVEDI/SVOI/PUT")
    model.cuda()

    text = '<s>Гороскоп:</s>'
    input = tok.encode(text, return_tensors="pt")

    out = model.generate(input.cuda(), max_length=100, repetition_penalty=5.0, do_sample=True, top_k=5, top_p=0.95,
                         temperature=0.7)
    return tok.decode(out[0])
