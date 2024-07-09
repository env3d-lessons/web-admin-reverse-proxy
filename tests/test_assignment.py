import os
import pathlib
import pytest
import re
import json

@pytest.fixture
def check_correct_files():
    os.popen('cp /etc/apache2/sites-available/000-default.conf .').read()
    os.popen('cp /var/www/html/full-stack-app/index.html .').read()
    return None

@pytest.fixture
def my_ip():
    if not pathlib.Path('my_ip.txt').is_file():
        f = open('my_ip.txt','w')
        f.write(os.popen('curl ident.me').read())
        f.close()

    return open('my_ip.txt').read()

def test_apache_config(check_correct_files):
    with open('000-default.conf') as config:
        content = config.read()
        assert re.search(r'ProxyPass.*localhost:8080', content, re.IGNORECASE), (
            "Need to add ProxyPass directive" )

def test_index_html(check_correct_files):
    with open('index.html') as index_html:
        content = index_html.read()
        assert len(content) > 0, "index.html must exist in /var/www/html/full-stack-app/ directory" 
        
def test_info_route(my_ip):
    content = os.popen(f'curl -L -s http://{my_ip}/full-stack-example-1/info').read()
    assert 'Full stack example' in content

def test_streets_route(my_ip):
    content = os.popen(f'curl -L -s http://{my_ip}/full-stack-example-1/streets').read()
    content_json = json.loads(content)
    assert len(content_json) == 180

def test_streets_water_st_route(my_ip):
    content = os.popen(f'curl -L -s http://{my_ip}/full-stack-example-1/streets/Water%20St').read()
    content_json = json.loads(content)
    assert len(content_json) == 14
