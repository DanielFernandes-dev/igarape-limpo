from werkzeug.security import generate_password_hash, check_password_hash

from app.repositories import usuario_repository


class ErroValidacao(Exception):
    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


class NaoAutenticado(Exception):
    pass


class SemPermissao(Exception):
    pass


def hash_senha(senha):
    return generate_password_hash(senha, method="pbkdf2:sha256")


def verificar_senha(senha_hash, senha):
    return check_password_hash(senha_hash, senha)


def autenticar(email, senha):
    if len(email) > 254 or len(senha) > 128:
        raise ErroValidacao("Credenciais inválidas.", status=401)
    usuario = usuario_repository.obter_por_email(email)
    if usuario is None or not dict(usuario).get("ativo"):
        raise ErroValidacao("Credenciais inválidas.", status=401)
    if not verificar_senha(dict(usuario)["senha_hash"], senha):
        raise ErroValidacao("Credenciais inválidas.", status=401)
    return serializar(dict(usuario))


def serializar(usuario):
    if usuario is None:
        return None
    return {
        "id": usuario["id"],
        "nome": usuario["nome"],
        "email": usuario["email"],
        "perfil": usuario["perfil"],
        "ativo": bool(usuario["ativo"]),
        "data_criacao": usuario["data_criacao"],
    }


def obter_por_id(usuario_id):
    usuario = usuario_repository.obter_por_id(usuario_id)
    return serializar(usuario)


def criar_usuario(dados):
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    perfil = (dados.get("perfil") or "usuario").strip()

    if not nome or not email:
        raise ErroValidacao("Nome e e-mail são obrigatórios.")
    if len(nome) > 120 or len(email) > 254:
        raise ErroValidacao("Nome ou e-mail excede o tamanho permitido.")
    if "@" not in email:
        raise ErroValidacao("E-mail inválido.")
    if not senha or len(senha) < 6:
        raise ErroValidacao("Senha deve ter ao menos 6 caracteres.")
    if len(senha) > 128:
        raise ErroValidacao("Senha excede o tamanho permitido.")
    if perfil not in ("usuario", "moderador", "administrador"):
        raise ErroValidacao("Perfil inválido.")

    existente = usuario_repository.obter_por_email(email)
    if existente:
        raise ErroValidacao("E-mail já cadastrado.", status=409)

    return usuario_repository.criar(
        {
            "nome": nome,
            "email": email,
            "senha_hash": hash_senha(senha),
            "perfil": perfil,
            "ativo": 1,
        }
    )


def atualizar_usuario(usuario_id, dados):
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    perfil = (dados.get("perfil") or "usuario").strip()

    if not nome or not email:
        raise ErroValidacao("Nome e e-mail são obrigatórios.")
    if "@" not in email:
        raise ErroValidacao("E-mail inválido.")
    if perfil not in ("usuario", "moderador", "administrador"):
        raise ErroValidacao("Perfil inválido.")

    existente = usuario_repository.obter_por_email(email)
    if existente and existente["id"] != usuario_id:
        raise ErroValidacao("E-mail já cadastrado.", status=409)

    usuario_repository.atualizar(
        usuario_id,
        {
            "nome": nome,
            "email": email,
            "perfil": perfil,
            "ativo": 1 if str(dados.get("ativo", "1")) in ("1", "true", "on") else 0,
        },
    )
    return usuario_id


def alterar_senha(usuario_id, senha_atual, nova_senha):
    usuario = usuario_repository.obter_autenticacao_por_id(usuario_id)
    if usuario is None:
        raise ErroValidacao("Usuário não encontrado.", status=404)
    usuario_dict = dict(usuario)
    if not verificar_senha(usuario_dict["senha_hash"], senha_atual):
        raise ErroValidacao("Senha atual incorreta.", status=400)
    if not nova_senha or len(nova_senha) < 6:
        raise ErroValidacao("Nova senha deve ter ao menos 6 caracteres.")
    usuario_repository.atualizar_senha(usuario_id, hash_senha(nova_senha))
    return usuario_id


def requer_perfil(perfis_permitidos):
    perfis_permitidos = list(perfis_permitidos)

    def decorator(func):
        def wrapper(usuario, *args, **kwargs):
            if usuario is None:
                raise SemPermissao()
            if usuario.get("perfil") not in perfis_permitidos:
                raise SemPermissao()
            return func(usuario, *args, **kwargs)

        return wrapper

    return decorator
