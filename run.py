import torch
import json
from transformers import T5ForConditionalGeneration,T5Tokenizer

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
set_seed(42)
#using pretrained T5 model for paraphrase generation
model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_paraphraser')
tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_paraphraser')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print ("device ",device)
model = model.to(device)
#loading the json file with question answer pairs
f = open('faqdata.json',encoding="utf8")
jsondata = json.load(f)
para=[]
x=1
#Below for loop is used to iterate and take each question as input
for q in jsondata['data']:
    intent="question"+str(x)
    x+=1
    temp=[]
    sentence=q['ques']
    text =  "paraphrase: " + sentence + " </s>"
    max_len = 256
    encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    beam_outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        do_sample=True,
        max_length=256,
        top_k=120,
        top_p=0.98,
        early_stopping=True,
        num_return_sequences=10
    )

    print ("\nOriginal Question ::")
    print (sentence)
    print ("\n")
    print ("Paraphrased Questions :: ")
    final_outputs =[]
    for beam_output in beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        if sent.lower() != sentence.lower() and sent not in final_outputs:
            final_outputs.append(sent)
    for i, final_output in enumerate(final_outputs):
        print("{}: {}".format(i, final_output))
        new_output=final_output.replace("’","'")
        temp.append(new_output)
    #para is the list of dictionaries contains actual question and its paraphrases
    para.append({"intent":intent,"examples":temp})
print(para)
