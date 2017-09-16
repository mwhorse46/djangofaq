#!/bin/bash

echo '';
echo -n "[+] commit ➜ ";
read commit

if [ "$commit" ]; then
    git add .;
    git commit -m "$commit";

    echo "$commit";

    # bitbucket
    git push -u origin master;

    # github
    git push -u github master;
fi
