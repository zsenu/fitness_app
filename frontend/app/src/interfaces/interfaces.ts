interface CustomUser {
    username:        string;
    email:           string;
    gender:          string;
    birth_date:      string;
    height:          number;
    starting_weight: number;
    activity_level:  string;
    target_weight:   number;
    target_date:     string;
    target_calories: number;
}

interface AuthState {
    isAuthenticated: boolean;
    userProfile:     CustomUser | null;
    accessToken:     string | null;
    loading:         boolean;
    error:           string | null;
};

export type { CustomUser, AuthState };