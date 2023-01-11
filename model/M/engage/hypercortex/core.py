from model.M.engage.hypercortex.alpha_sentinel import AlphaSentinel
from transformers import AutoModelForSeq2SeqLM as Model
from transformers import AutoTokenizer as Tokenizer
from model.M.super.reporter import Reporter
import logging
import time


log = logging.getLogger(__name__)


class Core:


    def __init__(self, admin, name):
        self.reporter  = Reporter(admin, name)
        self.admin     = admin
        self.reporter.report("Initializing HyperCortex (type-α) AI.")
        model          = "microsoft/GODEL-v1_1-base-seq2seq"
        self.model     = Model.from_pretrained(model)
        self.tokenizer = Tokenizer.from_pretrained(model, padding_side = "left")
        self.sentinel  = AlphaSentinel(admin, name)
        self.kwgs = {"max_length": 140, "min_length": 15, "top_p": 0.95, 
                "top_k": 0, "temperature": 0.80, "do_sample": True, 
                "pad_token_id": self.tokenizer.eos_token_id}


    def compose(self, uname, t_id, dialog, ptweet, knowledge, instruction, **k):
        if   self.sentinel.type_1(instruction):  return False
        elif self.sentinel.type_2():             return False
        elif self.sentinel.type_3(dialog, t_id): return False
        message = f"HyperCortext (type-α) AI is generating reply to {uname}."
        self.reporter.report(message)
        while True:
            tensor     = self.get_tensor(knowledge, instruction, dialog)
            generation = self.model.generate(tensor, **self.kwgs)
            response   = self.decode(generation); time.sleep(3)
            if   self.sentinel.type_4(response):         continue
            elif self.sentinel.type_5(response):         continue
            elif self.sentinel.type_6(response, ptweet): continue
            else:                                        break
        return response


    def get_tensor(self, knowledge, instruction, dialog):
        if knowledge: knowledge = f"[KNOWLEDGE] {knowledge}"
        dialog = " EOS ".join(dialog)
        query  = f"{instruction} [CONTEXT] {dialog} {knowledge}"
        tensor = self.tokenizer(f"{query}", return_tensors = "pt").input_ids
        return tensor


    def decode(self, generation):
        return self.tokenizer.decode(generation[0], skip_special_tokens = True)
