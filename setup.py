from setuptools import setup, find_packages

setup(
    name='coin_remitter',
    version='0.1.0',
    author='glizzykingdreko',
    author_email='glizzykingdreko@example.com',
    description='A Python SDK for integrating with the CoinRemitter cryptocurrency payment gateway API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/glizzykingdreko/coinremitter-sdk',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='cryptocurrency payment gateway coin remitter api sdk crypto',
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://coinremitter.com/docs',
        'Source': 'https://github.com/glizzykingdreko/coinremitter-sdk',
        'Tracker': 'https://github.com/glizzykingdreko/coinremitter-sdk/issues',
    },
)
