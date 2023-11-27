#!/bin/bash

# Base64-Kodierung
encode_base64() {
    echo "Geben Sie den Text ein, den Sie kodieren möchten: "
    read input_text
    echo "$input_text" | base64 > path.txt
}

# Base64-Dekodierung
decode_base64() {
    path=$(cat "path.txt")
    echo "$path" | base64 --decode
}

# Menü anzeigen
echo "1. Set path to pictures"
echo "2. Show path"
echo "Choose an option (1 or 2): "
read option

# Verarbeitung der Auswahl
case $option in
    1)
        encode_base64
        ;;
    2)
        decode_base64
        ;;
    *)
        echo "Invalid option"
        ;;
esac
