export interface UserPublic {
    id: number;
    username: string;
    email?: string;
    is_active: boolean;
}

export interface UserLogin {
    username: string;
    password: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

export interface Message {
    id: number;
    user_id: number;
    content: string;
    timestamp: string; // ISO 8601 string
    role: 'user' | 'assistant';
}

export interface Question {
    id: string;
    text: string; 
    type: 'text' | 'number' | 'choice';
    options?: string[]; // For 'choice' type
}

export interface Questionnaire {
    id: number;
    title: string;
    description?: string;
    questions: Question[];
    created_at: string;
    is_active: boolean;
}

export interface Answer {
    question_id: string;
    value: any; // Can be string, number, etc.
}

export interface ClinicalInsight {
    id?: number;
    user_id: number;
    title: string;
    content: string;
    generated_by_agent?: string;
    created_at?: string; // ISO 8601 string
    severity?: 'High' | 'Medium' | 'Low';
}


// Duplicate interfaces removed to avoid conflicts.

// Utility type guards (for runtime validation)
export function isUserPublic(obj: unknown): obj is UserPublic {
    return typeof obj === 'object' &&
        obj !== null &&
        typeof (obj as any).id === 'number' &&
        typeof (obj as any).username === 'string' &&
        typeof (obj as any).is_active === 'boolean';
}
export function isToken(obj: unknown): obj is Token {
    return typeof obj === 'object' &&
        obj !== null &&
        typeof (obj as any).access_token === 'string' &&
        typeof (obj as any).token_type === 'string';
}
export function isMessage(obj: unknown): obj is Message {
    return typeof obj === 'object' &&
        obj !== null &&
        typeof (obj as any).id === 'number' &&
        typeof (obj as any).user_id === 'number' &&
        typeof (obj as any).content === 'string' &&
        typeof (obj as any).timestamp === 'string' &&
        ((obj as any).role === 'user' || (obj as any).role === 'assistant');
}
export function isQuestionnaire(obj: unknown): obj is Questionnaire {
    return typeof obj === 'object' &&
        obj !== null &&
        typeof (obj as any).id === 'number' &&
        typeof (obj as any).title === 'string' &&
        Array.isArray((obj as any).questions) &&
        typeof (obj as any).created_at === 'string' &&
        typeof (obj as any).is_active === 'boolean';
}
export function isClinicalInsight(obj: unknown): obj is ClinicalInsight {
    return typeof obj === 'object' &&
        obj !== null &&
        typeof (obj as any).user_id === 'number' &&
        typeof (obj as any).title === 'string' &&
        typeof (obj as any).content === 'string';
}