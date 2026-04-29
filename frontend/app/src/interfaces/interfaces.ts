export interface ErrorResponse {
    detail: string;
};

export interface ValidationErrorResponse {
    [field : string]: string[];
};

export interface AuthState {
    isAuthenticated: boolean;
    userProfile:     ProfileDataType | null;
    accessToken:     string | null;
    loading:         boolean;
    error:           string | null;
};

export interface LoginDataType {
    username: string;
    password: string;
};

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
};

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
};

export interface DashboardState {
    activeDate: string;
};

export interface HealthLogType {
    id: number;
    date: string;
    bodyweight: number | null;
    hours_slept: number | null;
    liquid_consumed: number | null;
};

export interface HealthLogState {
    activeLog: HealthLogType | null;
    loading: boolean;
    error: ValidationErrorResponse | null;
};

export interface UpdatePayload {
    id: number;
    data: Partial<Pick<HealthLogType,
        'bodyweight' | 'hours_slept' | 'liquid_consumed'
    >>;
};

