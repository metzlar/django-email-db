from setuptools import setup

setup(
  name='Django Email DB Backend',
  version='0.1',
  py_modules=['django_email_db'],
  cmdclass={'upload':lambda x:None},
  install_requires=[
      'django',
      'south',
  ],
)# pragma: no cover 
 
