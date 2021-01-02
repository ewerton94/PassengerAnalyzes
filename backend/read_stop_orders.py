from core.models import * 
import pandas as pd  
linhas_por_numero = {l.numero: l for l in Linha.objects.all()}
empresa_por_numero_linha = {l.numero: l.empresa_id for l in Linha.objects.all()}
pontos_por_codigo = {(p.codigo_cittamobi, p.empresa_id): p.ponto for p in PontoPorEmpresa.objects.select_related().all()}
legenda_contexto = '200'
df = pd.read_pickle('../Resultados/'+legenda_contexto+'/stops .zip', compression='zip')
dic = df.to_dict('index')
dic = {('%03i'%int(k[0]), k[1], k[2]): [e for e in list(v.values()) if not e is None] for k,v in dic.items()}
ordens = []
for key, pontos in dic.items():
    for i, ponto in enumerate(pontos):
        try:
        
            ordens.append(
                OrdemPontosLinha(
                    linha = linhas_por_numero[str(key[0])],
                    ponto = pontos_por_codigo[(ponto, empresa_por_numero_linha[str(key[0])])],
                    ordem = i + 1,
                    atendimento = key[1],
                    sentido = key[2],
                )
            )
        except:
            print((ponto, str(key[0])))


OrdemPontosLinha.objects.bulk_create(ordens)

