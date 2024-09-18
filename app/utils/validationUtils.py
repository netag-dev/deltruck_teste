# utils/validationUtis.py

from marshmallow import validate, ValidationError

class ValidationUtils:
    @staticmethod
    def email():
        return validate.Email(
            error="O endereço de e-mail fornecido não é válido."
        )
    
    @staticmethod
    def password():
        return validate.Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@!#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/`~])[A-Za-z\d@!#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/`~]{6,}$",
            error=(
                "A senha deve ter pelo menos 6 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial."
            ),
        )