import os
print('\n'.join(sorted(os.listdir('.'))))
print('\nExists insights:', os.path.isdir('insights'))
print('Exists Insights:', os.path.isdir('Insights'))
print('insights files:', os.listdir('insights') if os.path.isdir('insights') else 'no')
print('Insights files:', os.listdir('Insights') if os.path.isdir('Insights') else 'no')
