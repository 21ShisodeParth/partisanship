from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

text = "This horrendous movie couldn't be any worse, will never ever watch again. On the other hand, I absolutely adored one part of it!"

result = nlp.annotate(text,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })

print (result)



for s in result["sentences"]:
    print("{}: '{}': {}".format(
        s["index"],
        " ".join([t["word"] for t in s["tokens"]]),
        s["sentimentValue"], s["sentiment"]))
