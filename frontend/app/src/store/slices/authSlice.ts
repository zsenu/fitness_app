import { createSlice }        from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

interface CustomUser {
    username:        string;
    gender:          string;
    birth_date:      string;
    height:          number;
    starting_weight: number;
    activity_level:  string;
    target_weight:   number;
    target_date:     string;
    target_calories: number;
}

interface SampleInitialState {
    isAuthenticated: boolean;
    userProfile:     CustomUser | null;
    accessToken:     string | null;
};

const initialState: SampleInitialState = {
    isAuthenticated: false,
    userProfile:     null,
    accessToken:     null
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        /* TODO: decide where requests will be sent from */
        login(state, action: PayloadAction<{ username: string; password: string }>) {
            console.log('LOGIN ATTEMPT WITH USERNAME ' + action.payload.username + ' AND PASSWORD ' + action.payload.password);
            
            state.isAuthenticated = true;
            state.accessToken     = 'mocked_access_token';
        },
        logout(state) {
            console.log('LOGOUT ATTEMPT');

            state.isAuthenticated = false;
            state.userProfile     = null;
            state.accessToken     = null;
        }
    },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
