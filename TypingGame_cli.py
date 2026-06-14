import requests
import random
import time
import os

url = 'https://www.mit.edu/~ecprice/wordlist.10000'

resposta = requests.get(url)
words = resposta.content.splitlines()

words = [word.decode('utf-8') for word in words]

game = input('Deseja iniciar, sim ou não? ')

while game != 'não':
  os.system('clear') or None
  if game == 'sim':
    sorted_words = input('Insira a quantia de palavras que você deseja: ')
    sorted_words_whole = int(sorted_words)
    random_words = random.sample(words, sorted_words_whole)

    pontos = 0
    tic = time.perf_counter()

    for word in random_words:
      print("\n", word)
      entrada = input()
      if entrada == word:
        pontos = pontos + 1

    toc = time.perf_counter()

    response_time = abs(tic - toc)
    time_actualized = (response_time * 10) // 10 

    print('Seus pontos foram: ' + str(pontos))
    print('Seu tempo foi de: ' + str(time_actualized) + ' segundos')
    game = input('\nDeseja iniciar, sim ou não? ')
  elif game == 'não':
    print('Tudo bem.')
    break
  else:
    print('Resposta inválida, digite sim ou não ')
    game = input('Deseja iniciar, sim ou não? ')