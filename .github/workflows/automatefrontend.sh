#!/bin/sh
cp -f api.yml frontend.yml
sed -i 's/api/frontend/g' frontend.yml
sed -i 's/API/FRONTEND/g' frontend.yml
sed -i 's/backend/frontend/g' frontend.yml

