# Injeta data.json no template e gera ../index.html
import pathlib
aqui = pathlib.Path(__file__).parent
t = (aqui / 'template.html').read_text()
d = (aqui / 'data.json').read_text().replace('</', '<\\/')
(aqui.parent / 'index.html').write_text(t.replace('__DATA__', d))
print('index.html gerado')
