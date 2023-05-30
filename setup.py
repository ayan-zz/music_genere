from setuptools import find_packages,setup
from typing import List

hypen_e='-e .'

def get_requirements(file_path:str)->List[str]:

    requirements=[]
    with open(file_path) as file:
        requirements=file.readlines()
        requirements=[req.replace('\n','') for req in requirements]

        if hypen_e in requirements:
            requirements.remove(hypen_e)

    return requirements

setup(
    version='0.0.1',
    name='music',
    author='ayan',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)