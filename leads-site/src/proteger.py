# Gera uma cópia da dashboard trancada com usuário e senha, pronta para o GitHub Pages.
# O conteúdo é criptografado (AES-GCM, chave derivada por PBKDF2-SHA256) e só abre no navegador
# de quem digitar as credenciais certas. O arquivo gerado não contém nenhum dado legível.
#
# Uso:  python3 proteger.py            (pede usuário e senha no terminal)
# Saída: ~/Code Claude/avva-leads-publico/index.html

import base64, getpass, json, os, pathlib, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 600_000
AQUI = pathlib.Path(__file__).resolve().parent
ORIGEM = AQUI.parent / 'index.html'
DESTINO = pathlib.Path(os.environ.get('DESTINO', pathlib.Path.home() / 'Code Claude' / 'avva-leads-publico' / 'index.html'))


def chave(usuario, senha, sal):
    segredo = (usuario.strip().lower() + '\n' + senha).encode('utf-8')
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal, iterations=ITER).derive(segredo)


def main():
    usuario = os.environ.get('USUARIO') or input('Usuário da equipe: ').strip()
    senha = os.environ.get('SENHA')
    if not senha:
        senha = getpass.getpass('Senha (não aparece enquanto digita): ')
        if getpass.getpass('Repita a senha: ') != senha:
            sys.exit('As senhas não conferem. Rode de novo.')
    if not usuario or len(senha) < 10:
        sys.exit('Use um usuário e uma senha com pelo menos 10 caracteres.')

    html = ORIGEM.read_bytes()
    sal, iv = os.urandom(16), os.urandom(12)
    cifrado = AESGCM(chave(usuario, senha, sal)).encrypt(iv, html, None)
    pacote = {k: base64.b64encode(v).decode() for k, v in (('sal', sal), ('iv', iv), ('dados', cifrado))}
    pacote['iter'] = ITER

    pagina = (AQUI / 'login.html').read_text().replace('__PACOTE__', json.dumps(pacote))
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(pagina)
    print(f'Pronto: {DESTINO}')
    print('Suba esse index.html no repositório público do GitHub Pages. Nenhum dado aparece sem a senha.')


if __name__ == '__main__':
    main()
