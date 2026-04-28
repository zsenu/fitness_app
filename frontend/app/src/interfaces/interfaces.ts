export interface ErrorResponse {
    detail: string;
}

export interface ValidationErrorResponse {
    [field : string]: string[];
}

export interface CustomUser {
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

export interface AuthState {
    isAuthenticated: boolean;
    userProfile:     CustomUser | null;
    accessToken:     string | null;
    loading:         boolean;
    error:           string | null;
};

export interface LoginDataType {
    username: string;
    password: string;
}

export interface RegisterDataType {
    username:        string;
    password:        string;
    password2:       string;
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

export interface ProfileDataType {
    id:              number;
    username:        string;
    email:           string;
    gender:          string;
    birth_date:      string;
    height:          number;
    starting_weight: number;
    current_weight:  number;
    activity_level:  string;
    target_weight:   number;
    target_date:     string;
    target_calories: number;
    bmr:             number;
    tdee:            number;
}
