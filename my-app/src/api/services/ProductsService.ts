/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CouponApplication } from '../models/CouponApplication';
import type { DiscountInput } from '../models/DiscountInput';
import type { ProductInput } from '../models/ProductInput';
import type { ProductList } from '../models/ProductList';
import type { ProductOutput } from '../models/ProductOutput';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ProductsService {
    /**
     * @param payload
     * @returns ProductOutput Success
     * @throws ApiError
     */
    public static createProduct(
        payload: ProductInput,
    ): CancelablePromise<ProductOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/products/',
            body: payload,
        });
    }

    /**
     * @param onlyOutOfStock Apenas produtos sem estoque
     * @param sortOrder Direção da ordenação
     * @param sortBy Campo para ordenação
     * @param hasDiscount Filtrar produtos com desconto
     * @param maxPrice Preço máximo
     * @param minPrice Preço mínimo
     * @param search Busca por nome ou descrição
     * @param limit Itens por página (1-50)
     * @param page Número da página
     * @returns ProductList Success
     * @throws ApiError
     */
    public static listProducts(
        onlyOutOfStock?: boolean,
        sortOrder: 'asc' | 'desc' = 'asc',
        sortBy?: 'name' | 'price' | 'stock' | 'created_at',
        hasDiscount?: boolean,
        maxPrice?: number,
        minPrice?: number,
        search?: string,
        limit: number = 10,
        page: number = 1,
    ): CancelablePromise<ProductList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/products',  // <-- Corrigido aqui!
            query: {
                'onlyOutOfStock': onlyOutOfStock,
                'sortOrder': sortOrder,
                'sortBy': sortBy,
                'hasDiscount': hasDiscount,
                'maxPrice': maxPrice,
                'minPrice': minPrice,
                'search': search,
                'limit': limit,
                'page': page,
            },
        });
    }

    /**
     * @param productId
     * @param payload
     * @returns ProductOutput Success
     * @throws ApiError
     */
    public static updateProduct(
        productId: number,
        payload: ProductInput,
    ): CancelablePromise<ProductOutput> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/products/{product_id}',
            path: {
                'product_id': productId,
            },
            body: payload,
        });
    }

    /**
     * @param productId
     * @returns any Success
     * @throws ApiError
     */
    public static deleteProduct(
        productId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/products/{product_id}',
            path: {
                'product_id': productId,
            },
        });
    }

    /**
     * @param productId
     * @returns ProductOutput Success
     * @throws ApiError
     */
    public static getProduct(
        productId: number,
    ): CancelablePromise<ProductOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/products/{product_id}',
            path: {
                'product_id': productId,
            },
        });
    }

    /**
     * @param productId
     * @returns any Success
     * @throws ApiError
     */
    public static removeDiscount(
        productId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/products/{product_id}/discount',
            path: {
                'product_id': productId,
            },
        });
    }

    /**
     * @param productId
     * @param payload
     * @returns any Success
     * @throws ApiError
     */
    public static applyCouponDiscount(
        productId: number,
        payload: CouponApplication,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/products/{product_id}/discount/coupon',
            path: {
                'product_id': productId,
            },
            body: payload,
        });
    }

    /**
     * @param productId
     * @param payload
     * @returns any Success
     * @throws ApiError
     */
    public static applyPercentDiscount(
        productId: number,
        payload: DiscountInput,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/products/{product_id}/discount/percent',
            path: {
                'product_id': productId,
            },
            body: payload,
        });
    }
}
