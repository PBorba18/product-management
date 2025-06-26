/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ProductInput = {
    /**
     * Nome único do produto
     */
    name: string;
    /**
     * Descrição do produto
     */
    description?: string;
    /**
     * Preço do produto (mín: R$ 0,01)
     */
    price: number;
    /**
     * Quantidade em estoque
     */
    stock: number;
};

