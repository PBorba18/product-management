/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CouponUpdate = {
    /**
     * Código do cupom
     */
    code?: string;
    /**
     * Descrição do cupom
     */
    description?: string;
    /**
     * Percentual de desconto (0-100)
     */
    discount_percentage?: number;
    /**
     * Data de início da validade (ISO format)
     */
    valid_from?: string;
    /**
     * Data de fim da validade (ISO format)
     */
    valid_until?: string;
    /**
     * Limite de uso do cupom
     */
    usage_limit?: number;
};

