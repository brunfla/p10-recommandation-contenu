FROM ubuntu:22.04

# Installer les dépendances de base
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    software-properties-common \
    lsb-release \
    python3 \
    python3-pip  # <--- Ajouter cette ligne

# Importer la clé Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg

# Ajouter le bon dépôt (pour Ubuntu Jammy => 22.04)
RUN echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list

# Installer Azure Functions Core Tools 4 (la commande func)
RUN apt-get update && apt-get install -y azure-functions-core-tools-4

# Vérification
RUN func --version

# Installer les dépendances Python
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copier le code source Azure Functions
WORKDIR /home/site/wwwroot
COPY . .

# Exposer le port local d'Azure Function
EXPOSE 7071

# Lancer Azure Functions en local
CMD ["func", "start", "--python", "--port", "7071", "--host", "0.0.0.0", "--verbose"]

