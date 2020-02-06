import setuptools


setuptools.setup(
    name='globalls',
    summary='Language Server based on GNU Global',
    version='0.1.0',
    author='fangzhen',
    author_email='fzhen.info@gmail.com',
    entry_points={
        'console_scripts': [
            'globalls = globalls.server:main']}
)
