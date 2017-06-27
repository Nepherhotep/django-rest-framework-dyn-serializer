from setuptools import setup, find_packages

__author__ = 'Alexey Zankevich'


setup(
    name="rest_framework_dyn_serializer",
    version="1.1.0",
    py_modules=['rest_framework_dyn_serializer'],
    author="Alexey Zankevich",
    author_email="alex.zankevich@gmail.com",
    description="Dynamic serializer for Django REST framework",
    keywords=['Django', 'REST', 'DRF'],
    license="MIT",
    platforms=['Platform Independent'],
    url="https://github.com/Nepherhotep/django-rest-framework-dyn-serializer",
    install_requires=['django>=1.9', 'djangorestframework>=3.3.0'],
    classifiers=["Framework :: Django :: 1.9",
                 "Development Status :: 5 - Production/Stable",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.5"]
)
