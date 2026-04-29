import { createSlice } from '@reduxjs/toolkit';
import type { FoodItemState } from '../../interfaces/interfaces.ts';
import { fetchAllFoodItems, createFoodItem } from '../thunks/foodItemThunk.ts';

const initialState: FoodItemState = {
    foodItems: [],
    loading: false,
    error: null
};

const foodItemSlice = createSlice({
    name: 'foodItem',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            // FETCH FOOD ITEMS
            .addCase(fetchAllFoodItems.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchAllFoodItems.fulfilled, (state, action) => {
                state.loading = false;
                state.foodItems = action.payload;
            })
            .addCase(fetchAllFoodItems.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE FOOD ITEM
            .addCase(createFoodItem.pending, (state) => {
                state.loading = true;
            })
            .addCase(createFoodItem.fulfilled, (state, action) => {
                state.loading = false;
                state.foodItems = action.payload;
            })
            .addCase(createFoodItem.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })
    }
});

export default foodItemSlice.reducer;
