import os
import re
import sys


DAMPING = 0.85
SAMPLES = 10000


def crawl(directory : str) -> dict:
    '''
        return a dictionary where each key is a page, and values are a list of all other pages in the corpus that are linked to by the page.
    '''

    pages = {}

    # extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as filename:
            content = filename.read()
            links = re.findall(r'<a\s+(?:[^>]*?)href="([^"]*)"', content)
            pages[filename] = set(links) - {filename}

    # only include links to other pages in the corpus  
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus : dict, page : str, damping_factor : float):
    '''
        return a probability distribution over which page to visit next, given a current page.
    '''
   resultado={}
   M = len(corpus)
   for aleatorio in corpus :
    resultado[aleatorio]= ((1-damping_factor)/M)
   if len(corpus[page]) > 0:
       N = len(corpus[page])
       for link in corpus[page]:
           resultado[link] += damping_factor/N
   else:
        for aleatorio in corpus:
            resultado[aleatorio] = 1 / M
    
   return resultado
    
raise NotImplementedError


def sample_pagerank(corpus : dict, damping_factor : float, n : int) -> dict:
    '''
        return PageRank values for each page by sampling `n` pages according to transition model, starting with a page at random.
    '''
   visitas={}
   visitas = {page:0 for page in corpus}


   paginas = list(corpus)
   pagina_atual = random.choice(paginas)
   for i in range(n):
       dist_prob = transition_model(corpus, pagina_atual, damping_factor)
       prox_pagina = random.choices(list(dist_prob.keys()), weights=dist_prob.values())[0]
       visitas[prox_pagina] += 1
       pagina_atual = prox_pagina
  
   total_visitas = sum(visitas.values())
   for page in visitas:
             # =         visitas[page]/ total visitas
        visitas[page] /= total_visitas
   return visitas

    raise NotImplementedError


def iterate_pagerank(corpus : dict, damping_factor : float) -> dict:
    '''
        return PageRank values for each page by iteratively updating PageRank values until convergence.
    '''
    n = len(corpus)
    tolerance = 0.001  # quanto maior, menos precisão; quanto menor, mais precisão 
    convergencia = False  # "convergencia" ela só vai mudar quando a diferença entre os valores for menor que a tolerância 
    ranksAnterior = {page: 1 / n for page in corpus}  # Inicializa ranks com o valorinicial antes da iteração 
    while not convergencia:
        rankAtual = {}        
        convergencia = True       
        for page in corpus:
            contador = 0             
            for other_page in corpus:  # other_page é tipo uma variável que se refere às outras páginas sem ser a atual
                if page in corpus[other_page]:  # isso aqui serve para saber se em outras páginas tem link para a página atual
                    contador += ranksAnterior[other_page] / len(corpus[other_page])
            rankAtual[page] = (1 - damping_factor) / n + damping_factor * contador
        for page in ranksAnterior:
           if abs(rankAtual[page] - ranksAnterior[page]) > tolerance:
            convergencia = False
        ranksAnterior = rankAtual
    return ranksAnterior

    raise NotImplementedError


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank results from sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")    

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank results from iteration")    
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")  
