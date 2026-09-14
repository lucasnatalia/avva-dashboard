import json, math, re, unicodedata
import pandas as pd

SRC = '/Users/natalialucas/Downloads/opps_avva.xlsx'
AVVA = (-27.5947, -48.5566)  # Rua Felipe Schmidt, 869, Centro, Florianópolis
HOJE = pd.Timestamp('2026-09-14')

PRECO = {'AVVA Essencial': 1500, 'AVVA Personal Trio': 1800, 'AVVA Personal Duo': 2400, 'AVVA Personal Uno': 2800}

# centróides aproximados (bairro na Grande Florianópolis, cidade no resto)
BAIRRO = {
 ('Florianópolis','Centro'):(-27.5960,-48.5490), ('Florianópolis','Agronômica'):(-27.5790,-48.5420),
 ('Florianópolis','Itacorubi'):(-27.5830,-48.5030), ('Florianópolis','Córrego Grande'):(-27.5960,-48.5060),
 ('Florianópolis','Trindade'):(-27.5880,-48.5230), ('Florianópolis','Campeche'):(-27.6830,-48.4870),
 ('Florianópolis','Capoeiras'):(-27.5930,-48.5890), ('Florianópolis','Carianos'):(-27.6620,-48.5390),
 ('Florianópolis','Coqueiros'):(-27.6040,-48.5790), ('Florianópolis','Rio Vermelho'):(-27.4990,-48.4200),
 ('Florianópolis','Vargem Grande'):(-27.4550,-48.4450), ('Florianópolis','Tapera da Base'):(-27.6960,-48.5580),
 ('Florianópolis','Rio Tavares'):(-27.6480,-48.4850), ('Florianópolis','Costeira do Pirajubaé'):(-27.6320,-48.5220),
 ('Florianópolis','Ribeirão da Ilha'):(-27.7200,-48.5620), ('Florianópolis','Monte Cristo'):(-27.5850,-48.5900),
 ('Florianópolis','Lagoa da Conceição'):(-27.6010,-48.4680), ('Florianópolis','Jurerê Internacional'):(-27.4400,-48.4950),
 ('Florianópolis','Jurerê'):(-27.4380,-48.5010), ('Florianópolis','João Paulo'):(-27.5610,-48.5080),
 ('Florianópolis','Jardim Atlântico'):(-27.5820,-48.5920), ('Florianópolis','Itaguaçu'):(-27.6090,-48.5840),
 ('Florianópolis','Balneário'):(-27.5880,-48.5760), ('Florianópolis','Abraão'):(-27.6100,-48.5880),
 ('São José','Barreiros'):(-27.5750,-48.6150), ('São José','Campinas'):(-27.5960,-48.6120),
 ('São José','Sertão do Maruim'):(-27.5750,-48.6700), ('São José','Areias'):(-27.5690,-48.6310),
 ('São José','Serraria'):(-27.6180,-48.6470), ('São José','Praia Comprida'):(-27.5850,-48.6200),
 ('São José','Nossa Senhora do Rosário'):(-27.6000,-48.6300), ('São José','Ipiranga'):(-27.5700,-48.6300),
 ('São José','Bosque das Mansões'):(-27.6050,-48.6150),
 ('Palhoça','Centro'):(-27.6450,-48.6700), ('Palhoça','Enseada do Brito (Ens Brito)'):(-27.7750,-48.6250),
 ('Palhoça','Pagani'):(-27.6380,-48.6660), ('Palhoça','Pedra Branca'):(-27.6280,-48.6800),
 ('Biguaçu','Centro'):(-27.4940,-48.6580), ('Biguaçu','Beira Rio'):(-27.4900,-48.6500),
}
CIDADE = {
 'Florianópolis':(-27.60,-48.52),'São José':(-27.59,-48.62),'Palhoça':(-27.64,-48.67),'Biguaçu':(-27.49,-48.66),
 'Orleans':(-28.359,-49.291),'Itapema':(-27.090,-48.611),'Itajaí':(-26.908,-48.662),'Blumenau':(-26.919,-49.066),
 'Balneário Camboriú':(-26.991,-48.635),'Camboriú':(-27.025,-48.654),'Brusque':(-27.098,-48.917),
 'Joinville':(-26.304,-48.846),'Chapecó':(-27.100,-52.615),'São João do Sul':(-29.223,-49.809),'Angelina':(-27.570,-48.987),
 'São Paulo':(-23.550,-46.633),'São Caetano do Sul':(-23.623,-46.551),'Rio Claro':(-22.411,-47.561),'Campinas':(-22.906,-47.061),
 'Praia Grande':(-24.006,-46.402),'Porto Alegre':(-30.035,-51.217),'Novo Hamburgo':(-29.678,-51.130),'Erechim':(-27.634,-52.274),
 'Rio de Janeiro':(-22.907,-43.173),'Duque de Caxias':(-22.785,-43.311),'Cabo Frio':(-22.879,-42.019),
 'Rondonópolis':(-16.470,-54.635),'Sorriso':(-12.545,-55.711),'Porto Seguro':(-16.444,-39.065),
 'Vitória da Conquista':(-14.866,-40.839),'Juazeiro':(-9.416,-40.503),'Recife':(-8.048,-34.877),'Vila Velha':(-20.329,-40.292),
 'Cachoeiro de Itapemirim':(-20.849,-41.113),'Uberlândia':(-18.919,-48.277),'Belo Horizonte':(-19.917,-43.934),
 'Ananindeua':(-1.365,-48.372),'Maringá':(-23.421,-51.933),'Brasília':(-15.827,-47.922),'Boa Vista':(2.820,-60.671),
 'Aracaju':(-10.947,-37.073),'Cabedelo':(-6.981,-34.834),
}
GRANDE_FLORIPA = {'Florianópolis','São José','Palhoça','Biguaçu'}

def km(a, b):
    R = 6371; la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

def bearing(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    y = math.sin(lo2-lo1)*math.cos(la2)
    x = math.cos(la1)*math.sin(la2) - math.sin(la1)*math.cos(la2)*math.cos(lo2-lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

MASC = set('arthur mateus carlos vinicius felipe paulo lucas thiago andre andré pedro bruno francisco ronaldo edilson everton brayan flavio marco henrique lincoln cairo michel gusttavo gabriel dionizio mozart yago will olivio guilherme nathan jeferson luciano renan daniel joao gustavo rodrigo evandro tiago rafael yuri ruan adriao benjamin kelvin kaua klaus'.split())
INDEF = set('elian evanir liarlei dodi cris a verbalize'.split())
FEM_EXTRA = set('dra ingrid isabel thays keren carol'.split())

def genero(nome):
    n = str(nome).strip().split()[0].lower() if str(nome).strip() else ''
    if n in INDEF or not n: return 'Indefinido'
    if n in MASC: return 'Masculino'
    if n in FEM_EXTRA or n[-1] in 'aeyln': return 'Feminino'
    return 'Indefinido'

def s(x):
    return None if pd.isna(x) else str(x).strip()

df = pd.read_excel(SRC)
leads = []
for _, r in df.iterrows():
    cel = s(r['Celular']) or ''
    dig = re.sub(r'\D', '', cel)
    m = re.match(r'\((\d\d)\)', cel)
    ddd = m.group(1) if m else None
    tel_status = 'ok'
    ddd_real = ddd
    if len(dig) != 11 or not m:
        tel_status = 'invalido' if not (len(dig) > 11 and not m) else 'internacional'
    elif ddd == '55' and dig[2] != '9':
        tel_status = 'ddi_no_ddd'; ddd_real = dig[2:4]
    cidade, bairro, uf, cep = s(r['Cidade']), s(r['Bairro']), s(r['UF']), s(r['CEP'])
    coord, precisao = None, None
    if cidade and (cidade, bairro) in BAIRRO:
        coord, precisao = BAIRRO[(cidade, bairro)], 'bairro'
    elif cidade in CIDADE:
        coord, precisao = CIDADE[cidade], 'cidade'
    elif cep and cep.startswith('880'):
        coord, precisao, cidade, uf = CIDADE['Florianópolis'], 'cep', 'Florianópolis (pelo CEP)', 'SC'
    dist = round(km(AVVA, coord), 1) if coord else None
    ang = round(bearing(AVVA, coord)) if coord else None

    if dist is not None:
        if dist <= 3: faixa = 'Até 3 km'
        elif dist <= 8: faixa = '3 a 8 km'
        elif dist <= 20: faixa = '8 a 20 km'
        elif dist <= 150: faixa = '20 a 150 km'
        else: faixa = 'Mais de 150 km'
    else:
        faixa = 'Sem endereço · DDD 48' if ddd_real == '48' else 'Sem endereço · outro DDD'

    idade = None if pd.isna(r['Idade']) else int(r['Idade'])
    data = r['Data de cadastro']
    plano = r['Plano de interesse']
    nome_comp = ' '.join(x for x in [s(r['Nome']), s(r['Sobrenome'])] if x)
    email = s(r['E-mail']) or ''

    flag = None
    low = (s(r['Nome']) or '').lower()
    if low == 'a' or email.endswith('@afaf'): flag = 'Teste'
    elif 'mozart@arborbrasil' in email: flag = 'Interno (fundador)'
    elif low == 'verbalize': flag = 'Empresa, não aluno'

    leads.append(dict(
        id=int(r['ID EVO']), data=data.strftime('%Y-%m-%d'), hora=s(r['Hora'])[:5], mes=data.strftime('%Y-%m'),
        dow=int(data.dayofweek), nome=nome_comp.title() if nome_comp.isupper() or nome_comp.islower() else nome_comp,
        email=email, celular=cel, whats=s(r['Link WhatsApp']), tel=tel_status, ddd=ddd_real,
        idade=idade, cep=cep, bairro=bairro, cidade=cidade, uf=uf, plano=plano, preco=PRECO[plano],
        dist=dist, ang=ang, precisao=precisao, faixa=faixa, genero=genero(r['Nome']),
        grande_floripa=bool(cidade and cidade.split(' (')[0] in GRANDE_FLORIPA) or (dist is None and ddd_real == '48'),
        dup_flag=s(r['Possível duplicado']) == 'Sim', flag=flag, dig=dig,
    ))

# deduplicação: mesmo telefone ou mesmo e-mail -> um lead (fica o cadastro mais recente)
grupos = {}
def chave(l):
    return l['dig'] if len(l['dig']) >= 10 else ('e:' + l['email'].lower() if l['email'] else 'id:%d' % l['id'])
for l in sorted(leads, key=lambda x: (x['data'], x['hora'])):
    k = chave(l)
    if k in grupos:
        grupos[k]['envios'] += 1; grupos[k]['primeiro'] = grupos[k]['primeiro']
        prev = grupos[k]
        l['envios'] = prev['envios']; l['primeiro'] = prev['primeiro']
        for f in ('idade', 'cep', 'bairro', 'cidade', 'uf', 'dist', 'ang', 'precisao'):
            if l[f] is None and prev[f] is not None: l[f] = prev[f]
        if prev['preco'] > l['preco']: l['plano_anterior'] = prev['plano']
        grupos[k] = l
    else:
        l['envios'] = 1; l['primeiro'] = l['data']; grupos[k] = l
unicos = list(grupos.values())

def score(l):
    if l['flag'] in ('Teste', 'Interno (fundador)', 'Empresa, não aluno'):
        return 0, ['Descartar: ' + l['flag']]
    motivos = []
    d = l['dist']
    if d is not None:
        p = 35 if d <= 3 else 30 if d <= 8 else 24 if d <= 15 else 18 if d <= 30 else 8 if d <= 150 else 4 if d <= 500 else 1
        if l['precisao'] == 'cep': p = 21
    else:
        p = 12 if l['ddd'] == '48' else 2
    motivos.append(('prox', p))
    mes = l['mes']
    rec = {'2026-09': 20, '2026-08': 10, '2026-07': 4}.get(mes, 2)
    pl = {'AVVA Personal Uno': 30, 'AVVA Personal Duo': 24, 'AVVA Personal Trio': 16, 'AVVA Essencial': 6}[l['plano']]
    i = l['idade']
    perf = 3 if i is None else 0 if i < 18 else 4 if i < 25 else 7 if i < 30 else 10 if i <= 60 else 7
    cont = (3 if l['tel'] == 'ok' else 0) + (2 if l['cep'] else 0)
    bonus = 3 if l['envios'] > 1 else 0
    total = min(100, p + rec + pl + perf + cont + bonus)
    if i is not None and i < 18:
        total = min(total, 54)  # menor de idade: contrato depende de responsável
    return total, dict(proximidade=p, recencia=rec, plano=pl, perfil=perf, contato=cont, recorrencia=bonus)

for l in unicos:
    sc, parts = score(l)
    l['score'] = sc
    l['parts'] = parts if isinstance(parts, dict) else {}
    if sc == 0: l['tier'] = 'X'
    elif sc >= 70: l['tier'] = 'A'
    elif sc >= 55: l['tier'] = 'B'
    elif sc >= 40: l['tier'] = 'C'
    else: l['tier'] = 'D'
    del l['dig']

unicos.sort(key=lambda l: (-l['score'], l['dist'] if l['dist'] is not None else 9e9))
out = dict(gerado='2026-09-14', total_registros=len(leads), avva=AVVA, precos=PRECO,
           registros=[{k: l[k] for k in ('id', 'data', 'hora', 'mes', 'dow', 'plano', 'idade', 'genero', 'faixa', 'dup_flag', 'tel', 'uf', 'cidade', 'bairro', 'dist')} for l in leads],
           leads=unicos)
json.dump(out, open('data.json', 'w'), ensure_ascii=False)

import collections
print('registros', len(leads), 'unicos', len(unicos))
print(collections.Counter(l['tier'] for l in unicos))
print(collections.Counter((l['mes'], l['tier']) for l in unicos if l['mes'] == '2026-09'))
print(collections.Counter(l['faixa'] for l in unicos))
print(collections.Counter(l['tel'] for l in leads))
print(collections.Counter(l['genero'] for l in unicos))
for l in unicos[:40]:
    print(l['tier'], l['score'], l['mes'], l['nome'][:22], l['plano'], l['idade'], l['cidade'], l['bairro'], l['dist'], l['envios'], l['parts'])
