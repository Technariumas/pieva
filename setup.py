#!/usr/bin/env python

from distutils.core import setup, Extension

setup(
    name='PievaCore',
    version='1.0.0',
    description='Low level pixel to led mapping provider',
    author='Albertas Mickenas',
    author_email='mic@wemakethings.net',
    
    packages=['core'],
    
	ext_modules=[
		Extension('core.PixelMapper', ['core/pixelMapper.c'], 
			extra_compile_args=['-Os', '-funroll-loops', '-ffast-math'],
		),
		Extension('core.NoiseGenerator', ['core/noiseGenerator.c'], 
			extra_compile_args=['-Os', '-funroll-loops', '-ffast-math'],
		),
	],
)
