import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';

const API_BASE = "http://localhost:8000/api";

export const login = createAsyncThunk(
    'auth/login',
    async (
        { username, password }: { username: string; password: string },
        thunkAPI
    ) => {
        try {

            const loginResponse = await fetch(`${ API_BASE }/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!loginResponse.ok) { throw new Error('Login failed.'); }

            const loginData = await loginResponse.json();
            const token = loginData.access;
            console.log(`LOGIN - data: ${ loginData }\nJSON data: ${ JSON.stringify(loginData) }`);

            const profileResponse = await fetch(`${ API_BASE }/auth/profiles/me/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${ token }`,
                },
            });

            if (!profileResponse.ok) { throw new Error('Failed to fetch user profile.'); }
            const profileData = await profileResponse.json();

            return { access: token, profile: profileData };

        } catch (error: unknown) {
            if (error instanceof Error) { return thunkAPI.rejectWithValue(error.message); }
            return thunkAPI.rejectWithValue('An unknown error occurred.');
        }
    }
);

export const logout = createAsyncThunk(
    'auth/logout',
    async (
        _,
        thunkAPI
    ) => {
        const state: RootState = thunkAPI.getState() as RootState;
        const token = state.auth.accessToken;

        try {
            const response = await fetch(`${ API_BASE }/auth/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${ token }`,
                },
            });

            if (!response.ok) { throw new Error('Logout failed.'); }
            return true;
        }
        catch (error: unknown) {
            if (error instanceof Error) { return thunkAPI.rejectWithValue(error.message); }
            return thunkAPI.rejectWithValue('An unknown error occurred.');
        }
    }
);