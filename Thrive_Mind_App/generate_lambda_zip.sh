#!/bin/bash

set -ex

# Download the dependencies
#rm -rf package
#pip3 install --upgrade pynamodb -t package

# Create the zip file
rm -f lambdafunctions.zip
cd package
zip -r ../lambdafunctions.zip .
cd ..

# Add our python files to it!
zip -g lambdafunctions.zip profilelambda.py
zip -g lambdafunctions.zip serviceslambda.py

echo "Done! Upload me to your lambda functions."
