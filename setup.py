from setuptools import setup, find_packages
from servee_image import get_version

setup(
    name = "django-servee-image",
    version = get_version(join="-"),
    license = '--',
    description = "Image plugin for django-servee",
    long_description=open("README.rst").read(),
    author = 'Issac Kelly',
    author_email = 'issac@kellycreativetech.com',
    packages = find_packages(exclude=["ez_setup"]),
    zip_safe = False,
    install_requires = [
        'PIL',
        'django-servee>=0.6.0',
        'easy-thumbnails>=1.0-alpha-16',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: --',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    
)