Pixelbot
========

⚙ `config.json <config.json>`_
  You need to manually fill it before use.

Installation
------------

.. code-block:: console

  apt-get update
  apt-get install -y git
  
  git clone https://github.com/start-from-scratch/pixelbot .

Usage
-----

python
""""""

.. code-block:: console

  apt-get install -y python3 python3-pip python3-venv zip
  find -type f -path "*.sh" | xargs chmod +x
  
  python3 -m venv venv
  python3 -m pip install -r requirements.txt
  python3 main.py

docker
""""""

.. code-block:: console

  apt-get install -y docker-ce
  
  docker build -t pixelbot .
  docker run -d --name pixelbot --restart unless-stopped pixelbot
