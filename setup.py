import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setuptools.setup(
    name="dlink-scraper",
    version="0.0.1",
    description="Scraper for getting data from D-Link DWR-921 LTE router",
    long_description=README,
    long_description_content='text/markdown',
    url='https://github.com/TheLastGimbus/D-Link_Scraper',
    author='TheLastGimbus',
    author_email='mateusz.soszynski@tuta.io',
    license='GPL-3.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Networking :: Monitoring'
    ],
    install_requires=(HERE/'requirements.txt').read_text().split('\n'),
    entry_points={
        'console_scripts': [
            'dlinkscraper=dlinkscraper.__main__:main'
        ]
    }
)