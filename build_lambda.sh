
#!/bin/bash
set -e

echo "🔧 Installing dependencies and creating lambda.zip..."

rm -rf build
mkdir -p build
cp lambda/lambda_function.py build/

pip install -r requirements.txt -t build/

cd build
zip -r ../lambda/lambda.zip .
cd ..
