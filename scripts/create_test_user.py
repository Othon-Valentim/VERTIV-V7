"""
VERTIV v6.0 - Script para criar usuário de teste no Supabase

Uso:
    python scripts/create_test_user.py

Requer:
    - SUPABASE_URL no ambiente ou .env
    - SUPABASE_KEY (service_role key) no ambiente ou .env
"""

import os
import sys

# Adicionar path do backend para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'backend'))

try:
    from supabase import create_client, Client
except ImportError:
    print("Erro: supabase-py não instalado.")
    print("Execute: pip install supabase")
    sys.exit(1)

# Configuração do usuário de teste
TEST_USER = {
    "email": "test@vertiv.tech",
    "password": "Test@2024!",
    "user_metadata": {
        "full_name": "Usuário de Teste",
        "role": "tester"
    }
}

def get_supabase_client() -> Client:
    """Cria cliente Supabase com service_role key."""
    url = os.getenv("SUPABASE_URL", "https://nutilcpmpapjowqmxoqf.supabase.co")

    # Para criar usuários, precisamos da service_role key (não a anon key)
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY", "")

    if not key:
        print("ERRO: SUPABASE_SERVICE_ROLE_KEY não configurada.")
        print("")
        print("Para criar usuários, você precisa da 'service_role' key do Supabase.")
        print("Obtenha em: https://app.supabase.com/project/YOUR_PROJECT/settings/api")
        print("")
        print("Configure via:")
        print("  export SUPABASE_SERVICE_ROLE_KEY='sua-service-role-key'")
        print("")
        sys.exit(1)

    return create_client(url, key)

def create_test_user():
    """Cria o usuário de teste no Supabase."""
    print("=" * 60)
    print("VERTIV v6.0 - Criação de Usuário de Teste")
    print("=" * 60)
    print()

    client = get_supabase_client()

    print(f"Email: {TEST_USER['email']}")
    print(f"Senha: {TEST_USER['password']}")
    print()

    try:
        # Método 1: Usar admin API para criar usuário
        response = client.auth.admin.create_user({
            "email": TEST_USER["email"],
            "password": TEST_USER["password"],
            "email_confirm": True,  # Auto-confirma o email
            "user_metadata": TEST_USER["user_metadata"]
        })

        if response.user:
            print("✅ Usuário criado com sucesso!")
            print()
            print(f"   ID: {response.user.id}")
            print(f"   Email: {response.user.email}")
            print(f"   Criado em: {response.user.created_at}")
            print()
            print("Agora você pode usar essas credenciais nos testes E2E.")
            return True
        else:
            print("❌ Falha ao criar usuário (resposta vazia)")
            return False

    except Exception as e:
        error_msg = str(e)

        # Verificar se usuário já existe
        if "already been registered" in error_msg or "User already registered" in error_msg:
            print("⚠️  Usuário já existe no Supabase.")
            print()
            print("   Isso não é um erro - você pode usar as credenciais existentes.")
            print()

            # Tentar resetar a senha para garantir que está correta
            try:
                # Buscar usuário existente
                users = client.auth.admin.list_users()
                for user in users:
                    if user.email == TEST_USER["email"]:
                        print(f"   ID do usuário existente: {user.id}")

                        # Atualizar senha
                        client.auth.admin.update_user_by_id(
                            user.id,
                            {"password": TEST_USER["password"]}
                        )
                        print("   ✅ Senha atualizada para: Test@2024!")
                        break
            except Exception as update_error:
                print(f"   Nota: Não foi possível atualizar senha: {update_error}")

            return True
        else:
            print(f"❌ Erro ao criar usuário: {error_msg}")
            print()
            print("Possíveis causas:")
            print("1. SUPABASE_SERVICE_ROLE_KEY inválida")
            print("2. Projeto Supabase não encontrado")
            print("3. Limite de usuários atingido (plano gratuito)")
            return False

def main():
    """Função principal."""
    success = create_test_user()

    print()
    print("=" * 60)

    if success:
        print("Próximos passos:")
        print()
        print("1. Configure as variáveis de ambiente:")
        print("   cp .env.example .env")
        print("   # Edite .env com suas credenciais")
        print()
        print("2. Rode os testes E2E:")
        print("   npx playwright test tests/e2e/test_full_wizard_flow.spec.ts")
        print()
    else:
        print("Resolva os erros acima e tente novamente.")

    print("=" * 60)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
