from setuptools import setup, find_packages

setup(
    version="1.0.1",
    name="auto_subtitle",
    packages=find_packages(),
    py_modules=["auto_subtitle"],
    author="Tobias Weigel, based on the work of Sectux, Miguel Piedrafita and RapDoodle",
    install_requires=[
        'youtube-dl',
        'psutil',
        'openai-whisper @ git+https://github.com/openai/whisper.git@main#egg=whisper'
    ],
    description="Automatically generate and/or embed subtitles into your videos",
    entry_points={
        'console_scripts': ['auto_subtitle_plus=auto_subtitle_plus.cli:main'],
    },
    include_package_data=True,
)
