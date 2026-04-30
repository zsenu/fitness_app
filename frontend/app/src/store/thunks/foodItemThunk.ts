import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { FoodItemType, ValidationErrorResponse } from '../../interfaces/interfaces';

export const fetchAllFoodItems = createAsyncThunk<
    FoodItemType[],
    void,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodItem/fetchAll',
    async (_, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-items/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            }
        });

        if (response.status === 404) return null;

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        return await response.json();
    }
);

export const createFoodItem = createAsyncThunk<
    FoodItemType[],
    Omit<FoodItemType, 'id'>,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodItem/create',
    async (data, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        const refetchResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-items/`, {
            headers: {
                Authorization: `Bearer ${ token }`
            }
        });

        if (!refetchResponse.ok) {
            return rejectWithValue(await refetchResponse.json());
        }

        return await refetchResponse.json();
     }
);
