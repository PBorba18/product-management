/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CouponInput } from '../models/CouponInput';
import type { CouponResponse } from '../models/CouponResponse';
import type { CouponUpdate } from '../models/CouponUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CouponsService {
    /**
     * Cria novo cupom promocional
     * @param payload
     * @returns CouponResponse Success
     * @throws ApiError
     */
    public static createCoupon(
        payload: CouponInput,
    ): CancelablePromise<CouponResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/coupons/',
            body: payload,
        });
    }
    /**
     * Lista cupons disponíveis
     * @returns any Success
     * @throws ApiError
     */
    public static listCoupons(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coupons/',
        });
    }
    /**
     * Marca um cupom como usado
     * @param couponCode
     * @returns CouponResponse Success
     * @throws ApiError
     */
    public static useCoupon(
        couponCode: string,
    ): CancelablePromise<CouponResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/coupons/use/{coupon_code}',
            path: {
                'coupon_code': couponCode,
            },
        });
    }
    /**
     * Valida se um cupom pode ser usado
     * @param couponCode
     * @returns any Success
     * @throws ApiError
     */
    public static validateCoupon(
        couponCode: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coupons/validate/{coupon_code}',
            path: {
                'coupon_code': couponCode,
            },
        });
    }
    /**
     * Atualiza um cupom pelo código
     * @param couponCode
     * @param payload
     * @returns CouponResponse Success
     * @throws ApiError
     */
    public static updateCoupon(
        couponCode: string,
        payload: CouponUpdate,
    ): CancelablePromise<CouponResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/coupons/{coupon_code}',
            path: {
                'coupon_code': couponCode,
            },
            body: payload,
        });
    }
    /**
     * Remove um cupom pelo código (soft delete)
     * @param couponCode
     * @returns any Success
     * @throws ApiError
     */
    public static deleteCoupon(
        couponCode: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/coupons/{coupon_code}',
            path: {
                'coupon_code': couponCode,
            },
        });
    }
    /**
     * Detalhes de um cupom pelo código
     * @param couponCode
     * @returns CouponResponse Success
     * @throws ApiError
     */
    public static getCoupon(
        couponCode: string,
    ): CancelablePromise<CouponResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coupons/{coupon_code}',
            path: {
                'coupon_code': couponCode,
            },
        });
    }
    /**
     * Detalhes de um cupom pelo ID
     * @param couponId
     * @returns CouponResponse Success
     * @throws ApiError
     */
    public static getCouponById(
        couponId: number,
    ): CancelablePromise<CouponResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/coupons/{coupon_id}',
            path: {
                'coupon_id': couponId,
            },
        });
    }
}
