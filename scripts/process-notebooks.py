import json
import zipfile
import os

def process(dir):
    print('Processing {}'.format(dir))
    repo = os.environ.get('GITHUB_REPOSITORY', 'example/repo')
    website = 'https://{}.github.io/{}'.format(repo.split('/')[0], repo.split('/')[1])
    with open(os.path.join('notebooks', dir, dir+'.ipynb'), 'r') as fp:
        ipynb = json.load(fp)
    with open(os.path.join('notebooks', 'ATTRIBUTION.md'), 'r') as fp:
        attribution = fp.read().splitlines()
    attr_cell = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [line+'\n' for line in attribution]
    }
    ipynb['cells'].insert(0, attr_cell)
    aux = {}
    for filename in os.listdir(os.path.join('notebooks', dir)):
        if filename[0]!='.' and filename!=dir+'.ipynb':
            with open(os.path.join('notebooks', dir, filename), 'r') as fp:
                aux[filename] = fp.read()
    with zipfile.ZipFile(os.path.join('public', dir+'.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(dir+'.ipynb', json.dumps(ipynb))
        for filename, data in aux.items():
            zipf.writestr(filename, data)
    with zipfile.ZipFile(os.path.join('public', dir+'-aux.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename, data in aux.items():
            zipf.writestr(filename, data)
    if len(aux)>0:
        download_cell = {
            'cell_type': 'code',
            'metadata': {},
            'source': [
                '# This part downloads needed auxiliary files to Google Colab\n',
                '! curl {}/{}-aux.zip > {}-aux.zip && unzip -o {}-aux.zip\n'.format(website, dir, dir, dir)
            ]
        }
        ipynb['cells'].insert(1, download_cell)
    with open(os.path.join('colab', dir+'.ipynb'), 'w') as fp:
        json.dump(ipynb, fp)

if __name__ == '__main__':
    if not os.path.exists('public'):
        os.mkdir('public')
    if not os.path.exists('colab'):
        os.mkdir('colab')
    for dir in os.listdir('notebooks'):
        if os.path.exists(os.path.join('notebooks', dir, dir+'.ipynb')):
            process(dir)