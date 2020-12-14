from setuptools import setup

setup(
    name='snapshotalyzer-30k',
    version='0.3',
    author="Robin Norwood",
    author_email="robin@acloud.guru",
    description="SnapshotAlyzer 30K is a tool to manage AWS EC2 snapshots",
    license="GPLv3+",
    packages=['shotty'],
    url="https://githib.com/xxxx",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        cons_shotty=shotty.shotty:cli
    ''',
)
