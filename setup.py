from setuptools import setup, find_packages
import re


def requirements(filename):
    with open(filename) as f:
        ll = f.read().splitlines()
    req = []
    for l in ll:
        k, v = re.split(r'==|>=', l)
        req.append(k)
    return req


setup(
    name='Photoric',
    version='0.0.1',
    license='AGPLv3',
    description='Photoric photographic gallery builder',
    author='Dmitry Argunov',
    author_email='dargunov@yahoo,com',
    url='http://www.dmitryargunovphotography.com',
    #namespace_packages=['photoric'],
    packages=[
        'photoric',
        'photoric/modules/admin',
        'photoric/modules/albums',
        'photoric/modules/api',
        'photoric/modules/auth',
        'photoric/modules/images',
        'photoric/modules/nav',
        'photoric/modules/search',
        'photoric/modules/upload',
        'photoric/modules/views',
        ],
    #package_data={'': ['*.png', '*.ico', '*.webmanifest', '*.svg', '*.css', '*.js','*.html'],},
    include_requires=requirements('requirements.txt'),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        ],
)