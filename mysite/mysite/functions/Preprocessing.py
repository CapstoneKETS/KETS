from kiwipiepy import Kiwi

kiwi = Kiwi(model_type='knlm')
kiwi.add_user_word('발락', 'NNP', 0)

print(*kiwi.analyze('손흥민의'), sep='\n')
