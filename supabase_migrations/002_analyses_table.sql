-- Tabela para salvar análises do wizard
-- Executar no Supabase SQL Editor

-- 1. Criar tabela analyses
CREATE TABLE IF NOT EXISTS public.analyses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Índices para performance
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON public.analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_updated_at ON public.analyses(updated_at DESC);

-- 3. Habilitar RLS (Row Level Security)
ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;

-- 4. Política: Usuários só veem suas próprias análises
CREATE POLICY "Users can view own analyses"
    ON public.analyses
    FOR SELECT
    USING (auth.uid() = user_id);

-- 5. Política: Usuários só inserem suas próprias análises
CREATE POLICY "Users can insert own analyses"
    ON public.analyses
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- 6. Política: Usuários só atualizam suas próprias análises
CREATE POLICY "Users can update own analyses"
    ON public.analyses
    FOR UPDATE
    USING (auth.uid() = user_id);

-- 7. Política: Usuários só deletam suas próprias análises
CREATE POLICY "Users can delete own analyses"
    ON public.analyses
    FOR DELETE
    USING (auth.uid() = user_id);

-- 8. Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_analyses_updated_at
    BEFORE UPDATE ON public.analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Verificar se tabela foi criada
SELECT 'Tabela analyses criada com sucesso!' as status;
