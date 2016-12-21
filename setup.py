

import sys

from setuptools import setup , find_packages


setup(name="onyxproject",
      description="Intelligent Dashboard",
      version='0.3.8',
      include_package_data=True,
      packages=['onyx'],
      url="https://github.com/OnyxProject/Onyx",
      maintainer=("Aituglo"),
      maintainer_email="onyxlabs@outlook.fr",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.5",
          "Topic :: Software Development :: Build Tools",
          "Topic :: System :: Software Distribution"],
      zip_safe=True,
      entry_points={
          'console_scripts': ['onyxstart=Onyx:runserver']
      },
      install_requires=['pip', 'pytz' , 'Babel' , 'uptime', 'onyxbabel', 'flask-apidoc', 'configparser' ,'psutil', 'Flask-Script' , 'pylibmc' , 'Flask-restplus' , 'Flask-FlatPages' , 'Markdown' , 'PyYAML' , 'Werkzeug' , 'flask-migrate' ,'itsdangerous' , 'speaklater' , 'Flask-Cache' , 'pylibmc' , 'redis' , 'celery' , 'flask-restless' ,'Flask==0.10.1','Flask-WTF','Flask-sqlalchemy','requests','beautifulsoup4','Flask-Menu','Flask-Login','SQLAlchemy-migrate','flask_bcrypt','flask-Mail','blinker','wikipedia','markupsafe'],
      options={
          'bdist_wheel': {'universal': True},
      },
      platforms=['any'],
      )
