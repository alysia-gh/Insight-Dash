import sys, os
print('CWD:', os.getcwd())
for i,p in enumerate(sys.path[:10]):
    print(i, p)
print('\nContains insights dir?:', os.path.isdir(os.path.join(os.getcwd(),'insights')))
print('Contains Insights dir?:', os.path.isdir(os.path.join(os.getcwd(),'Insights')))
