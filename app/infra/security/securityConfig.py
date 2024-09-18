# securityConfig.py

import secrets
import logging

from flask import Flask, g, jsonify
from app.extensions import bcrypt
from flask_cors import CORS
from flask_talisman import Talisman


class SecurityConfig:
    def __init__(self, app):
        """Inicializa a configuração de segurança para a aplicação Flask."""
        self.app = app
        self._configure_cors()
        self._configure_default_csp_policy()

    def _configure_cors(self):
        """Configura a política de CORS para a aplicação, controlando quais origens podem acessar os recursos da aplicação."""
        origins = self.app.config.get("CORS_ORIGINS")
        CORS(
            self.app,
            resources={r"/*": {"origins": origins.split(",")}},
            supports_credentials=True,
        )

    def _configure_default_csp_policy(self):
        """Configura a Política de Segurança de Conteúdo (CSP) usando 'Flask-Talisman' para mitigar
         ataques XSS e outras ameaças, como clickjacking e content spoofing.

         Esta configuração define as seguintes regras:
            - **default-src**: Define a política padrão para todas as fontes de recursos não especificadas por outras diretivas.
            - **script-src**: Permite scripts apenas da mesma origem.
            - **style-src**: Permite estilos apenas da mesma origem.
            - **img-src**: Permite imagens apenas da mesma origem.
            - **connect-src**: Permite conexões (AJAX, WebSockets) apenas da mesma origem.

        **Observação**: Inicilaizar 'SecurityHandlers()' antes de 'SecurityConfig()' em appConfigurator para garantir
        que o nonce esteja disponível para a política CSP do Talisman. Ordem recomendada:
           - SecurityHandlers(app)
           - SecurityConfig(app)
        """
        Talisman(
            # Adiciona o cabeçalho Content-Security-Policy às respostas HTTP para reforçar a segurança.
            self.app,
            content_security_policy={
                "default-src": "'self'",
                "script-src": [
                    "'self'",
                    "'nonce-{nonce}'",
                    "https://cdn.jsdelivr.net",
                ],
                "style-src": ["'self'", "'nonce-{nonce}'"],
                "img-src": ["'self'"],
                "font-src": ["'self'", "data:", "https://fonts.googleapis.com"],
            },
            force_https=True,
        )

    @staticmethod
    def hash_password(password):
        """Criptografa uma senha usando bcrypt."""
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @staticmethod
    def check_password(hashed_password, plain_password):
        """Verifica se uma senha corresponde à senha criptografada."""
        return bcrypt.check_password_hash(hashed_password, plain_password)
