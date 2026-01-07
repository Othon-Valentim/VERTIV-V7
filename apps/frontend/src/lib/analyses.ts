import { createClient } from './supabase';

export interface Analysis {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  data: AnalysisData;
  created_at: string;
  updated_at: string;
}

export interface AnalysisData {
  currentStep: number;
  completedSteps: number[];
  stepResults: Record<string, any>;
  sessionId: string;
}

export const analysesService = {
  // Listar todas as análises do usuário
  async list(): Promise<Analysis[]> {
    const supabase = createClient();
    const { data, error } = await supabase
      .from('analyses')
      .select('*')
      .order('updated_at', { ascending: false });

    if (error) throw error;
    return data || [];
  },

  // Buscar uma análise específica
  async get(id: string): Promise<Analysis | null> {
    const supabase = createClient();
    const { data, error } = await supabase
      .from('analyses')
      .select('*')
      .eq('id', id)
      .single();

    if (error) {
      if (error.code === 'PGRST116') return null; // Not found
      throw error;
    }
    return data;
  },

  // Criar nova análise
  async create(name: string, description: string, data: AnalysisData): Promise<Analysis> {
    const supabase = createClient();
    const { data: { user } } = await supabase.auth.getUser();

    if (!user) throw new Error('Usuário não autenticado');

    const { data: analysis, error } = await supabase
      .from('analyses')
      .insert({
        user_id: user.id,
        name,
        description,
        data
      })
      .select()
      .single();

    if (error) throw error;
    return analysis;
  },

  // Atualizar análise existente
  async update(id: string, updates: Partial<Pick<Analysis, 'name' | 'description' | 'data'>>): Promise<Analysis> {
    const supabase = createClient();
    const { data, error } = await supabase
      .from('analyses')
      .update(updates)
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;
    return data;
  },

  // Deletar análise
  async delete(id: string): Promise<void> {
    const supabase = createClient();
    const { error } = await supabase
      .from('analyses')
      .delete()
      .eq('id', id);

    if (error) throw error;
  },

  // Auto-save (salva automaticamente se já existe, senão cria)
  async autoSave(
    analysisId: string | null,
    name: string,
    data: AnalysisData
  ): Promise<Analysis> {
    if (analysisId) {
      return this.update(analysisId, { data });
    } else {
      return this.create(name, '', data);
    }
  }
};
