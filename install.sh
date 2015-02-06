#!/usr/bin/env bash

echo "Copying main script"
cp mathematica.py /usr/bin/mathematica
echo "Making it executable"
chmod +x /usr/bin/mathematica
echo "Installation is successful, to run it type mathematica in the console"
