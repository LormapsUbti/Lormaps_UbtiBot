from transformers import GPT2Tokenizer, GPT2LMHeadModel
import config
import csv
import pandas as pd
from behavior import Horoscope


def get_model_answer():
    if len(Horoscope.Horoscope.data) < 12:
        sign_new = [sign.split()[0] for sign in config.zodiac_signs]
        if len(Horoscope.Horoscope.data) == 0:
            sign_name = sign_new[0]
        else:
            sign_name = list(set(sign_new) - set(Horoscope.Horoscope.data.Sign.unique()))[0]
    else:
        sign_name = 'random'

    tok = GPT2Tokenizer.from_pretrained("models/res_iter2")
    model = GPT2LMHeadModel.from_pretrained("models/res_iter2")
    model.cuda()

    text = 'Гороскоп: '
    inpt = tok.encode(text, return_tensors="pt")

    out = model.generate(inpt.cuda(), min_length=200, max_length=300, do_sample=True, top_k=2,
                         top_p=0.90, temperature=0.7, no_repeat_ngram_size=3)

    predict = str(tok.decode(out[0]).split('Гороскоп:')[1].split('\n')[0])

    with open('data/Horoscope_data.csv', 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([sign_name, predict])

    Horoscope.Horoscope.data = pd.read_csv('data/Horoscope_data.csv', sep=';')
    print(f"len(Horoscope.data[{sign_name}]) === ",
          len(Horoscope.Horoscope.data))
