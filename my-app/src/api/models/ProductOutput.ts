/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ProductOutput = {
    /**
     * ID único do produto
     */
    id?: number;
    /**
     * Nome do produto
     */
    name?: string;
    /**
     * Descrição do produto
     */
    description?: string;
    /**
     * Preço original
     */
    price?: number;
    /**
     * Estoque atual
     */
    stock?: number;
    /**
     * Preço com desconto (se aplicável)
     */
    finalPrice?: number;
    /**
     * Produto sem estoque
     */
    isOutOfStock?: boolean;
    /**
     * Informações do desconto ativo
     */
    discount?: any;
    /**
     * Possui cupom aplicado
     */
    hasCouponApplied?: boolean;
    /**
     * Data de criação
     */
    createdAt?: string;
    /**
     * Data de atualização
     */
    updatedAt?: string;
};

