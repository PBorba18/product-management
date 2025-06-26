/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CouponResponse = {
    /**
     * ID do cupom
     */
    id?: number;
    /**
     * Código do cupom
     */
    code?: string;
    /**
     * Descrição do cupom
     */
    description?: string;
    /**
     * Percentual de desconto
     */
    discount_percentage?: number;
    /**
     * Data de início da validade
     */
    valid_from?: string;
    /**
     * Data de fim da validade
     */
    valid_until?: string;
    /**
     * Limite de uso
     */
    usage_limit?: number;
    /**
     * Quantidade de usos
     */
    usage_count?: number;
    /**
     * Se o cupom está ativo
     */
    is_active?: boolean;
    /**
     * Se o cupom está válido
     */
    is_valid?: boolean;
    /**
     * Se o cupom está expirado
     */
    is_expired?: boolean;
    /**
     * Usos restantes
     */
    remaining_uses?: number;
    /**
     * Data de criação
     */
    created_at?: string;
    /**
     * Data de atualização
     */
    updated_at?: string;
};

